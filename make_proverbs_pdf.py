"""
Enhanced 한국 속담·격언 100선 PDF.
"""
import re, subprocess, time, io, base64, random, urllib.parse, json
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "proverbs100.json"
HTML_OUT = ROOT / "proverbs-100-enhanced.html"
PDF_OUT  = ROOT / "proverbs-100-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

THEMES = [
    ("🌅 인생·운명", ["인생"]),
    ("💪 노력·성취", ["노력"]),
    ("🤝 우정·관계", ["우정"]),
    ("🧠 지혜·판단", ["지혜"]),
    ("⚖️ 처세·세상살이", ["처세"]),
    ("⏰ 시간·기회", ["시간"]),
    ("💰 말과 돈", ["말돈"]),
]

SCENARIO = {
    "🌅 인생·운명": [
        ("선배", "사업이 풀리는가 싶더니 또 문제가 터졌어."),
        ("후배", "산 넘어 산이네요. 비 온 뒤에 땅이 굳는다고 하잖아요."),
        ("선배", "맞아. 끝이 좋으면 다 좋은 거지."),
        ("후배", "쥐구멍에도 볕들 날이 있다는 거 믿어야죠."),
        ("선배", "긍정적으로 가자!"),
    ],
    "💪 노력·성취": [
        ("코치", "포기하지 마. 천 리 길도 한 걸음부터야."),
        ("선수", "정말 힘들어요."),
        ("코치", "고생 끝에 낙이 온다잖아. 끝까지 가보자."),
        ("선수", "공든 탑이 무너지랴 — 그 말 명심할게요."),
        ("코치", "그래, 그 마음이면 된다."),
    ],
    "🤝 우정·관계": [
        ("친구1", "오랜만이지만 어제 본 것 같아."),
        ("친구2", "친구 따라 강남 간다더니, 너 때문에 여기까지 왔잖아."),
        ("친구1", "친구는 옛 친구가 좋고 옷은 새 옷이 좋대."),
        ("친구2", "맞아. 가는 정이 있어야 오는 정이 있지."),
        ("친구1", "오늘 술 한잔하자!"),
    ],
    "🧠 지혜·판단": [
        ("스승", "아는 길도 물어 가라고 했어."),
        ("제자", "신중하게 결정하라는 뜻이군요."),
        ("스승", "그래. 돌다리도 두들겨 보고 건너야지."),
        ("제자", "급할수록 돌아가라는 말도 같은 맥락이죠."),
        ("스승", "지혜는 신중함에서 나온다."),
    ],
    "⚖️ 처세·세상살이": [
        ("선배", "회사에선 가는 말이 고와야 오는 말이 곱다."),
        ("후배", "사람 대할 때 늘 명심할게요."),
        ("선배", "그리고 등잔 밑이 어둡다는 거 잊지 마."),
        ("후배", "가까운 사람을 더 챙겨야 한다는 뜻이군요."),
        ("선배", "맞아. 잘하면 다 잘된다."),
    ],
    "⏰ 시간·기회": [
        ("멘토", "기회는 한번 가면 안 와. 쇠뿔도 단김에 빼라."),
        ("멘티", "지금 결정하라는 거죠?"),
        ("멘토", "시간은 금이야. 그리고 호미로 막을 것을 가래로 막지 마."),
        ("멘티", "미루지 말라는 뜻이군요."),
        ("멘토", "그래. 늦었다고 생각할 때가 가장 빠른 때다."),
    ],
    "💰 말과 돈": [
        ("선배", "말 한마디로 천 냥 빚도 갚는다고 했다."),
        ("후배", "말의 힘이 크네요."),
        ("선배", "그리고 티끌 모아 태산이라잖아. 작은 돈도 무시하지 마."),
        ("후배", "꾸준히 저축하라는 거군요."),
        ("선배", "돈은 돌고 돈다. 너무 집착하지 말고."),
    ],
}

COMPARE = {
    "🌅 인생·운명": [
        ("산 넘어 산 / 갈수록 태산", "out of frying pan / from bad to worse"),
        ("쥐구멍에도 볕들 날 / 고생 끝에 낙", "every dog has its day / no pain no gain"),
        ("비 온 뒤에 땅이 굳어진다", "after rain, the ground hardens"),
        ("호랑이도 제 말 하면 온다", "speak of the devil"),
    ],
    "💪 노력·성취": [
        ("천 리 길도 한 걸음부터", "journey of 1,000 li starts with one step"),
        ("공든 탑이 무너지랴", "an honest tower won't fall"),
        ("고생 끝에 낙이 온다", "after hardship comes joy"),
        ("우물을 파도 한 우물을 파라", "dig one well deep"),
    ],
    "🤝 우정·관계": [
        ("친구 따라 강남 간다", "follow friend to Gangnam (peer influence)"),
        ("가는 정 오는 정", "what goes around comes around"),
        ("백지장도 맞들면 낫다", "two heads better than one"),
    ],
    "🧠 지혜·판단": [
        ("돌다리도 두들겨 보고 건너라", "tap stone bridge before crossing"),
        ("아는 길도 물어 가라", "ask even if you know the way"),
        ("급할수록 돌아가라", "in haste, take the longer way"),
        ("등잔 밑이 어둡다", "darkest under the lamp"),
    ],
    "⚖️ 처세·세상살이": [
        ("가는 말이 고와야 오는 말이 곱다", "kind words bring kind words"),
        ("호의가 계속되면 권리인 줄 안다", "kindness taken for granted"),
        ("말로 천 냥 빚 갚는다", "words can pay 1,000 nyang debt"),
    ],
    "⏰ 시간·기회": [
        ("쇠뿔도 단김에 빼라", "strike while iron is hot"),
        ("시간은 금이다", "time is money"),
        ("늦었다고 할 때가 가장 빠를 때", "best time is now"),
        ("호미로 막을 것을 가래로 막는다", "stitch in time saves nine"),
    ],
    "💰 말과 돈": [
        ("말 한마디로 천 냥 빚", "one word can pay great debt"),
        ("티끌 모아 태산", "dust gathered becomes mountain"),
        ("돈이 돈을 번다", "money makes money"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

data = json.loads(SRC.read_text(encoding="utf-8"))
print(f"Loaded {len(data)} proverbs")

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
        en = item["en"]
        wrong_pool = [d["en"] for d in data if d["en"] != en]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [en]; random.shuffle(options)
        qs.append((ko, options, options.index(en)))
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
        items.append('<table><thead><tr><th class="num-col">#</th><th class="ko-col">한국 속담</th><th class="en-col">English Equivalent</th><th>뜻 / 유래 / 활용</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme

    similar_html = ""
    if item.get("similar"):
        similar_html = f'<div class="sim-line"><span class="sim-label">유사:</span> {escape(" · ".join(item["similar"]))}</div>'
    rest = f'''
        <div class="literal-line"><span class="lit-label">직역:</span> {escape(item.get("literal", ""))}</div>
        <div class="meaning-line">{escape(item["meaning"])}</div>
        <div class="origin-line"><span class="ol-label">유래:</span> {escape(item["origin"])}</div>
        <div class="modern-line"><span class="ml-label">활용:</span> {escape(item["modern"])}</div>
        {similar_html}
    '''
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(item['ko'])}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td>'
        f'<td class="ko">{escape(item["ko"])}</td>'
        f'<td class="en">{escape(item["en"])}</td>'
        f'<td class="rest">{rest}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )

    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">다음 한국 속담에 해당하는 영어 표현을 고르세요.</div>']
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
<html lang="ko"><head><meta charset="UTF-8"><title>한국 속담 100선 · Enhanced</title>
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:240px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:28px;} th.ko-col{width:160px;} th.en-col{width:140px;} th.qr-col{width:34px;}
  td { padding:8px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.ko { font-weight:800; color:#C0392B; font-size:12px; line-height:1.4; }
  td.en { color:#1A4A8A; font-size:11px; font-weight:600; line-height:1.4; }
  td.rest .literal-line { font-size:9.5px; color:#666; font-style:italic; margin-bottom:3px; }
  td.rest .lit-label, td.rest .ol-label, td.rest .ml-label, td.rest .sim-label { color:#888; font-weight:700; margin-right:3px; }
  td.rest .meaning-line { color:#1a1a2e; font-size:11px; font-weight:600; margin-bottom:5px; }
  td.rest .origin-line, td.rest .sim-line { font-size:9.5px; color:#666; margin-top:2px; line-height:1.5; }
  td.rest .modern-line { font-size:10px; background:#f0fdf4; padding:4px 6px; border-left:2px solid #059669; margin:4px 0; color:#1a1a2e; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.quiz-row td { padding:0; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:8px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-q { color:#1a1a2e; font-weight:600; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; margin-top:4px; font-size:10px; }
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>
<div class="cover">
  <div class="label">Korean Proverbs & Sayings · Enhanced</div>
  <h1>한국 속담 100선</h1>
  <div class="kr">Korean Wisdom in 100 Proverbs · 향상판</div>
  <p class="desc">인생·노력·우정·지혜·처세·시간·말과 돈 7개 테마, 100개 속담 — 자연스러운 영어 대응 표현·직역·뜻·유래·현대 활용 예문·유사 속담 포함.</p>
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
