"""
Append trust footer (About/Privacy/Terms/Contact links) to Home and Learn Korean pages.
"""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

def wp_html(s): return f"<!-- wp:html -->\n{s}\n<!-- /wp:html -->"

# Fetch existing content
def get_page(pid):
    r = requests.get(f"{SITE}/wp-json/wp/v2/pages/{pid}?context=edit", headers=HEADERS, timeout=30)
    return r.json() if r.ok else None

FOOTER_HTML = """
<div style="margin-top:48px;padding:32px 24px;background:#1a1a2e;color:#fff;border-radius:14px;text-align:center;font-family:'Noto Sans KR',sans-serif;">
  <div style="font-size:13px;color:#f97316;font-weight:700;letter-spacing:3px;margin-bottom:10px;">KR GUIDE</div>
  <p style="opacity:0.7;font-size:13px;margin:0 0 18px;">Learn Korean — The Easiest, Deepest Way · 한국어를 가장 쉽게, 가장 깊이</p>
  <div style="display:flex;justify-content:center;flex-wrap:wrap;gap:18px;font-size:14px;font-weight:600;">
    <a href="https://krguide.com/about/" style="color:#fff;text-decoration:none;">About</a>
    <a href="https://krguide.com/contact/" style="color:#fff;text-decoration:none;">Contact</a>
    <a href="https://krguide.com/privacy-policy/" style="color:#fff;text-decoration:none;">Privacy Policy</a>
    <a href="https://krguide.com/terms/" style="color:#fff;text-decoration:none;">Terms of Use</a>
    <a href="https://krguide-vocab.pages.dev/vocab-hub" style="color:#fbbf24;text-decoration:none;">Learning Hub</a>
  </div>
  <div style="margin-top:18px;font-size:12px;opacity:0.5;">© 2026 KR Guide. All rights reserved.</div>
  <div style="margin-top:8px;font-size:11px;opacity:0.5;">Payments processed by Gumroad · Hosted on Cloudflare</div>
</div>
"""

for pid in [21, 1147]:
    page = get_page(pid)
    if not page:
        print(f"[FAIL] cannot fetch page {pid}")
        continue
    raw = page["content"]["raw"]
    # Append footer just before the closing wp:html block (if present), else at the end
    if "<!-- /wp:html -->" in raw:
        # find last content block and append before its end
        # simplest: replace last </div></div> at end of content
        new_content = raw.rstrip()
        # remove trailing wp:html close, append footer, re-close
        last_close = "<!-- /wp:html -->"
        if new_content.endswith(last_close):
            inner = new_content[:-len(last_close)].rstrip()
            new_content = inner + "\n" + FOOTER_HTML + "\n" + last_close
        else:
            new_content = raw + "\n" + wp_html(FOOTER_HTML)
    else:
        new_content = raw + "\n" + wp_html(FOOTER_HTML)
    r = requests.post(f"{SITE}/wp-json/wp/v2/pages/{pid}", headers=HEADERS, json={"content": new_content}, timeout=60)
    if r.ok:
        print(f"[OK] Footer added to page {pid}")
    else:
        print(f"[FAIL] page {pid}: {r.status_code} {r.text[:200]}")

print("\n=== Done ===")
