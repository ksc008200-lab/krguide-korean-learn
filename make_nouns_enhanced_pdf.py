"""
Enhanced nouns PDF — QR + scenarios + comparison + quizzes.
Reuses examples from make_nouns_pdf.py.
"""
import re, subprocess, time, io, base64, random, urllib.parse, ast
from pathlib import Path
from html import unescape, escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "essential-nouns-enhanced.html"
PDF_OUT  = ROOT / "essential-nouns-enhanced.pdf"

# Load EX dict from make_nouns_pdf.py by parsing source — avoids executing the whole file
nouns_src = (ROOT / "make_nouns_pdf.py").read_text(encoding="utf-8")
m_ex = re.search(r"^EX\s*=\s*(\{[\s\S]+?^\})", nouns_src, re.M)
EX = ast.literal_eval(m_ex.group(1))

# Group categories into themes
THEMES = [
    ("👨‍👩‍👧 사람·관계·직업", ["가족", "사회", "직업"]),
    ("🫀 신체·건강", ["신체", "건강"]),
    ("🍚 음식·식사·식당", ["식사", "재료", "과일·채소", "식당 관련"]),
    ("🕐 시간·날씨·계절", ["시간 단위", "시점 표현", "날씨·계절"]),
    ("🏙️ 장소·집·건물·교통", ["집 안", "공공장소", "상업시설", "지리", "교통"]),
    ("🏠 사물·가전·문구·의류", ["가전·IT", "가구·소품", "필기구·문구", "통신"]),
    ("📚 교육·업무·감정·개념", ["교육", "업무", "감정", "개념"]),
]

SCENARIO = {
    "👨‍👩‍👧 사람·관계·직업": [
        ("아이",  "엄마, 아빠는 어디 가셨어요?"),
        ("엄마",  "회사에 가셨어. 의사 선생님 만나러."),
        ("아이",  "할머니께도 전화드릴까요?"),
        ("엄마",  "응. 친척들에게도 안부 전해드려."),
        ("아이",  "네! 동생도 같이요?"),
    ],
    "🫀 신체·건강": [
        ("환자",   "머리도 아프고 열이 나요."),
        ("간호사", "감기 증상이네요. 약국에서 약 받으셨어요?"),
        ("환자",   "아직요. 운동도 못 하고 있어요."),
        ("간호사", "휴식이 필요해요. 검사도 받아 보세요."),
        ("환자",   "건강이 제일 중요한데… 알겠습니다."),
    ],
    "🍚 음식·식사·식당": [
        ("손님",   "메뉴 좀 볼게요."),
        ("점원",   "이 식당은 반찬이 다양해요. 찌개도 추천드려요."),
        ("손님",   "그럼 점심 정식 하나랑 차 한 잔 주세요."),
        ("점원",   "네, 숟가락이랑 젓가락 가져다드릴게요."),
        ("손님",   "감사합니다. 아주 맛있겠어요."),
    ],
    "🕐 시간·날씨·계절": [
        ("친구1", "내일 날씨 어때?"),
        ("친구2", "오후에 비가 온대. 봄인데 추워."),
        ("친구1", "그럼 주말에 만날까?"),
        ("친구2", "이번 주말은 휴일이야. 좋아!"),
        ("친구1", "낮에 만나자. 새벽엔 추워."),
    ],
    "🏙️ 장소·집·건물·교통": [
        ("관광객", "공원에 어떻게 가나요?"),
        ("주민",   "지하철 타고 두 정거장 가면 돼요. 정류장에서 내려요."),
        ("관광객", "근처에 도서관도 있나요?"),
        ("주민",   "네, 박물관 옆 건물이에요."),
        ("관광객", "감사합니다. 좋은 도시네요."),
    ],
    "🏠 사물·가전·문구·의류": [
        ("엄마",  "노트북이랑 핸드폰 챙겼니?"),
        ("아들",  "네, 가방에 넣었어요. 충전기도요."),
        ("엄마",  "코트랑 모자 잊지 말고."),
        ("아들",  "안경이랑 우산도 챙길게요."),
        ("엄마",  "잘 다녀와."),
    ],
    "📚 교육·업무·감정·개념": [
        ("학생",   "선생님, 시험 문제가 너무 어려웠어요."),
        ("선생님", "괜찮아. 다음 학기에 더 잘하면 돼."),
        ("학생",   "걱정이 많아서 잠도 못 잤어요."),
        ("선생님", "기분 풀어. 결과보다 과정이 중요해."),
        ("학생",   "감사합니다. 마음이 한결 편해졌어요."),
    ],
}

COMPARE = {
    "👨‍👩‍👧 사람·관계·직업": [
        ("아버지 / 어머니", "father / mother"),
        ("아들 / 딸", "son / daughter"),
        ("형·오빠 / 누나·언니 / 동생", "older brother / older sister / younger sibling"),
        ("선배 ↔ 후배", "senior ↔ junior"),
        ("어른 ↔ 아이", "adult ↔ child"),
    ],
    "🫀 신체·건강": [
        ("머리 / 얼굴 / 목 / 어깨", "head / face / neck / shoulder"),
        ("손 / 손가락 / 발 / 발가락", "hand / finger / foot / toe"),
        ("병 / 약 / 병원 / 약국", "illness / medicine / hospital / pharmacy"),
        ("운동 ↔ 휴식", "exercise ↔ rest"),
    ],
    "🍚 음식·식사·식당": [
        ("아침 / 점심 / 저녁 / 간식", "breakfast / lunch / dinner / snack"),
        ("물 / 우유 / 커피 / 차 / 술", "water / milk / coffee / tea / alcohol"),
        ("소고기 / 돼지고기 / 닭고기 / 생선", "beef / pork / chicken / fish"),
    ],
    "🕐 시간·날씨·계절": [
        ("오늘 / 어제 / 내일 / 모레", "today / yesterday / tomorrow / day after"),
        ("봄 / 여름 / 가을 / 겨울", "spring / summer / autumn / winter"),
        ("오전 ↔ 오후, 낮 ↔ 밤", "AM ↔ PM, day ↔ night"),
    ],
    "🏙️ 장소·집·건물·교통": [
        ("집 / 학교 / 회사 / 병원", "home / school / company / hospital"),
        ("버스 / 지하철 / 택시 / 기차 / 비행기", "bus / subway / taxi / train / airplane"),
        ("도시 ↔ 시골", "city ↔ countryside"),
    ],
    "🏠 사물·가전·문구·의류": [
        ("컴퓨터 / 노트북 / 핸드폰", "computer / laptop / mobile phone"),
        ("연필 / 펜 / 종이 / 공책", "pencil / pen / paper / notebook"),
        ("티셔츠 / 바지 / 치마 / 코트", "T-shirt / pants / skirt / coat"),
    ],
    "📚 교육·업무·감정·개념": [
        ("수업 / 공부 / 시험 / 숙제", "class / study / exam / homework"),
        ("출근 ↔ 퇴근", "go to work ↔ leave work"),
        ("성공 ↔ 실패, 행복 ↔ 슬픔", "success ↔ failure, happiness ↔ sadness"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Extract nouns
html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch38">.*?(?=<div class="chapter" id="ch39")', html, re.S)
block = m.group(0)
def clean(s): return unescape(re.sub(r"<[^>]+>", "", s)).strip()

rows = []
current = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="6"' in row:
        txt = clean(row)
        if txt and not txt.startswith("한글"): current = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 6: continue
    g1, p1, e1, g2, p2, e2 = [clean(c) for c in cells]
    if g1 == "한글": continue
    for g, p, e in [(g1, p1, e1), (g2, p2, e2)]:
        if not g: continue
        rows.append((current, g, p, e))

print(f"Extracted {len(rows)} nouns")

# Map subcategory → theme by prefix match
sub_to_theme = {}
for theme_name, prefixes in THEMES:
    for prefix in prefixes:
        sub_to_theme[prefix] = theme_name
def get_theme(sub):
    for key, theme in sub_to_theme.items():
        if sub.startswith(key): return theme
    return "기타"

# Quizzes
random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sub, g, p, e = chunk[s]
        wrong_pool = [r[3] for r in rows if r[3] != e]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [e]; random.shuffle(options)
        correct_idx = options.index(e)
        qs.append((g, options, correct_idx))
    quizzes.append((start+1, min(start+20, len(rows)), qs))

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
last_theme = None; last_sub = None
quiz_idx = 0
for i, (sub, g, p, e) in enumerate(rows, 1):
    theme = get_theme(sub)
    if theme != last_theme:
        items.append('</tbody></table>'); items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">한글</th><th class="r-col">발음</th><th class="en-col">English</th><th>예문</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sub = None
    if sub != last_sub:
        items.append(f'<tr class="section"><td colspan="6">{escape(sub)}</td></tr>')
        last_sub = sub
    ex_ko, ex_en = EX.get(i, ("", ""))
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(g)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td><td class="k">{escape(g)}</td><td class="r">{escape(p)}</td>'
        f'<td class="en">{escape(e)}</td>'
        f'<td class="ex"><span class="ex-ko">{escape(ex_ko)}</span><span class="ex-en">{escape(ex_en)}</span></td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="6"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">명사의 영어 뜻을 고르세요.</div>']
        for qi, (w, opts, _) in enumerate(qs, 1):
            opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
            qh.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-word">{escape(w)}</span> = ? {opt_html}</div>')
        qh.append('</div></td></tr>')
        items.extend(qh)
items.append('</tbody></table>')

answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>Essential Korean Nouns · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 12mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:600px; margin:0 auto; line-height:1.7; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }
  h2.cat-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:14px 22px; margin:0 0 14px; font-size:18px; border-left:6px solid #C0392B; }
  .scenario-box { background:#fff8f0; border-left:4px solid #f97316; padding:14px 18px; margin-bottom:14px; border-radius:6px; }
  .scenario-box .sb-title { font-weight:800; color:#9a3412; font-size:13px; margin-bottom:8px; }
  .scenario-box .dl-line { font-size:12px; margin:3px 0; }
  .scenario-box .dl-speaker { color:#C0392B; font-weight:700; margin-right:6px; }
  .compare-box { background:#f0f5ff; border-left:4px solid #1A4A8A; padding:14px 18px; margin-bottom:16px; border-radius:6px; }
  .compare-box .cb-title { font-weight:800; color:#1e3a8a; font-size:13px; margin-bottom:8px; }
  .compare-box .cb-pair { font-size:12px; margin:3px 0; display:flex; gap:12px; }
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:220px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:30px;} th.k-col{width:80px;} th.r-col{width:70px;} th.en-col{width:120px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:12.5px; }
  td.r   { color:#6b6b6b; font-style:italic; font-size:10px; }
  td.en  { color:#1A4A8A; font-size:11px; }
  td.ex .ex-ko { display:block; color:#C0392B; font-weight:600; font-size:10.5px; }
  td.ex .ex-en { display:block; color:#666; font-style:italic; font-size:10px; margin-top:1px; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:11px; padding:7px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
  tr.quiz-row td { padding:0; }
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
  <div class="label">Essential Korean Nouns · Enhanced</div>
  <h1>Essential Korean Nouns</h1>
  <div class="kr">필수 명사 · 향상판</div>
  <p class="desc">By theme — Korean noun · romanization · English meaning · example sentence — plus scenarios, comparison boxes, quizzes, and pronunciation QR codes.</p>
  <div class="features">
    <span class="feat">🎭 시나리오</span><span class="feat">🔍 비교</span><span class="feat">📝 퀴즈</span><span class="feat">🔊 QR</span>
  </div>
</div>
""" + "\n".join(items) + "\n".join(answer_html) + """
</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML → {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url = f"file:///{HTML_OUT.as_posix()}"
if PDF_OUT.exists(): PDF_OUT.unlink()
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=300)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
