"""Fix Navigation menu: change Learn Korean URL from learn.krguide.com to krguide.com home."""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

# Fetch current navigation
r = requests.get(f"{SITE}/wp-json/wp/v2/navigation/4?context=edit", headers=HEADERS, timeout=30)
nav = r.json()
raw = nav["content"]["raw"]
print("Before:")
print(raw)

# Replace dead learn.krguide.com URL with home
new_raw = raw.replace(
    '"url":"https://learn.krguide.com"',
    '"url":"https://krguide.com/"'
)
# Also catch trailing slash variant
new_raw = new_raw.replace(
    '"url":"https://learn.krguide.com/"',
    '"url":"https://krguide.com/"'
)

if new_raw == raw:
    print("\n[no change needed]")
else:
    r = requests.post(f"{SITE}/wp-json/wp/v2/navigation/4", headers=HEADERS,
                      json={"content": new_raw}, timeout=60)
    if r.ok:
        print("\n[OK] Menu updated")
        print("\nAfter:")
        print(r.json()["content"]["raw"])
    else:
        print(f"\n[FAIL] {r.status_code}: {r.text[:300]}")
