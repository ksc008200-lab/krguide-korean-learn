"""Retry the 8th blog post that failed."""
import requests, base64

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

CTA = """
<div style="background:linear-gradient(135deg,#C0392B,#1A4A8A);color:#fff;padding:32px 28px;border-radius:14px;text-align:center;margin:30px 0;">
<h3 style="color:#fff;margin:0 0 10px;font-size:22px;">📚 Start Your Korean Journey Today</h3>
<a href="https://krguide-vocab.pages.dev/vocab-hub" style="display:inline-block;background:#fff;color:#C0392B;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">📚 Browse Resources</a>
<a href="https://jssmn21.gumroad.com/l/gnefla" target="_blank" rel="noopener" style="display:inline-block;background:transparent;color:#fff;border:2px solid #fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;margin:4px;">💳 Buy $19.90</a>
</div>"""

CONTENT = """<!-- wp:html -->
<div style="max-width:780px;margin:0 auto;font-family:'Noto Sans KR',sans-serif;line-height:1.75;color:#1a1a2e;font-size:16px;">

<p style="font-size:18px;color:#555;font-style:italic;border-left:4px solid #C0392B;padding-left:16px;margin:20px 0;">2026년 한국어를 배워야 하는 5가지 이유 — Korean has become one of the most valuable languages to learn worldwide.</p>

<p>The number of Korean learners worldwide has exploded. Korean is the <strong>7th most-studied language globally</strong> on Duolingo, ahead of Italian, Mandarin, and Russian. Why? Here are five compelling reasons why now is the perfect time to start.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #C0392B;padding-left:14px;margin-top:36px;">1. 🎵 Hallyu (한류) — The Korean Wave</h2>
<p>K-pop is no longer a niche genre. BTS topped global charts. BLACKPINK headlined Coachella. Stray Kids, NewJeans dominate global music. K-dramas like Squid Game became Netflix's biggest non-English content.</p>
<p>Learning Korean unlocks: K-pop lyrics in original meaning, K-drama cultural nuances, direct fan connection on V Live and Weverse, and webtoons (Korea is the world's #1 source of digital comics). K-content is projected to grow into a <strong>$200 billion industry by 2030</strong>.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #1A4A8A;padding-left:14px;margin-top:36px;">2. 💼 Korea Is a Global Economic Powerhouse</h2>
<p>South Korea is the world's 10th-largest economy. Korean companies dominate multiple sectors:</p>
<ul>
<li><strong>Samsung</strong> — world's largest memory chip maker</li>
<li><strong>Hyundai/Kia</strong> — top-3 global automaker</li>
<li><strong>LG</strong> — leader in displays, batteries, home appliances</li>
<li><strong>Naver, Kakao</strong> — Korea's tech giants</li>
</ul>
<p>For careers in tech, manufacturing, K-beauty ($13B industry), and tourism, Korean proficiency gives major advantages.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #059669;padding-left:14px;margin-top:36px;">3. 📚 Hangul Is the Easiest Major Alphabet</h2>
<p>If Chinese kanji put you off Asian languages, Hangul changes everything:</p>
<ul>
<li>Only <strong>24 letters</strong> vs 50,000+ Chinese characters</li>
<li>Learnable in <strong>2-5 hours</strong></li>
<li>Letters shaped after vocal organs — visual mnemonics built in</li>
<li>Strictly phonetic — no chaos like "though/through/thought"</li>
<li>UNESCO-recognized as humanity's most scientific alphabet</li>
</ul>
<p>King Sejong designed Hangul in 1443 so anyone could learn to read in a single day. He succeeded.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #D97706;padding-left:14px;margin-top:36px;">4. 🇰🇷 Korea Is an Amazing Travel Destination</h2>
<p>17+ million tourists visit Korea annually. Seoul, Busan, Jeju, Gyeongju, and the DMZ are world-class destinations. Korean transforms your travel:</p>
<ul>
<li>Order at hole-in-the-wall restaurants (often the best ones)</li>
<li>Navigate any city's magnificent subway system</li>
<li>Connect with locals beyond tourist-level interactions</li>
<li>Understand cultural rules — bowing, drinking etiquette, gift exchanges</li>
</ul>
<p>Korea is also a major medical tourism and K-beauty pilgrimage destination.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #7C3AED;padding-left:14px;margin-top:36px;">5. 🧠 Korean Trains Your Brain Uniquely</h2>
<p>Learning Korean offers unique cognitive benefits:</p>
<ul>
<li><strong>SOV word order</strong> — restructures sentence processing</li>
<li><strong>Honorific system</strong> — develops social awareness</li>
<li><strong>Particles</strong> — fine-grained grammatical precision</li>
<li><strong>Sino-Korean roots</strong> — opens doors to Chinese and Japanese</li>
</ul>
<p>Bilingual brains have measurable advantages: better memory, delayed cognitive decline, enhanced problem-solving.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #B91C1C;padding-left:14px;margin-top:36px;">🎯 How to Start Right Now</h2>
<p>Realistic 6-month roadmap:</p>
<ul>
<li><strong>Today</strong>: Learn Hangul (4-5 hours)</li>
<li><strong>Week 1</strong>: 30 essential verbs</li>
<li><strong>Month 1</strong>: 1,000 most common words + basic sentence structure</li>
<li><strong>Month 3</strong>: Watch K-drama with Korean subtitles</li>
<li><strong>Month 6</strong>: TOPIK Level 2 (intermediate) achievable</li>
</ul>
<p>Keys are <strong>consistency over intensity</strong>, <strong>output over input</strong>, and <strong>systematized vocabulary</strong>.</p>

<h2 style="color:#1a1a2e;border-left:4px solid #0E7490;padding-left:14px;margin-top:36px;">💡 The Best Time to Start Is Now</h2>
<p>K-content is everywhere. Korea's global influence is rising. Hangul is genuinely easy. Resources have never been more abundant.</p>
<p>Whether your motivation is K-pop lyrics, career in Asia, travel, or pure intellectual curiosity — 2026 is a fantastic year to start learning Korean.</p>

""" + CTA + """

<p style="margin-top:24px;color:#666;font-size:14px;">한국어 학습은 가장 보람 있는 도전입니다. Korean is one of the most rewarding languages you can choose to learn. Start today.</p>

</div>
<!-- /wp:html -->"""

body = {
    "title": "5 Reasons to Learn Korean in 2026",
    "slug": "why-learn-korean-2026",
    "excerpt": "Korean is the fastest-growing language for foreigners worldwide. 5 compelling reasons to start learning Korean in 2026 — K-pop, careers, easy alphabet, travel, and brain benefits.",
    "content": CONTENT,
    "status": "publish",
}
r = requests.post(f"{SITE}/wp-json/wp/v2/posts", headers=HEADERS, json=body, timeout=60)
if r.ok:
    d = r.json()
    print(f"[OK] Post {d['id']}: {d['link']}")
else:
    print(f"[FAIL] {r.status_code}: {r.text[:300]}")
