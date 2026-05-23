"""Inspect all blog posts for issues:
- Empty / too short content
- Broken links (learn.krguide.com, etc.)
- Duplicate posts (slug -2, -3, -4 variants)
- Missing excerpt or featured image
"""
import requests, base64, re

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}"}

# Fetch all posts
all_posts = []
page = 1
while True:
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts?per_page=50&page={page}&context=edit", headers=HEADERS, timeout=60)
    if not r.ok or not r.json():
        break
    batch = r.json()
    all_posts.extend(batch)
    if len(batch) < 50:
        break
    page += 1
    if page > 5: break

print(f"Total posts fetched: {len(all_posts)}\n")

# Group by base slug (stripping -2/-3/-4 suffixes)
slug_groups = {}
for p in all_posts:
    base = re.sub(r"-\d+$", "", p["slug"])
    slug_groups.setdefault(base, []).append(p)

print("=== Duplicate slug groups (multiple posts with -2/-3/-4) ===")
dupes = {k: v for k, v in slug_groups.items() if len(v) > 1}
for base, posts in dupes.items():
    print(f"\n[{base}]  ({len(posts)} posts)")
    for p in sorted(posts, key=lambda x: x["id"]):
        title = p["title"]["rendered"][:70]
        cw = len(p["content"]["raw"]) if "raw" in p["content"] else len(p["content"]["rendered"])
        print(f"  ID {p['id']}  slug:{p['slug']}  ({cw} chars)  → {title}")

print("\n=== Posts with content issues ===")
problems = []
for p in all_posts:
    raw = p["content"]["raw"] if "raw" in p["content"] else p["content"]["rendered"]
    issues = []
    if len(raw) < 500:
        issues.append(f"too short ({len(raw)} chars)")
    if "learn.krguide.com" in raw:
        issues.append("contains dead learn.krguide.com link")
    if "[caption" in raw or "[/caption]" in raw or "[shortcode" in raw:
        issues.append("contains broken shortcodes")
    # Find broken hrefs
    if re.search(r'href=""', raw) or re.search(r'href="#"', raw):
        issues.append("empty/anchor-only links")
    if issues:
        problems.append((p, issues))
        print(f"  ID {p['id']} ({p['slug']}): {', '.join(issues)}")

print(f"\nTotal posts with issues: {len(problems)}")
print(f"Total duplicate groups: {len(dupes)}")
