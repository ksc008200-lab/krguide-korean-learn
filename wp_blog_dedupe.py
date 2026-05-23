"""De-duplicate blog posts.

Strategy:
  Group posts by base slug (strip trailing -N).
  In each group with >1 posts, KEEP one post and TRASH the rest.
  Keep priority:
    1. Slug without -N suffix (the 'original' canonical slug)
    2. Otherwise the post with the lowest ID

Trash = force=false (WordPress trash, recoverable for 30 days).
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
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts?per_page=50&page={page}&context=edit",
                     headers=HEADERS, timeout=60)
    if not r.ok or not r.json():
        break
    batch = r.json()
    all_posts.extend(batch)
    if len(batch) < 50:
        break
    page += 1
    if page > 10: break

print(f"Total posts fetched: {len(all_posts)}\n")

# Group by base slug
slug_groups = {}
for p in all_posts:
    base = re.sub(r"-\d+$", "", p["slug"])
    slug_groups.setdefault(base, []).append(p)

dupes = {k: v for k, v in slug_groups.items() if len(v) > 1}
print(f"Duplicate groups: {len(dupes)}\n")

def has_suffix(p):
    return bool(re.search(r"-\d+$", p["slug"]))

trash_ids = []
keep_log = []

for base, posts in dupes.items():
    # Sort: prefer no -N suffix, then lowest ID
    posts_sorted = sorted(posts, key=lambda p: (has_suffix(p), p["id"]))
    keeper = posts_sorted[0]
    to_trash = posts_sorted[1:]
    keep_log.append((base, keeper, to_trash))
    trash_ids.extend(p["id"] for p in to_trash)

print(f"Posts to KEEP: {len(dupes)}")
print(f"Posts to TRASH: {len(trash_ids)}\n")

# Show plan
for base, keeper, to_trash in keep_log:
    print(f"[{base}]")
    print(f"  KEEP   ID {keeper['id']:>5}  slug:{keeper['slug']}")
    for p in to_trash:
        print(f"  TRASH  ID {p['id']:>5}  slug:{p['slug']}")

print("\n--- Executing trash operations ---\n")

ok = 0
fail = 0
for pid in trash_ids:
    r = requests.delete(f"{SITE}/wp-json/wp/v2/posts/{pid}?force=false",
                        headers=HEADERS, timeout=30)
    if r.ok:
        ok += 1
        print(f"  [OK]   trashed ID {pid}")
    else:
        fail += 1
        print(f"  [FAIL] ID {pid}  {r.status_code}: {r.text[:120]}")

print(f"\n=== Result: {ok} trashed, {fail} failed ===")
