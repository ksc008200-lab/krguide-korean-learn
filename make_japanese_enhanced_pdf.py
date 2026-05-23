"""
Enhanced Japanese loanwords PDF with QR + scenarios + comparison + quizzes.
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "japanese_loanwords.txt"
HTML_OUT = ROOT / "japanese-loanwords-enhanced.html"
PDF_OUT  = ROOT / "japanese-loanwords-enhanced.pdf"

# Theme-level scenarios + compares
THEMES = [
    ("생활·일상 어휘", ["생활 및 일상 어휘", "일상 생활 및 잡화"]),
    ("건설·작업 현장", ["건설 및 기술/작업 현장 어휘", "건설, 공구 및 작업 현장 용어", "인테리어 및 건축 건설 분야"]),
    ("스포츠·여가·유흥", ["스포츠 및 여가/유흥 어휘", "스포츠, 유흥 및 전문 용어", "낚시 분야"]),
    ("음식·의류", ["음식 및 식재료 (더 구체적으로)", "음식 및 의류 관련"]),
    ("사회·법률·행정", ["기타 및 사회 어휘", "생활 기타 및 사회 한자어", "법률 및 행정 용어", "기타 전문 및 일상 용어"]),
    ("군대·경찰", ["군대 및 경찰 용어"]),
    ("자동차 정비", ["자동차 정비 분야"]),
]

SCENARIO = {
    "생활·일상 어휘": [
        ("엄마",  "구루무 좀 발랐니?"),
        ("딸",    "네, 발랐어요. 그런데 사라 좀 꺼내 주세요."),
        ("엄마",  "오뎅 국물 데웠다. 와사비도 가져와."),
        ("딸",    "쓰리빠 신고 갈게요."),
        ("엄마",  "조심해. 다꾸앙도 같이 먹자."),
    ],
    "건설·작업 현장": [
        ("팀장", "오늘은 공구리 작업이야. 단도리 잘해."),
        ("막내", "네! 야스리랑 헤라 준비했어요."),
        ("팀장", "데모도 한 명 더 부르고, 가도 부분 시아게 마무리해."),
        ("막내", "기스 안 나게 조심하겠습니다."),
        ("팀장", "함바 식당에서 점심 먹고 시작하자."),
    ],
    "스포츠·여가·유흥": [
        ("친구1", "오늘 당구 한 판 어때? 다마 잘 맞을 거 같은데."),
        ("친구2", "좋아. 그런데 겐세이 놓지 마라."),
        ("친구1", "후루꾸로 이겨도 인정 안 해줄게."),
        ("친구2", "오시랑 히끼만 잘 쓰면 돼."),
        ("친구1", "맛세이는 무리하지 말고."),
    ],
    "음식·의류": [
        ("주문자", "스시 한 접시 주세요. 쇼가도 같이요."),
        ("점원",   "네, 와사비는 따로 드릴까요?"),
        ("주문자", "네. 우동도 하나 추가할게요."),
        ("점원",   "감사합니다. 가쓰오부시 올려 드릴까요?"),
        ("주문자", "좋아요. 잘 부탁드려요."),
    ],
    "사회·법률·행정": [
        ("의뢰인", "지불 기한이 언제까지인가요?"),
        ("변호사", "납기 내에 처리하셔야 합니다. 잔고 확인부터요."),
        ("의뢰인", "수속이 복잡해서 가불이 필요한데요."),
        ("변호사", "구좌 정보 주시면 익일 안내해 드리겠습니다."),
        ("의뢰인", "감사합니다. 조속히 진행해 주세요."),
    ],
    "군대·경찰": [
        ("선임", "오늘 야간에 비상 단도리 점검이야."),
        ("후임", "네, 단도리는 다 마쳤습니다."),
        ("선임", "총기 점검도 빈틈없이 해."),
        ("후임", "알겠습니다. 다시 한번 확인하겠습니다."),
        ("선임", "수고해."),
    ],
    "자동차 정비": [
        ("운전자", "차에서 이상한 소리가 나요."),
        ("정비사", "쇼바 문제인 것 같네요. 데후 오일도 확인할게요."),
        ("운전자", "빳데리도 약한 것 같아요."),
        ("정비사", "빳데리 교체하고 뼁끼 부분 보수도 같이 할까요?"),
        ("운전자", "네, 부탁드립니다."),
    ],
}

COMPARE = {
    "생활·일상 어휘": [
        ("구루무 (크림) / 다꾸앙 (단무지)", "Cream / Pickled radish"),
        ("쓰리빠 (슬리퍼) / 사라 (접시)", "Slippers / Plate"),
        ("벤또 (도시락) / 모찌 (찹쌀떡)", "Lunchbox / Rice cake"),
    ],
    "건설·작업 현장": [
        ("시아게 (마무리) ↔ 나라시 (고르기)", "Finishing ↔ Leveling"),
        ("야스리 (줄) ↔ 기리 (드릴 날)", "File ↔ Drill bit"),
        ("단도리 (단속) ↔ 무대뽀 (막무가내)", "Preparation ↔ Reckless"),
    ],
    "스포츠·여가·유흥": [
        ("오시 (밀어치기) ↔ 히끼 (끌어치기)", "Push shot ↔ Pull shot"),
        ("후루꾸 (요행) ↔ 실력", "Luck ↔ Skill"),
        ("나와바리 (구역) / 야바위 (속임수)", "Territory / Scam"),
    ],
    "음식·의류": [
        ("스시 (초밥) / 사시미 (회)", "Sushi / Sashimi"),
        ("와사비 (고추냉이) / 쇼가 (생강)", "Wasabi / Ginger"),
        ("카라 (깃) / 시보리 (조임)", "Collar / Tight band"),
    ],
    "사회·법률·행정": [
        ("지불 (지급) / 납기 (기한)", "Payment / Deadline"),
        ("가불 ↔ 잔고", "Advance pay ↔ Balance"),
        ("승인 ↔ 거절", "Approval ↔ Rejection"),
    ],
    "군대·경찰": [
        ("단도리 (준비/단속)", "Preparation / Discipline check"),
        ("쇼부 (담판)", "Showdown / Settle"),
    ],
    "자동차 정비": [
        ("쇼바 (쇼크업소버) / 데후 (디퍼런셜)", "Shock absorber / Differential"),
        ("빳데리 (배터리) / 세루 (스타트 모터)", "Battery / Starter motor"),
        ("기스 (흠집) ↔ 시아게 (마무리)", "Scratch ↔ Finishing"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Parse loanwords (same parser as before)
lines = SRC.read_text(encoding="utf-8").splitlines()
section_re_a = re.compile(r"^\s*(\d+)~(\d+)\s*:\s*(.+?)\s*$")
section_re_b = re.compile(r"^\s*(\d+)\.\s+(.+?)\s+\((\d+)\s*~\s*(\d+)\)\s*$")
entry_re = re.compile(r'^\s*([^\s(][^()]*?)\s*\(([^)]+)\)\s*:\s*"(.+?)"\s*[,，]\s*"(.+?)"')

rows = []
current = "(미분류)"
for raw in lines:
    line = raw.strip()
    if not line: continue
    if "(중복 제거)" in line or line.startswith("괄호 안에는") or line.startswith("한국어 속에는") or line.startswith("가장 딱딱하고"):
        continue
    ma = section_re_a.match(line)
    if ma:
        current = ma.group(3).strip(); continue
    mb = section_re_b.match(line)
    if mb:
        current = mb.group(2).strip(); continue
    me = entry_re.match(line)
    if me:
        word, orig, ex1, ex2 = me.groups()
        rows.append((current, word.strip(), orig.strip(), ex1.strip(), ex2.strip()))
        continue
    me2 = re.match(r'^\s*([^\s(][^()]*?)\s*\(([^)]+)\)\s*:\s*(.+)$', line)
    if me2:
        word, orig, rest = me2.groups()
        exs = re.findall(r'"([^"]+)"', rest)
        if len(exs) >= 1:
            rows.append((current, word.strip(), orig.strip(), exs[0], exs[1] if len(exs) >= 2 else ""))

print(f"Parsed {len(rows)} entries")

# Map subcategory → theme
sub_to_theme = {}
for theme_name, subs in THEMES:
    for s in subs:
        sub_to_theme[s] = theme_name

# Group rows by theme in source order
def get_theme(sub):
    return sub_to_theme.get(sub, "기타")

# Build quizzes (every 20)
random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sub, word, orig, ex1, ex2 = chunk[s]
        wrong_pool = [r[2] for r in rows if r[2] != orig]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [orig]; random.shuffle(options)
        correct_idx = options.index(orig)
        qs.append((word, options, correct_idx))
    quizzes.append((start+1, min(start+20, len(rows)), qs))

def cat_intro(theme):
    blocks = []
    if theme in SCENARIO:
        lines_html = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCENARIO[theme])
        blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>{lines_html}</div>')
    if theme in COMPARE:
        pairs = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMPARE[theme])
        blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 비교 박스 · Comparison</div>{pairs}</div>')
    return "".join(blocks)

items = []
last_theme = None
last_sub = None
quiz_idx = 0
for i, (sub, word, orig, ex1, ex2) in enumerate(rows, 1):
    theme = get_theme(sub)
    if theme != last_theme:
        items.append('</tbody></table>')
        items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">🌟 {escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">일본어 외래어</th><th class="en-col">우리말</th><th>예문</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sub = None
    if sub != last_sub:
        items.append(f'<tr class="section"><td colspan="5">{escape(sub)}</td></tr>')
        last_sub = sub
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(word)}"
    qr_data = qr_png_data_url(qr_url)
    ex_html = f'<span class="ex-row">{escape(ex1)}</span>'
    if ex2: ex_html += f'<span class="ex-row">{escape(ex2)}</span>'
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(word)}</td>'
        f'<td class="en">{escape(orig)}</td>'
        f'<td class="ex">{ex_html}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td>'
        f'</tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qhtml = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
                 f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
                 '<div class="q-sub">일본어 외래어의 우리말 뜻을 고르세요.</div>']
        for qi, (w, opts, _) in enumerate(qs, 1):
            opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
            qhtml.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-word">{escape(w)}</span> = ? {opt_html}</div>')
        qhtml.append('</div></td></tr>')
        items.extend(qhtml)
items.append('</tbody></table>')

answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>일본어 외래어 · Enhanced</title>
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:230px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:30px;} th.k-col{width:90px;} th.en-col{width:110px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#C0392B; font-size:12px; }
  td.en  { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.ex .ex-row { display:block; color:#555; font-size:10px; margin-bottom:2px; }
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
  <div class="label">Japanese Loanwords in Korean · Enhanced</div>
  <h1>일본어 외래어 사전</h1>
  <div class="kr">우리말 속 일본어 표현 · 향상판</div>
  <p class="desc">Japanese-origin word in Korean, its native Korean equivalent, example sentences — plus theme scenarios, comparison boxes, quizzes, and pronunciation QR codes.</p>
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
