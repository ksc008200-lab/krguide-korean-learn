"""
Enhanced IT Terms 1,000 PDF — 컴퓨터·휴대폰 용어 사전.
"""
import re, subprocess, time, io, base64, random, urllib.parse, json
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "itterms1000.json"
HTML_OUT = ROOT / "it-terms-1000-enhanced.html"
PDF_OUT  = ROOT / "it-terms-1000-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 10 categories → 5 themes
THEMES = [
    ("💻 하드웨어·디스플레이", ["하드웨어", "디스플레이·주변기기"]),
    ("🖥️ 소프트웨어·OS·프로그래밍", ["소프트웨어·OS", "프로그래밍·개발"]),
    ("🌐 네트워크·모바일·인터넷", ["네트워크·인터넷", "모바일·스마트폰"]),
    ("🔐 보안·데이터·AI·클라우드", ["보안", "데이터·AI·클라우드"]),
    ("🎬 멀티미디어·신기술", ["멀티미디어", "신기술"]),
]

SCENARIO = {
    "💻 하드웨어·디스플레이": [
        ("후배", "CPU랑 GPU 차이가 정확히 뭐예요?"),
        ("선배", "CPU는 두뇌, 직렬 처리에 강해. GPU는 병렬 처리에 특화돼서 그래픽·AI 학습에 써."),
        ("후배", "RAM이 부족하면 SSD가 더 빨라도 의미 없나요?"),
        ("선배", "맞아. RAM은 작업 중인 데이터 저장소라 절대 부족하면 안 돼."),
        ("후배", "그럼 듀얼 모니터에 USB-C 모니터 연결도 잘 되겠죠?"),
    ],
    "🖥️ 소프트웨어·OS·프로그래밍": [
        ("팀장", "이번 프로젝트는 Python으로 가자."),
        ("개발자", "API는 REST로 할까요, GraphQL로 할까요?"),
        ("팀장", "REST가 더 직관적이고 캐싱도 쉬워. CI/CD는 GitHub Actions로."),
        ("개발자", "Docker로 컨테이너화하고요?"),
        ("팀장", "당연. Kubernetes는 다음 단계로 가자."),
    ],
    "🌐 네트워크·모바일·인터넷": [
        ("고객", "Wi-Fi가 자꾸 끊겨요."),
        ("기사", "라우터 위치도 중요하고, 2.4GHz와 5GHz 신호도 다릅니다."),
        ("고객", "VPN 켜놓으면 더 느려져요."),
        ("기사", "데이터가 한 번 더 경유하니까요. 필요할 때만 켜세요."),
        ("고객", "5G는 정말 빠른가요?"),
    ],
    "🔐 보안·데이터·AI·클라우드": [
        ("보안팀", "2단계 인증 꼭 설정하세요."),
        ("직원",   "비밀번호 매니저도 써야 하나요?"),
        ("보안팀", "네, 그리고 피싱 메일 조심하세요. AWS·GCP 키 노출도 큰 문제예요."),
        ("직원",   "AI 모델에 회사 자료 입력해도 되나요?"),
        ("보안팀", "민감 데이터는 절대 안 됩니다."),
    ],
    "🎬 멀티미디어·신기술": [
        ("크리에이터", "4K로 찍을까, 8K로 찍을까?"),
        ("편집자",     "용량이 크니까 4K HDR로 충분해요."),
        ("크리에이터", "AI 영상 편집 툴 어때?"),
        ("편집자",     "자막·노이즈 제거에 정말 강해요. VR·AR 콘텐츠도 늘고 있어요."),
        ("크리에이터", "메타버스 콘텐츠도 도전해보자!"),
    ],
}

COMPARE = {
    "💻 하드웨어·디스플레이": [
        ("CPU ↔ GPU", "directed processing ↔ parallel"),
        ("SSD ↔ HDD", "flash speed ↔ disk capacity"),
        ("RAM ↔ ROM", "volatile temp ↔ permanent read-only"),
        ("LCD / OLED / Mini-LED", "backlit ↔ self-emissive ↔ refined backlight"),
    ],
    "🖥️ 소프트웨어·OS·프로그래밍": [
        ("Windows / macOS / Linux", "MS / Apple / open-source"),
        ("Python / JavaScript / Java", "scripting / web / enterprise"),
        ("Frontend ↔ Backend / Full-stack", "user side ↔ server side / both"),
        ("Git / Docker / Kubernetes", "version control / container / orchestrator"),
    ],
    "🌐 네트워크·모바일·인터넷": [
        ("IPv4 ↔ IPv6", "old 32-bit ↔ new 128-bit address"),
        ("Wi-Fi 6 / 5G / LTE", "wireless LAN / mobile gen 5 / gen 4"),
        ("HTTP / HTTPS / WebSocket", "plain / secure / persistent connection"),
        ("DNS / CDN / VPN", "address book / global cache / encrypted tunnel"),
    ],
    "🔐 보안·데이터·AI·클라우드": [
        ("Encryption / Hashing / Signing", "scramble / fingerprint / verify"),
        ("Phishing / Malware / Ransomware", "deceive / harmful / hostage"),
        ("AWS / GCP / Azure", "Amazon / Google / Microsoft cloud"),
        ("AI / ML / Deep Learning / LLM", "broad → narrow → specific terms"),
    ],
    "🎬 멀티미디어·신기술": [
        ("VR / AR / MR / XR", "virtual / augmented / mixed / extended"),
        ("4K / 8K / HDR", "resolution & dynamic range"),
        ("Blockchain / NFT / Web3", "ledger / unique token / decentralized web"),
        ("IoT / Smart Home / Wearable", "things online / home auto / body device"),
    ],
}

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

data = json.loads(SRC.read_text(encoding="utf-8"))
print(f"Loaded {len(data)} IT terms")

def get_theme(cat):
    for theme_name, cats in THEMES:
        if cat in cats: return theme_name
    return "기타"

random.seed(42)
quizzes = []
for start in range(0, len(data), 25):
    chunk = data[start:start+25]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        item = chunk[s]
        term = item["term"]
        wrong_pool = [d["term"] for d in data if d["term"] != term]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [term]; random.shuffle(options)
        m = item["meaning"]
        q_text = (m[:50] + "…") if len(m) > 50 else m
        qs.append((q_text, options, options.index(term)))
    if qs:
        quizzes.append((start+1, min(start+25, len(data)), qs))

def cat_intro(theme):
    blocks = []
    if theme in SCENARIO:
        ls = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCENARIO[theme])
        blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>{ls}</div>')
    if theme in COMPARE:
        ps = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMPARE[theme])
        blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 비교 박스 · Comparison</div>{ps}</div>')
    return "".join(blocks)

# Group by theme + sub-category preserving source order
items = []
last_theme = None
last_sub = None
quiz_idx = 0
for i, item in enumerate(data, 1):
    theme = get_theme(item["cat"])
    if theme != last_theme:
        items.append('</tbody></table>')
        items.append('<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
        items.append(cat_intro(theme))
        items.append('<table><thead><tr><th class="num-col">#</th><th class="term-col">Term</th><th class="ko-col">한글</th><th>설명 · Meaning</th><th class="qr-col">🔊</th></tr></thead><tbody>')
        last_theme = theme; last_sub = None
    if item["cat"] != last_sub:
        items.append(f'<tr class="section"><td colspan="5">{escape(item["cat"])}</td></tr>')
        last_sub = item["cat"]
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(item['term'])}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr><td class="num">{i}</td>'
        f'<td class="term">{escape(item["term"])}</td>'
        f'<td class="ko">{escape(item["ko"])}</td>'
        f'<td class="meaning">{escape(item["meaning"])}</td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
    )
    if i % 25 == 0 and quiz_idx < len(quizzes):
        a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
        qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
              f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
              '<div class="q-sub">다음 설명에 해당하는 IT 용어를 고르세요.</div>']
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
<html lang="ko"><head><meta charset="UTF-8"><title>IT 용어 1,000 · Enhanced</title>
<style>
  @page { size: A4; margin: 14mm 12mm; } * { box-sizing: border-box; }
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
  th.num-col{width:30px;} th.term-col{width:100px;} th.ko-col{width:100px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.term { font-weight:800; color:#C0392B; font-size:12px; }
  td.ko { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.meaning { color:#333; font-size:10.5px; line-height:1.5; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:11px; padding:7px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
  tr.quiz-row td { padding:0; }
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
  <div class="label">IT Terms 1,000 · Enhanced</div>
  <h1>컴퓨터·휴대폰 핵심 용어 1,000</h1>
  <div class="kr">IT Vocabulary Dictionary · 향상판</div>
  <p class="desc">하드웨어·디스플레이·OS·프로그래밍·네트워크·모바일·보안·AI·클라우드·멀티미디어·신기술 10개 분야, 1,000개 IT 용어 — 영문 용어 + 한글 의미 + 1줄 설명 + 시나리오·비교·미니 퀴즈·QR 코드.</p>
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
