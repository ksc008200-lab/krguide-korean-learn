/**
 * KR Guide — Auth Worker
 * 회원 가입 / 로그인 / 세션 검증 / 이메일
 *
 * Bindings (wrangler.toml):
 *   R2  : MEMBERS_BUCKET  — 회원 프로파일 JSON 저장
 *   KV  : SESSIONS        — 세션 토큰 (TTL 7일)
 *   KV  : EMAIL_INDEX     — email → userId 매핑
 *   KV  : RESET_TOKENS    — 비밀번호 재설정 토큰 (TTL 1시간)
 *
 * Secrets (Dashboard):
 *   RESEND_API_KEY
 *   ADMIN_KEY
 *
 * Endpoints:
 *   POST /auth/register         { email, password, name }
 *   POST /auth/login            { email, password }
 *   GET  /auth/verify           (cookie: krg_session)
 *   GET  /auth/profile          (cookie: krg_session)
 *   POST /auth/logout           (cookie: krg_session)
 *   POST /auth/forgot-password  { email }
 *   POST /auth/reset-password   { token, newPassword }
 *   GET  /auth/members          ?key=ADMIN_KEY
 */

const COOKIE_NAME        = "krg_session";
const SESSION_TTL        = 60 * 60 * 24 * 7;   // 7일
const RESET_TTL          = 60 * 60;             // 1시간
const SITE_URL           = "https://krguide.com";
const AUTH_URL           = "https://auth.krguide.com";
const FROM_EMAIL         = "KR Guide <hello@krguide.com>";
const GOOGLE_REDIRECT    = `${AUTH_URL}/auth/google/callback`;
const ALLOWED_ORIGINS    = ["https://krguide.com", "https://www.krguide.com", "https://auth.krguide.com", "https://study.krguide.com", "https://krguide-vocab.pages.dev"];
const GUMROAD_PRODUCT_ID = "X6QtsRuC5u8WoIw38pB6qg==";   // Gumroad product_id (from product page "Use your product ID...")

// ── CORS ──────────────────────────────────────────────────────────────────────
function corsHeaders(request) {
  const origin = request.headers.get("Origin") || "";
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function json(data, status = 200, request) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders(request) },
  });
}

// ── 비밀번호 해시 ──────────────────────────────────────────────────────────────
async function hashPassword(password, salt) {
  const s = salt || crypto.randomUUID().replace(/-/g, "");
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s + password));
  const hex = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
  return { hash: hex, salt: s };
}

async function verifyPassword(password, salt, hash) {
  const { hash: h } = await hashPassword(password, salt);
  return h === hash;
}

// ── R2: 회원 저장/조회 ─────────────────────────────────────────────────────────
async function getMember(env, userId) {
  const obj = await env.MEMBERS_BUCKET.get(`members/${userId}.json`);
  if (!obj) return null;
  return JSON.parse(await obj.text());
}

async function saveMember(env, member) {
  await env.MEMBERS_BUCKET.put(
    `members/${member.id}.json`,
    JSON.stringify(member),
    { httpMetadata: { contentType: "application/json" } }
  );
}

// ── KV helpers ────────────────────────────────────────────────────────────────
async function getUserIdByEmail(env, email) {
  return env.EMAIL_INDEX.get(email.toLowerCase());
}
async function setEmailIndex(env, email, userId) {
  await env.EMAIL_INDEX.put(email.toLowerCase(), userId);
}

async function createSession(env, userId, email, plan) {
  const token = crypto.randomUUID().replace(/-/g, "") + crypto.randomUUID().replace(/-/g, "");
  await env.SESSIONS.put(`session:${token}`, JSON.stringify({ userId, email, plan, createdAt: Date.now() }), { expirationTtl: SESSION_TTL });
  return token;
}
async function getSession(env, token) {
  if (!token) return null;
  const raw = await env.SESSIONS.get(`session:${token}`);
  return raw ? JSON.parse(raw) : null;
}
async function deleteSession(env, token) {
  await env.SESSIONS.delete(`session:${token}`);
}

async function createResetToken(env, userId) {
  const token = crypto.randomUUID().replace(/-/g, "") + crypto.randomUUID().replace(/-/g, "");
  await env.RESET_TOKENS.put(`reset:${token}`, userId, { expirationTtl: RESET_TTL });
  return token;
}
async function getResetToken(env, token) {
  return env.RESET_TOKENS.get(`reset:${token}`);
}
async function deleteResetToken(env, token) {
  await env.RESET_TOKENS.delete(`reset:${token}`);
}

// ── 쿠키 ──────────────────────────────────────────────────────────────────────
function getTokenFromCookie(request) {
  const match = (request.headers.get("Cookie") || "").match(new RegExp(`${COOKIE_NAME}=([^;]+)`));
  return match ? match[1] : null;
}
function sessionCookie(token, expire = false) {
  if (expire) return `${COOKIE_NAME}=; Path=/; Domain=.krguide.com; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;
  return `${COOKIE_NAME}=${token}; Path=/; Domain=.krguide.com; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL}`;
}

// ── Resend 이메일 발송 ─────────────────────────────────────────────────────────
async function sendEmail(env, { to, subject, html }) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ from: FROM_EMAIL, to, subject, html }),
  });
  if (!res.ok) {
    const err = await res.text();
    console.error("Resend error:", err);
  }
  return res.ok;
}

// ── 이메일 템플릿 ──────────────────────────────────────────────────────────────
function welcomeEmail(name) {
  return `
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif">
  <div style="max-width:560px;margin:40px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#0071e3,#005bb5);padding:36px 40px;text-align:center">
      <div style="font-size:1.6rem;font-weight:900;color:#fff;letter-spacing:-.03em">
        <span style="color:#60a5fa">KR</span> Guide
      </div>
      <p style="color:rgba(255,255,255,.8);margin:8px 0 0;font-size:.9rem">Your Complete Guide to Korea</p>
    </div>
    <!-- Body -->
    <div style="padding:40px">
      <h1 style="font-size:1.5rem;font-weight:800;color:#1d1d1f;margin:0 0 12px">
        Welcome to KR Guide, ${name}! 🎉
      </h1>
      <p style="color:#374151;line-height:1.7;margin:0 0 24px">
        Your account is ready. You now have access to <strong>free Korean learning lessons</strong> and Korea guides.
      </p>
      <!-- What's available -->
      <div style="background:#f5f5f7;border-radius:12px;padding:20px 24px;margin-bottom:24px">
        <p style="font-weight:700;color:#1d1d1f;margin:0 0 12px">✅ What you can do now:</p>
        <ul style="margin:0;padding-left:20px;color:#374151;line-height:1.8">
          <li>Read <strong>free Korean lessons</strong> (Chapters 1–5)</li>
          <li>Browse 190+ guides on Travel &amp; Living in Korea</li>
          <li>Translate any page into your language</li>
        </ul>
      </div>
      <!-- CTA -->
      <div style="text-align:center;margin-bottom:28px">
        <a href="${SITE_URL}/korean-library/"
           style="display:inline-block;background:#0071e3;color:#fff;text-decoration:none;padding:14px 36px;border-radius:24px;font-weight:700;font-size:1rem">
          Start Learning Korean →
        </a>
      </div>
      <!-- Upgrade nudge -->
      <div style="border:1px solid #e0e0e5;border-radius:12px;padding:20px 24px;text-align:center">
        <p style="font-weight:700;color:#1d1d1f;margin:0 0 6px">Want the full 190+ lessons?</p>
        <p style="color:#86868b;font-size:.88rem;margin:0 0 14px">Unlock everything for a one-time payment of $19.90</p>
        <a href="${SITE_URL}/ebook-landing/"
           style="color:#0071e3;font-weight:700;text-decoration:none;font-size:.9rem">
          See Full Access Plans →
        </a>
      </div>
    </div>
    <!-- Footer -->
    <div style="background:#f5f5f7;padding:20px 40px;text-align:center;border-top:1px solid #e8e8eb">
      <p style="color:#86868b;font-size:.78rem;margin:0">
        © 2026 KR Guide · <a href="${SITE_URL}/privacy-policy/" style="color:#86868b">Privacy</a> · <a href="${SITE_URL}/contact/" style="color:#86868b">Contact</a>
      </p>
    </div>
  </div>
</body>
</html>`;
}

function resetEmail(resetUrl) {
  return `
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif">
  <div style="max-width:560px;margin:40px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#0071e3,#005bb5);padding:36px 40px;text-align:center">
      <div style="font-size:1.6rem;font-weight:900;color:#fff;letter-spacing:-.03em">
        <span style="color:#60a5fa">KR</span> Guide
      </div>
    </div>
    <!-- Body -->
    <div style="padding:40px">
      <h1 style="font-size:1.4rem;font-weight:800;color:#1d1d1f;margin:0 0 12px">
        Password Reset Request 🔐
      </h1>
      <p style="color:#374151;line-height:1.7;margin:0 0 8px">
        We received a request to reset your KR Guide password.
      </p>
      <p style="color:#374151;line-height:1.7;margin:0 0 28px">
        Click the button below to set a new password. This link expires in <strong>1 hour</strong>.
      </p>
      <!-- CTA -->
      <div style="text-align:center;margin-bottom:28px">
        <a href="${resetUrl}"
           style="display:inline-block;background:#0071e3;color:#fff;text-decoration:none;padding:14px 36px;border-radius:24px;font-weight:700;font-size:1rem">
          Reset My Password →
        </a>
      </div>
      <!-- Security note -->
      <div style="background:#fff8e7;border:1px solid #fcd34d;border-radius:12px;padding:16px 20px">
        <p style="color:#92400e;font-size:.85rem;margin:0;line-height:1.6">
          ⚠️ If you did not request a password reset, please ignore this email. Your password will not change.
        </p>
      </div>
      <!-- Fallback URL -->
      <p style="color:#86868b;font-size:.78rem;margin:24px 0 0;word-break:break-all">
        Or copy this link: <a href="${resetUrl}" style="color:#0071e3">${resetUrl}</a>
      </p>
    </div>
    <!-- Footer -->
    <div style="background:#f5f5f7;padding:20px 40px;text-align:center;border-top:1px solid #e8e8eb">
      <p style="color:#86868b;font-size:.78rem;margin:0">
        © 2026 KR Guide · <a href="${SITE_URL}/privacy-policy/" style="color:#86868b">Privacy</a> · <a href="${SITE_URL}/contact/" style="color:#86868b">Contact</a>
      </p>
    </div>
  </div>
</body>
</html>`;
}

// ── 메인 핸들러 ───────────────────────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request) });
    }

    // ── POST /api/license-verify (Gumroad license key check) ───────────────
    if (path === "/api/license-verify" && request.method === "POST") {
      try {
        const body = await request.json();
        const key = (body.license_key || "").trim();
        if (!key) return json({ success: false, error: "라이선스 키를 입력하세요" }, 400, request);
        const params = new URLSearchParams({
          product_id: GUMROAD_PRODUCT_ID,
          license_key: key,
        });
        const gr = await fetch("https://api.gumroad.com/v2/licenses/verify", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: params.toString(),
        });
        const data = await gr.json();
        if (data && data.success) {
          return json({
            success: true,
            email: data.purchase?.email || null,
            uses: data.uses || 0,
          }, 200, request);
        }
        return json({ success: false, error: data?.message || "유효하지 않은 라이선스 키입니다" }, 200, request);
      } catch (e) {
        return json({ success: false, error: "검증 실패: " + e.message }, 500, request);
      }
    }

    // ── POST /auth/register ──────────────────────────────────────────────────
    if (path === "/auth/register" && request.method === "POST") {
      try {
        const { email, password, name } = await request.json();
        if (!email || !password || !name) return json({ error: "Missing fields" }, 400, request);
        if (password.length < 8) return json({ error: "Password must be at least 8 characters" }, 400, request);

        const existing = await getUserIdByEmail(env, email);
        if (existing) return json({ error: "Email already registered" }, 409, request);

        const { hash, salt } = await hashPassword(password);
        const userId = crypto.randomUUID();
        const member = {
          id: userId,
          email: email.toLowerCase(),
          name,
          passwordHash: hash,
          passwordSalt: salt,
          plan: "free",
          createdAt: new Date().toISOString(),
          lastLogin: null,
        };

        await saveMember(env, member);
        await setEmailIndex(env, email, userId);

        // 환영 이메일 발송
        await sendEmail(env, {
          to: member.email,
          subject: "Welcome to KR Guide! 🎉",
          html: welcomeEmail(name),
        });

        const token = await createSession(env, userId, member.email, member.plan);

        return new Response(JSON.stringify({ success: true, name: member.name, plan: member.plan }), {
          status: 201,
          headers: { "Content-Type": "application/json", "Set-Cookie": sessionCookie(token), ...corsHeaders(request) },
        });
      } catch (e) {
        return json({ error: "Server error", detail: e.message }, 500, request);
      }
    }

    // ── POST /auth/login ─────────────────────────────────────────────────────
    if (path === "/auth/login" && request.method === "POST") {
      try {
        const { email, password } = await request.json();
        if (!email || !password) return json({ error: "Missing fields" }, 400, request);

        const userId = await getUserIdByEmail(env, email);
        if (!userId) return json({ error: "Invalid email or password" }, 401, request);

        const member = await getMember(env, userId);
        if (!member) return json({ error: "Invalid email or password" }, 401, request);

        const valid = await verifyPassword(password, member.passwordSalt, member.passwordHash);
        if (!valid) return json({ error: "Invalid email or password" }, 401, request);

        member.lastLogin = new Date().toISOString();
        await saveMember(env, member);

        const token = await createSession(env, userId, member.email, member.plan);

        return new Response(JSON.stringify({ success: true, name: member.name, plan: member.plan }), {
          status: 200,
          headers: { "Content-Type": "application/json", "Set-Cookie": sessionCookie(token), ...corsHeaders(request) },
        });
      } catch (e) {
        return json({ error: "Server error" }, 500, request);
      }
    }

    // ── GET /auth/verify ─────────────────────────────────────────────────────
    if (path === "/auth/verify" && request.method === "GET") {
      const token = getTokenFromCookie(request);
      const session = await getSession(env, token);
      if (!session) return json({ loggedIn: false }, 200, request);
      return json({ loggedIn: true, userId: session.userId, email: session.email, plan: session.plan }, 200, request);
    }

    // ── GET /auth/profile ────────────────────────────────────────────────────
    if (path === "/auth/profile" && request.method === "GET") {
      const token = getTokenFromCookie(request);
      const session = await getSession(env, token);
      if (!session) return json({ error: "Not authenticated" }, 401, request);

      const member = await getMember(env, session.userId);
      if (!member) return json({ error: "Member not found" }, 404, request);

      return json({ id: member.id, name: member.name, email: member.email, plan: member.plan, createdAt: member.createdAt, lastLogin: member.lastLogin }, 200, request);
    }

    // ── POST /auth/logout ────────────────────────────────────────────────────
    if (path === "/auth/logout" && request.method === "POST") {
      const token = getTokenFromCookie(request);
      if (token) await deleteSession(env, token);
      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { "Content-Type": "application/json", "Set-Cookie": sessionCookie(null, true), ...corsHeaders(request) },
      });
    }

    // ── POST /auth/forgot-password ───────────────────────────────────────────
    if (path === "/auth/forgot-password" && request.method === "POST") {
      try {
        const { email } = await request.json();
        if (!email) return json({ error: "Email required" }, 400, request);

        // 이메일이 없어도 같은 응답 (보안상 이메일 존재 여부 노출 방지)
        const userId = await getUserIdByEmail(env, email);
        if (userId) {
          const resetToken = await createResetToken(env, userId);
          const resetUrl = `${SITE_URL}/reset-password/?token=${resetToken}`;

          await sendEmail(env, {
            to: email.toLowerCase(),
            subject: "KR Guide — Password Reset Request",
            html: resetEmail(resetUrl),
          });
        }

        return json({ success: true, message: "If this email is registered, a reset link has been sent." }, 200, request);
      } catch (e) {
        return json({ error: "Server error" }, 500, request);
      }
    }

    // ── POST /auth/reset-password ────────────────────────────────────────────
    if (path === "/auth/reset-password" && request.method === "POST") {
      try {
        const { token, newPassword } = await request.json();
        if (!token || !newPassword) return json({ error: "Missing fields" }, 400, request);
        if (newPassword.length < 8) return json({ error: "Password must be at least 8 characters" }, 400, request);

        const userId = await getResetToken(env, token);
        if (!userId) return json({ error: "Invalid or expired reset link" }, 400, request);

        const member = await getMember(env, userId);
        if (!member) return json({ error: "Member not found" }, 404, request);

        const { hash, salt } = await hashPassword(newPassword);
        member.passwordHash = hash;
        member.passwordSalt = salt;
        await saveMember(env, member);
        await deleteResetToken(env, token);

        return json({ success: true, message: "Password updated. You can now log in." }, 200, request);
      } catch (e) {
        return json({ error: "Server error" }, 500, request);
      }
    }

    // ── GET /auth/google ─────────────────────────────────────────────────────
    if (path === "/auth/google" && request.method === "GET") {
      const state = crypto.randomUUID().replace(/-/g, "");
      await env.SESSIONS.put(`gstate:${state}`, "1", { expirationTtl: 600 });
      const params = new URLSearchParams({
        client_id: env.GOOGLE_CLIENT_ID,
        redirect_uri: GOOGLE_REDIRECT,
        response_type: "code",
        scope: "openid email profile",
        state,
        prompt: "select_account",
      });
      return Response.redirect(`https://accounts.google.com/o/oauth2/v2/auth?${params}`, 302);
    }

    // ── GET /auth/google/callback ─────────────────────────────────────────────
    if (path === "/auth/google/callback" && request.method === "GET") {
      const code  = url.searchParams.get("code");
      const state = url.searchParams.get("state");
      const err   = url.searchParams.get("error");

      if (err || !code || !state) {
        return Response.redirect(`${SITE_URL}/login/?error=google_cancelled`, 302);
      }

      // CSRF 검증
      const stateOk = await env.SESSIONS.get(`gstate:${state}`);
      if (!stateOk) return Response.redirect(`${SITE_URL}/login/?error=invalid_state`, 302);
      await env.SESSIONS.delete(`gstate:${state}`);

      // 코드 → 액세스 토큰 교환
      const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          code,
          client_id: env.GOOGLE_CLIENT_ID,
          client_secret: env.GOOGLE_CLIENT_SECRET,
          redirect_uri: GOOGLE_REDIRECT,
          grant_type: "authorization_code",
        }),
      });
      if (!tokenRes.ok) return Response.redirect(`${SITE_URL}/login/?error=google_token_failed`, 302);
      const tokens = await tokenRes.json();

      // 구글 사용자 정보 조회
      const userRes = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
        headers: { Authorization: `Bearer ${tokens.access_token}` },
      });
      if (!userRes.ok) return Response.redirect(`${SITE_URL}/login/?error=google_userinfo_failed`, 302);
      const gUser = await userRes.json();
      const email = gUser.email.toLowerCase();

      // 기존 회원 조회 또는 신규 생성
      let userId = await getUserIdByEmail(env, email);
      let member;

      if (userId) {
        member = await getMember(env, userId);
      } else {
        userId = crypto.randomUUID();
        member = {
          id: userId,
          email,
          name: gUser.name || email.split("@")[0],
          passwordHash: null,
          passwordSalt: null,
          provider: "google",
          googleId: gUser.id,
          plan: "free",
          createdAt: new Date().toISOString(),
          lastLogin: null,
        };
        await saveMember(env, member);
        await setEmailIndex(env, email, userId);
        // 환영 이메일 (비동기, 실패해도 무시)
        sendEmail(env, { to: email, subject: "Welcome to KR Guide! 🎉", html: welcomeEmail(member.name) }).catch(() => {});
      }

      member.lastLogin = new Date().toISOString();
      if (!member.googleId) member.googleId = gUser.id;
      await saveMember(env, member);

      const token = await createSession(env, userId, email, member.plan);
      return new Response(null, {
        status: 302,
        headers: { Location: `${SITE_URL}/korean-library/`, "Set-Cookie": sessionCookie(token) },
      });
    }

    // ── GET /auth/members (admin) ────────────────────────────────────────────
    if (path === "/auth/members" && request.method === "GET") {
      const adminKey = url.searchParams.get("key");
      if (adminKey !== env.ADMIN_KEY) return json({ error: "Unauthorized" }, 401, request);

      const list = await env.MEMBERS_BUCKET.list({ prefix: "members/" });
      const members = await Promise.all(
        list.objects.map(async obj => {
          const raw = await env.MEMBERS_BUCKET.get(obj.key);
          const m = JSON.parse(await raw.text());
          return { id: m.id, email: m.email, name: m.name, plan: m.plan, createdAt: m.createdAt, lastLogin: m.lastLogin };
        })
      );
      return json({ total: members.length, members }, 200, request);
    }

    return json({ service: "KR Guide Auth API", version: "1.0", endpoints: ["/auth/register", "/auth/login", "/auth/verify", "/auth/profile", "/auth/logout", "/auth/forgot-password", "/auth/reset-password"] }, 200, request);
  },
};
