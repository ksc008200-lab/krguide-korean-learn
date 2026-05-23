"""
Enhanced 500-honorifics PDF — QR + scenarios + comparison + quizzes.
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "honorifics_500.txt"
HTML_OUT = ROOT / "500-honorifics-enhanced.html"
PDF_OUT  = ROOT / "500-honorifics-enhanced.pdf"

# Group categories (text-prefix match)
THEMES = [
    ("👋 일상 인사·기본 표현", ["일상적인 종결 어미", "높임 어휘"]),
    ("💼 비즈니스·격식", ["직장 및 비즈니스 매너", "주체 높임", "비즈니스 이메일", "격식 있는 발표", "상황별 공손한 의문문"]),
    ("🙏 사과·거절·완곡", ["정중한 사과와 양해", "부드럽고 정중한 거절", "거절 후의 대안", "일상 속 부드러운 완곡어법"]),
    ("🎉 행사·축하·칭찬", ["경조사 및 특별한 날", "품격 있는 칭찬과 인정", "칭찬을 받았을 때의 겸손한 반응"]),
    ("❤️ 감정·위로·배려", ["일상의 깊은 배려와 안부", "섬세한 감정 표현과 위로", "일상 속의 정중한 제안", "상대방을 극진히 높이는"]),
    ("🌸 마무리·고풍·예술적", ["품격 있는 마무리", "고풍스럽고 격조 있는", "갈등과 오해를 푸는", "예술적이고 감성적인", "경청과 공감", "깊은 감사와 영광", "대화의 흐름을 부드럽게"]),
]

SCENARIO = {
    "👋 일상 인사·기본 표현": [
        ("후배", "안녕하세요? 처음 뵙겠습니다."),
        ("선배", "반갑습니다. 잘 부탁드려요."),
        ("후배", "제가 도울 일이 있으면 말씀해 주세요."),
        ("선배", "감사합니다. 부탁드릴게요."),
        ("후배", "수고하셨습니다. 먼저 들어가 보겠습니다."),
    ],
    "💼 비즈니스·격식": [
        ("부장", "검토해 주십시오. 의견을 여쭙고 싶습니다."),
        ("직원", "확인 후 보고드리겠습니다."),
        ("부장", "회의 시간을 조정해 주실 수 있나요?"),
        ("직원", "네, 양해 부탁드립니다."),
        ("부장", "수고가 많으십니다."),
    ],
    "🙏 사과·거절·완곡": [
        ("동료1", "이번 일은 송구스럽습니다만 제가 도와드리기 어렵습니다."),
        ("동료2", "괜찮습니다. 충분히 이해합니다."),
        ("동료1", "다음 기회에 꼭 도와드리겠습니다."),
        ("동료2", "감사합니다. 마음만 받겠습니다."),
        ("동료1", "양해해 주셔서 감사드려요."),
    ],
    "🎉 행사·축하·칭찬": [
        ("친구1", "이번 승진 축하드려요!"),
        ("친구2", "감사합니다. 부족한 제게 과분한 칭찬이세요."),
        ("친구1", "정말 자랑스러워요."),
        ("친구2", "응원해 주신 덕분입니다."),
        ("친구1", "앞으로도 응원할게요."),
    ],
    "❤️ 감정·위로·배려": [
        ("선배", "요즘 많이 힘드시죠?"),
        ("후배", "네… 솔직히 마음이 많이 무거워요."),
        ("선배", "마음 잘 추스르세요. 제가 옆에 있어요."),
        ("후배", "감사합니다. 큰 힘이 됩니다."),
        ("선배", "언제든 편하게 말씀하세요."),
    ],
    "🌸 마무리·고풍·예술적": [
        ("동료A", "긴 여정 마치고 작별의 시간이 왔네요."),
        ("동료B", "그동안 마음 깊이 감사드렸습니다."),
        ("동료A", "당신과 함께한 시간이 큰 영광이었어요."),
        ("동료B", "그 마음 평생 간직하겠습니다."),
        ("동료A", "다시 만날 날을 기다리겠습니다."),
    ],
}

COMPARE = {
    "👋 일상 인사·기본 표현": [
        ("안녕히 가세요 ↔ 안녕히 계세요", "to one leaving ↔ to one staying"),
        ("진지 ↔ 밥", "honorific ↔ plain (meal)"),
        ("성함 ↔ 이름", "honorific ↔ plain (name)"),
        ("연세·춘추 ↔ 나이", "honorific ↔ plain (age)"),
        ("드시다·잡수시다 ↔ 먹다", "honorific ↔ plain (eat)"),
    ],
    "💼 비즈니스·격식": [
        ("주십시오 (격식) / 주세요 (보통)", "highest formal vs polite"),
        ("말씀드립니다 ↔ 말합니다", "honorific 'I say' ↔ plain"),
        ("부탁드립니다 / 부탁드려요 / 부탁해요", "formal → polite spectrum"),
    ],
    "🙏 사과·거절·완곡": [
        ("죄송합니다 ↔ 미안해요 ↔ 미안", "extreme formal ↔ polite ↔ casual"),
        ("어렵겠습니다 / 곤란합니다", "polite refusal: 'difficult'"),
        ("송구스럽습니다 (highest)", "deepest apology"),
    ],
    "🎉 행사·축하·칭찬": [
        ("축하드립니다 ↔ 축하해요 ↔ 축하해", "formal ↔ polite ↔ casual"),
        ("과찬이십니다 (humble)", "'you flatter me'"),
        ("부족한 제게 (humble)", "'unworthy me'"),
    ],
    "❤️ 감정·위로·배려": [
        ("힘내세요 / 마음 추스르세요", "cheer up / take care of your heart"),
        ("그 마음 잘 알아요", "I know how you feel"),
        ("언제든 말씀하세요", "feel free to talk anytime"),
    ],
    "🌸 마무리·고풍·예술적": [
        ("영광입니다 / 큰 영광", "honor / great honor"),
        ("진심으로 감사드립니다", "sincerely thank you"),
        ("다시 만날 날을", "until we meet again"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Parse honorifics from the English-paired section
text = SRC.read_text(encoding="utf-8")
start_match = re.search(r"^\s*1\.\s+일상적인 종결 어미\s+\(Daily Ending Phrases", text, re.M)
body = text[start_match.start():]

rows = []
current_sub = ""
sec_re = re.compile(r"^\s*(\d+)\.\s+(.+?)\s+\((.+?)\)\s*$")
for raw in body.splitlines():
    line = raw.strip()
    if not line: continue
    msec = sec_re.match(line)
    if msec:
        ko_name = msec.group(2).strip()
        current_sub = ko_name
        continue
    parts = [p.strip() for p in line.split(" / ") if p.strip()]
    if len(parts) < 2: continue
    ko_parts, en_parts = [], []
    for p in parts:
        if re.search(r"[가-힣]", p):
            (en_parts if en_parts else ko_parts).append(p)
        else:
            en_parts.append(p)
    if not ko_parts or not en_parts: continue
    rows.append((current_sub, " / ".join(ko_parts), " / ".join(en_parts)))

print(f"Parsed {len(rows)} entries")

# Map sub → theme
def get_theme(sub):
    for theme_name, prefixes in THEMES:
        for prefix in prefixes:
            if sub.startswith(prefix):
                return theme_name
    return "기타"

# Quizzes
random.seed(42)
quizzes = []
for start in range(0, len(rows), 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sub, ko, en = chunk[s]
        # Use first English meaning before " / " as the correct
        correct = en.split(" / ")[0]
        wrong_pool = [r[2].split(" / ")[0] for r in rows if r[2].split(" / ")[0] != correct]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [correct]; random.shuffle(options)
        correct_idx = options.index(correct)
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
for i, (sub, ko, en) in enumerate(rows, 1):
    theme = get_theme(sub)
    if theme != last_theme:
        items.append('</tbody></table>'); items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">한국어 표현</th><th>English Meaning</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sub = None
    if sub != last_sub:
        items.append(f'<tr class="section"><td colspan="4">{escape(sub)}</td></tr>')
        last_sub = sub
    # QR: use first Korean variant
    qr_text = ko.split(" / ")[0]
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(qr_text)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td><td class="k">{escape(ko)}</td><td class="en">{escape(en)}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="4"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">한국어 표현의 영어 뜻을 고르세요.</div>']
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
<html lang="ko"><head><meta charset="UTF-8"><title>500 Korean Honorifics · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 14mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.5; }
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
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:240px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:11.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:8px 8px; font-size:10.5px; border-bottom:2px solid #C0392B; }
  th.num-col{width:40px;} th.k-col{width:42%;} th.qr-col{width:38px;}
  td { padding:7px 9px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10.5px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:13px; line-height:1.5; }
  td.en  { color:#1A4A8A; font-size:11.5px; line-height:1.5; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; padding:9px 14px; text-transform:uppercase; }
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
  <div class="label">Korean Honorifics · Enhanced</div>
  <h1>500 Honorific Expressions</h1>
  <div class="kr">존댓말 표현 500개 · 향상판</div>
  <p class="desc">Korean honorific expression with English meaning by theme — plus scenarios, comparison boxes, mini quizzes, and pronunciation QR codes.</p>
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
