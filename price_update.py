"""Bulk replace $19.90 → $19.90 across all local files AND on WordPress pages."""
import re, requests, base64
from pathlib import Path

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
OLD_PRICES = ["$19.90", "$19.90", "$19.90", "$19.90", "$19.90", "$19.90"]
NEW_PRICE = "$19.90"

# Skip these (binary or non-content)
SKIP_PATTERNS = ["node_modules", ".git", "v2_unpack", "favicon", ".pdf",
                 ".png", ".jpg", ".jpeg", ".docx", ".doc", ".zip"]

# ── 1. Local files ──
total_files = 0
total_replacements = 0
for f in ROOT.rglob("*"):
    if not f.is_file():
        continue
    sp = str(f)
    if any(s in sp for s in SKIP_PATTERNS):
        continue
    try:
        txt = f.read_text(encoding="utf-8")
    except Exception:
        continue
    orig = txt
    for old in OLD_PRICES:
        txt = txt.replace(old, NEW_PRICE)
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        n = sum(orig.count(old) for old in OLD_PRICES)
        total_replacements += n
        total_files += 1
        print(f"  {f.relative_to(ROOT)}  ({n} replacements)")

print(f"\nLocal: {total_files} files updated, {total_replacements} replacements")

# ── 2. WordPress pages/posts ──
SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS_GET  = {"Authorization": f"Basic {cred}"}
HEADERS_POST = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

print("\n--- WordPress scan ---")

def patch_endpoint(endpoint, label):
    updated = 0
    page = 1
    while True:
        r = requests.get(f"{SITE}/wp-json/wp/v2/{endpoint}?per_page=50&page={page}&context=edit",
                         headers=HEADERS_GET, timeout=60)
        if not r.ok or not r.json():
            break
        items = r.json()
        for item in items:
            raw = item["content"]["raw"]
            new_raw = raw
            for old in OLD_PRICES:
                new_raw = new_raw.replace(old, NEW_PRICE)
            if new_raw != raw:
                pr = requests.post(f"{SITE}/wp-json/wp/v2/{endpoint}/{item['id']}",
                                   headers=HEADERS_POST,
                                   json={"content": new_raw}, timeout=60)
                if pr.ok:
                    print(f"  {label} ID {item['id']}: '{item['title']['rendered'][:50]}'")
                    updated += 1
        if len(items) < 50:
            break
        page += 1
        if page > 10:
            break
    return updated

p_updated = patch_endpoint("pages", "page")
print(f"Pages updated: {p_updated}")
posts_updated = patch_endpoint("posts", "post")
print(f"Posts updated: {posts_updated}")
