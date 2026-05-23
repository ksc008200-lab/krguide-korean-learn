"""Fix the middle button on the home page download section.
Change from study.krguide.com/vocab-hub.html → krguide.com/blog/
(User wants the button to point to the blog 'Korean Learning Tips' section,
since the homepage already contains vocab content inline.)
"""
import requests, base64, re

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS_GET  = {"Authorization": f"Basic {cred}"}
HEADERS_POST = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

PAGE_ID = 21
OLD_URL = "https://study.krguide.com/vocab-hub.html"
NEW_URL = "https://krguide.com/blog/"

# Fetch home page
r = requests.get(f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", headers=HEADERS_GET, timeout=30)
page = r.json()
raw = page["content"]["raw"]

# Replace the button URL and label
# Original button: "🎯 Browse Vocab Hub" → study.krguide
# New: "📝 Read Blog · Korean Learning Tips" → krguide.com/blog/

new_raw = raw.replace(OLD_URL, NEW_URL)
# Replace button label too
new_raw = new_raw.replace(
    "🎯 Browse Vocab Hub",
    "📝 Read Blog · 한국어 학습팁",
)

if new_raw == raw:
    print("[no change] — already updated or button text differs")
else:
    r = requests.post(
        f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}",
        headers=HEADERS_POST,
        json={"content": new_raw},
        timeout=60,
    )
    if r.ok:
        d = r.json()
        print(f"[OK] Middle button updated → {NEW_URL}")
        print(f"     Label: 📝 Read Blog · 한국어 학습팁")
        print(f"     Page: {d['link']}")
    else:
        print(f"[FAIL] {r.status_code}: {r.text[:300]}")
