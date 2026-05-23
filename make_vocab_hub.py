"""
Build the full freemium structure:
  - vocab-hub.html            : Card grid landing page
  - preview-{key}.html (×8)   : Free 7% preview of each resource
  - full-{key}.html (×8)      : Full content, paywall-locked
  - Add a button in learn-korean.html linking to vocab-hub

Each card → preview page → full page (after license unlock).
Google Translate widget on all pages.
"""
import re, subprocess, time, io, base64, urllib.parse
from pathlib import Path
from html import escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
GUMROAD = "https://jssmn21.gumroad.com/l/gnefla"

# Resource definitions
RESOURCES = [
    {
        "key": "verbs",
        "emoji": "🏃",
        "title": "200 Essential Korean Verbs",
        "kr_title": "필수 동사 200개",
        "desc": "한국어로 행동을 표현하는 핵심 동사 200개 — 발음, 해요체, 과거형, 예문, QR 코드까지.",
        "count": "200 verbs",
        "color": "#C0392B",
        "source_html": "200-verbs-enhanced.html",
        "source_pdf": "200-verbs-enhanced.pdf",
        "preview_pct": 0.10,  # 10%
    },
    {
        "key": "adverbs",
        "emoji": "📊",
        "title": "200 Essential Korean Adverbs",
        "kr_title": "필수 부사 200개",
        "desc": "시간·정도·방식·의성·의태어까지 200개 부사 — 자연스러운 한국어 표현의 비밀.",
        "count": "200 adverbs",
        "color": "#1A4A8A",
        "source_html": "200-adverbs-enhanced.html",
        "source_pdf": "200-adverbs-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "nouns",
        "emoji": "📦",
        "title": "Essential Korean Nouns",
        "kr_title": "필수 명사 369개",
        "desc": "가족·신체·음식·시간·장소·사물 등 7개 테마, 369개 명사를 예문과 함께.",
        "count": "369 nouns",
        "color": "#0F766E",
        "source_html": "essential-nouns-enhanced.html",
        "source_pdf": "essential-nouns-enhanced.pdf",
        "preview_pct": 0.08,
    },
    {
        "key": "honorifics",
        "emoji": "🙇",
        "title": "500 Honorific Expressions",
        "kr_title": "존댓말 표현 500개",
        "desc": "일상 인사부터 비즈니스 격식, 고풍스러운 문어체까지 — 한국식 존경 표현 500개.",
        "count": "500 expressions",
        "color": "#7C3AED",
        "source_html": "500-honorifics-enhanced.html",
        "source_pdf": "500-honorifics-enhanced.pdf",
        "preview_pct": 0.06,
    },
    {
        "key": "japanese",
        "emoji": "🏯",
        "title": "Japanese Loanwords in Korean",
        "kr_title": "일본어 외래어 391개",
        "desc": "한국어 속 일본어 표현과 그 우리말 순화어 — 건설·낚시·자동차 등 16개 분야.",
        "count": "391 loanwords",
        "color": "#B91C1C",
        "source_html": "japanese-loanwords-enhanced.html",
        "source_pdf": "japanese-loanwords-enhanced.pdf",
        "preview_pct": 0.08,
    },
    {
        "key": "adjadv",
        "emoji": "🎨",
        "title": "Adjectives · Adverbs · Idioms",
        "kr_title": "형용사·부사·관용구 1067개",
        "desc": "관형사·고급 형용사·관용구·속담·사자성어·의성/의태어 등 1067개 — 가장 풍부한 표현 모음.",
        "count": "1,067 entries",
        "color": "#9A3412",
        "source_html": "adjectives-adverbs-enhanced.html",
        "source_pdf": "adjectives-adverbs-enhanced.pdf",
        "preview_pct": 0.05,
    },
    {
        "key": "internet",
        "emoji": "💬",
        "title": "Korean Internet & Chat Expressions",
        "kr_title": "인터넷·채팅 한국어 500개",
        "desc": "ㅋㅋㅋ부터 K-pop 팬덤, 게임, MZ 신조어까지 — 한국 인터넷 문화의 모든 것.",
        "count": "500 expressions",
        "color": "#2563EB",
        "source_html": "internet-500-enhanced.html",
        "source_pdf": "internet-500-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "konglish",
        "emoji": "🌐",
        "title": "Konglish: Korean-English Expressions",
        "kr_title": "콩글리시 500개",
        "desc": "한국에서만 통하는 영어식 표현과 진짜 영어 — 잘못된 영어 vs 올바른 영어 비교.",
        "count": "500 expressions",
        "color": "#059669",
        "source_html": "konglish-500-enhanced.html",
        "source_pdf": "konglish-500-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "mimetic",
        "emoji": "🌧️",
        "title": "Onomatopoeia & Mimetic Words",
        "kr_title": "의성어·의태어 500개",
        "desc": "주룩주룩·반짝반짝·두근두근 — 한국어를 생생하게 만드는 소리와 모양 흉내말 500개.",
        "count": "500 expressions",
        "color": "#D97706",
        "source_html": "mimetic-500-enhanced.html",
        "source_pdf": "mimetic-500-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "idioms",
        "emoji": "📜",
        "title": "Four-Character Idioms (사자성어)",
        "kr_title": "사자성어 100선",
        "desc": "새옹지마·고진감래·관포지교 — 인생·노력·우정·지혜·비즈니스·수양·처세 7개 테마의 사자성어 100선. 한자 풀이·유래·현대 활용 예문 포함.",
        "count": "100 idioms",
        "color": "#831843",
        "source_html": "idioms-100-enhanced.html",
        "source_pdf": "idioms-100-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "proverbs",
        "emoji": "🗣️",
        "title": "Korean Proverbs & Sayings",
        "kr_title": "한국 속담 100선",
        "desc": "호랑이도 제 말 하면 온다·티끌 모아 태산 — 한국 전통 속담 100선 + 영어 대응 표현·직역·유래·현대 활용 예문 포함.",
        "count": "100 proverbs",
        "color": "#854D0E",
        "source_html": "proverbs-100-enhanced.html",
        "source_pdf": "proverbs-100-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "visual",
        "emoji": "🎴",
        "title": "Visual Vocabulary 1,100",
        "kr_title": "시각 어휘 1,100개",
        "desc": "과일·채소·동물·곤충·꽃·신체·의복·악기·운동·공구·장소·교통수단·색깔·모양 등 22개 카테고리, 1,100개 한국어 단어를 카드 그리드로 학습.",
        "count": "1,100 words",
        "color": "#0E7490",
        "source_html": "visual-vocab-1100-enhanced.html",
        "source_pdf": "visual-vocab-1100-enhanced.pdf",
        "preview_pct": 0.05,
    },
    {
        "key": "bible",
        "emoji": "📖",
        "title": "Bible · 100 Key Verses",
        "kr_title": "성경 핵심 100구절",
        "desc": "창조부터 계시록까지 — 한국어(개역개정) + ESV 영어 매칭 100구절. 출처·묵상 노트·묵상 대화·주제 비교·미니 퀴즈 포함.",
        "count": "100 verses",
        "color": "#7C2D12",
        "source_html": "bible-100-enhanced.html",
        "source_pdf": "bible-100-enhanced.pdf",
        "preview_pct": 0.10,
    },
    {
        "key": "itterms",
        "emoji": "💻",
        "title": "IT Terms 1,000",
        "kr_title": "컴퓨터·휴대폰 용어 1,000",
        "desc": "하드웨어·OS·프로그래밍·네트워크·보안·AI·클라우드·멀티미디어 등 10개 분야, 1,000개 IT 용어. 영문 + 한글 + 1줄 설명.",
        "count": "1,000 terms",
        "color": "#374151",
        "source_html": "it-terms-1000-enhanced.html",
        "source_pdf": "it-terms-1000-enhanced.pdf",
        "preview_pct": 0.05,
    },
    {
        "key": "hangulhanja",
        "emoji": "🇰🇷",
        "title": "Hangul vs Hanja — Bilingual Reference",
        "kr_title": "한글 vs 한자 (한·영 병기)",
        "desc": "세종대왕이 창제한 한글의 5가지 언어 문화적 특징과, 동아시아 한자와의 본질적 차이 5가지를 한국어·영어로 정리.",
        "count": "5 features + 5 comparisons",
        "color": "#9333EA",
        "source_html": "hangul-vs-hanja-enhanced.html",
        "source_pdf": "hangul-vs-hanja-enhanced.pdf",
        "preview_pct": 0.20,
    },
]

# ─── Common HTML pieces ─────────────────────────────────────────
GOOGLE_TRANSLATE = """
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'ko', includedLanguages: 'en,ja,zh-CN,zh-TW,es,fr,de,vi,th,id,ar,ru,pt'}, 'google_translate_element');
}
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

PAYWALL_JS = f"""
<script>
(function() {{
  const STORAGE_KEY = 'krguide_license_v1';
  const GUMROAD_LINK = '{GUMROAD}';

  function isUnlocked() {{
    try {{
      const d = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return d && d.valid === true;
    }} catch(e) {{ return false; }}
  }}

  function markUnlocked(key) {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{valid:true,key:key,ts:Date.now()}}));
  }}

  window.unlockWithKey = function() {{
    const input = document.getElementById('license-key-input');
    const msg = document.getElementById('license-msg');
    const btn = document.querySelector('#license-modal .lm-btn.primary');
    const key = (input.value || '').trim();
    if (!key) {{ msg.textContent = '라이선스 키를 입력하세요.'; msg.className = 'license-msg err'; return; }}
    if (btn) {{ btn.disabled = true; btn.textContent = '검증 중…'; }}
    msg.textContent = '';
    fetch('https://auth.krguide.com/api/license-verify', {{
      method:'POST', headers:{{'Content-Type':'application/json'}},
      body: JSON.stringify({{license_key: key}})
    }}).then(r => r.json()).then(data => {{
      if (data && data.success) {{
        markUnlocked(key);
        msg.textContent = '✅ 잠금 해제 완료! 새로고침합니다…';
        msg.className = 'license-msg ok';
        setTimeout(() => location.reload(), 800);
      }} else {{
        msg.textContent = data.error || '유효하지 않은 라이선스 키입니다.';
        msg.className = 'license-msg err';
        if (btn) {{ btn.disabled = false; btn.textContent = '잠금 해제'; }}
      }}
    }}).catch(err => {{
      msg.textContent = '서버 연결 실패. 잠시 후 다시 시도해 주세요.';
      msg.className = 'license-msg err';
      if (btn) {{ btn.disabled = false; btn.textContent = '잠금 해제'; }}
    }});
  }};

  window.showLicenseModal = function() {{
    document.getElementById('license-modal').style.display = 'flex';
    document.getElementById('license-key-input').focus();
  }};
  window.closeLicenseModal = function() {{
    document.getElementById('license-modal').style.display = 'none';
  }};

  // Apply lock on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function() {{
    if (isUnlocked()) {{
      document.body.classList.add('unlocked');
    }} else {{
      document.body.classList.add('locked');
    }}
  }});
}})();
</script>
"""

LICENSE_MODAL = f"""
<div id="license-modal" style="display:none">
  <div class="lm-box">
    <h3>🔓 라이선스 키 입력</h3>
    <p>Gumroad에서 구매 후 이메일로 받은 라이선스 키를 입력하세요.</p>
    <input id="license-key-input" type="text" placeholder="XXXX-XXXX-XXXX-XXXX" maxlength="40" autocomplete="off">
    <div class="license-msg" id="license-msg"></div>
    <button class="lm-btn primary" onclick="unlockWithKey()">잠금 해제</button>
    <button class="lm-btn ghost" onclick="closeLicenseModal()">취소</button>
    <a href="{GUMROAD}" target="_blank" class="lm-buy">💳 아직 구매 안 했어요 — Gumroad에서 구매</a>
  </div>
</div>
"""

LICENSE_MODAL_CSS = """
#license-modal { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.7); display:none; align-items:center; justify-content:center; z-index:9999; }
#license-modal .lm-box { background:#fff; padding:32px; border-radius:14px; max-width:420px; width:90%; box-shadow:0 20px 60px rgba(0,0,0,0.3); text-align:center; }
#license-modal h3 { margin:0 0 12px; font-size:20px; color:#1a1a2e; }
#license-modal p { color:#666; margin:0 0 16px; font-size:13px; }
#license-modal input { width:100%; padding:12px; font-size:14px; border:2px solid #e5e5ea; border-radius:8px; text-align:center; font-family:'Courier New',monospace; }
#license-modal input:focus { border-color:#C0392B; outline:none; }
#license-modal .license-msg { font-size:12px; min-height:18px; margin:10px 0; }
#license-modal .license-msg.err { color:#C0392B; }
#license-modal .license-msg.ok  { color:#059669; }
#license-modal .lm-btn { display:block; width:100%; padding:12px; border:none; border-radius:8px; font-size:14px; font-weight:700; cursor:pointer; margin-top:8px; }
#license-modal .lm-btn.primary { background:#1a1a2e; color:#fff; }
#license-modal .lm-btn.primary:hover { background:#C0392B; }
#license-modal .lm-btn.ghost { background:transparent; color:#666; }
#license-modal .lm-buy { display:block; margin-top:14px; padding:10px; background:#fef3c7; color:#92400e; border-radius:8px; text-decoration:none; font-size:13px; font-weight:700; }
"""

# ─── Vocab Hub Page ─────────────────────────────────────────────
def build_vocab_hub():
    cards_html = []
    for r in RESOURCES:
        cards_html.append(f'''
        <div class="vh-card" style="--card-color:{r["color"]};">
          <div class="vh-emoji">{r["emoji"]}</div>
          <div class="vh-title">{escape(r["title"])}</div>
          <div class="vh-kr">{escape(r["kr_title"])}</div>
          <div class="vh-desc">{escape(r["desc"])}</div>
          <div class="vh-meta"><span class="vh-count">{escape(r["count"])}</span></div>

          <!-- LOCKED state: single preview link -->
          <div class="card-actions locked-only">
            <a href="preview-{r["key"]}.html" class="vh-btn vh-btn-preview">🔓 맛보기 →</a>
          </div>

          <!-- UNLOCKED state: view online + download PDF -->
          <div class="card-actions unlocked-only">
            <a href="full-{r["key"]}.html" class="vh-btn vh-btn-view">🌐 온라인 학습</a>
            <a href="{escape(r["source_pdf"])}" download class="vh-btn vh-btn-dl">📥 PDF 다운로드</a>
          </div>
        </div>''')

    html = f"""<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>📚 한국어 학습 자료 허브 · KR Guide Vocabulary Hub</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; background:#f9f7f3; line-height:1.6; }}
  .topbar {{ background:#1a1a2e; color:#fff; padding:14px 24px; display:flex; align-items:center; gap:16px; }}
  .topbar a {{ color:#fff; text-decoration:none; font-weight:700; font-size:14px; }}
  .topbar .brand {{ font-size:16px; font-weight:800; color:#C0392B; }}
  .topbar .spacer {{ flex:1; }}
  .topbar #google_translate_element {{ font-size:12px; }}
  .hero {{ text-align:center; padding:60px 20px 40px; background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; }}
  .hero h1 {{ font-size:38px; margin-bottom:10px; color:#fff; }}
  .hero .kr {{ font-size:20px; color:#f97316; font-weight:700; margin-bottom:14px; }}
  .hero p {{ max-width:680px; margin:0 auto; font-size:15px; opacity:0.85; }}
  .hero .stats {{ margin-top:24px; display:flex; justify-content:center; gap:32px; flex-wrap:wrap; }}
  .hero .stat-num {{ font-size:30px; font-weight:800; color:#f97316; }}
  .hero .stat-label {{ font-size:12px; opacity:0.7; letter-spacing:1px; text-transform:uppercase; }}
  .container {{ max-width:1200px; margin:0 auto; padding:48px 24px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; }}
  .vh-card {{ background:#fff; border-radius:14px; padding:24px; text-decoration:none; color:inherit; display:flex; flex-direction:column; transition:all 0.2s; border-top:4px solid var(--card-color); box-shadow:0 2px 8px rgba(0,0,0,0.04); }}
  .vh-card:hover {{ transform:translateY(-4px); box-shadow:0 12px 24px rgba(0,0,0,0.12); }}
  .vh-emoji {{ font-size:48px; margin-bottom:12px; }}
  .vh-title {{ font-size:17px; font-weight:800; color:#1a1a2e; margin-bottom:4px; }}
  .vh-kr {{ font-size:14px; color:var(--card-color); font-weight:700; margin-bottom:12px; }}
  .vh-desc {{ font-size:13px; color:#666; flex:1; margin-bottom:16px; line-height:1.6; }}
  .vh-meta {{ display:flex; justify-content:space-between; align-items:center; padding-top:12px; border-top:1px solid #f1ede5; margin-bottom:14px; }}
  .vh-count {{ font-size:11px; color:#888; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; }}
  .vh-cta {{ font-size:12px; color:var(--card-color); font-weight:800; }}
  .card-actions {{ display:flex; flex-direction:column; gap:8px; }}
  .vh-btn {{ display:block; padding:11px 14px; border-radius:8px; text-decoration:none; font-weight:800; font-size:13px; text-align:center; transition:all 0.15s; }}
  .vh-btn-preview {{ background:#f8f5ef; color:var(--card-color); border:2px solid var(--card-color); }}
  .vh-btn-preview:hover {{ background:var(--card-color); color:#fff; }}
  .vh-btn-view {{ background:var(--card-color); color:#fff; }}
  .vh-btn-view:hover {{ filter:brightness(1.1); }}
  .vh-btn-dl {{ background:#059669; color:#fff; }}
  .vh-btn-dl:hover {{ background:#047857; }}
  body.locked .unlocked-only {{ display:none; }}
  body.unlocked .locked-only {{ display:none; }}
  body.unlocked .vh-card {{ border-top-width:4px; border-top-color:#059669 !important; }}
  .footer-cta {{ background:#fff; border-radius:14px; padding:40px 24px; text-align:center; margin-top:48px; border:2px dashed #C0392B; }}
  .footer-cta h2 {{ font-size:24px; margin-bottom:10px; }}
  .footer-cta p {{ color:#666; margin-bottom:20px; }}
  .footer-cta .btn-buy {{ display:inline-block; background:#C0392B; color:#fff; padding:14px 28px; border-radius:8px; text-decoration:none; font-weight:800; font-size:15px; }}
  .footer-cta .btn-buy:hover {{ background:#9c2818; }}
  .footer-cta .btn-key {{ display:inline-block; background:transparent; color:#1a1a2e; padding:14px 28px; border:2px solid #1a1a2e; border-radius:8px; cursor:pointer; font-weight:800; font-size:15px; margin-left:10px; }}
  {LICENSE_MODAL_CSS}
</style>
</head><body>

<div class="topbar">
  <a href="learn-korean.html" class="brand">🇰🇷 KR Guide</a>
  <a href="learn-korean.html">메인 가이드</a>
  <a href="vocab-hub.html">📚 학습 자료</a>
  <div class="spacer"></div>
  {GOOGLE_TRANSLATE}
</div>

<div class="hero">
  <h1>📚 한국어 학습 자료 허브</h1>
  <div class="kr">Korean Vocabulary & Expressions · Complete Collection</div>
  <p>15개 카테고리, 6,546개 단어·표현 + 한글·한자 비교 자료. 각 카드를 클릭해 맛보기 콘텐츠를 확인하고, 전체 학습을 원하시면 구매하세요. 외국인 학습자는 우측 상단 Google Translate로 모국어로 학습할 수 있어요.</p>
  <div class="stats">
    <div><div class="stat-num">15</div><div class="stat-label">자료 카테고리</div></div>
    <div><div class="stat-num">6,546</div><div class="stat-label">단어·표현</div></div>
    <div><div class="stat-num">8,000+</div><div class="stat-label">예문</div></div>
  </div>
</div>

<div class="container">
  <div class="grid">
    {''.join(cards_html)}
  </div>

  <div class="footer-cta">
    <h2>💳 모든 자료 한 번에 — Premium Bundle</h2>
    <p>8개 PDF + 웹 전체 콘텐츠 + 무제한 다운로드</p>
    <a href="{GUMROAD}" target="_blank" class="btn-buy">Gumroad에서 구매 — $19.90</a>
    <button class="btn-key" onclick="showLicenseModal()">🔓 이미 구매했어요</button>
  </div>
</div>

{LICENSE_MODAL}
{PAYWALL_JS}

</body></html>"""
    (ROOT / "vocab-hub.html").write_text(html, encoding="utf-8")
    print(f"vocab-hub.html → {(ROOT/'vocab-hub.html').stat().st_size:,} bytes")

# ─── Preview Page Builder ───────────────────────────────────────
def build_preview(r):
    src_html = (ROOT / r["source_html"]).read_text(encoding="utf-8")
    # Find body section and extract first ~preview_pct of <tr> rows
    body_m = re.search(r"<body[^>]*>([\s\S]*?)</body>", src_html)
    body = body_m.group(1) if body_m else src_html
    # Cover stays. Get all tr rows
    trs = re.findall(r"<tr[^>]*>[\s\S]*?</tr>", body)
    keep_n = max(15, int(len(trs) * r["preview_pct"]))
    kept = trs[:keep_n]
    # Replace the original table content with kept rows
    # Build a simplified body: cover + first category intro + truncated table
    # Approach: take body up to first <table> + first <tbody>, insert kept rows, close table, append "more" CTA

    # Extract head/styles from original
    head_m = re.search(r"<head[^>]*>([\s\S]*?)</head>", src_html)
    head = head_m.group(1) if head_m else ""
    # Strip the title's tag
    head = re.sub(r"<title>.*?</title>", f"<title>맛보기 · {escape(r['title'])}</title>", head, flags=re.S)

    # Body structure: cover up to first <table>, then truncated table, then CTA
    pre_table = re.split(r"<table\b", body, maxsplit=1)
    pre = pre_table[0] if pre_table else ""
    # Get table head
    table_head_m = re.search(r"<table[\s\S]*?<tbody>", body)
    table_head = table_head_m.group(0) if table_head_m else "<table><tbody>"

    cta_block = f"""
<div class="paywall-cta" style="margin:40px auto; max-width:720px; background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:32px 28px; border-radius:14px; text-align:center;">
  <div style="font-size:32px; margin-bottom:10px;">🔒</div>
  <h2 style="font-size:22px; margin:0 0 8px; color:#fff;">전체 콘텐츠는 결제 후 학습 가능합니다</h2>
  <p style="margin:0 0 18px; opacity:0.85; font-size:14px;">위 미리보기는 약 {int(r['preview_pct']*100)}%입니다. 전체 <strong>{escape(r['count'])}</strong>, 모든 예문·시나리오·퀴즈·QR 코드까지 잠금 해제하려면:</p>
  <a href="{GUMROAD}" target="_blank" style="display:inline-block; background:#f97316; color:#fff; padding:14px 32px; border-radius:8px; text-decoration:none; font-weight:800; font-size:15px; margin:4px;">💳 Gumroad에서 구매 — $19.90</a>
  <button onclick="showLicenseModal()" style="display:inline-block; background:transparent; color:#fff; padding:14px 32px; border:2px solid #fff; border-radius:8px; cursor:pointer; font-weight:800; font-size:15px; margin:4px;">🔓 이미 구매했어요</button>
  <p style="margin-top:16px; font-size:12px; opacity:0.7;">키 1개로 <strong>모든 8개 자료</strong> 잠금 해제</p>
  <p style="margin-top:20px;"><a href="vocab-hub.html" style="color:#f97316; text-decoration:none; font-weight:700;">← 다른 자료 둘러보기</a></p>
</div>
"""

    # Compose
    preview_html = f"""<!DOCTYPE html>
<html lang="ko"><head>{head}{LICENSE_MODAL_CSS_TAG}
<style>
  .topbar {{ background:#1a1a2e; color:#fff; padding:12px 20px; display:flex; align-items:center; gap:14px; font-size:13px; }}
  .topbar a {{ color:#fff; text-decoration:none; font-weight:700; }}
  .topbar .brand {{ color:#C0392B; font-size:15px; font-weight:800; }}
  .topbar .spacer {{ flex:1; }}
  .preview-banner {{ background:#fef3c7; color:#92400e; padding:10px 20px; text-align:center; font-size:13px; font-weight:700; border-bottom:2px solid #f59e0b; }}
</style>
</head><body>

<div class="topbar">
  <a href="learn-korean.html" class="brand">🇰🇷 KR Guide</a>
  <a href="learn-korean.html">메인 가이드</a>
  <a href="vocab-hub.html">📚 학습 자료</a>
  <div class="spacer"></div>
  {GOOGLE_TRANSLATE}
</div>

<div class="preview-banner">🔓 맛보기 · Free Preview ({int(r['preview_pct']*100)}%) — 전체 학습은 결제 후 가능합니다</div>

{pre}
{table_head}
{''.join(kept)}
</tbody></table>

{cta_block}

{LICENSE_MODAL}
{PAYWALL_JS}

</body></html>"""
    out = ROOT / f"preview-{r['key']}.html"
    out.write_text(preview_html, encoding="utf-8")
    print(f"preview-{r['key']}.html → {out.stat().st_size:,} bytes")

# ─── Full Page Builder (paywall-locked) ────────────────────────
def build_full(r):
    src_html = (ROOT / r["source_html"]).read_text(encoding="utf-8")
    head_m = re.search(r"<head[^>]*>([\s\S]*?)</head>", src_html)
    head = head_m.group(1) if head_m else ""
    head = re.sub(r"<title>.*?</title>", f"<title>전체 · {escape(r['title'])}</title>", head, flags=re.S)

    body_m = re.search(r"<body[^>]*>([\s\S]*?)</body>", src_html)
    body = body_m.group(1) if body_m else src_html

    download_btn = f"""
<div class="dl-section" style="background:linear-gradient(135deg,#059669,#0f766e); color:#fff; padding:24px; border-radius:14px; margin:24px auto; max-width:720px; text-align:center;">
  <div style="font-size:28px; margin-bottom:8px;">✅ 잠금 해제 완료</div>
  <p style="margin:0 0 14px; opacity:0.9; font-size:14px;">아래에서 모든 자료를 PDF로 다운로드하거나 웹에서 학습할 수 있습니다.</p>
  <a href="{escape(r['source_pdf'])}" download style="display:inline-block; background:#fff; color:#059669; padding:12px 28px; border-radius:8px; text-decoration:none; font-weight:800; font-size:14px; margin:4px;">📥 이 자료 PDF 다운로드</a>
  <a href="vocab-hub.html" style="display:inline-block; background:transparent; color:#fff; padding:12px 28px; border:2px solid #fff; border-radius:8px; text-decoration:none; font-weight:800; font-size:14px; margin:4px;">📚 다른 자료 보기</a>
</div>
"""

    locked_banner = f"""
<div class="locked-banner" style="background:#fff; border:3px dashed #C0392B; padding:40px 24px; border-radius:14px; max-width:720px; margin:40px auto; text-align:center;">
  <div style="font-size:48px;">🔒</div>
  <h2 style="margin:10px 0; color:#C0392B;">전체 콘텐츠는 결제 후 학습 가능</h2>
  <p style="color:#666; margin-bottom:20px;">라이선스 키를 입력하거나 Gumroad에서 구매하세요.</p>
  <a href="{GUMROAD}" target="_blank" style="display:inline-block; background:#C0392B; color:#fff; padding:14px 28px; border-radius:8px; text-decoration:none; font-weight:800; margin:4px;">💳 구매 — $19.90</a>
  <button onclick="showLicenseModal()" style="display:inline-block; background:transparent; color:#1a1a2e; padding:14px 28px; border:2px solid #1a1a2e; border-radius:8px; cursor:pointer; font-weight:800; margin:4px;">🔓 키 입력</button>
  <p style="margin-top:14px;"><a href="preview-{r['key']}.html" style="color:#888;">← 맛보기로 돌아가기</a></p>
</div>
"""

    full_html = f"""<!DOCTYPE html>
<html lang="ko"><head>{head}
<style>
  body.locked .content-locked {{ display:none; }}
  body.unlocked .lock-screen {{ display:none; }}
  body.locked .dl-section {{ display:none; }}
  .topbar {{ background:#1a1a2e; color:#fff; padding:12px 20px; display:flex; align-items:center; gap:14px; font-size:13px; }}
  .topbar a {{ color:#fff; text-decoration:none; font-weight:700; }}
  .topbar .brand {{ color:#C0392B; font-size:15px; font-weight:800; }}
  .topbar .spacer {{ flex:1; }}
  {LICENSE_MODAL_CSS}
</style>
</head><body class="locked">

<div class="topbar">
  <a href="learn-korean.html" class="brand">🇰🇷 KR Guide</a>
  <a href="learn-korean.html">메인 가이드</a>
  <a href="vocab-hub.html">📚 학습 자료</a>
  <div class="spacer"></div>
  {GOOGLE_TRANSLATE}
</div>

<div class="lock-screen">
{locked_banner}
</div>

<div class="content-locked">
{download_btn}
{body}
{download_btn}
</div>

{LICENSE_MODAL}
{PAYWALL_JS}

</body></html>"""
    out = ROOT / f"full-{r['key']}.html"
    out.write_text(full_html, encoding="utf-8")
    print(f"full-{r['key']}.html    → {out.stat().st_size:,} bytes")

# placeholder before use
LICENSE_MODAL_CSS_TAG = f"<style>{LICENSE_MODAL_CSS}</style>"

# ─── Build all ─────────────────────────────────────────────────
build_vocab_hub()
for r in RESOURCES:
    build_preview(r)
    build_full(r)

# ─── Add button to learn-korean.html linking to vocab-hub ──────
lk_path = ROOT / "learn-korean.html"
lk_html = lk_path.read_text(encoding="utf-8")
button_html = '''
<!-- VOCAB HUB CTA (inserted by make_vocab_hub.py) -->
<div id="vocab-hub-cta" style="max-width:800px; margin:60px auto; padding:36px 28px; background:linear-gradient(135deg,#C0392B,#1A4A8A); border-radius:18px; text-align:center; color:#fff; box-shadow:0 12px 32px rgba(0,0,0,0.15);">
  <div style="font-size:48px; margin-bottom:12px;">📚</div>
  <h2 style="margin:0 0 8px; color:#fff; font-size:26px;">추가 학습 자료 — Vocabulary Hub</h2>
  <p style="margin:0 0 20px; opacity:0.92; font-size:15px;">동사 200, 명사 369, 형용사·부사 1067, 존댓말 500, 일본어 외래어, 인터넷 한국어, 콩글리시, 의성어·의태어 등 <strong>4,124개</strong>의 단어와 표현을 한 곳에서. 카드를 클릭해 맛보기 후 구매하세요.</p>
  <a href="vocab-hub.html" style="display:inline-block; background:#fff; color:#C0392B; padding:14px 34px; border-radius:8px; text-decoration:none; font-weight:800; font-size:15px;">📚 학습 자료 둘러보기 →</a>
</div>
'''
# Insert just before </body> if not already there
if 'id="vocab-hub-cta"' not in lk_html:
    lk_html = lk_html.replace("</body>", button_html + "\n</body>")
    lk_path.write_text(lk_html, encoding="utf-8")
    print(f"learn-korean.html: vocab-hub CTA button inserted")
else:
    print(f"learn-korean.html: vocab-hub CTA already present")

print("\n✅ Freemium structure built. Files:")
print(f"  vocab-hub.html")
for r in RESOURCES:
    print(f"  preview-{r['key']}.html  +  full-{r['key']}.html")
