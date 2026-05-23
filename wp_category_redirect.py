"""Update 'Learn Korean' category description with redirect to home."""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

# Category 4 = "Learn Korean"
desc_html = """<div style="text-align:center;padding:20px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:12px;color:#fff;margin:20px 0;">
<p style="margin:0 0 10px;font-size:16px;">한국어를 배우세요 · Visit our home page for the complete Korean learning experience</p>
<a href="https://krguide.com/" style="display:inline-block;background:#f97316;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:800;">🇰🇷 Go to Home →</a>
</div>
<script>setTimeout(function(){window.location.href='https://krguide.com/';},500);</script>"""

r = requests.post(
    f"{SITE}/wp-json/wp/v2/categories/4",
    headers=HEADERS,
    json={"description": desc_html, "name": "Learn Korean"},
    timeout=30,
)
if r.ok:
    d = r.json()
    print(f"[OK] Category 4 updated: {d['name']}")
    print(f"     Description preview: {d['description'][:200]}")
    print(f"     Link: {d['link']}")
else:
    print(f"[FAIL] {r.status_code}: {r.text[:300]}")
