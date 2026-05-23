"""
Enhanced 200-adverbs PDF — QR + scenarios + comparison + quizzes.
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import unescape, escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "200-adverbs-enhanced.html"
PDF_OUT  = ROOT / "200-adverbs-enhanced.pdf"

# Comparison pairs per top category (시간, 정도, 상태·방식, 부정·의문, 문장 연결, 추측·양태, 의성·의태어)
COMPARE = {
    "1. 시간 부사": [
        ("일찍 ↔ 늦게", "early ↔ late"),
        ("아까 ↔ 이따가", "a while ago ↔ a little later"),
        ("이미 / 벌써 ↔ 아직", "already ↔ yet/still"),
        ("자주 ↔ 가끔", "often ↔ sometimes"),
        ("어제 / 오늘 / 내일", "yesterday / today / tomorrow"),
    ],
    "2. 정도 부사": [
        ("아주 / 매우 / 정말", "very / really (synonyms)"),
        ("조금 ↔ 많이", "a little ↔ a lot"),
        ("훨씬 ↔ 약간", "much more ↔ slightly"),
        ("거의 ↔ 전혀", "almost ↔ not at all"),
    ],
    "3. 상태·방식 부사": [
        ("빨리 ↔ 천천히", "quickly ↔ slowly"),
        ("같이 / 함께 ↔ 따로", "together ↔ separately"),
        ("잘 ↔ 못", "well ↔ poorly"),
        ("정확하게 ↔ 대충", "accurately ↔ roughly"),
    ],
    "4. 부정·의문 부사": [
        ("안 / 못 ↔ 잘", "not ↔ well"),
        ("왜 / 어떻게 / 언제 / 어디", "why / how / when / where"),
    ],
    "5. 문장 연결 부사": [
        ("그래서 ↔ 그러나", "so ↔ but"),
        ("그리고 ↔ 하지만", "and ↔ however"),
        ("따라서 ↔ 그럼에도", "therefore ↔ nevertheless"),
    ],
    "6. 추측·양태 부사": [
        ("아마 ↔ 절대", "perhaps ↔ never/absolutely"),
        ("물론 ↔ 설마", "of course ↔ surely not"),
    ],
    "7. 의성·의태어": [
        ("두근두근 (heart pounding)", "심장이 빠르게 뛰는 모양"),
        ("쿵쿵 (thud thud)", "무거운 발소리"),
        ("졸졸 (trickling)", "물이 흐르는 소리"),
        ("반짝반짝 (sparkling)", "빛이 빛나는 모양"),
    ],
}

# Scenario dialogues per top category
SCENARIO = {
    "1. 시간 부사": [
        ("민수", "오늘 일찍 일어났어요?"),
        ("지영", "아니요, 늦게 일어났어요. 어제 늦게 잤거든요."),
        ("민수", "이따가 점심 같이 먹을래요?"),
        ("지영", "좋아요. 자주 가는 식당으로 가요."),
        ("민수", "내일도 만나요!"),
    ],
    "2. 정도 부사": [
        ("선생님", "이 책 정말 재미있어요?"),
        ("학생",   "아주 재미있어요! 추천해요."),
        ("선생님", "조금 어려운가요?"),
        ("학생",   "거의 안 어려워요. 가볍게 읽을 수 있어요."),
        ("선생님", "그럼 저도 한번 봐야겠네요."),
    ],
    "3. 상태·방식 부사": [
        ("코치", "조심해서 천천히 뛰어요."),
        ("선수", "네, 정확하게 자세를 잡을게요."),
        ("코치", "혼자 말고 같이 연습해요."),
        ("선수", "잘 따라가겠습니다."),
        ("코치", "끝까지 열심히 합시다!"),
    ],
    "4. 부정·의문 부사": [
        ("친구1", "왜 늦었어?"),
        ("친구2", "차가 안 와서… 미안해."),
        ("친구1", "어디 갔다 왔어?"),
        ("친구2", "도서관에. 어떻게 알았어?"),
        ("친구1", "그냥 짐작했지!"),
    ],
    "5. 문장 연결 부사": [
        ("발표자", "오늘은 한국어를 배웁니다."),
        ("청중",   "그래서요?"),
        ("발표자", "한국어는 재미있어요. 그리고 매우 유용해요."),
        ("청중",   "하지만 어렵지 않을까요?"),
        ("발표자", "그러나 매일 연습하면 누구나 잘할 수 있어요."),
    ],
    "6. 추측·양태 부사": [
        ("동료1", "내일 비 오려나?"),
        ("동료2", "아마 올 것 같아요."),
        ("동료1", "설마 우산 안 가져왔어요?"),
        ("동료2", "물론 가져왔죠! 절대 안 잊어버려요."),
        ("동료1", "그럼 다행이네요."),
    ],
    "7. 의성·의태어": [
        ("아이",   "엄마, 심장이 두근두근해요!"),
        ("엄마",   "왜? 무슨 일 있어?"),
        ("아이",   "오늘 발표가 있어요. 다리가 후들후들해요."),
        ("엄마",   "심호흡해. 천천히 졸졸 흐르는 물 생각해."),
        ("아이",   "네, 마음이 차분해졌어요."),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch40">.*?(?=<div class="chapter" id="ch41")', html, re.S)
if not m:
    m = re.search(r'<div class="chapter" id="ch40">.*?(?=<!--|<script|<footer|</body>)', html, re.S)
block = m.group(0)
def clean(s):
    s = re.sub(r"<em>", "**", s); s = re.sub(r"</em>", "**", s)
    s = re.sub(r"<[^>]+>", "", s); return unescape(s).strip()

rows = []
current_sub = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="4"' in row:
        txt = clean(row)
        if txt and not txt.startswith("부사"):
            current_sub = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 4: continue
    adv, pron, eng, ex = [clean(c) for c in cells]
    if adv == "부사": continue
    rows.append((current_sub, adv, pron, eng, ex))

# Auto-assign top categories by source order (35/30/40/15/20/20/40 = 200, but we have 197)
def top_cat(i):
    if i <= 35: return "1. 시간 부사"
    if i <= 65: return "2. 정도 부사"
    if i <= 105: return "3. 상태·방식 부사"
    if i <= 120: return "4. 부정·의문 부사"
    if i <= 140: return "5. 문장 연결 부사"
    if i <= 160: return "6. 추측·양태 부사"
    return "7. 의성·의태어"

# Build quizzes (every 20)
random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sub, adv, pron, eng, ex = chunk[s]
        wrong_pool = [r[3] for r in rows if r[3] != eng]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [eng]; random.shuffle(options)
        correct_idx = options.index(eng)
        qs.append((adv, options, correct_idx))
    quizzes.append((start+1, min(start+20, len(rows)), qs))

def cat_intro(cat):
    blocks = []
    if cat in SCENARIO:
        lines = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCENARIO[cat])
        blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>{lines}</div>')
    if cat in COMPARE:
        pairs = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMPARE[cat])
        blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 비교 박스 · Comparison</div>{pairs}</div>')
    return "".join(blocks)

items = []
last_cat = None
last_sub = None
quiz_idx = 0
for i, (sub, adv, pron, eng, ex) in enumerate(rows, 1):
    tc = top_cat(i)
    if tc != last_cat:
        items.append('</tbody></table>')
        items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">🌟 {escape(tc)}</h2>')
        items.append(cat_intro(tc))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">부사</th><th class="r-col">발음</th><th class="en-col">English</th><th>예문 Example</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_cat = tc; last_sub = None
    if sub != last_sub:
        items.append(f'<tr class="section"><td colspan="6">{escape(sub)}</td></tr>')
        last_sub = sub

    # Parse Korean ex / English from "ko — en"
    ex_html = escape(ex).replace("**", "<em>")
    parts = ex_html.split("<em>")
    rebuilt = parts[0]
    for j, p in enumerate(parts[1:], 1):
        rebuilt += ("<em>" if j % 2 == 1 else "</em>") + p
    sep = None
    for s in [" — ", " – ", " - "]:
        if s in rebuilt:
            ex_ko, ex_en = rebuilt.split(s, 1); sep = s; break
    if sep is None:
        ex_ko, ex_en = rebuilt, ""

    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(adv)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(adv)}</td>'
        f'<td class="r">{escape(pron)}</td>'
        f'<td class="en">{escape(eng)}</td>'
        f'<td class="ex"><span class="ex-ko">{ex_ko.strip()}</span><span class="ex-en">{ex_en.strip()}</span></td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td>'
        f'</tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qhtml = [f'<tr class="quiz-row"><td colspan="6"><div class="quiz">',
                 f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
                 '<div class="q-sub">부사의 영어 뜻을 고르세요. · Choose the English meaning.</div>']
        for qi, (word, opts, _) in enumerate(qs, 1):
            opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
            qhtml.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-word">{escape(word)}</span> = ? {opt_html}</div>')
        qhtml.append('</div></td></tr>')
        items.extend(qhtml)

items.append('</tbody></table>')

answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>200 Korean Adverbs · Enhanced</title>
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:200px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:28px;} th.k-col{width:75px;} th.r-col{width:65px;} th.en-col{width:120px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:13px; }
  td.r   { color:#6b6b6b; font-style:italic; font-size:10.5px; }
  td.en  { color:#1A4A8A; font-size:11px; }
  td.ex .ex-ko { display:block; color:#C0392B; font-weight:600; font-size:10.5px; }
  td.ex .ex-en { display:block; color:#666; font-style:italic; font-size:10px; margin-top:1px; }
  td.ex em { font-style:normal; background:#fef3c7; color:#92400e; padding:0 3px; border-radius:3px; font-weight:700; }
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
  <div class="label">Korean Essential Adverbs · Enhanced</div>
  <h1>200 Essential Korean Adverbs</h1>
  <div class="kr">필수 부사 200개 · 향상판</div>
  <p class="desc">By category — adverb · romanization · English meaning · example sentence — plus scenario dialogues, comparison boxes, mini quizzes, and pronunciation QR codes.</p>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=240)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
