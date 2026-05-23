"""
Inject SEO meta tags + Naver dictionary search bar into all HTML pages in dist-vocab.
"""
import re
from pathlib import Path

DIST = Path(r"C:\Users\무지랭이\krguide-korean-learn\dist-vocab")

# Per-page SEO metadata
SEO = {
    "vocab-hub.html": {
        "title": "Korean Vocabulary Hub — 14 Resources, 6,546 Words | KR Guide",
        "description": "Korean vocabulary across 14 categories: verbs, nouns, adjectives, honorifics, idioms, proverbs, Konglish, and more. 6,546 essential words with examples, pronunciation QR, and quizzes.",
        "keywords": "learn Korean, Korean vocabulary, 한국어 단어, Korean verbs, Korean honorifics, Korean idioms, Konglish, 한국어 학습",
    },
    "learn-korean.html": {
        "title": "Learn Korean — Complete 41-Chapter Guide | KR Guide",
        "description": "Complete Korean learning guide for foreigners. 41 chapters covering Hangul, pronunciation, grammar, conversations, honorifics, Korean culture, and modern slang.",
        "keywords": "learn Korean, Korean grammar, Hangul, Korean for beginners, Korean pronunciation, Korean honorifics, 한국어",
    },
}

def gen_default_seo(filename, title_fallback):
    """Generate SEO for preview-*/full-* pages."""
    is_preview = filename.startswith("preview-")
    is_full = filename.startswith("full-")
    name = filename.replace("preview-", "").replace("full-", "").replace(".html", "")
    if is_preview:
        return {
            "title": f"Free Preview — {title_fallback} | KR Guide Korean Learning",
            "description": f"Free preview of {title_fallback}. Sample 5-10% of the complete vocabulary resource. Korean learning with examples, pronunciation QR, and mini-quizzes.",
            "keywords": f"learn Korean, {name}, Korean vocabulary preview, 한국어 학습",
        }
    if is_full:
        return {
            "title": f"{title_fallback} — Complete Resource | KR Guide",
            "description": f"Complete {title_fallback} vocabulary resource. Categorized words with scenarios, comparison boxes, mini-quizzes, and pronunciation QR codes.",
            "keywords": f"Korean {name}, learn Korean, Korean vocabulary, 한국어 학습",
        }
    return None

RESOURCE_TITLES = {
    "verbs": "200 Essential Korean Verbs",
    "adverbs": "200 Essential Korean Adverbs",
    "nouns": "Essential Korean Nouns (369)",
    "honorifics": "500 Korean Honorifics",
    "japanese": "Japanese Loanwords in Korean (391)",
    "adjadv": "1,067 Korean Adjectives, Adverbs & Idioms",
    "internet": "500 Korean Internet & Chat Expressions",
    "konglish": "500 Konglish: Korean-English Expressions",
    "mimetic": "500 Korean Onomatopoeia & Mimetic Words",
    "idioms": "100 Korean Four-Character Idioms (사자성어)",
    "proverbs": "100 Korean Proverbs & Sayings",
    "visual": "1,100 Korean Visual Vocabulary",
    "bible": "100 Bible Verses — Korean + ESV",
    "itterms": "1,000 Korean IT Terms",
}

NAVER_SEARCH_BAR = """
<div id="krg-dict-bar" style="background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin:14px auto;max-width:680px;display:flex;gap:8px;align-items:center;font-family:'Noto Sans KR',sans-serif;">
<span style="font-size:20px;">🔍</span>
<input id="krg-dict-input" type="text" placeholder="네이버 사전 · Korean ↔ English Dictionary" style="flex:1;padding:10px 14px;border:1.5px solid #e5e5ea;border-radius:8px;font-size:14px;font-family:inherit;outline:none;" onkeypress="if(event.key==='Enter') krgDictSearch()">
<button onclick="krgDictSearch()" style="background:#03c75a;color:#fff;border:none;padding:10px 22px;border-radius:8px;font-weight:800;cursor:pointer;font-size:14px;font-family:inherit;">N 사전</button>
</div>
<script>
function krgDictSearch(){
  var q = (document.getElementById('krg-dict-input').value || '').trim();
  if(!q) return;
  var isKo = /[\\uAC00-\\uD7AF]/.test(q);
  var url = isKo
    ? 'https://ko.dict.naver.com/#/search?query=' + encodeURIComponent(q)
    : 'https://en.dict.naver.com/#/search?query=' + encodeURIComponent(q);
  window.open(url, '_blank', 'noopener');
}
</script>
"""

JSONLD_WEBSITE = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "KR Guide — Learn Korean",
  "url": "https://krguide.com/",
  "description": "Complete Korean learning resource for foreigners. 41 chapters + 6,546 essential words across 14 categories.",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://ko.dict.naver.com/#/search?query={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "KR Guide",
  "url": "https://krguide.com/",
  "logo": "https://krguide.com/favicon.ico",
  "sameAs": ["https://krguide-vocab.pages.dev/"]
}
</script>
"""

JSONLD_COURSE = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Learn Korean — Complete 41-Chapter Guide",
  "description": "Complete Korean learning resource covering Hangul, pronunciation, grammar, conversations, honorifics, and Korean culture.",
  "provider": {
    "@type": "Organization",
    "name": "KR Guide",
    "url": "https://krguide.com/"
  },
  "inLanguage": ["ko", "en"],
  "offers": {
    "@type": "Offer",
    "price": "9.90",
    "priceCurrency": "USD",
    "url": "https://jssmn21.gumroad.com/l/gnefla"
  }
}
</script>
"""

def build_meta_block(filename):
    seo = SEO.get(filename)
    if not seo:
        # auto-gen for preview-*/full-*
        for key, title in RESOURCE_TITLES.items():
            if filename in (f"preview-{key}.html", f"full-{key}.html"):
                seo = gen_default_seo(filename, title)
                break
    if not seo:
        return ""

    canonical = f"https://krguide-vocab.pages.dev/{filename.replace('.html','')}"
    is_main = filename in ("vocab-hub.html", "learn-korean.html")
    jsonld = (JSONLD_WEBSITE + (JSONLD_COURSE if is_main else "")) if is_main else ""

    return f"""<meta name="description" content="{seo['description']}">
<meta name="keywords" content="{seo['keywords']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="KR Guide">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KR Guide — Learn Korean">
<meta property="og:title" content="{seo['title']}">
<meta property="og:description" content="{seo['description']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://krguide.com/favicon.svg">
<meta property="og:locale" content="ko_KR">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{seo['title']}">
<meta name="twitter:description" content="{seo['description']}">
<meta name="twitter:image" content="https://krguide.com/favicon.svg">
{jsonld}
"""

def patch_file(path):
    filename = path.name
    html = path.read_text(encoding="utf-8")
    meta_block = build_meta_block(filename)
    if not meta_block:
        return False, "no SEO config"

    # Replace existing title with SEO title
    seo = SEO.get(filename)
    if not seo:
        for key, title in RESOURCE_TITLES.items():
            if filename in (f"preview-{key}.html", f"full-{key}.html"):
                seo = gen_default_seo(filename, title)
                break
    if seo:
        if "<title>" in html:
            html = re.sub(r"<title>[^<]*</title>", f"<title>{seo['title']}</title>", html, count=1)

    # Insert meta block after <head> or right before </head>
    if "<!-- SEO_META -->" in html:
        # already injected, replace block
        html = re.sub(r"<!-- SEO_META -->.*?<!-- /SEO_META -->", f"<!-- SEO_META -->{meta_block}<!-- /SEO_META -->", html, flags=re.S)
    else:
        # Insert after <meta charset...>
        m = re.search(r'(<meta[^>]+charset[^>]*>)', html)
        if m:
            insert_at = m.end()
            html = html[:insert_at] + f"\n<!-- SEO_META -->{meta_block}<!-- /SEO_META -->\n" + html[insert_at:]
        else:
            html = html.replace("</head>", f"<!-- SEO_META -->{meta_block}<!-- /SEO_META -->\n</head>", 1)

    # Insert Naver search bar at start of <body> for main pages only
    if filename in ("vocab-hub.html", "learn-korean.html"):
        if "id=\"krg-dict-bar\"" not in html:
            html = re.sub(r"(<body[^>]*>)",
                          lambda m: m.group(1) + "\n" + NAVER_SEARCH_BAR,
                          html, count=1)

    path.write_text(html, encoding="utf-8")
    return True, "patched"

count = 0
for path in sorted(DIST.glob("*.html")):
    ok, msg = patch_file(path)
    if ok:
        print(f"[OK]   {path.name:35s} {msg}")
        count += 1
    else:
        print(f"[skip] {path.name:35s} {msg}")
print(f"\n=== Patched {count} files ===")
