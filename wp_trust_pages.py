"""
Strengthen trust pages: Privacy Policy, Terms of Use, About, Contact.
Also add footer with all links to Home + Learn Korean.
"""
import requests
import base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"

cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

def wp_html(s): return f"<!-- wp:html -->\n{s}\n<!-- /wp:html -->"

# ---- Privacy Policy ----
PRIVACY_HTML = """<div style="max-width:780px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.7;color:#1a1a2e;">

<div style="text-align:center;padding:48px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:32px;">
<h1 style="font-size:34px;margin:0 0 10px;color:#fff;">Privacy Policy</h1>
<p style="font-size:14px;opacity:0.85;">개인정보 처리방침 · Last updated: 2026-05-22</p>
</div>

<h2 style="border-left:4px solid #C0392B;padding-left:14px;margin:32px 0 14px;">1. Information We Collect</h2>
<p>KR Guide collects only the information necessary to provide our Korean learning service:</p>
<ul style="line-height:2;">
<li><strong>Payment information</strong> — processed entirely by Gumroad; we do not store credit card details.</li>
<li><strong>Email address</strong> — used by Gumroad to deliver your license key after purchase.</li>
<li><strong>License key</strong> — stored locally in your browser (localStorage) to unlock paid content.</li>
</ul>

<h2 style="border-left:4px solid #1A4A8A;padding-left:14px;margin:32px 0 14px;">2. How We Use Your Information</h2>
<ul style="line-height:2;">
<li>To verify your purchase and grant access to paid Korean learning materials.</li>
<li>To send you the license key after a successful purchase (via Gumroad).</li>
<li>To respond to support inquiries you send to <a href="mailto:hello@krguide.com">hello@krguide.com</a>.</li>
</ul>

<h2 style="border-left:4px solid #059669;padding-left:14px;margin:32px 0 14px;">3. Third-Party Services</h2>
<ul style="line-height:2;">
<li><strong>Gumroad</strong> — payment processing and license key generation. See <a href="https://gumroad.com/privacy" target="_blank" rel="noopener">Gumroad's privacy policy</a>.</li>
<li><strong>Cloudflare</strong> — site hosting and security.</li>
<li><strong>Google Translate</strong> — optional translation widget (loaded only if you use it).</li>
<li><strong>Naver Dictionary</strong> — optional external search (opens a new tab when used).</li>
</ul>

<h2 style="border-left:4px solid #D97706;padding-left:14px;margin:32px 0 14px;">4. Cookies and Local Storage</h2>
<p>We use browser localStorage to remember your license key so you don't need to re-enter it each visit. We do not use third-party tracking cookies.</p>

<h2 style="border-left:4px solid #7C3AED;padding-left:14px;margin:32px 0 14px;">5. Your Rights</h2>
<p>You can request deletion of your data by emailing <a href="mailto:hello@krguide.com">hello@krguide.com</a>. Refunds are processed directly by Gumroad within 7 days of purchase.</p>

<h2 style="border-left:4px solid #B91C1C;padding-left:14px;margin:32px 0 14px;">6. Contact</h2>
<p>Questions about this Privacy Policy? Email <a href="mailto:hello@krguide.com">hello@krguide.com</a>.</p>

</div>"""

# ---- Terms of Use ----
TERMS_HTML = """<div style="max-width:780px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.7;color:#1a1a2e;">

<div style="text-align:center;padding:48px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:32px;">
<h1 style="font-size:34px;margin:0 0 10px;color:#fff;">Terms of Use</h1>
<p style="font-size:14px;opacity:0.85;">이용약관 · Last updated: 2026-05-22</p>
</div>

<h2 style="border-left:4px solid #C0392B;padding-left:14px;margin:32px 0 14px;">1. Service Description</h2>
<p>KR Guide ("we", "our") provides Korean language learning materials including a 41-chapter main guide and 14 vocabulary resources (6,546 words and expressions). The service is accessible via the web at krguide.com and krguide-vocab.pages.dev.</p>

<h2 style="border-left:4px solid #1A4A8A;padding-left:14px;margin:32px 0 14px;">2. Purchase & License</h2>
<ul style="line-height:2;">
<li>A one-time payment of $19.90 (via Gumroad) grants the buyer a personal, non-transferable license to access all paid content.</li>
<li>Upon successful payment, Gumroad automatically issues a license key by email.</li>
<li>The license key is for personal use only and may not be shared, resold, or distributed.</li>
<li>Future content updates are included at no extra cost.</li>
</ul>

<h2 style="border-left:4px solid #059669;padding-left:14px;margin:32px 0 14px;">3. Refund Policy</h2>
<p>Refunds are handled directly by Gumroad. Buyers may request a refund within 7 days of purchase through their Gumroad account. After 7 days, refunds are not guaranteed.</p>

<h2 style="border-left:4px solid #D97706;padding-left:14px;margin:32px 0 14px;">4. Copyright & Intellectual Property</h2>
<p>All Korean learning content (text, examples, dialogues, designs) is the intellectual property of KR Guide and protected by copyright. You may:</p>
<ul style="line-height:2;">
<li>Use the materials for personal study.</li>
<li>Print pages for personal reference.</li>
</ul>
<p>You may NOT:</p>
<ul style="line-height:2;">
<li>Redistribute, resell, or share the content with others.</li>
<li>Copy substantial portions of content for commercial use.</li>
<li>Remove copyright notices or attempt to bypass paywall mechanisms.</li>
</ul>

<h2 style="border-left:4px solid #7C3AED;padding-left:14px;margin:32px 0 14px;">5. Limitation of Liability</h2>
<p>KR Guide provides materials "as is" without warranty. We strive for accuracy in all Korean language explanations but cannot guarantee 100% accuracy for every nuance. Use the materials as a learning aid, not as a definitive linguistic authority.</p>

<h2 style="border-left:4px solid #B91C1C;padding-left:14px;margin:32px 0 14px;">6. Account Termination</h2>
<p>We reserve the right to revoke license keys obtained through fraudulent means, refund disputes, or breach of these Terms.</p>

<h2 style="border-left:4px solid #374151;padding-left:14px;margin:32px 0 14px;">7. Changes to Terms</h2>
<p>We may update these Terms occasionally. Material changes will be announced on the homepage. Continued use after changes constitutes acceptance.</p>

<h2 style="border-left:4px solid #1a1a2e;padding-left:14px;margin:32px 0 14px;">8. Contact</h2>
<p>Questions about these Terms? Email <a href="mailto:hello@krguide.com">hello@krguide.com</a>.</p>

</div>"""

# ---- About (refresh, with trust signals) ----
ABOUT_HTML = """<div style="max-width:780px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.7;color:#1a1a2e;">

<div style="text-align:center;padding:60px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:32px;">
<h1 style="font-size:38px;margin:0 0 12px;color:#fff;">About KR Guide</h1>
<p style="font-size:17px;opacity:0.9;">The Easiest, Deepest Way to Learn Korean</p>
</div>

<h2 style="border-left:4px solid #C0392B;padding-left:14px;margin:32px 0 14px;">🇰🇷 Mission</h2>
<p>KR Guide creates the most accessible and deep Korean learning resource for foreigners. We believe language learning should be both <strong>simple to start</strong> and <strong>rich enough to master</strong> — without overwhelming subscriptions or fragmented content.</p>

<h2 style="border-left:4px solid #1A4A8A;padding-left:14px;margin:32px 0 14px;">📚 What We Offer</h2>
<ul style="line-height:2;">
<li><strong>41-chapter Main Guide</strong> — Hangul · pronunciation · grammar · conversations · culture · honorifics.</li>
<li><strong>14 vocabulary categories · 6,546 words</strong> — verbs, nouns, adjectives, honorifics, idioms, proverbs, Konglish, onomatopoeia, IT terms, and more.</li>
<li><strong>Each entry includes</strong> — example sentences, scenario dialogues, comparison boxes, mini-quizzes, pronunciation QR codes.</li>
<li><strong>13 languages supported</strong> — Google Translate built-in for foreign learners.</li>
</ul>

<h2 style="border-left:4px solid #059669;padding-left:14px;margin:32px 0 14px;">✨ Our Promise</h2>
<ul style="line-height:2;">
<li><strong>One purchase · Lifetime access</strong> — no subscriptions, no recurring fees.</li>
<li><strong>Free updates included</strong> — same license key works for all future content.</li>
<li><strong>7-day money-back guarantee</strong> — refund through Gumroad if it's not for you.</li>
</ul>

<h2 style="border-left:4px solid #D97706;padding-left:14px;margin:32px 0 14px;">🛡️ Trust & Security</h2>
<ul style="line-height:2;">
<li><strong>Payments</strong> — processed by Gumroad (PCI-compliant, trusted by 100,000+ creators).</li>
<li><strong>Hosting</strong> — Cloudflare Pages (global CDN, free SSL).</li>
<li><strong>License verification</strong> — automatic via Gumroad's API.</li>
<li><strong>No third-party tracking</strong> — your data stays minimal.</li>
</ul>

<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:32px;border-radius:14px;text-align:center;margin-top:40px;">
<h3 style="color:#fff;margin:0 0 12px;">Start Learning Today</h3>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#fff;color:#C0392B;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">📚 Start Learning</a>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:transparent;color:#fff;border:2px solid #fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">💳 Buy $19.90</a>
</div>

</div>"""

# ---- Contact (refresh with full information) ----
CONTACT_HTML = """<div style="max-width:680px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.7;color:#1a1a2e;">

<div style="text-align:center;padding:60px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:32px;">
<h1 style="font-size:38px;margin:0 0 12px;color:#fff;">📧 Contact</h1>
<p style="font-size:17px;opacity:0.9;">Customer Support · 문의</p>
</div>

<div style="background:#fff;padding:32px;border-radius:14px;border-left:4px solid #C0392B;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:20px;">
<h2 style="margin:0 0 10px;">✉️ Email Support</h2>
<p style="color:#666;margin:0 0 12px;">For all support inquiries — learning content, payment, license key, or account issues:</p>
<p style="font-size:18px;"><a href="mailto:hello@krguide.com" style="color:#C0392B;font-weight:800;text-decoration:none;">hello@krguide.com</a></p>
<p style="color:#888;font-size:13px;margin-top:8px;">Response time: usually within 24 hours (KST business days).</p>
</div>

<div style="background:#fff;padding:32px;border-radius:14px;border-left:4px solid #1A4A8A;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:20px;">
<h2 style="margin:0 0 10px;">💳 Payment & Refunds</h2>
<p style="color:#666;margin:0 0 8px;">All payments are processed by <strong>Gumroad</strong>. After purchase, your license key is sent automatically by email.</p>
<p style="color:#666;margin:0;"><strong>Refunds:</strong> requested directly from Gumroad within 7 days of purchase.</p>
</div>

<div style="background:#fff;padding:32px;border-radius:14px;border-left:4px solid #059669;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:20px;">
<h2 style="margin:0 0 10px;">🔑 Lost License Key</h2>
<p style="color:#666;margin:0;">Email <a href="mailto:hello@krguide.com">hello@krguide.com</a> with the address used for purchase. We will help recover your key.</p>
</div>

<div style="background:#fff;padding:32px;border-radius:14px;border-left:4px solid #D97706;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:20px;">
<h2 style="margin:0 0 10px;">🐛 Report a Problem</h2>
<p style="color:#666;margin:0;">Found an error in a Korean example or broken link? Let us know — content fixes are usually deployed within 1-2 days.</p>
</div>

<div style="background:#fff;padding:32px;border-radius:14px;border-left:4px solid #7C3AED;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:20px;">
<h2 style="margin:0 0 10px;">💼 Business Inquiries</h2>
<p style="color:#666;margin:0;">For licensing, bulk purchase, or partnership inquiries, please email with subject line "Business".</p>
</div>

<div style="text-align:center;margin-top:32px;">
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#1a1a2e;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;">📚 Browse Learning Resources</a>
</div>

</div>"""

def update_page(page_id, content, title=None, excerpt=None):
    body = {"content": wp_html(content)}
    if title: body["title"] = title
    if excerpt: body["excerpt"] = excerpt
    r = requests.post(f"{SITE}/wp-json/wp/v2/pages/{page_id}", headers=HEADERS, json=body, timeout=60)
    if r.ok:
        d = r.json()
        print(f"[OK] Page {page_id} ('{d['title']['rendered']}')")
    else:
        print(f"[FAIL] Page {page_id}: {r.status_code} {r.text[:200]}")

print("=== Update Privacy Policy (ID 3) ===")
update_page(3, PRIVACY_HTML,
    title="Privacy Policy | KR Guide",
    excerpt="KR Guide privacy policy: what information we collect, how we use it, and your rights. We collect minimal data and use trusted third-party services like Gumroad and Cloudflare.")

print("\n=== Update Terms of Use (ID 1033) ===")
update_page(1033, TERMS_HTML,
    title="Terms of Use | KR Guide",
    excerpt="KR Guide terms of use: purchase, license, refunds, copyright. One-time $19.90 payment grants personal lifetime access to all Korean learning materials.")

print("\n=== Update About (ID 1490) ===")
update_page(1490, ABOUT_HTML,
    title="About KR Guide — Korean Learning for Foreigners",
    excerpt="KR Guide creates the most accessible Korean learning resource for foreigners. 41-chapter main guide + 6,546 essential words across 14 categories.")

print("\n=== Update Contact (ID 46) ===")
update_page(46, CONTACT_HTML,
    title="Contact KR Guide — Korean Learning Support",
    excerpt="Contact KR Guide for Korean learning support, payment questions, license key recovery, bug reports, or business inquiries.")

print("\n=== Done ===")
