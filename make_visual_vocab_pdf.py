"""
Enhanced Korean Visual Vocabulary 1100 PDF.
"""
import re, subprocess, time, io, base64, random, urllib.parse, json
from pathlib import Path
from html import escape, unescape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "Korean_Vocab_1100.html"
HTML_OUT = ROOT / "visual-vocab-1100-enhanced.html"
PDF_OUT  = ROOT / "visual-vocab-1100-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 22 sub-categories grouped into 6 themes
THEMES = [
    ("🍽️ 음식·주방 Food & Kitchen", ["Fruits", "Vegetables", "Food", "Drinks", "Kitchen"]),
    ("🐾 자연·생물 Nature & Living", ["Animals", "Insects", "Flowers", "Nature"]),
    ("🏠 일상생활 Daily Life", ["Family", "Body", "Clothing", "Household"]),
    ("🎨 활동·물건 Activities & Objects", ["Music", "Sports", "Toys", "Tools"]),
    ("🚌 장소·교통 Places & Transport", ["Places", "School", "Vehicles"]),
    ("🌈 색·모양 Colors & Shapes", ["Colors", "Shapes"]),
]

# Korean names for sub-categories
KO_CAT_NAMES = {
    "Fruits":"과일","Vegetables":"채소","Food":"음식","Drinks":"음료","Kitchen":"주방",
    "Animals":"동물","Insects":"곤충","Flowers":"꽃","Nature":"자연",
    "Family":"가족","Body":"신체","Clothing":"의복","Household":"생활용품",
    "Music":"음악","Sports":"운동","Toys":"장난감","Tools":"공구",
    "Places":"장소","School":"학교","Vehicles":"교통수단",
    "Colors":"색깔","Shapes":"모양",
}

SCENARIO = {
    "🍽️ 음식·주방 Food & Kitchen": [
        ("손님", "사과 한 개랑 우유 한 병 주세요."),
        ("상인", "네, 양파도 같이 드릴까요?"),
        ("손님", "아니요, 김치하고 밥만 있으면 돼요."),
        ("상인", "물도 한 병 가져가세요. 4,500원입니다."),
        ("손님", "감사합니다!"),
    ],
    "🐾 자연·생물 Nature & Living": [
        ("아이",   "엄마, 강아지가 멍멍 짖어요!"),
        ("엄마",   "꽃밭에 나비도 있네."),
        ("아이",   "저기 산 위에 새도 있어요."),
        ("엄마",   "오늘 날씨가 좋으니 자연을 마음껏 즐겨."),
        ("아이",   "토끼도 보이면 좋겠어요!"),
    ],
    "🏠 일상생활 Daily Life": [
        ("엄마", "오늘 무슨 옷 입을 거야?"),
        ("아이", "셔츠랑 바지 입을게요. 신발은 운동화로요."),
        ("엄마", "손은 씻었니? 양치도 잘 해."),
        ("아이", "네! 가방도 챙겼어요."),
        ("엄마", "조심해서 학교 잘 다녀와."),
    ],
    "🎨 활동·물건 Activities & Objects": [
        ("친구1", "주말에 같이 축구할래?"),
        ("친구2", "좋아! 공도 가져갈게."),
        ("친구1", "끝나고 노래방 갈래? 피아노 치는 거 보고 싶어."),
        ("친구2", "그래! 망치랑 페인트도 좀 사야 해서…"),
        ("친구1", "공구점도 같이 가자."),
    ],
    "🚌 장소·교통 Places & Transport": [
        ("관광객", "공항에서 호텔까지 어떻게 가나요?"),
        ("주민",   "지하철 타고 학교 역에서 내리세요."),
        ("관광객", "버스는 어디서 타나요?"),
        ("주민",   "역 앞 정류장이에요. 택시도 많이 있어요."),
        ("관광객", "고맙습니다!"),
    ],
    "🌈 색·모양 Colors & Shapes": [
        ("디자이너", "이번엔 빨간색이랑 파란색을 메인으로 하자."),
        ("팀원",     "원형이 좋을까요, 사각형이 좋을까요?"),
        ("디자이너", "삼각형도 같이 써보자. 노란색도 추가해."),
        ("팀원",     "별 모양은 어떨까요?"),
        ("디자이너", "좋아! 컬러풀하게 가자."),
    ],
}

COMPARE = {
    "🍽️ 음식·주방 Food & Kitchen": [
        ("사과 / 바나나 / 포도 / 딸기", "apple / banana / grape / strawberry"),
        ("양파 / 마늘 / 감자 / 무", "onion / garlic / potato / radish"),
        ("물 / 우유 / 커피 / 차", "water / milk / coffee / tea"),
    ],
    "🐾 자연·생물 Nature & Living": [
        ("강아지 / 고양이 / 토끼 / 새", "dog / cat / rabbit / bird"),
        ("나비 / 벌 / 개미 / 모기", "butterfly / bee / ant / mosquito"),
        ("산 / 바다 / 강 / 하늘", "mountain / sea / river / sky"),
    ],
    "🏠 일상생활 Daily Life": [
        ("아빠 / 엄마 / 형 / 누나 / 동생", "father/mother/older bro/older sis/younger"),
        ("머리 / 손 / 발 / 눈 / 입", "head / hand / foot / eye / mouth"),
        ("셔츠 / 바지 / 모자 / 양말 / 신발", "shirt / pants / hat / socks / shoes"),
    ],
    "🎨 활동·물건 Activities & Objects": [
        ("피아노 / 기타 / 드럼 / 바이올린", "piano / guitar / drum / violin"),
        ("축구 / 야구 / 농구 / 테니스", "soccer / baseball / basketball / tennis"),
        ("망치 / 못 / 톱 / 드라이버", "hammer / nail / saw / screwdriver"),
    ],
    "🚌 장소·교통 Places & Transport": [
        ("학교 / 병원 / 공원 / 시장", "school / hospital / park / market"),
        ("차 / 버스 / 지하철 / 기차 / 비행기", "car / bus / subway / train / airplane"),
        ("교실 / 도서관 / 운동장 / 식당", "classroom / library / playground / cafeteria"),
    ],
    "🌈 색·모양 Colors & Shapes": [
        ("빨강 / 파랑 / 노랑 / 초록", "red / blue / yellow / green"),
        ("검정 ↔ 흰색, 어둠 ↔ 빛", "black ↔ white, dark ↔ light"),
        ("원 / 사각형 / 삼각형 / 별", "circle / square / triangle / star"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Parse word cards from HTML
html = SRC.read_text(encoding="utf-8")

# Extract category sections with their icons
cat_pattern = re.compile(
    r'<section class="category-section"[^>]*data-category="([^"]+)"[^>]*>\s*'
    r'<div class="category-header">\s*'
    r'<div class="category-icon">(.+?)</div>'
    r'.*?(<div class="word-grid">[\s\S]*?</div>\s*</section>)',
    re.S
)

# Extract individual word cards
card_re = re.compile(
    r'data-cat="([^"]+)"\s+data-ko="([^"]+)"\s+data-en="([^"]+)"\s+data-ro="([^"]+)"'
)

cards = []
cat_emojis = {}

# Get category emojis
for m in cat_pattern.finditer(html):
    cat = m.group(1)
    icon = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    cat_emojis[cat] = icon

# Get all word cards
for m in card_re.finditer(html):
    cat, ko, en, ro = m.groups()
    cards.append({"cat": cat, "ko": unescape(ko), "en": unescape(en), "ro": unescape(ro)})

print(f"Parsed {len(cards)} word cards across {len(cat_emojis)} categories")

# Group cards by theme + sub-category, preserving source order
theme_groups = {}  # theme → list of (sub_cat, [cards])
for theme_name, sub_cats in THEMES:
    sub_dict = {}
    for c in cards:
        if c["cat"] in sub_cats:
            sub_dict.setdefault(c["cat"], []).append(c)
    # Keep order as in THEMES
    ordered = [(sc, sub_dict[sc]) for sc in sub_cats if sc in sub_dict]
    theme_groups[theme_name] = ordered

# Quizzes: split cards in flat order into chunks of 20, generate 5 questions each
flat_cards = []
for theme_name, sub_cats in THEMES:
    for sc in sub_cats:
        for c in cards:
            if c["cat"] == sc:
                flat_cards.append(c)

random.seed(42)
quizzes = []
for start in range(0, len(flat_cards), 20):
    chunk = flat_cards[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        c = chunk[s]
        wrong_pool = [d["en"] for d in flat_cards if d["en"] != c["en"]]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [c["en"]]; random.shuffle(options)
        qs.append((c["ko"], options, options.index(c["en"])))
    if qs:
        quizzes.append((start+1, min(start+20, len(flat_cards)), qs))

def cat_intro(theme):
    blocks = []
    if theme in SCENARIO:
        ls = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCENARIO[theme])
        blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>{ls}</div>')
    if theme in COMPARE:
        ps = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMPARE[theme])
        blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 비교 박스 · Comparison</div>{ps}</div>')
    return "".join(blocks)

items = []
n = 0
quiz_idx = 0
for theme_name, sub_cats in THEMES:
    items.append('<div class="page-break"></div>')
    items.append(f'<h2 class="cat-h">{escape(theme_name)}</h2>')
    items.append(cat_intro(theme_name))
    for sc in sub_cats:
        sub_cards = [c for c in cards if c["cat"] == sc]
        if not sub_cards: continue
        ko_name = KO_CAT_NAMES.get(sc, sc)
        emoji = cat_emojis.get(sc, "•")
        items.append(f'<h3 class="sub-h">{escape(emoji)} {escape(sc)} · {escape(ko_name)} <span class="sub-count">({len(sub_cards)})</span></h3>')
        items.append('<div class="word-grid">')
        for c in sub_cards:
            n += 1
            qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(c['ko'])}"
            qr_data = qr_png_data_url(qr_url)
            items.append(
                f'<div class="word-card">'
                f'<div class="wc-num">{n}</div>'
                f'<div class="wc-ko">{escape(c["ko"])}</div>'
                f'<div class="wc-ro">{escape(c["ro"])}</div>'
                f'<div class="wc-en">{escape(c["en"])}</div>'
                f'<img class="wc-qr" src="{qr_data}" alt="QR"/>'
                f'</div>'
            )
            if n % 20 == 0 and quiz_idx < len(quizzes):
                items.append('</div>')  # close grid
                a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
                qhtml = [f'<div class="quiz">',
                         f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
                         '<div class="q-sub">한국어 단어의 영어 뜻을 고르세요.</div>']
                for qi, (w, opts, _) in enumerate(qs, 1):
                    opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
                    qhtml.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-word">{escape(w)}</span> = ? {opt_html}</div>')
                qhtml.append('</div>')
                items.extend(qhtml)
                items.append('<div class="word-grid">')  # reopen grid
        items.append('</div>')

# Answer key
answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>Korean Visual Vocabulary 1,100 · Enhanced</title>
<style>
  @page { size: A4; margin: 14mm 10mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.4; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:620px; margin:0 auto; line-height:1.7; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }
  h2.cat-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:14px 22px; margin:0 0 14px; font-size:18px; border-left:6px solid #C0392B; }
  h3.sub-h { color:#1a1a2e; font-size:15px; margin:16px 0 10px; padding-bottom:6px; border-bottom:2px solid #C0392B; }
  h3.sub-h .sub-count { color:#888; font-weight:500; font-size:12px; margin-left:6px; }
  .scenario-box { background:#fff8f0; border-left:4px solid #f97316; padding:14px 18px; margin-bottom:14px; border-radius:6px; }
  .scenario-box .sb-title { font-weight:800; color:#9a3412; font-size:13px; margin-bottom:8px; }
  .scenario-box .dl-line { font-size:12px; margin:3px 0; }
  .scenario-box .dl-speaker { color:#C0392B; font-weight:700; margin-right:6px; }
  .compare-box { background:#f0f5ff; border-left:4px solid #1A4A8A; padding:14px 18px; margin-bottom:16px; border-radius:6px; }
  .compare-box .cb-title { font-weight:800; color:#1e3a8a; font-size:13px; margin-bottom:8px; }
  .compare-box .cb-pair { font-size:12px; margin:3px 0; display:flex; gap:12px; }
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:240px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  .word-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap:8px; margin-bottom:12px; }
  .word-card { background:#fff; border:1px solid #e5e5ea; border-radius:8px; padding:8px; position:relative; min-height:88px; text-align:center; }
  .word-card .wc-num { position:absolute; top:3px; left:6px; font-size:8.5px; color:#bbb; font-weight:600; }
  .word-card .wc-ko { font-size:13px; font-weight:800; color:#1a1a2e; margin-top:4px; line-height:1.2; }
  .word-card .wc-ro { font-size:9.5px; color:#888; font-style:italic; margin-top:1px; }
  .word-card .wc-en { font-size:10.5px; color:#1A4A8A; font-weight:600; margin-top:3px; line-height:1.2; }
  .word-card .wc-qr { width:18px; height:18px; position:absolute; bottom:4px; right:4px; opacity:0.7; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:6px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-word { font-weight:800; color:#1a1a2e; font-size:13px; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; }
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>
<div class="cover">
  <div class="label">Korean Visual Vocabulary · Enhanced</div>
  <h1>Korean Visual Vocabulary 1,100</h1>
  <div class="kr">시각 어휘 1,100 · 22 카테고리 · 향상판</div>
  <p class="desc">과일·채소·동물·곤충·꽃·가족·신체·의복·악기·운동·공구·장소·교통수단·색깔·모양 등 22개 카테고리, 1,100개 단어를 카드 그리드로 학습. QR로 발음 듣기, 시나리오·비교·미니 퀴즈까지.</p>
  <div class="features">
    <span class="feat">🎭 시나리오</span><span class="feat">🔍 비교</span><span class="feat">📝 퀴즈</span><span class="feat">🔊 QR</span>
  </div>
</div>
""" + "\n".join(items) + "\n".join(answer_html) + """
</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML -> {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

if PDF_OUT.exists(): PDF_OUT.unlink()
url = f"file:///{HTML_OUT.as_posix()}"
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=420)
time.sleep(4)
if PDF_OUT.exists():
    print(f"PDF  -> {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
