"""
Enhanced 성경 100구절 PDF — Korean (개역개정) + English (ESV).
"""
import re, subprocess, time, io, base64, random, urllib.parse, json
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "bible100.json"
HTML_OUT = ROOT / "bible-100-enhanced.html"
PDF_OUT  = ROOT / "bible-100-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

THEMES = [
    ("🌅 창조와 타락 · Creation & Fall", ["창조와 타락"]),
    ("📜 역사와 지혜 · History & Wisdom", ["역사와 지혜"]),
    ("🔥 선지자 예언 · Prophets", ["선지자 예언"]),
    ("✝️ 복음 · The Gospel", ["복음"]),
    ("🕊️ 초대교회 · Early Church", ["초대 교회"]),
    ("✉️ 바울 서신 · Pauline Epistles", ["바울 서신"]),
    ("📖 공동 서신·계시록 · General Epistles & Revelation", ["공동 서신·계시록"]),
]

# 묵상 대화 (스승-제자, 부모-자녀, 성도-목사 등)
SCENARIO = {
    "🌅 창조와 타락 · Creation & Fall": [
        ("아이",   "선생님, 하나님은 누가 만드셨어요?"),
        ("선생님", "하나님은 만들어지지 않으셨어. 태초에 계신 분이지."),
        ("아이",   "그럼 우리는요?"),
        ("선생님", "우리는 하나님의 형상대로 지음을 받았어. 정말 귀한 존재지."),
        ("아이",   "와! 그래서 모든 사람이 소중한 거군요."),
    ],
    "📜 역사와 지혜 · History & Wisdom": [
        ("멘티", "두려운 일이 너무 많아요."),
        ("멘토", "강하고 담대하라. 여호와가 함께 하신다고 했지."),
        ("멘티", "지혜를 어떻게 얻을 수 있을까요?"),
        ("멘토", "여호와를 경외하는 것이 지혜의 근본이야."),
        ("멘티", "마음에 새기겠습니다."),
    ],
    "🔥 선지자 예언 · Prophets": [
        ("청년", "고난이 너무 길게 느껴져요."),
        ("선배", "이사야 40장 — '오직 여호와를 앙망하는 자는 새 힘을 얻으리니'"),
        ("청년", "독수리가 날개치며 올라가듯이…"),
        ("선배", "달려가도 곤비치 않으리라. 약속이야."),
        ("청년", "다시 일어설 힘이 생겨요."),
    ],
    "✝️ 복음 · The Gospel": [
        ("친구1", "요한복음 3장 16절 — '하나님이 세상을 이처럼 사랑하사…'"),
        ("친구2", "'독생자를 주셨으니…'"),
        ("친구1", "'멸망치 않고 영생을 얻게 하려 함이라.'"),
        ("친구2", "사랑이 모든 것의 시작이네."),
        ("친구1", "복음의 핵심이지."),
    ],
    "🕊️ 초대교회 · Early Church": [
        ("성도1", "사도행전 보면 초대교회가 정말 멋졌어."),
        ("성도2", "서로 사랑하고 모든 것을 함께 나눴잖아."),
        ("성도1", "성령 충만 — 그게 비결이었어."),
        ("성도2", "우리도 그런 공동체가 되면 좋겠다."),
        ("성도1", "기도부터 시작하자."),
    ],
    "✉️ 바울 서신 · Pauline Epistles": [
        ("목사", "로마서 8장이 가장 강한 위로의 장입니다."),
        ("성도", "'우리를 위하시면 누가 우리를 대적하리요'"),
        ("목사", "어떤 것도 하나님의 사랑에서 끊을 수 없다고 했어요."),
        ("성도", "환난도, 곤고도, 박해도…"),
        ("목사", "그 사랑 안에서 우리는 넉넉히 이깁니다."),
    ],
    "📖 공동 서신·계시록 · General Epistles & Revelation": [
        ("장로", "야고보서 — '시험을 당하거든 온전히 기쁘게 여기라'"),
        ("청년", "고난이 기쁨이 될 수 있나요?"),
        ("장로", "인내를 통해 온전케 되는 거지."),
        ("청년", "계시록은 어떤가요?"),
        ("장로", "보라 만물을 새롭게 하노라 — 마지막 약속이야."),
    ],
}

COMPARE = {
    "🌅 창조와 타락 · Creation & Fall": [
        ("창조 ↔ 타락", "Creation ↔ Fall"),
        ("하나님의 형상 / 죄", "Image of God / Sin"),
        ("아담과 하와 / 노아 / 아브라함", "Adam & Eve / Noah / Abraham"),
        ("율법 (출 20장)", "The Ten Commandments"),
    ],
    "📜 역사와 지혜 · History & Wisdom": [
        ("강하고 담대 / 두려움", "Be strong & courageous / fear"),
        ("여호와 경외 = 지혜의 근본", "Fear of the LORD = beginning of wisdom"),
        ("시편 / 잠언 / 전도서", "Psalms / Proverbs / Ecclesiastes"),
    ],
    "🔥 선지자 예언 · Prophets": [
        ("회개 / 회복", "Repentance / Restoration"),
        ("새 힘 / 새 마음", "New strength (Isa 40) / new heart (Eze 36)"),
        ("이사야 / 예레미야 / 에스겔", "Isaiah / Jeremiah / Ezekiel"),
    ],
    "✝️ 복음 · The Gospel": [
        ("요한복음 3:16 — 사랑의 핵심", "John 3:16 — core of the gospel"),
        ("죄 ↔ 구원", "Sin ↔ Salvation"),
        ("길·진리·생명 (요 14:6)", "Way, Truth, Life"),
    ],
    "🕊️ 초대교회 · Early Church": [
        ("성령 충만 / 사도 직분", "Spirit-filled / Apostolic ministry"),
        ("교회 ↔ 세상", "Church ↔ World"),
        ("나눔 / 기도 / 전도", "Fellowship / Prayer / Evangelism"),
    ],
    "✉️ 바울 서신 · Pauline Epistles": [
        ("이신칭의 (롬 3장)", "Justification by faith"),
        ("성령의 열매 (갈 5장)", "Fruit of the Spirit"),
        ("사랑장 (고전 13장)", "The love chapter"),
    ],
    "📖 공동 서신·계시록 · General Epistles & Revelation": [
        ("믿음의 행함 (약 2:17)", "Faith and works"),
        ("새 하늘 새 땅 (계 21장)", "New heavens & new earth"),
        ("어린 양의 혼인 잔치", "The wedding of the Lamb"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

data = json.loads(SRC.read_text(encoding="utf-8"))
print(f"Loaded {len(data)} bible verses")

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
        ref = item["ref"]
        ko = item["ko"]
        ko_snippet = (ko[:30] + "…") if len(ko) > 30 else ko
        wrong_pool = [d["ref"] for d in data if d["ref"] != ref]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [ref]; random.shuffle(options)
        qs.append((ko_snippet, options, options.index(ref)))
    if qs:
        quizzes.append((start+1, min(start+20, len(data)), qs))

def cat_intro(theme):
    blocks = []
    if theme in SCENARIO:
        ls = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCENARIO[theme])
        blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 묵상 대화 · Reflection Dialogue</div>{ls}</div>')
    if theme in COMPARE:
        ps = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMPARE[theme])
        blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 주제별 비교 · Key Themes</div>{ps}</div>')
    return "".join(blocks)

items = []
last_theme = None
quiz_idx = 0
for i, item in enumerate(data, 1):
    theme = get_theme(item["cat"])
    if theme != last_theme:
        items.append('</div>')
        items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<div class="verse-list">')
        last_theme = theme

    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(item['ko'])}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<div class="verse-card">'
        f'<div class="vc-header">'
        f'<span class="vc-num">{i}</span>'
        f'<span class="vc-ref">{escape(item["ref"])}</span>'
        f'<span class="vc-ref-en">{escape(item["ref_en"])}</span>'
        f'<img class="vc-qr" src="{qr_data}" alt="QR"/>'
        f'</div>'
        f'<div class="vc-ko">{escape(item["ko"])}</div>'
        f'<div class="vc-en">{escape(item["en"])}</div>'
        f'<div class="vc-note">💡 {escape(item.get("note",""))}</div>'
        f'</div>'
    )
    if i % 20 == 0 and quiz_idx < len(quizzes):
        items.append('</div>')
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">다음 본문의 출처(성구)를 고르세요.</div>']
        for qi, (q, opts, _) in enumerate(qs, 1):
            opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
            qh.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-q">"{escape(q)}"</span><br>{opt_html}</div>')
        qh.append('</div>')
        items.extend(qh)
        items.append('<div class="verse-list">')
items.append('</div>')

answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>성경 100구절 · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 14mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.55; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:620px; margin:0 auto; line-height:1.7; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }
  h2.cat-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:14px 22px; margin:0 0 14px; font-size:17px; border-left:6px solid #C0392B; }
  .scenario-box { background:#fff8f0; border-left:4px solid #f97316; padding:14px 18px; margin-bottom:14px; border-radius:6px; }
  .scenario-box .sb-title { font-weight:800; color:#9a3412; font-size:13px; margin-bottom:8px; }
  .scenario-box .dl-line { font-size:12px; margin:3px 0; }
  .scenario-box .dl-speaker { color:#C0392B; font-weight:700; margin-right:6px; }
  .compare-box { background:#f0f5ff; border-left:4px solid #1A4A8A; padding:14px 18px; margin-bottom:16px; border-radius:6px; }
  .compare-box .cb-title { font-weight:800; color:#1e3a8a; font-size:13px; margin-bottom:8px; }
  .compare-box .cb-pair { font-size:12px; margin:3px 0; display:flex; gap:12px; }
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:260px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  .verse-list { display:flex; flex-direction:column; gap:10px; margin-bottom:14px; }
  .verse-card { background:#fff; border-left:4px solid #C0392B; border-radius:6px; padding:12px 16px; position:relative; }
  .verse-card .vc-header { display:flex; align-items:center; gap:10px; margin-bottom:6px; font-size:11px; }
  .verse-card .vc-num { background:#1a1a2e; color:#fff; padding:2px 8px; border-radius:10px; font-weight:700; font-size:10.5px; }
  .verse-card .vc-ref { color:#C0392B; font-weight:800; font-size:12px; }
  .verse-card .vc-ref-en { color:#888; font-style:italic; font-size:10.5px; }
  .verse-card .vc-qr { width:24px; height:24px; margin-left:auto; opacity:0.7; }
  .verse-card .vc-ko { color:#1a1a2e; font-size:12px; line-height:1.65; margin-bottom:6px; font-weight:500; }
  .verse-card .vc-en { color:#1A4A8A; font-size:11px; line-height:1.55; font-style:italic; margin-bottom:6px; }
  .verse-card .vc-note { font-size:10px; color:#666; padding:4px 8px; background:#fef3c7; border-radius:4px; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:8px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-q { color:#1a1a2e; font-style:italic; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; margin-top:4px; }
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>
<div class="cover">
  <div class="label">Bible · 100 Key Verses · Enhanced</div>
  <h1>성경 핵심 100구절</h1>
  <div class="kr">한국어(개역개정) + ESV 영어 매칭 · 향상판</div>
  <p class="desc">창조와 타락 → 역사와 지혜 → 선지자 예언 → 복음 → 초대교회 → 바울 서신 → 공동 서신·계시록까지 — 성경 흐름을 따라가는 100구절. 한국어·영어 본문, 출처, 묵상 노트, 묵상 대화, 주제 비교, 미니 퀴즈, 발음 QR.</p>
  <div class="features">
    <span class="feat">🎭 묵상 대화</span><span class="feat">🔍 주제 비교</span><span class="feat">📝 퀴즈</span><span class="feat">🔊 QR</span>
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
