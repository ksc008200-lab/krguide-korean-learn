"""Add a 'Learn Korean → Home' banner at the top of the Blog page."""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

# Fetch Blog page raw content
r = requests.get(f"{SITE}/wp-json/wp/v2/pages?slug=blog&context=edit", headers=HEADERS, timeout=30)
page = r.json()[0]
pid = page["id"]
raw = page["content"]["raw"]

# Banner HTML to inject right after the opening wp:html block
BANNER = """
<a href="https://krguide.com/" style="display:block;text-align:center;background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:20px 24px;border-radius:14px;text-decoration:none;font-weight:800;font-size:18px;margin-bottom:24px;max-width:1080px;margin-left:auto;margin-right:auto;">
  🇰🇷 한국어를 배우세요 · Learn Korean — Back to Home →
</a>
"""

# Avoid duplicate insertion
if "한국어를 배우세요" in raw:
    # Replace existing banner with the latest version
    import re
    new_raw = re.sub(
        r'<a href="https://krguide\.com/"[^>]*>[\s\S]*?한국어를 배우세요[\s\S]*?</a>',
        BANNER.strip(),
        raw,
        count=1
    )
    if new_raw == raw:
        # not found via regex - just leave as is
        new_raw = raw
    print("[info] existing banner replaced")
else:
    # Insert right after the first <!-- wp:html -->
    new_raw = raw.replace("<!-- wp:html -->", "<!-- wp:html -->\n" + BANNER, 1)
    print("[info] new banner inserted")

r = requests.post(f"{SITE}/wp-json/wp/v2/pages/{pid}", headers=HEADERS,
                  json={"content": new_raw}, timeout=60)
if r.ok:
    d = r.json()
    print(f"[OK] Blog page updated → {d['link']}")
else:
    print(f"[FAIL] {r.status_code}: {r.text[:200]}")
