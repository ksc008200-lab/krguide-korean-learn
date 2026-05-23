"""Add a prominent PDF download button to the home page (Page ID 21)."""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS_GET  = {"Authorization": f"Basic {cred}"}
HEADERS_POST = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

PDF_URL = "https://krguide.com/wp-content/uploads/2026/05/learn-korean-v3.pdf"
VOCAB_HUB = "https://study.krguide.com/vocab-hub.html"
GUMROAD   = "https://jssmn21.gumroad.com/l/gnefla"

PAGE_ID = 21

# Fetch current home page
r = requests.get(f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", headers=HEADERS_GET, timeout=30)
page = r.json()
raw = page["content"]["raw"]
print(f"Home page raw length: {len(raw)} chars\n")

# Build download section HTML
DOWNLOAD_SECTION = """
<!-- wp:html -->
<div id="ebook-download" style="background:linear-gradient(135deg,#1A4A8A 0%,#C0392B 100%);color:#fff;padding:48px 32px;border-radius:18px;margin:40px auto;max-width:1080px;text-align:center;box-shadow:0 12px 40px rgba(0,0,0,0.15);">
  <div style="font-size:14px;font-weight:800;letter-spacing:3px;color:#FACC15;margin-bottom:12px;">📘 COMPLETE EDITION</div>
  <h2 style="margin:0 0 14px;font-size:34px;color:#fff;line-height:1.2;">Learn Korean — 41-Chapter Complete Guide</h2>
  <p style="margin:0 0 28px;font-size:17px;opacity:0.95;max-width:680px;margin-left:auto;margin-right:auto;line-height:1.6;">
    한국어 배우기 완전 가이드 · From Hangul basics to Jeju dialect — every chapter bilingual with romanization, cultural notes, and learning tips.
  </p>
  <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
    <a href="HREF_PDF" download style="display:inline-block;background:#FACC15;color:#1A1A2E;padding:18px 36px;border-radius:10px;text-decoration:none;font-weight:800;font-size:17px;box-shadow:0 6px 20px rgba(0,0,0,0.2);">
      📥 Download PDF (Free)
    </a>
    <a href="HREF_HUB" style="display:inline-block;background:rgba(255,255,255,0.15);color:#fff;padding:18px 36px;border-radius:10px;text-decoration:none;font-weight:800;font-size:17px;border:2px solid rgba(255,255,255,0.4);">
      🎯 Browse Vocab Hub
    </a>
    <a href="HREF_GUM" style="display:inline-block;background:rgba(255,255,255,0.15);color:#fff;padding:18px 36px;border-radius:10px;text-decoration:none;font-weight:800;font-size:17px;border:2px solid rgba(255,255,255,0.4);">
      📚 Get Premium Edition
    </a>
  </div>
  <div style="margin-top:24px;font-size:13px;opacity:0.85;">
    🇰🇷 41 chapters · ~10 MB · Bilingual EN/KR · Updated 2026-05
  </div>
</div>
<!-- /wp:html -->
""".replace("HREF_PDF", PDF_URL).replace("HREF_HUB", VOCAB_HUB).replace("HREF_GUM", GUMROAD)

# Detect if already added; replace existing block if so
if "ebook-download" in raw:
    import re
    new_raw = re.sub(
        r'<!-- wp:html -->\s*<div id="ebook-download"[\s\S]*?<!-- /wp:html -->',
        DOWNLOAD_SECTION.strip(),
        raw,
        count=1,
    )
    print("[info] Existing download section replaced with updated version")
else:
    new_raw = DOWNLOAD_SECTION + "\n" + raw
    print("[info] Download section inserted at top of home page")

# PUT update
r = requests.post(
    f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}",
    headers=HEADERS_POST,
    json={"content": new_raw},
    timeout=60,
)
if r.ok:
    d = r.json()
    print(f"\n[OK] Home page updated → {d['link']}")
    print(f"     Content size: {len(d['content']['rendered'])} chars")
else:
    print(f"[FAIL] {r.status_code}")
    print(r.text[:300])
