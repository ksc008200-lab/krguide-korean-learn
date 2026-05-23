"""
Update WordPress pages with:
- Naver dictionary search bar (auto-detect Korean/English)
- SEO meta (title, excerpt)
"""
import requests
import base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"

cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {cred}",
    "Content-Type": "application/json",
}

def wp_html_block(inner_html: str) -> str:
    return f"<!-- wp:html -->\n{inner_html}\n<!-- /wp:html -->"

NAVER_SEARCH = """
<div style="background:#fff;border-radius:12px;padding:16px 18px;box-shadow:0 2px 12px rgba(0,0,0,0.06);margin:20px auto 28px;max-width:680px;display:flex;gap:8px;align-items:center;">
<span style="font-size:22px;">🔍</span>
<input id="krg-dict" type="text" placeholder="네이버 사전 검색 · Search Korean ↔ English" style="flex:1;padding:11px 14px;border:1.5px solid #e5e5ea;border-radius:8px;font-size:14px;font-family:inherit;outline:none;" onkeypress="if(event.key==='Enter') krgDict()">
<button onclick="krgDict()" style="background:#03c75a;color:#fff;border:none;padding:11px 22px;border-radius:8px;font-weight:800;cursor:pointer;font-size:14px;">N 사전</button>
</div>
<script>
function krgDict(){
  var q = (document.getElementById('krg-dict').value || '').trim();
  if(!q) return;
  var isKo = /[가-힯]/.test(q);
  var url = isKo
    ? 'https://ko.dict.naver.com/#/search?query=' + encodeURIComponent(q)
    : 'https://en.dict.naver.com/#/search?query=' + encodeURIComponent(q);
  window.open(url, '_blank');
}
</script>
"""

HOME_HTML = """<div style="max-width:1100px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;line-height:1.6;color:#1a1a2e;">

""" + NAVER_SEARCH + """

<div style="padding:80px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:24px;text-align:center;margin-bottom:32px;">
<div style="font-size:13px;color:#f97316;font-weight:700;letter-spacing:4px;margin-bottom:16px;">KR GUIDE · KOREAN LEARNING</div>
<h1 style="font-size:46px;margin:0 0 14px;color:#fff;font-weight:800;line-height:1.2;">Learn Korean —<br>The Easiest, Deepest Way</h1>
<p style="font-size:20px;color:#fbbf24;font-weight:700;margin:0 0 22px;">한국어를 가장 쉽게, 가장 깊이</p>
<p style="font-size:16px;opacity:0.92;max-width:640px;margin:0 auto 36px;">From Hangul to fluent conversations. 41 chapters + 6,546 essential words — one purchase, lifetime access.</p>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#f97316;color:#fff;padding:18px 44px;border-radius:12px;text-decoration:none;font-weight:800;font-size:17px;margin:6px;">🚀 Start Learning</a>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:transparent;color:#fff;padding:18px 40px;border:2px solid #fff;border-radius:12px;text-decoration:none;font-weight:800;font-size:16px;margin:6px;">💳 Buy $19.90</a>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:48px;">
<div style="text-align:center;background:#fff;padding:28px 20px;border-radius:14px;border-top:4px solid #C0392B;"><div style="font-size:38px;font-weight:800;color:#C0392B;">41</div><div style="font-size:11px;color:#666;letter-spacing:2px;margin-top:4px;">CHAPTERS</div></div>
<div style="text-align:center;background:#fff;padding:28px 20px;border-radius:14px;border-top:4px solid #1A4A8A;"><div style="font-size:38px;font-weight:800;color:#1A4A8A;">6,546</div><div style="font-size:11px;color:#666;letter-spacing:2px;margin-top:4px;">WORDS</div></div>
<div style="text-align:center;background:#fff;padding:28px 20px;border-radius:14px;border-top:4px solid #059669;"><div style="font-size:38px;font-weight:800;color:#059669;">14</div><div style="font-size:11px;color:#666;letter-spacing:2px;margin-top:4px;">CATEGORIES</div></div>
<div style="text-align:center;background:#fff;padding:28px 20px;border-radius:14px;border-top:4px solid #D97706;"><div style="font-size:38px;font-weight:800;color:#D97706;">13</div><div style="font-size:11px;color:#666;letter-spacing:2px;margin-top:4px;">LANGUAGES</div></div>
</div>

<h2 style="text-align:center;font-size:30px;margin:48px 0 10px;">📚 14 Learning Resources</h2>
<p style="text-align:center;color:#666;margin-bottom:24px;">Click any card for a free preview · 카드를 클릭하면 무료 미리보기</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));grid-auto-rows:1fr;gap:16px;margin-bottom:48px;">

<a href="https://krguide-vocab.pages.dev/learn-korean" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #1a1a2e;"><div style="font-size:42px;margin-bottom:8px;">🇰🇷</div><div style="font-weight:800;font-size:16px;">Main Guide</div><div style="color:#1a1a2e;font-size:13px;font-weight:700;margin:4px 0 10px;">메인 가이드 (41 챕터)</div><div style="color:#666;font-size:12px;flex:1;">Hangul · pronunciation · grammar · conversations · culture.</div><div style="margin-top:12px;text-align:right;color:#1a1a2e;font-weight:800;font-size:12px;">Start →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-verbs" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #C0392B;"><div style="font-size:42px;margin-bottom:8px;">🏃</div><div style="font-weight:800;font-size:16px;">200 Verbs</div><div style="color:#C0392B;font-size:13px;font-weight:700;margin:4px 0 10px;">필수 동사 200</div><div style="color:#666;font-size:12px;flex:1;">Essential Korean verbs with pronunciation, polite form, past tense.</div><div style="margin-top:12px;text-align:right;color:#C0392B;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-adverbs" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #1A4A8A;"><div style="font-size:42px;margin-bottom:8px;">📊</div><div style="font-weight:800;font-size:16px;">200 Adverbs</div><div style="color:#1A4A8A;font-size:13px;font-weight:700;margin:4px 0 10px;">필수 부사 200</div><div style="color:#666;font-size:12px;flex:1;">Time · degree · manner · onomatopoeia adverbs.</div><div style="margin-top:12px;text-align:right;color:#1A4A8A;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-nouns" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #0F766E;"><div style="font-size:42px;margin-bottom:8px;">📦</div><div style="font-weight:800;font-size:16px;">369 Nouns</div><div style="color:#0F766E;font-size:13px;font-weight:700;margin:4px 0 10px;">필수 명사 369</div><div style="color:#666;font-size:12px;flex:1;">Family · body · food · time · places — 7 themes.</div><div style="margin-top:12px;text-align:right;color:#0F766E;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-honorifics" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #7C3AED;"><div style="font-size:42px;margin-bottom:8px;">🙇</div><div style="font-weight:800;font-size:16px;">500 Honorifics</div><div style="color:#7C3AED;font-size:13px;font-weight:700;margin:4px 0 10px;">존댓말 500</div><div style="color:#666;font-size:12px;flex:1;">Daily greetings · business etiquette · classical phrases.</div><div style="margin-top:12px;text-align:right;color:#7C3AED;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-japanese" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #B91C1C;"><div style="font-size:42px;margin-bottom:8px;">🏯</div><div style="font-weight:800;font-size:16px;">391 Loanwords</div><div style="color:#B91C1C;font-size:13px;font-weight:700;margin:4px 0 10px;">일본어 외래어 391</div><div style="color:#666;font-size:12px;flex:1;">Japanese-origin words in Korean and native equivalents.</div><div style="margin-top:12px;text-align:right;color:#B91C1C;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-adjadv" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #9A3412;"><div style="font-size:42px;margin-bottom:8px;">🎨</div><div style="font-weight:800;font-size:16px;">1067 Adj·Adv·Idioms</div><div style="color:#9A3412;font-size:13px;font-weight:700;margin:4px 0 10px;">형용사·부사·관용구 1067</div><div style="color:#666;font-size:12px;flex:1;">Adjectives, adverbs, idioms, proverbs, four-character sayings.</div><div style="margin-top:12px;text-align:right;color:#9A3412;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-internet" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #2563EB;"><div style="font-size:42px;margin-bottom:8px;">💬</div><div style="font-weight:800;font-size:16px;">500 Internet Korean</div><div style="color:#2563EB;font-size:13px;font-weight:700;margin:4px 0 10px;">인터넷·채팅 500</div><div style="color:#666;font-size:12px;flex:1;">ㅋㅋㅋ · K-pop · gaming · MZ-generation slang.</div><div style="margin-top:12px;text-align:right;color:#2563EB;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-konglish" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #059669;"><div style="font-size:42px;margin-bottom:8px;">🌐</div><div style="font-weight:800;font-size:16px;">500 Konglish</div><div style="color:#059669;font-size:13px;font-weight:700;margin:4px 0 10px;">콩글리시 500</div><div style="color:#666;font-size:12px;flex:1;">Korean-English vs real English — wrong vs right.</div><div style="margin-top:12px;text-align:right;color:#059669;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-mimetic" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #D97706;"><div style="font-size:42px;margin-bottom:8px;">🌧️</div><div style="font-weight:800;font-size:16px;">500 Onomatopoeia</div><div style="color:#D97706;font-size:13px;font-weight:700;margin:4px 0 10px;">의성어·의태어 500</div><div style="color:#666;font-size:12px;flex:1;">주룩주룩 · 반짝반짝 · 두근두근 — vivid Korean.</div><div style="margin-top:12px;text-align:right;color:#D97706;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-idioms" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #831843;"><div style="font-size:42px;margin-bottom:8px;">📜</div><div style="font-weight:800;font-size:16px;">100 Idioms</div><div style="color:#831843;font-size:13px;font-weight:700;margin:4px 0 10px;">사자성어 100</div><div style="color:#666;font-size:12px;flex:1;">Four-character idioms with hanja, origin, modern use.</div><div style="margin-top:12px;text-align:right;color:#831843;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-proverbs" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #854D0E;"><div style="font-size:42px;margin-bottom:8px;">🗣️</div><div style="font-weight:800;font-size:16px;">100 Proverbs</div><div style="color:#854D0E;font-size:13px;font-weight:700;margin:4px 0 10px;">한국 속담 100</div><div style="color:#666;font-size:12px;flex:1;">Korean proverbs with English equivalents and origins.</div><div style="margin-top:12px;text-align:right;color:#854D0E;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-visual" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #0E7490;"><div style="font-size:42px;margin-bottom:8px;">🎴</div><div style="font-weight:800;font-size:16px;">1100 Visual Words</div><div style="color:#0E7490;font-size:13px;font-weight:700;margin:4px 0 10px;">시각 어휘 1100</div><div style="color:#666;font-size:12px;flex:1;">22 categories · 1,100 words in card grid.</div><div style="margin-top:12px;text-align:right;color:#0E7490;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-bible" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #7C2D12;"><div style="font-size:42px;margin-bottom:8px;">📖</div><div style="font-weight:800;font-size:16px;">100 Bible Verses</div><div style="color:#7C2D12;font-size:13px;font-weight:700;margin:4px 0 10px;">성경 100구절</div><div style="color:#666;font-size:12px;flex:1;">Korean (개역개정) + ESV English key verses.</div><div style="margin-top:12px;text-align:right;color:#7C2D12;font-weight:800;font-size:12px;">Preview →</div></a>

<a href="https://krguide-vocab.pages.dev/preview-itterms" style="display:flex;flex-direction:column;background:#fff;padding:22px;border-radius:14px;text-decoration:none;color:#1a1a2e;border-top:4px solid #374151;"><div style="font-size:42px;margin-bottom:8px;">💻</div><div style="font-weight:800;font-size:16px;">1000 IT Terms</div><div style="color:#374151;font-size:13px;font-weight:700;margin:4px 0 10px;">IT 용어 1000</div><div style="color:#666;font-size:12px;flex:1;">Hardware · OS · programming · AI · cloud.</div><div style="margin-top:12px;text-align:right;color:#374151;font-weight:800;font-size:12px;">Preview →</div></a>

</div>

<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:60px 28px;border-radius:20px;text-align:center;">
<h2 style="color:#fff;font-size:32px;margin:0 0 12px;">One Purchase, Lifetime Access</h2>
<p style="opacity:0.92;font-size:16px;margin-bottom:28px;">14 resources · 6,546 words · 41-chapter main guide</p>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:#fff;color:#C0392B;padding:20px 56px;border-radius:12px;text-decoration:none;font-weight:800;font-size:18px;margin:6px;">💳 Buy Now — $19.90</a>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:transparent;color:#fff;padding:20px 44px;border:2px solid #fff;border-radius:12px;text-decoration:none;font-weight:800;font-size:16px;margin:6px;">📚 Browse First</a>
</div>

</div>"""


LEARN_KOREAN_HTML = """<div style="max-width:880px;margin:30px auto;font-family:'Noto Sans KR',sans-serif;color:#1a1a2e;line-height:1.6;">

""" + NAVER_SEARCH + """

<div style="text-align:center;padding:60px 24px;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;border-radius:18px;margin-bottom:30px;">
<div style="font-size:48px;margin-bottom:12px;">🇰🇷</div>
<h1 style="font-size:42px;margin:0 0 12px;color:#fff;">Learn Korean</h1>
<p style="font-size:20px;color:#f97316;font-weight:700;margin:0 0 18px;">한국어 완전 학습 가이드</p>
<p style="font-size:15px;opacity:0.9;max-width:600px;margin:0 auto 28px;line-height:1.7;">From the birth of Hangul to everyday conversations — 41 comprehensive chapters covering pronunciation, grammar, honorifics, culture, and modern slang.</p>
<a href="https://krguide-vocab.pages.dev/learn-korean" style="display:inline-block;background:#f97316;color:#fff;padding:14px 36px;border-radius:8px;text-decoration:none;font-weight:800;font-size:15px;">🚀 Start Reading →</a>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:30px;">
<div style="background:#fff;border-left:4px solid #C0392B;padding:20px;border-radius:8px;">
<div style="font-size:32px;">📚</div>
<h3 style="margin:8px 0;">41 Chapters</h3>
<p style="font-size:13px;color:#666;">Hangul · pronunciation · grammar · conversations · culture</p>
</div>
<div style="background:#fff;border-left:4px solid #1A4A8A;padding:20px;border-radius:8px;">
<div style="font-size:32px;">🎯</div>
<h3 style="margin:8px 0;">14 Resources</h3>
<p style="font-size:13px;color:#666;">Verbs, nouns, honorifics, idioms, proverbs — 6,546 words</p>
</div>
<div style="background:#fff;border-left:4px solid #059669;padding:20px;border-radius:8px;">
<div style="font-size:32px;">🌍</div>
<h3 style="margin:8px 0;">13 Languages</h3>
<p style="font-size:13px;color:#666;">Google Translate built-in — learn in your own language</p>
</div>
</div>

<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:36px 28px;border-radius:18px;text-align:center;">
<div style="font-size:48px;margin-bottom:12px;">📚</div>
<h2 style="margin:0 0 8px;color:#fff;font-size:24px;">Vocabulary & Expression Hub</h2>
<p style="margin:0 0 20px;opacity:0.92;font-size:14px;">14 categories · 6,546 essential words and expressions in one place.</p>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#fff;color:#C0392B;padding:14px 34px;border-radius:8px;text-decoration:none;font-weight:800;font-size:15px;">Browse Resources →</a>
</div>

</div>"""

# SEO excerpts (meta descriptions)
EXCERPTS = {
    21: "Learn Korean the easiest, deepest way. 41-chapter main guide + 6,546 essential words across 14 categories. One purchase, lifetime access. From Hangul to fluent conversations.",
    1147: "Complete Korean learning guide for foreigners. 41 chapters covering Hangul, pronunciation, grammar, conversations, honorifics, and Korean culture.",
    46: "Contact KR Guide for support with Korean learning materials, payment questions, or license key recovery. Email: hello@krguide.com.",
}

def update_page(page_id, content=None, title=None, excerpt=None):
    body = {}
    if content is not None:
        body["content"] = wp_html_block(content)
    if title:
        body["title"] = title
    if excerpt:
        body["excerpt"] = excerpt
    r = requests.post(
        f"{SITE}/wp-json/wp/v2/pages/{page_id}",
        headers=HEADERS,
        json=body,
        timeout=60,
    )
    if r.ok:
        d = r.json()
        print(f"[OK] Page {page_id} ('{d['title']['rendered']}')")
    else:
        print(f"[FAIL] Page {page_id}: {r.status_code} {r.text[:200]}")
    return r.ok

# Update with Naver search + SEO excerpt
print("=== Update Home (with Naver search + SEO) ===")
update_page(21, HOME_HTML,
    title="Learn Korean — The Easiest, Deepest Way | KR Guide",
    excerpt=EXCERPTS[21])

print("\n=== Update Learn Korean (with Naver search + SEO) ===")
update_page(1147, LEARN_KOREAN_HTML,
    title="Learn Korean — Complete Guide | 한국어 완전 학습",
    excerpt=EXCERPTS[1147])

print("\n=== Update Contact SEO only ===")
update_page(46, title="Contact — KR Guide Korean Learning Support",
    excerpt=EXCERPTS[46])

print("\n=== Done ===")
