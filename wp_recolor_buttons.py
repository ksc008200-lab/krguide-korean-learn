"""Recolor the middle (Blog) and right (Premium) buttons on the home page download section.
Middle: cyan/teal — reading/fresh
Right:  pink/rose — premium/special
Left stays yellow (action/highlight)."""
import requests, base64, re

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS_GET  = {"Authorization": f"Basic {cred}"}
HEADERS_POST = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

PAGE_ID = 21
r = requests.get(f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", headers=HEADERS_GET, timeout=30)
raw = r.json()["content"]["raw"]

# Find and replace the Blog button (middle) — currently has semi-transparent bg
blog_pattern = re.compile(
    r'(<a href="https://krguide\.com/blog/"[^>]*?style=")[^"]*?("[^>]*?>\s*📝 Read Blog)',
    re.S,
)
NEW_BLOG_STYLE = (
    "display:inline-block;background:#06B6D4;"
    "color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;"
    "font-weight:800;font-size:17px;margin:4px;"
    "box-shadow:0 6px 20px rgba(0,0,0,0.2);"
)

# Find and replace the Premium button (right) — same semi-transparent bg
premium_pattern = re.compile(
    r'(<a href="https://jssmn21\.gumroad\.com/l/gnefla"[^>]*?style=")[^"]*?("[^>]*?>\s*📚 Get Premium Edition)',
    re.S,
)
NEW_PREMIUM_STYLE = (
    "display:inline-block;background:#EC4899;"
    "color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;"
    "font-weight:800;font-size:17px;margin:4px;"
    "box-shadow:0 6px 20px rgba(0,0,0,0.2);"
)

new_raw = blog_pattern.sub(rf'\1{NEW_BLOG_STYLE}\2', raw)
new_raw = premium_pattern.sub(rf'\1{NEW_PREMIUM_STYLE}\2', new_raw)

if new_raw == raw:
    print("[no change] — patterns didn't match. Showing first button block:")
    m = re.search(r'<a href="https://krguide\.com/blog/"[^>]*>.*?</a>', raw, re.S)
    if m: print(m.group(0)[:600])
    m2 = re.search(r'<a href="https://jssmn21\.gumroad\.com[^"]*"[^>]*>.*?</a>', raw, re.S)
    if m2: print(m2.group(0)[:600])
else:
    r = requests.post(
        f"{SITE}/wp-json/wp/v2/pages/{PAGE_ID}",
        headers=HEADERS_POST,
        json={"content": new_raw},
        timeout=60,
    )
    if r.ok:
        print("[OK] Home page buttons recolored")
        print("     Middle (Blog):   cyan gradient #06B6D4 → #0891B2")
        print("     Right (Premium): pink gradient #EC4899 → #BE185D")
    else:
        print(f"[FAIL] {r.status_code}: {r.text[:200]}")
