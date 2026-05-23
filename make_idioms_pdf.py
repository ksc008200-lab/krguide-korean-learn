"""
Enhanced 사자성어 100 PDF — same style as other enhanced PDFs.
"""
import re, subprocess, time, io, base64, random, urllib.parse, json
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "idioms100.json"
HTML_OUT = ROOT / "idioms-100-enhanced.html"
PDF_OUT  = ROOT / "idioms-100-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

THEMES = [
    ("🌅 인생·운명", ["인생"]),
    ("💪 노력·성취", ["노력"]),
    ("🤝 우정·관계", ["우정"]),
    ("🧠 지혜·판단", ["지혜"]),
    ("💼 비즈니스·전략", ["비즈니스"]),
    ("🧘 수양·자기관리", ["수양"]),
    ("⚖️ 처세·세상살이", ["처세"]),
]

SCENARIO = {
    "🌅 인생·운명": [
        ("선배", "사업 망해서 절망했었지?"),
        ("후배", "네… 그런데 그 덕에 더 좋은 길을 찾았어요."),
        ("선배", "그게 바로 새옹지마야. 인생 어떻게 될지 몰라."),
        ("후배", "전화위복이라는 말이 딱 맞네요."),
        ("선배", "흥망성쇠는 누구에게나 있는 법이지."),
    ],
    "💪 노력·성취": [
        ("코치", "포기하지 말고 끝까지 가자."),
        ("선수", "정말 힘들어요…"),
        ("코치", "고진감래라잖아. 지금의 고통이 달콤한 결실이 될 거야."),
        ("선수", "각골난망이에요. 코치님 가르침 잊지 않을게요."),
        ("코치", "백절불굴의 정신이 진짜 챔피언을 만든다."),
    ],
    "🤝 우정·관계": [
        ("친구1", "오랜만이야. 그래도 변함이 없네."),
        ("친구2", "관포지교라더니, 우리도 그런 사이지."),
        ("친구1", "어려울 때 도와준 거 잊지 않을게."),
        ("친구2", "이심전심 아니야? 말 안 해도 알아."),
        ("친구1", "역시 죽마고우다!"),
    ],
    "🧠 지혜·판단": [
        ("CEO",   "이 결정 어떻게 봐?"),
        ("자문",  "심사숙고하셔야 합니다. 한 번 가면 돌이키기 어려워요."),
        ("CEO",   "역시 군자삼사 — 세 번 생각하는 게 맞겠지."),
        ("자문",  "결단은 빠르되, 판단은 신중하셔야죠."),
        ("CEO",   "지피지기면 백전불태라 했으니, 우선 정보부터 모으자."),
    ],
    "💼 비즈니스·전략": [
        ("팀장", "경쟁사 분석이 우선이야. 지피지기면 백전불태."),
        ("팀원", "그쪽 약점부터 찾아볼게요."),
        ("팀장", "이번 분기에 승부수를 띄워야 해. 진검승부야."),
        ("팀원", "이번엔 일거양득의 전략이 필요해 보여요."),
        ("팀장", "좋아, 두 가지 목표를 한 번에 잡자."),
    ],
    "🧘 수양·자기관리": [
        ("스승",  "마음 다스리는 게 가장 어려운 법이지."),
        ("제자",  "수신제가가 우선이라 하셨죠."),
        ("스승",  "초심을 잃지 말고. 멀리 가려면 함께 가야 한다."),
        ("제자",  "유비무환의 자세로 늘 준비하겠습니다."),
        ("스승",  "그게 진짜 강한 사람의 모습이다."),
    ],
    "⚖️ 처세·세상살이": [
        ("선배", "회사 생활은 인간관계가 9할이야."),
        ("후배", "이청득심이라고 — 잘 들어주면 마음을 얻는다 하셨죠."),
        ("선배", "맞아. 그리고 역지사지로 상대 입장도 봐야 해."),
        ("후배", "꼰대처럼 굴면 안 되겠죠?"),
        ("선배", "겸손해야 사람이 따라온다. 그게 처세의 기본이야."),
    ],
}

COMPARE = {
    "🌅 인생·운명": [
        ("새옹지마 / 전화위복", "fortune unpredictable / misfortune→blessing"),
        ("호사다마 ↔ 만사형통", "good things have obstacles ↔ all goes well"),
        ("일장춘몽 / 인생무상", "fleeting glory / impermanence"),
        ("인과응보 / 자업자득 / 사필귀정", "karma / reap what you sow / truth prevails"),
    ],
    "💪 노력·성취": [
        ("고진감래 / 우공이산", "sweet fruit after labor / persistence moves mountains"),
        ("각골난망 / 백절불굴", "never forget kindness / never give up"),
        ("절차탁마 / 형설지공", "polish like a gem / study by snow & firefly light"),
    ],
    "🤝 우정·관계": [
        ("관포지교 / 죽마고우", "true friendship / childhood friend"),
        ("이심전심 / 동상이몽", "minds meet / same bed different dreams"),
        ("막역지우 / 백아절현", "intimate friend / cut strings (mourning friend)"),
    ],
    "🧠 지혜·판단": [
        ("지피지기 백전불태", "know self & enemy = 100 wins"),
        ("심사숙고 ↔ 경거망동", "deep deliberation ↔ rash action"),
        ("타산지석 / 반면교사", "lessons from others' stones / negative role model"),
    ],
    "💼 비즈니스·전략": [
        ("일거양득 / 일석이조", "two gains in one (synonyms)"),
        ("선견지명 / 미연방지", "foresight / prevent before it happens"),
        ("진검승부 / 배수진", "real swordfight / no retreat strategy"),
    ],
    "🧘 수양·자기관리": [
        ("수신제가 치국평천하", "self → family → nation → world"),
        ("유비무환 / 거안사위", "prepared = no danger / think of danger in peace"),
        ("초심 / 초지일관", "original mind / consistent purpose"),
    ],
    "⚖️ 처세·세상살이": [
        ("이청득심 / 역지사지", "listen to win heart / put yourself in others' shoes"),
        ("겸손 / 군자삼간", "humility / a gentleman is cautious in 3 things"),
        ("화이부동", "harmony without conformity"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

data = json.loads(SRC.read_text(encoding="utf-8"))
print(f"Loaded {len(data)} idioms")

def get_theme(cat):
    for theme_name, cats in THEMES:
        if cat in cats: return theme_name
    return "기타"

random.seed(42)
quizzes = []
for start in range(0, len(data), 20):
    chunk = data[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        item = chunk[s]
        ko = item["ko"]
        meaning = item["meaning"]
        # Show meaning, choose ko
        wrong_pool = [d["ko"] for d in data if d["ko"] != ko]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [ko]; random.shuffle(options)
        # Display meaning excerpt as question
        q_text = (meaning[:40] + "…") if len(meaning) > 40 else meaning
        qs.append((q_text, options, options.index(ko)))
    if qs:
        quizzes.append((start+1, min(start+20, len(data)), qs))

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
last_theme = None
quiz_idx = 0
for i, item in enumerate(data, 1):
    theme = get_theme(item["cat"])
    if theme != last_theme:
        items.append('</tbody></table>')
        items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="hanja-col">한자</th><th class="ko-col">한글</th><th>뜻 / 유래 / 활용</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme

    # Character breakdown
    chars_html = " ".join(
        f'<span class="char-cell"><span class="char-h">{escape(c["c"])}</span><span class="char-m">{escape(c["m"])}</span></span>'
        for c in item["chars"]
    )
    similar_html = ""
    if item.get("similar"):
        similar_html = f'<div class="sim-line"><span class="sim-label">유사:</span> {escape(" · ".join(item["similar"]))}</div>'
    rest = f'''
        <div class="meaning-line">{escape(item["meaning"])}</div>
        <div class="en-line">{escape(item["en"])}</div>
        <div class="chars-row">{chars_html}</div>
        <div class="origin-line"><span class="ol-label">유래:</span> {escape(item["origin"])}</div>
        <div class="modern-line"><span class="ml-label">활용:</span> {escape(item["modern"])}</div>
        {similar_html}
    '''
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(item['ko'] + ' (' + item['hanja'] + ')')}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td>'
        f'<td class="hanja">{escape(item["hanja"])}</td>'
        f'<td class="ko">{escape(item["ko"])}</td>'
        f'<td class="rest">{rest}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )

    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">다음 뜻에 해당하는 사자성어를 고르세요.</div>']
        for qi, (q, opts, _) in enumerate(qs, 1):
            opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
            qh.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-q">{escape(q)}</span><br>{opt_html}</div>')
        qh.append('</div></td></tr>')
        items.extend(qh)
items.append('</tbody></table>')

answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>사자성어 100선 · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 12mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.5; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:32px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:220px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:28px;} th.hanja-col{width:70px;} th.ko-col{width:75px;} th.qr-col{width:34px;}
  td { padding:8px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.hanja { font-family:'Noto Serif KR','SimSun',serif; font-weight:700; color:#C0392B; font-size:15px; line-height:1.3; text-align:center; }
  td.ko    { font-weight:800; color:#1a1a2e; font-size:13px; }
  td.rest .meaning-line { color:#1a1a2e; font-size:11px; font-weight:600; margin-bottom:3px; }
  td.rest .en-line { color:#1A4A8A; font-size:10.5px; font-style:italic; margin-bottom:6px; }
  td.rest .chars-row { display:flex; gap:6px; margin-bottom:5px; flex-wrap:wrap; }
  td.rest .char-cell { background:#fef3c7; padding:2px 6px; border-radius:4px; display:inline-flex; align-items:center; gap:4px; font-size:9.5px; }
  td.rest .char-h { font-family:'Noto Serif KR',serif; font-weight:800; color:#92400e; }
  td.rest .char-m { color:#78350f; font-size:9px; }
  td.rest .origin-line, td.rest .modern-line, td.rest .sim-line { font-size:9.5px; color:#666; margin-top:2px; line-height:1.5; }
  td.rest .ol-label, td.rest .ml-label, td.rest .sim-label { color:#888; font-weight:700; margin-right:3px; }
  td.rest .modern-line { background:#f0fdf4; padding:3px 5px; border-left:2px solid #059669; margin:3px 0; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:11px; padding:7px 12px; text-transform:uppercase; }
  tr.quiz-row td { padding:0; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:8px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-q { color:#1a1a2e; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; margin-top:4px; }
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>
<div class="cover">
  <div class="label">Korean Four-Character Idioms · Enhanced</div>
  <h1>사자성어 100선</h1>
  <div class="kr">Four-Character Wisdom · 향상판</div>
  <p class="desc">인생·노력·우정·지혜·비즈니스·수양·처세 7개 테마, 100개 사자성어 — 한자 글자 풀이·뜻·유래·현대 활용 예문·유사어·시나리오·비교·퀴즈·QR까지.</p>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=300)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  -> {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
