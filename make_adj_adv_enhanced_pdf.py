"""
Enhanced adjectives/adverbs PDF — QR + scenarios + comparison + quizzes.
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "adjectives_adverbs.txt"
HTML_OUT = ROOT / "adjectives-adverbs-enhanced.html"
PDF_OUT  = ROOT / "adjectives-adverbs-enhanced.pdf"

# Theme mapping by Korean substring of section header
THEMES = [
    ("🎯 관형사·형용사", ["성상 및 상태", "지시 및 수량", "성격 및 감정", "모양 및 성질", "기타 필수 관형", "상태와 성질을 나타내는 고급 형용사", "감정 및 성격 묘사", "한국인의 정서가 담긴 미묘한 형용사", "마무리 인심"]),
    ("📊 부사 (정도·시간·방법)", ["정도와 강조", "시간 및 빈도", "방법 및 태도", "추측 및 태도", "문장의 뉘앙스", "태도와 양상", "세련된 대화를 위한 부사"]),
    ("🔗 접속사·감탄사·조사·대명사", ["문장 연결 접속사", "일상 감탄사", "필수 조사", "필수 대명사"]),
    ("🔢 수사·단위", ["수사 및 단위 명사"]),
    ("💬 구어체·일상 표현", ["일상 구어체 핵심 표현", "일상 대화의 감초", "일상에서 자주 쓰는 구어체 꿀팁"]),
    ("🥋 관용구·속담·사자성어", ["신체 부위를 이용한 관용구", "상황별 필수 속담", "지혜와 교훈이 담긴 필수 사자성어"]),
    ("🌀 의성·의태어", ["의성어 및 의태어", "움직임과 모양을 흉내", "소리를 흉내"]),
]

SCENARIO = {
    "🎯 관형사·형용사": [
        ("친구1", "새 옷이 정말 잘 어울려요!"),
        ("친구2", "헌 옷보다 첫 느낌이 좋죠?"),
        ("친구1", "넓은 마음으로 칭찬해 주셔서 감사해요."),
        ("친구2", "밝은 색깔이 얼굴을 환하게 해요."),
        ("친구1", "다음엔 다른 스타일도 도전해 볼게요."),
    ],
    "📊 부사 (정도·시간·방법)": [
        ("상사", "오늘 정말 바쁘죠?"),
        ("직원", "네, 아주 바빠요. 그래도 천천히 처리하고 있어요."),
        ("상사", "조금만 더 빨리 할 수 있을까요?"),
        ("직원", "최선을 다해 보겠습니다. 이미 거의 마무리 단계예요."),
        ("상사", "수고가 많아요."),
    ],
    "🔗 접속사·감탄사·조사·대명사": [
        ("학생", "선생님, 이 문제가 어려워요."),
        ("선생님", "그래서 같이 풀어보자. 우선 천천히."),
        ("학생", "그러나 시간이 부족해요…"),
        ("선생님", "괜찮아. 그리고 너 잘하고 있어!"),
        ("학생", "와! 감사합니다."),
    ],
    "🔢 수사·단위": [
        ("손님", "사과 다섯 개 주세요."),
        ("상인", "한 봉지에 담아드릴까요?"),
        ("손님", "네, 그리고 우유 두 병도 같이요."),
        ("상인", "모두 합쳐서 만 원입니다."),
        ("손님", "감사합니다."),
    ],
    "💬 구어체·일상 표현": [
        ("친구1", "야, 진짜 대박이다!"),
        ("친구2", "응? 뭐가?"),
        ("친구1", "이거 봐봐, 짱이지?"),
        ("친구2", "헐, 완전 신기해."),
        ("친구1", "맞아 맞아!"),
    ],
    "🥋 관용구·속담·사자성어": [
        ("선배", "발 벗고 나서서 도와주는 친구가 진짜 친구야."),
        ("후배", "맞아요. 가는 말이 고와야 오는 말이 곱죠."),
        ("선배", "고진감래라고, 노력하면 좋은 결과가 있을 거야."),
        ("후배", "마음에 새기겠습니다."),
        ("선배", "잘할 수 있어. 응원할게."),
    ],
    "🌀 의성·의태어": [
        ("아이",  "엄마! 비가 주룩주룩 와요."),
        ("엄마",  "맞아. 천둥도 우르르 쾅쾅 치네."),
        ("아이",  "강아지가 멍멍 짖어요!"),
        ("엄마",  "고양이는 야옹 하지."),
        ("아이",  "비가 그치면 새가 짹짹 울 거예요."),
    ],
}

COMPARE = {
    "🎯 관형사·형용사": [
        ("새 ↔ 헌", "new ↔ old/used"),
        ("긴 ↔ 짧은, 높은 ↔ 낮은", "long ↔ short, high ↔ low"),
        ("넓은 ↔ 좁은, 무거운 ↔ 가벼운", "wide ↔ narrow, heavy ↔ light"),
        ("밝은 ↔ 어두운", "bright ↔ dark"),
        ("모든 / 온 / 딴 / 순", "every / whole / other / pure"),
    ],
    "📊 부사 (정도·시간·방법)": [
        ("아주 / 매우 / 정말", "very / really / truly"),
        ("일찍 ↔ 늦게, 자주 ↔ 가끔", "early ↔ late, often ↔ sometimes"),
        ("빨리 ↔ 천천히, 잘 ↔ 못", "fast ↔ slow, well ↔ poorly"),
        ("아마 / 물론 / 절대", "perhaps / of course / never"),
    ],
    "🔗 접속사·감탄사·조사·대명사": [
        ("그리고 / 그래서 / 그러나 / 하지만", "and / so / but / however"),
        ("이 / 그 / 저, 여기 / 거기 / 저기", "this/that/that-far"),
        ("을·를 / 이·가 / 에 / 에서", "OBJ / SUBJ / to / at"),
    ],
    "🔢 수사·단위": [
        ("하나·한 / 둘·두 / 셋·세 / 넷·네", "1/2/3/4 (native Korean)"),
        ("일 / 이 / 삼 / 사", "1/2/3/4 (Sino-Korean)"),
        ("개 / 명 / 마리 / 권", "items / people / animals / books"),
    ],
    "💬 구어체·일상 표현": [
        ("대박 / 짱 / 헐", "amazing / great / OMG"),
        ("진짜 ↔ 가짜, 완전 / 진짜", "real ↔ fake, totally / really"),
    ],
    "🥋 관용구·속담·사자성어": [
        ("발이 넓다 / 손이 크다 / 입이 무겁다", "well-connected / generous / discreet"),
        ("가는 말이 고와야 오는 말이 곱다", "kind words bring kind words"),
        ("고진감래 / 새옹지마", "no pain no gain / blessing in disguise"),
    ],
    "🌀 의성·의태어": [
        ("주룩주룩 / 보슬보슬", "pouring rain / drizzling"),
        ("멍멍 / 야옹 / 짹짹", "woof / meow / tweet"),
        ("우르르 쾅쾅 / 졸졸", "thunder / trickling"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Parser (same as before)
raw_lines = SRC.read_text(encoding="utf-8").splitlines()
lines = [ln.strip() for ln in raw_lines if ln.strip()]
section_re = re.compile(r"^\d+\.\s+(.+?)\s+\((.+?)\)\s*$")

def is_section_header(s): return bool(section_re.match(s))
def parse_word_line(s):
    m = re.match(r"^(.+?)\s+\((.+?)\)\s*$", s)
    if not m: return None
    ko, en = m.group(1).strip(), m.group(2).strip()
    if len(ko) > 25: return None
    if any(c in ko for c in ".?!,"): return None
    return (ko, en)
def parse_example_line(s):
    m = re.match(r"^(.+?)\s+\((.+)\)\s*$", s)
    if not m: return (s, "")
    return (m.group(1).strip(), m.group(2).strip())

rows = []
current_sub = "(unknown)"
i = 0
while i < len(lines):
    line = lines[i]
    if is_section_header(line):
        m = section_re.match(line)
        current_sub = m.group(1).strip()
        i += 1; continue
    wl = parse_word_line(line)
    if wl:
        ko_word, en_meaning = wl
        ex1_ko = ex1_en = ex2_ko = ex2_en = ""
        if i+1 < len(lines):
            ex1_ko, ex1_en = parse_example_line(lines[i+1])
        if i+2 < len(lines):
            nxt = lines[i+2]
            if not is_section_header(nxt) and not parse_word_line(nxt):
                ex2_ko, ex2_en = parse_example_line(nxt); i += 3
            else: i += 2
        else: i += 2
        rows.append((current_sub, ko_word, en_meaning, ex1_ko, ex1_en, ex2_ko, ex2_en))
    else:
        i += 1

print(f"Parsed {len(rows)} entries")

# Theme mapping
def get_theme(sub):
    for theme_name, prefixes in THEMES:
        for prefix in prefixes:
            if sub.startswith(prefix):
                return theme_name
    return "기타"

random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sub, ko, en, _, _, _, _ = chunk[s]
        wrong_pool = [r[2] for r in rows if r[2] != en]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [en]; random.shuffle(options)
        correct_idx = options.index(en)
        qs.append((ko, options, correct_idx))
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
for i, (sub, ko, en, e1k, e1e, e2k, e2e) in enumerate(rows, 1):
    theme = get_theme(sub)
    if theme != last_theme:
        items.append('</tbody></table>'); items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">한국어</th><th class="en-col">English</th><th>예문</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sub = None
    if sub != last_sub:
        items.append(f'<tr class="section"><td colspan="5">{escape(sub)}</td></tr>')
        last_sub = sub
    ex_html = ""
    if e1k: ex_html += f'<div class="ex"><span class="ko">{escape(e1k)}</span><span class="en">{escape(e1e)}</span></div>'
    if e2k: ex_html += f'<div class="ex"><span class="ko">{escape(e2k)}</span><span class="en">{escape(e2e)}</span></div>'
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(ko)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td><td class="k">{escape(ko)}</td><td class="en">{escape(en)}</td>'
        f'<td class="ex-cell">{ex_html}</td><td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">단어의 영어 뜻을 고르세요.</div>']
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
<html lang="ko"><head><meta charset="UTF-8"><title>한국어 형용사·부사·관용구 · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 12mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:28px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:620px; margin:0 auto; line-height:1.7; }
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:240px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:28px;} th.k-col{width:82px;} th.en-col{width:105px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#1a1a2e; font-size:12.5px; }
  td.en  { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.ex-cell .ex { margin-bottom:3px; }
  td.ex-cell .ex .ko { display:block; color:#C0392B; font-size:10.5px; font-weight:600; }
  td.ex-cell .ex .en { display:block; color:#666; font-style:italic; font-size:9.5px; margin-top:1px; }
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
  <div class="label">Korean Adjectives · Adverbs · Idioms · Enhanced</div>
  <h1>한국어 형용사·부사·관용구 가이드</h1>
  <div class="kr">필수 표현 종합 · 향상판</div>
  <p class="desc">관형사·고급 형용사·부사·접속사·조사·관용구·속담·사자성어·의성/의태어 — 카테고리별 단어와 영어 의미, 한국어 예문, 시나리오, 비교 박스, 미니 퀴즈, 발음 QR 코드까지.</p>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=420)
time.sleep(5)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
