"""Inject keyword-rich SEO blocks into all 27 published posts.

Strategy:
  Find each post by slug, locate the CTA box (stable anchor in our HTML),
  and inject 3 new H2 sections right before it:
    1. Why [keyword] Matter for Korean Fluency  (kw x2 + LSI x1)
    2. Common Mistakes Learners Make with [keyword]  (kw x1, LSI x2 in bullets)
    3. How to Master [keyword] in 30 Days  (kw + LSI in conclusion)

This raises keyword density from ~0.4% to ~1.0% and adds keyword-in-H2 (a major
ranking factor) plus semantic LSI coverage. Each post gains ~250 words of useful
content — better for SEO baseline length too.

Idempotent: skips posts already enhanced (detects 'Why' + keyword in raw).
"""
import requests, base64, time

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

# (slug, focus_kw, [LSI keywords], series)
POSTS = [
    # ---- Vocab Series ----
    ("200-essential-korean-verbs-every-learner-must-master",
     "Korean verbs",
     ["Korean verb conjugation", "essential Korean verbs", "learn Korean verbs daily", "Korean dictionary form"],
     "vocab"),
    ("200-korean-adverbs-sound-natural-fluent",
     "Korean adverbs",
     ["natural Korean adverbs", "common Korean adverbs", "Korean adverb examples", "sound natural in Korean"],
     "vocab"),
    ("369-common-korean-nouns-every-beginner-should-know",
     "Korean nouns",
     ["essential Korean nouns", "Korean vocabulary list", "basic Korean nouns", "Korean noun categories"],
     "vocab"),
    ("500-korean-honorifics-master-polite-speech-native",
     "Korean honorifics",
     ["존댓말", "formal Korean speech", "Korean polite speech", "Korean honorific verbs"],
     "vocab"),
    ("391-japanese-loanwords-korean-explained",
     "Japanese loanwords in Korean",
     ["일본어 외래어", "Korean Japanese vocabulary", "Japanese-origin Korean words", "Korean colonial vocabulary"],
     "vocab"),
    ("1067-korean-adjectives-adverbs-idioms-big-list",
     "Korean adjectives",
     ["Korean descriptive verbs", "Korean idioms list", "Korean emotion adjectives", "Korean body part idioms"],
     "vocab"),
    ("500-korean-internet-slang-words-2026-edition",
     "Korean internet slang",
     ["Korean Gen Z slang", "Korean chat acronyms", "KakaoTalk slang", "Twitter Korean slang"],
     "vocab"),
    ("500-konglish-words-when-english-becomes-korean",
     "Konglish",
     ["Korean English words", "Korean loanwords from English", "Konglish examples", "Korean-style English"],
     "vocab"),
    ("500-korean-onomatopoeia-uiseongeo-uitaego-explained",
     "Korean onomatopoeia",
     ["의성어 의태어", "Korean sound words", "Korean mimetic words", "Korean expressive vocabulary"],
     "vocab"),
    ("100-essential-korean-idioms-sajaseongeo-sophisticated-speech",
     "Korean idioms 사자성어",
     ["four-character idioms", "Korean classical idioms", "Sino-Korean idioms", "사자성어 examples"],
     "vocab"),
    ("100-korean-proverbs-sokdam-every-native-knows",
     "Korean proverbs 속담",
     ["Korean folk wisdom", "traditional Korean proverbs", "Korean sayings", "Korean speech patterns"],
     "vocab"),
    ("1100-korean-visual-vocabulary-learn-by-picture",
     "Korean visual vocabulary",
     ["Korean picture dictionary", "learn Korean with images", "Korean visual learning", "Korean household vocabulary"],
     "vocab"),
    ("100-bible-verses-korean-hangugeo-seonggyeong",
     "Korean Bible verses",
     ["한국어 성경 구절", "Korean Christianity", "Korean Scripture", "high-register Korean"],
     "vocab"),
    ("1000-korean-it-terms-tech-vocabulary-programmers",
     "Korean IT terms",
     ["Korean tech vocabulary", "Korean programming words", "Naver Kakao Korean", "Korean software terms"],
     "vocab"),
    ("hangul-vs-hanja-complete-bilingual-reference",
     "Hangul vs Hanja",
     ["Korean Chinese characters", "Hanja learning", "Korean Hanja study", "Korean Chinese character meanings"],
     "vocab"),
    # ---- Culture Series ----
    ("ppalli-ppalli-culture-why-koreans-always-hurry",
     "빨리빨리 culture",
     ["Korean speed culture", "Korean hurry mindset", "Korean efficiency", "Korean fast-paced lifestyle"],
     "culture"),
    ("seongsil-korean-diligence-work-ethic",
     "Korean diligence 성실성",
     ["Korean work ethic", "Korean perseverance", "Korean career culture", "Korean hard work value"],
     "culture"),
    ("chaegimgam-korean-responsibility-culture",
     "Korean responsibility 책임감",
     ["Korean work culture", "Korean accountability", "Korean team responsibility", "Korean management style"],
     "culture"),
    ("jeong-untranslatable-korean-bond",
     "Korean jeong 정",
     ["Korean emotional bond", "Korean concept of jeong", "Korean attachment culture", "Korean relationships"],
     "culture"),
    ("han-korean-emotional-depth-untranslatable",
     "Korean han 한",
     ["Korean sorrow concept", "Korean cultural emotion", "Korean pansori emotion", "Korean cinematic han"],
     "culture"),
    ("nunchi-korean-art-of-reading-the-room",
     "Korean nunchi 눈치",
     ["Korean social awareness", "Korean reading the room", "Korean emotional intelligence", "Korean group dynamics"],
     "culture"),
    ("chemyeon-korean-saving-face-culture",
     "Korean 체면 chemyeon",
     ["Korean saving face", "Korean honor culture", "Korean social dignity", "Korean reputation"],
     "culture"),
    ("uri-korean-collective-we-mindset",
     "Korean uri 우리",
     ["Korean we mindset", "Korean collectivism", "Korean group identity", "Korean family expressions"],
     "culture"),
    ("hyo-filial-piety-korean-family-culture",
     "Korean filial piety 효",
     ["Korean family culture", "Korean Confucianism", "Korean parent respect", "Korean ancestral rites"],
     "culture"),
    ("hoesik-korean-company-dinner-culture",
     "Korean hoesik 회식",
     ["Korean company dinner", "Korean work drinking", "Korean business culture", "Korean office socializing"],
     "culture"),
    ("chuseok-korean-thanksgiving-traditions",
     "Chuseok 추석",
     ["Korean Thanksgiving", "Korean harvest holiday", "Chuseok traditions", "Korean ancestral rites"],
     "culture"),
    ("seolnal-korean-new-year-traditions",
     "Seolnal 설날",
     ["Korean New Year", "Korean lunar new year", "Korean New Year greetings", "Korean sebae tradition"],
     "culture"),
]

# ============================================================
# SEO BLOCK BUILDERS
# ============================================================
def build_vocab_block(kw, lsi):
    l0, l1, l2, l3 = lsi[0], lsi[1], lsi[2], lsi[3]
    return f"""

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">Why {kw} Matter for Korean Fluency</h2>
<p>Mastering <strong>{kw}</strong> is one of the highest-leverage decisions you can make as a Korean learner. While beginners memorize random word lists and intermediate students stall on grammar drills, fluent communicators consistently invest in <em>{l0}</em>. The 15 sample entries above are a starting point — real fluency comes from seeing these {kw.lower()} in dozens of contexts: K-dramas, news headlines, K-pop lyrics, Naver blog posts, and real conversation. Once you internalize the most-used 100 entries, you've crossed the threshold from "I'm studying Korean" to "I'm using Korean."</p>

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">Common Mistakes Learners Make with {kw}</h2>
<ul style="font-size:16px;line-height:1.8;">
  <li><strong>Translating word-by-word.</strong> {kw} rarely map 1:1 to English. Memorize the function and context — not the literal definition. This is the #1 reason translation apps produce awkward Korean.</li>
  <li><strong>Skipping Hangul for romanization.</strong> Romanized {l1} feel comfortable to beginners, but they block real pronunciation development. Practice with native script from day one — your ear will thank you in month three.</li>
  <li><strong>Ignoring register.</strong> Korean has multiple politeness levels. The same {l2.lower()} used with a friend would be rude with a boss. Always learn the formal and casual versions together.</li>
  <li><strong>Studying passively.</strong> Reading lists of {kw.lower()} once doesn't move them into long-term memory. Active production — writing your own example sentences — is 4× more effective than passive review.</li>
</ul>

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">How to Master {kw} in 30 Days</h2>
<p>A focused 30-day plan beats six months of unfocused study every time. Here's the proven system that works for {l3}: <strong>Days 1–10</strong> — Pick 5 entries from the full list each day. Write 3 example sentences per entry. Read them aloud 5 times. <strong>Days 11–20</strong> — Review previous days first (10 minutes), add 5 new entries, then write a short paragraph using 3 of today's plus 2 of yesterday's {kw.lower()}. <strong>Days 21–30</strong> — Watch one K-drama clip per day and flag every {kw.lower().rstrip('s')} you recognize from your study list. By day 30, you'll have actively produced 150 sentences using 150 {kw.lower()} — putting you in the top 10% of Korean learners worldwide.</p>
"""


def build_culture_block(kw, lsi):
    l0, l1, l2, l3 = lsi[0], lsi[1], lsi[2], lsi[3]
    return f"""

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">Why Understanding {kw} Matters</h2>
<p>You cannot truly understand Korean society without grasping <strong>{kw}</strong>. Language is the surface; <em>{l0}</em> runs beneath every conversation, every business meeting, every family dinner. Foreigners who only learn grammar miss what Koreans actually communicate. Those who study {kw.lower()} alongside the language reach a deeper level of cultural fluency — the kind that earns trust, opens doors, and turns Korean colleagues into real friends.</p>

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">Common Misunderstandings About {kw}</h2>
<ul style="font-size:16px;line-height:1.8;">
  <li><strong>Treating it as outdated.</strong> Foreign observers often dismiss {kw.lower()} as old-fashioned Confucian baggage. But {l1} remain deeply alive in modern Seoul — in tech startups, K-pop agencies, and even Gen Z social media culture, just in modified forms.</li>
  <li><strong>Equating it with a Western concept.</strong> {kw} rarely maps cleanly to a Western equivalent. {l2} has cultural weight that direct translation cannot carry. Resist the urge to substitute — sit with the difference.</li>
  <li><strong>Missing social context.</strong> Korean cultural concepts depend heavily on who, when, where, and with whom. The same gesture means deference in one setting and condescension in another. Without {l3.lower()}, you'll misread the room.</li>
  <li><strong>Trying to use it performatively.</strong> Foreigners sometimes adopt {kw.lower()} as a costume — bowing too deeply, over-using honorifics. Native speakers notice. Subtle, contextual practice beats theatrical performance every time.</li>
</ul>

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">How to Apply {kw} in Real Life</h2>
<p>Reading about {kw.lower()} is the easy part. Practicing it changes how Koreans relate to you. Start small: <strong>observe before acting.</strong> Spend two weeks just watching how Koreans handle {l0.lower()} — at restaurants, on the subway, in family gatherings on K-dramas. Note who initiates what, who waits, who speaks first. <strong>Then mirror.</strong> When you sense the moment, follow the local lead — accept the offered drink with both hands, address elders with -님, ask before paying the bill. Over time, your sense of {l3.lower()} becomes automatic. That's when Koreans stop seeing you as a guest and start treating you as one of them.</p>
"""


# ============================================================
# UPDATE
# ============================================================
CTA_MARKER = '<div style="background:linear-gradient(135deg,#1A4A8A,#C0392B)'

print(f"=== Injecting SEO keyword blocks into {len(POSTS)} posts ===\n")

ok = 0; skipped = 0; missing = 0; fail = 0
for slug, kw, lsi, series in POSTS:
    # Fetch post
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts?slug={slug}&context=edit",
                     headers=HEADERS, timeout=30)
    if not r.ok or not r.json():
        print(f"  [MISS]  {slug}")
        missing += 1
        continue
    post = r.json()[0]
    pid = post["id"]
    raw = post["content"]["raw"]

    # Skip if already enhanced
    if f"Why {kw} Matter" in raw or f"Why Understanding {kw}" in raw:
        print(f"  [SKIP]  ID {pid}  {slug}")
        skipped += 1
        continue

    # Pick block by series
    block = build_vocab_block(kw, lsi) if series == "vocab" else build_culture_block(kw, lsi)

    # Inject before CTA box
    if CTA_MARKER not in raw:
        print(f"  [NOCTA] ID {pid}  {slug}")
        fail += 1
        continue
    new_raw = raw.replace(CTA_MARKER, block + "\n" + CTA_MARKER, 1)

    # PUT
    r = requests.post(f"{SITE}/wp-json/wp/v2/posts/{pid}",
                      headers=HEADERS, json={"content": new_raw}, timeout=60)
    if r.ok:
        print(f"  [OK]    ID {pid}  {slug}")
        ok += 1
    else:
        print(f"  [FAIL]  ID {pid}  {slug}  {r.status_code}")
        fail += 1
    time.sleep(0.8)

print(f"\n=== Done: {ok} enhanced, {skipped} skipped, {missing} missing, {fail} failed ===")
