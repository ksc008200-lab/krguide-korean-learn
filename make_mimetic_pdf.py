"""
Enhanced mimetic 500 PDF — same style as internet/konglish enhanced.
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SRC = ROOT / "mimetic_500.txt"
HTML_OUT = ROOT / "mimetic-500-enhanced.html"
PDF_OUT  = ROOT / "mimetic-500-enhanced.pdf"
GUMROAD = "https://jssmn21.gumroad.com/l/gnefla"

THEMES = [
    ("🌧️ 자연·동물 소리", ["자연 소리", "동물 소리"]),
    ("👤 사람·감정·신체", ["사람 소리", "감정·표정", "신체·자세"]),
    ("⚙️ 사물·기계·움직임", ["사물·기계 소리", "움직임·속도"]),
    ("✨ 빛·음식·기타", ["빛·반짝임", "음식·맛", "양·정도·기타"]),
]

SCENARIO = {
    "🌧️ 자연·동물 소리": [
        ("아이",  "엄마! 밖에 비가 주룩주룩 와요!"),
        ("엄마",  "어머, 바람도 휘잉 부네."),
        ("아이",  "마당에서 강아지가 멍멍 짖어요."),
        ("엄마",  "옆집 고양이도 야옹 하네."),
        ("아이",  "참새들은 짹짹 노래해요!"),
    ],
    "👤 사람·감정·신체": [
        ("친구1", "왜 이렇게 두근두근해?"),
        ("친구2", "발표 때문에 가슴이 콩닥콩닥…"),
        ("친구1", "심호흡 한번 하자. 천천히."),
        ("친구2", "응. 다리도 후들후들 떨려."),
        ("친구1", "괜찮아, 너 잘할 거야! 빙긋 웃어봐."),
    ],
    "⚙️ 사물·기계·움직임": [
        ("선배", "기계가 덜컹덜컹 소리 나는데?"),
        ("후배", "방금 부품을 갈았는데, 아직 삐걱대요."),
        ("선배", "기름칠 한번 더 해봐. 슝슝 잘 돌아갈 거야."),
        ("후배", "네! 이제 부드럽게 돌아가요."),
        ("선배", "딸깍 잠그면 끝."),
    ],
    "✨ 빛·음식·기타": [
        ("친구1", "와! 별이 반짝반짝 빛나!"),
        ("친구2", "오늘 밤은 진짜 예쁘다."),
        ("친구1", "이 빵 바삭바삭 정말 맛있어."),
        ("친구2", "안은 쫄깃쫄깃하고."),
        ("친구1", "더 먹어볼래? 한입만!"),
    ],
}

COMPARE = {
    "🌧️ 자연·동물 소리": [
        ("주룩주룩 / 보슬보슬 / 부슬부슬", "heavy / light spring / fine drizzle"),
        ("쏴아 / 휘잉", "whoosh waves / wind howl"),
        ("멍멍 / 야옹 / 짹짹 / 음매", "woof / meow / tweet / moo"),
        ("꿀꿀 / 까악까악", "oink / caw caw"),
    ],
    "👤 사람·감정·신체": [
        ("두근두근 / 콩닥콩닥", "heart pounding (similar nuance)"),
        ("후들후들 / 부들부들", "trembling (cold/fear) / shaking"),
        ("빙긋 / 깔깔 / 키득키득", "smile / loud laugh / giggle"),
        ("훌쩍훌쩍 / 엉엉", "sniffling cry / loud sob"),
    ],
    "⚙️ 사물·기계·움직임": [
        ("덜컹덜컹 / 삐걱삐걱", "rattling / creaking"),
        ("슝슝 / 쌩쌩", "whoosh fast / zipping"),
        ("딸깍 / 똑딱", "click / tick-tock"),
        ("쿵쿵 / 콰당", "thud thud / crash"),
    ],
    "✨ 빛·음식·기타": [
        ("반짝반짝 / 번쩍번쩍", "twinkle / flash"),
        ("바삭바삭 / 쫄깃쫄깃", "crispy / chewy"),
        ("아삭아삭 / 사각사각", "crunchy fruit / crunchy snow"),
        ("주렁주렁 / 송이송이", "hanging in clusters / in bunches"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def parse_entries(text):
    lines = text.splitlines()
    sec_re = re.compile(r"^\s+([A-Z])\.\s+(.+?)\s+—\s+(.+?)\s+\((\d+)\s*items?\)\s*$")
    entry_re = re.compile(r"^#(\d+)\s+(.+?)\s*$")
    rows = []
    current_sec = ""
    cur_word = None; cur_fields = {}; cur_tip = ""; cur_order = []
    def flush():
        nonlocal cur_word, cur_fields, cur_tip, cur_order
        if cur_word is not None:
            rows.append((current_sec, cur_word, cur_fields.copy(), cur_tip, list(cur_order)))
        cur_word = None; cur_fields = {}; cur_tip = ""; cur_order = []
    for raw in lines:
        line = raw.rstrip()
        ms = sec_re.match(line)
        if ms:
            flush()
            current_sec = f"{ms.group(1)}. {ms.group(2)} · {ms.group(3)}"
            continue
        me = entry_re.match(line)
        if me:
            flush()
            cur_word = me.group(2).strip(); continue
        if cur_word is None: continue
        s = line.strip()
        if not s: continue
        if s.startswith("💡"):
            cur_tip = s.lstrip("💡").strip(); continue
        mf = re.match(r"^([^:]+?):\s*(.+)$", s)
        if mf:
            k, v = mf.group(1).strip(), mf.group(2).strip()
            cur_fields[k] = v; cur_order.append(k)
        else:
            if cur_order:
                last = cur_order[-1]
                cur_fields[last] = (cur_fields[last] + " " + s).strip()
    flush()
    return rows

text = SRC.read_text(encoding="utf-8")
rows = parse_entries(text)
print(f"Parsed {len(rows)} entries")

def get_theme(sec):
    for theme_name, prefixes in THEMES:
        for prefix in prefixes:
            if prefix in sec: return theme_name
    return "기타"

random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sec, word, fields, tip, order = chunk[s]
        correct = fields.get("English", "") or fields.get("뜻", "")
        if not correct: continue
        wrong_pool = [(r[2].get("English", "") or r[2].get("뜻", "")) for r in rows]
        wrong_pool = [w for w in wrong_pool if w and w != correct]
        if len(wrong_pool) < 3: continue
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [correct]; random.shuffle(options)
        qs.append((word, options, options.index(correct)))
    if qs:
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
last_theme = None; last_sec = None
quiz_idx = 0
for i, (sec, word, fields, tip, order) in enumerate(rows, 1):
    theme = get_theme(sec)
    if theme != last_theme:
        items.append('</tbody></table>'); items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">의성어·의태어</th><th class="en-col">English</th><th>뜻 / 예문 / 팁</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sec = None
    if sec != last_sec:
        items.append(f'<tr class="section"><td colspan="5">{escape(sec)}</td></tr>')
        last_sec = sec
    main_eng = fields.get("English", "")
    rest_lines = []
    for k in order:
        if k == "English": continue
        v = fields[k]
        rest_lines.append(f'<div class="r-line"><span class="r-label">{escape(k)}:</span> <span class="r-val">{escape(v)}</span></div>')
    if tip:
        rest_lines.append(f'<div class="r-tip">💡 {escape(tip)}</div>')
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(word)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td><td class="k">{escape(word)}</td>'
        f'<td class="en">{escape(main_eng)}</td>'
        f'<td class="rest">{"".join(rest_lines)}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">의성어·의태어의 영어 뜻을 고르세요.</div>']
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
<html lang="ko"><head><meta charset="UTF-8"><title>의성어·의태어 500 · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 12mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
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
  th.num-col{width:30px;} th.k-col{width:90px;} th.en-col{width:130px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#C0392B; font-size:13px; }
  td.en  { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.rest .r-line { font-size:10px; margin:1px 0; }
  td.rest .r-label { color:#888; font-weight:700; margin-right:3px; font-size:9.5px; }
  td.rest .r-val { color:#333; }
  td.rest .r-tip { font-size:9.5px; color:#666; font-style:italic; margin-top:3px; padding:2px 4px; background:#fefce8; border-left:2px solid #f59e0b; }
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
  <div class="label">Korean Onomatopoeia & Mimetic Words · Enhanced</div>
  <h1>의성어·의태어 500</h1>
  <div class="kr">한국어 소리·모양 흉내말 · 향상판</div>
  <p class="desc">자연·동물·사람·사물·움직임·빛·감정·음식 등 10개 분야 500개 — 한국어를 생생하게 만드는 소리와 모양 흉내말. 시나리오·비교·퀴즈·QR 포함.</p>
  <div class="features">
    <span class="feat">🎭 시나리오</span><span class="feat">🔍 비교</span><span class="feat">📝 퀴즈</span><span class="feat">🔊 QR</span>
  </div>
</div>
""" + "\n".join(items) + "\n".join(answer_html) + """
</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML → {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

if PDF_OUT.exists(): PDF_OUT.unlink()
url = f"file:///{HTML_OUT.as_posix()}"
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=300)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  -> {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
