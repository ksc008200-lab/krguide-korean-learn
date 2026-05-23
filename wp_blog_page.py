"""
1. Retry the 8th post that failed (why-learn-korean-2026)
2. Fetch all posts and build a Blog listing page with search bar
3. Add Blog link to Home page
"""
import requests, base64, time

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

def wp_html(s): return f"<!-- wp:html -->\n{s}\n<!-- /wp:html -->"

# ---- Retry 8th post ----
POST_8 = {
    "title": "5 Reasons to Learn Korean in 2026",
    "slug": "why-learn-korean-2026",
    "excerpt": "Korean is the fastest-growing language for foreigners worldwide. Here are 5 compelling reasons to start learning Korean in 2026.",
    "content": wp_html("""<div style="max-width:780px;margin:0 auto;font-family:'Noto Sans KR',sans-serif;line-height:1.75;color:#1a1a2e;font-size:16px;">
<p style="font-size:18px;color:#555;font-style:italic;border-left:4px solid #C0392B;padding-left:16px;margin:20px 0;">2026년 한국어를 배워야 하는 5가지 이유 — Korean has become one of the most valuable languages to learn worldwide.</p>
<p>The number of Korean learners worldwide has exploded. Korean is the 7th most-studied language globally on Duolingo. Why? Here are five reasons why now is the time.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #C0392B;padding-left:14px;margin-top:36px;">1. 🎵 Hallyu (한류) — The Korean Wave</h2>
<p>K-pop, K-drama, K-content dominate global culture. BTS topped charts, Squid Game became Netflix's biggest non-English show. Learning Korean unlocks lyrics, drama nuances, direct fan connection on V Live, and the world's #1 webtoon industry. K-content is projected to grow into a $200 billion industry by 2030.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #1A4A8A;padding-left:14px;margin-top:36px;">2. 💼 Korea Is a Global Economic Powerhouse</h2>
<p>South Korea is the world's 10th-largest economy. Samsung, SK Hynix, Hyundai, LG, Naver, Kakao — Korean companies dominate semiconductors, automotive, displays, K-beauty ($13B industry). Korean proficiency gives major career advantages in tech, manufacturing, and entertainment.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #059669;padding-left:14px;margin-top:36px;">3. 📚 Hangul Is the Easiest Major Alphabet</h2>
<p>Only 24 letters. Learnable in 2-5 hours. Letters shaped after vocal organs — visual mnemonic built in. Strictly phonetic, no "though/through/thought" chaos. UNESCO-recognized.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #D97706;padding-left:14px;margin-top:36px;">4. 🇰🇷 Korea Is an Amazing Travel Destination</h2>
<p>17+ million tourists yearly. Seoul, Busan, Jeju, Gyeongju, DMZ are world-class destinations. Korean unlocks authentic experiences — hole-in-the-wall restaurants, subway navigation, real cultural connections, traditional sites with context.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #7C3AED;padding-left:14px;margin-top:36px;">5. 🧠 Korean Trains Your Brain Uniquely</h2>
<p>SOV word order, honorific system, particles, sound-based writing, Sino-Korean roots that open doors to Chinese and Japanese. Bilingual brains have better memory, delayed cognitive decline. Korean's structure offers especially rich neural exercise.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #B91C1C;padding-left:14px;margin-top:36px;">🎯 How to Start Right Now</h2>
<p>Today: Learn Hangul (4-5 hours). Week 1: 30 essential verbs. Month 1: Watch K-drama with Korean subs. Month 6: TOPIK Level 2 achievable. K-content is everywhere, resources have never been more abundant.</p>

<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:32px 28px;border-radius:14px;text-align:center;margin:30px 0;">
<h3 style="color:#fff;margin:0 0 10px;font-size:22px;">📚 Start Your Korean Journey Today</h3>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#fff;color:#C0392B;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">📚 Browse Resources</a>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:transparent;color:#fff;border:2px solid #fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">💳 Buy $19.90</a>
</div>
</div>"""),
    "status": "publish",
}

# Retry posting
r = requests.post(f"{SITE}/wp-json/wp/v2/posts", headers=HEADERS, json=POST_8, timeout=60)
if r.ok:
    d = r.json()
    print(f"[OK] Retry post {d['id']}: '{d['title']['rendered'][:60]}'")
else:
    print(f"[FAIL] retry: {r.status_code}")
time.sleep(1)

# ---- Fetch all posts ----
r = requests.get(f"{SITE}/wp-json/wp/v2/posts?per_page=50&status=publish&_fields=id,title,excerpt,link,date,slug", headers=HEADERS, timeout=30)
posts = r.json() if r.ok else []
print(f"\nFound {len(posts)} posts")

# ---- Build Blog page HTML ----
cards = []
for p in posts:
    title = p["title"]["rendered"]
    link = p["link"]
    excerpt = p["excerpt"]["rendered"].replace("<p>", "").replace("</p>", "").strip()
    if len(excerpt) > 180:
        excerpt = excerpt[:180] + "…"
    date = p["date"][:10]
    cards.append(f"""
<a href="{link}" style="display:flex;flex-direction:column;background:#fff;padding:24px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #C0392B;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
<div style="font-size:12px;color:#888;margin-bottom:8px;">{date}</div>
<h3 style="font-size:17px;margin:0 0 10px;color:#1a1a2e;font-weight:800;line-height:1.4;">{title}</h3>
<p style="font-size:13px;color:#666;line-height:1.6;flex:1;margin:0 0 12px;">{excerpt}</p>
<div style="font-size:12px;color:#C0392B;font-weight:800;text-align:right;">Read more →</div>
</a>""")

BLOG_HTML = """<div style="max-width:1080px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.6;color:#1a1a2e;">

<div style="text-align:center;padding:60px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:32px;">
<h1 style="font-size:38px;margin:0 0 12px;color:#fff;">📝 Blog</h1>
<p style="font-size:17px;opacity:0.9;margin:0;">Korean learning tips, culture, language insights</p>
</div>

<form method="GET" action="https://krguide.com/" style="background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin:0 auto 30px;max-width:680px;display:flex;gap:8px;align-items:center;">
<span style="font-size:20px;">🔎</span>
<input type="search" name="s" placeholder="Search blog posts · 블로그 글 검색" style="flex:1;padding:10px 14px;border:1.5px solid #e5e5ea;border-radius:8px;font-size:14px;outline:none;">
<button type="submit" style="background:#1a1a2e;color:#fff;border:none;padding:10px 22px;border-radius:8px;font-weight:800;cursor:pointer;font-size:14px;">Search</button>
</form>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));grid-auto-rows:1fr;gap:20px;margin-bottom:40px;">
""" + "".join(cards) + """
</div>

<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:36px 28px;border-radius:18px;text-align:center;">
<h2 style="margin:0 0 10px;color:#fff;font-size:24px;">📚 Ready for the Full Learning Experience?</h2>
<p style="margin:0 0 20px;opacity:0.92;">14 vocabulary resources · 6,546 words · 41-chapter Main Guide</p>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#fff;color:#C0392B;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">📚 Browse Resources</a>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:transparent;color:#fff;border:2px solid #fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">💳 Buy $19.90</a>
</div>

</div>"""

# ---- Check if Blog page exists, else create ----
def find_page(slug):
    r = requests.get(f"{SITE}/wp-json/wp/v2/pages?slug={slug}&status=publish,draft", headers=HEADERS, timeout=30)
    if r.ok and r.json():
        return r.json()[0]["id"]
    return None

blog_id = find_page("blog")
if blog_id:
    print(f"\nBlog page exists (ID {blog_id}), updating…")
    r = requests.post(f"{SITE}/wp-json/wp/v2/pages/{blog_id}", headers=HEADERS,
                      json={"title": "Blog — Korean Learning Tips", "content": wp_html(BLOG_HTML),
                            "excerpt": "Korean learning blog: tips, culture insights, vocabulary guides. New posts regularly."},
                      timeout=60)
else:
    print("\nCreating Blog page…")
    r = requests.post(f"{SITE}/wp-json/wp/v2/pages", headers=HEADERS,
                      json={"title": "Blog — Korean Learning Tips", "slug": "blog",
                            "content": wp_html(BLOG_HTML),
                            "excerpt": "Korean learning blog: tips, culture insights, vocabulary guides. New posts regularly.",
                            "status": "publish"},
                      timeout=60)
if r.ok:
    d = r.json()
    print(f"[OK] Blog page → {d['link']}")
    blog_id = d["id"]
else:
    print(f"[FAIL] Blog page: {r.status_code} {r.text[:200]}")

# ---- Add Blog link to Home page footer ----
print("\nAdding Blog link to Home + Learn Korean…")
for pid in [21, 1147]:
    r = requests.get(f"{SITE}/wp-json/wp/v2/pages/{pid}?context=edit", headers=HEADERS, timeout=30)
    if not r.ok:
        print(f"[FAIL] fetch page {pid}")
        continue
    page = r.json()
    content = page["content"]["raw"]
    # Add blog link near top, before hero (or just after Naver search bar)
    blog_btn = """
<div style="text-align:center;margin:14px auto 24px;max-width:680px;">
<a href="https://krguide.com/blog/" style="display:inline-block;background:#1A4A8A;color:#fff;padding:10px 28px;border-radius:24px;text-decoration:none;font-weight:700;font-size:14px;">📝 Read Our Blog → Korean Learning Tips</a>
</div>
"""
    if "blog/" not in content:
        # insert after Naver search dict closing </script>
        if 'id="krg-dict-bar"' in content:
            idx = content.find('</script>', content.find('id="krg-dict-bar"'))
            if idx > 0:
                idx += len('</script>')
                content = content[:idx] + "\n" + blog_btn + content[idx:]
            else:
                content = content.replace("<!-- wp:html -->", "<!-- wp:html -->\n" + blog_btn, 1)
        else:
            content = content.replace("<!-- wp:html -->", "<!-- wp:html -->\n" + blog_btn, 1)
        r = requests.post(f"{SITE}/wp-json/wp/v2/pages/{pid}", headers=HEADERS, json={"content": content}, timeout=60)
        if r.ok:
            print(f"[OK] Added blog link to page {pid}")
        else:
            print(f"[FAIL] page {pid}: {r.status_code}")
    else:
        print(f"[skip] page {pid} already has blog link")

# ---- Try to set Posts page in Settings (optional) ----
print("\nSetting WordPress Posts page to Blog…")
r = requests.post(f"{SITE}/wp-json/wp/v2/settings", headers=HEADERS,
                  json={"page_for_posts": blog_id, "show_on_front": "page"}, timeout=30)
if r.ok:
    print(f"[OK] Posts page set to ID {blog_id}")
else:
    print(f"[note] Settings update: {r.status_code} (page still works as Blog list)")

print("\n=== Done ===")
