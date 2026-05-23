"""Build Gumroad-ready images:
  1) gumroad-cover.png       — 1280x720 hero/thumbnail
  2) gumroad-features.png    — 1280x720 value-prop ('무료 증정 외의 놀라운 자료 평생 무료 접근')
  3) gumroad-chapters.png    — 1280x1280 41-chapter grid (cleaned titles)
"""
import subprocess
from pathlib import Path

PROJECT = Path(r"C:\Users\무지랭이\krguide-korean-learn")

# Cleaned 41 chapter titles (English title · Korean title)
CHAPTERS = [
    (1,  "Birth of Hangul",            "한글의 탄생",            "F"),
    (2,  "Korean Consonants",          "한국어 자음",             "F"),
    (3,  "Korean Vowels",              "한국어 모음",             "F"),
    (4,  "Batchim (받침)",             "받침 — 음절의 기초",       "F"),
    (5,  "Numbers Two Systems",        "두 가지 숫자 체계",        "V"),
    (6,  "Essential 200 Words",        "필수 단어 200",           "V"),
    (7,  "Sentence Structure",         "문장 구조",               "G"),
    (8,  "Verb Conjugation",           "동사 활용",               "G"),
    (9,  "Real Life Conversations",    "실생활 대화",             "C"),
    (10, "존댓말 & 반말",              "존댓말과 반말",            "G"),
    (11, "Three Tenses",               "시제 — 과거·현재·미래",   "G"),
    (12, "Grammar Patterns",           "필수 문법 패턴",           "G"),
    (13, "Particles (조사)",           "조사 — 한국어의 GPS",      "G"),
    (14, "Question Words",             "의문사 7가지",             "C"),
    (15, "Food & Restaurants",         "음식과 식당",              "D"),
    (16, "Shopping & Money",           "쇼핑과 돈",               "D"),
    (17, "Transportation",             "교통과 길 찾기",          "D"),
    (18, "Family & Relationships",     "가족과 관계",              "D"),
    (19, "Weather & Seasons",          "날씨와 계절",              "D"),
    (20, "Holidays & Culture",         "명절과 문화",              "D"),
    (21, "Adjectives",                 "형용사",                  "G"),
    (22, "Body & Health",              "신체와 건강",              "D"),
    (23, "K-pop & Hallyu",             "K팝과 한류",              "M"),
    (24, "Hobbies & Free Time",        "취미와 여가",              "D"),
    (25, "Work & School",              "직장과 학교",              "D"),
    (26, "Love & Dating",              "사랑과 연애",              "M"),
    (27, "Travel in Korea",            "한국 여행",               "D"),
    (28, "Slang & Internet",           "한국어 슬랭",              "M"),
    (29, "Spelling Rules",             "맞춤법",                  "G"),
    (30, "Using a Dictionary",         "사전 사용법",             "G"),
    (31, "'Uri' Culture",              "'우리' 문화",             "K"),
    (32, "Speaking Without Subject",   "주어 없이 말하기",         "K"),
    (33, "Hanja & Pure Korean",        "한자어와 고유어",          "K"),
    (34, "千字文 & Hanja Keys",        "천자문과 한자 마스터키",    "K"),
    (35, "Standard & Dialects",        "표준어와 사투리",          "K"),
    (36, "5000-Year Korean History",   "한국 5,000년 역사",        "K"),
    (37, "BTS & K-Culture",            "BTS와 K-컬처",           "K"),
    (38, "500 Essential Nouns",        "필수 명사 500",            "R"),
    (39, "200 Essential Verbs",        "필수 동사 200",            "R"),
    (40, "200 Essential Adverbs",      "필수 부사 200",            "R"),
    (41, "Jeju Dialect (제주어)",      "제주 방언",                "K"),
]

# Section colors
SEC_COLORS = {
    "F": "#1A4A8A", "V": "#0EA5E9", "G": "#7C3AED", "C": "#F59E0B",
    "D": "#10B981", "M": "#EC4899", "K": "#C0392B", "R": "#6B7280",
}

FONT_FAMILY = "'Malgun Gothic','Apple SD Gothic Neo','Segoe UI',sans-serif"

# ========== 1. THUMBNAIL (600x600 square, Gumroad standard) ==========
COVER_HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ margin:0; padding:24px 22px; width:600px; height:600px; font-family:{FONT_FAMILY}; background:linear-gradient(135deg,#1A4A8A 0%,#C0392B 100%); color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; box-sizing:border-box; position:relative; }}
.flag {{ font-size:42px; line-height:1; margin-bottom:4px; }}
.tag {{ font-size:10px; letter-spacing:3.5px; color:#FACC15; font-weight:800; margin-bottom:6px; }}
.title {{ font-size:42px; font-weight:900; margin:0; line-height:1.0; text-shadow:0 3px 14px rgba(0,0,0,0.3); }}
.subtitle-kr {{ font-size:18px; margin-top:8px; color:#FACC15; font-weight:800; }}
.headline-kr {{ font-size:26px; color:#FACC15; font-weight:900; margin:18px 0 4px; text-align:center; text-shadow:0 3px 12px rgba(0,0,0,0.45); line-height:1.18; }}
.headline-en {{ font-size:14px; color:#FACC15; font-weight:800; text-align:center; opacity:0.95; line-height:1.25; padding:0 8px; }}
.chips {{ display:flex; gap:6px; margin-top:14px; flex-wrap:wrap; justify-content:center; max-width:560px; }}
.chip {{ background:rgba(255,255,255,0.18); padding:5px 11px; border-radius:18px; font-size:11px; font-weight:700; border:1.5px solid rgba(255,255,255,0.32); }}
.cta-box {{ margin-top:14px; background:#FACC15; color:#1A1A2E; padding:8px 18px; border-radius:9px; font-size:12px; font-weight:900; box-shadow:0 5px 16px rgba(0,0,0,0.3); text-align:center; }}
.brand {{ position:absolute; bottom:10px; left:0; right:0; text-align:center; font-size:10px; opacity:0.85; }}
</style></head><body>
<div class="flag">🇰🇷</div>
<div class="tag">COMPLETE KOREAN GUIDE · 2026</div>
<h1 class="title">Learn Korean</h1>
<div class="subtitle-kr">한국어 배우기 — 완전 가이드</div>
<div class="headline-kr">이 책이면 당신은<br>최단기간에 한국을 알 수 있습니다</div>
<div class="headline-en">— With this book, you can master Korea in record time —</div>
<div class="chips">
  <div class="chip">📚 41 Chapters</div>
  <div class="chip">🗣 Bilingual EN/KR</div>
  <div class="chip">🎯 Romanization</div>
  <div class="chip">🏛️ Cultural Notes</div>
</div>
<div class="cta-box">🎁 무료 증정 외의 놀라운 자료 · 평생 무료 접근</div>
<div class="brand">krguide.com · study.krguide.com</div>
</body></html>"""

# ========== 2. FEATURES (1280x720) ==========
FEATURES_HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ margin:0; padding:50px 60px; width:1280px; height:720px; font-family:{FONT_FAMILY}; background:#FAFAFA; color:#1A1A2E; box-sizing:border-box; }}
.banner {{ background:linear-gradient(135deg,#FACC15,#F97316); padding:24px 32px; border-radius:18px; text-align:center; margin-bottom:36px; box-shadow:0 8px 24px rgba(0,0,0,0.12); }}
.banner-title {{ font-size:42px; font-weight:900; color:#1A1A2E; margin:0; }}
.banner-sub {{ font-size:18px; margin-top:8px; color:#7C2D12; font-weight:700; }}
.grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }}
.card {{ background:#fff; border-radius:14px; padding:22px 26px; box-shadow:0 4px 14px rgba(0,0,0,0.06); border-left:6px solid #1A4A8A; }}
.card-num {{ font-size:16px; color:#1A4A8A; font-weight:800; letter-spacing:2px; }}
.card-title {{ font-size:22px; font-weight:800; margin:6px 0 10px; }}
.card-body {{ font-size:16px; color:#444; line-height:1.4; }}
.foot {{ margin-top:28px; text-align:center; font-size:16px; color:#666; font-weight:700; }}
.url {{ color:#C0392B; font-size:18px; }}
</style></head><body>
<div class="banner">
  <div class="banner-title">🎁 무료 증정 외의 놀라운 자료</div>
  <div class="banner-sub">평생 무료 접근 · LIFETIME FREE ACCESS TO BONUS RESOURCES</div>
</div>
<div class="grid">
  <div class="card" style="border-left-color:#1A4A8A;">
    <div class="card-num">BONUS 01</div>
    <div class="card-title">200 Essential Verbs · 필수 동사 200</div>
    <div class="card-body">고빈도 동사 + 활용 + 예문. 일상 대화 80% 커버.</div>
  </div>
  <div class="card" style="border-left-color:#0EA5E9;">
    <div class="card-num">BONUS 02</div>
    <div class="card-title">500 Essential Nouns · 필수 명사 500</div>
    <div class="card-body">10개 생활 영역별 정리. 즉시 활용 가능.</div>
  </div>
  <div class="card" style="border-left-color:#10B981;">
    <div class="card-num">BONUS 03</div>
    <div class="card-title">500 Honorifics · 존댓말 500</div>
    <div class="card-body">상황별 정중·격식 표현 완전 정리.</div>
  </div>
  <div class="card" style="border-left-color:#7C3AED;">
    <div class="card-num">BONUS 04</div>
    <div class="card-title">1,100 Visual Vocabulary · 그림 어휘 1,100</div>
    <div class="card-body">30개 카테고리 이미지 기반 단어 학습.</div>
  </div>
  <div class="card" style="border-left-color:#F59E0B;">
    <div class="card-num">BONUS 05</div>
    <div class="card-title">500 Internet Slang · 인터넷 슬랭 500</div>
    <div class="card-body">MZ세대가 실제로 쓰는 2026 최신 표현.</div>
  </div>
  <div class="card" style="border-left-color:#C0392B;">
    <div class="card-num">BONUS 06</div>
    <div class="card-title">100 사자성어 + 100 속담</div>
    <div class="card-body">한국 문화 깊이를 더하는 고전 표현.</div>
  </div>
</div>
<div class="foot">📚 총 15+ 보너스 리소스 · 모든 구매자에게 평생 무료 업데이트 제공<br><span class="url">krguide.com · study.krguide.com</span></div>
</body></html>"""

# ========== 3. CHAPTERS (1280x1280) ==========
cards = ""
for n, en, kr, sec in CHAPTERS:
    c = SEC_COLORS[sec]
    cards += f"""
<div class="ch-card" style="border-top:4px solid {c};">
  <div class="ch-num" style="color:{c};">CH {n:02d}</div>
  <div class="ch-en">{en}</div>
  <div class="ch-kr">{kr}</div>
</div>"""

CHAPTERS_HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ margin:0; padding:18px 22px; width:1280px; height:720px; font-family:{FONT_FAMILY}; background:#fff; color:#222; box-sizing:border-box; overflow:hidden; }}
.header {{ background:linear-gradient(135deg,#1A4A8A 0%,#C0392B 100%); color:#fff; padding:12px 22px; border-radius:10px; text-align:center; margin-bottom:10px; }}
.header h1 {{ margin:0; font-size:24px; font-weight:900; }}
.header .sub {{ font-size:13px; color:#FACC15; font-weight:800; margin-top:3px; letter-spacing:1.5px; }}
.grid {{ display:grid; grid-template-columns:repeat(7,1fr); gap:6px; }}
.ch-card {{ background:#fff; border:1px solid #E5E7EB; border-radius:7px; padding:7px 8px; min-height:78px; box-shadow:0 1px 3px rgba(0,0,0,0.05); }}
.ch-num {{ font-size:10px; font-weight:900; letter-spacing:1px; }}
.ch-en {{ font-size:11.5px; font-weight:800; color:#1A1A2E; margin-top:3px; line-height:1.2; }}
.ch-kr {{ font-size:10.5px; color:#555; margin-top:2px; line-height:1.2; }}
.foot {{ margin-top:10px; padding:10px 18px; background:linear-gradient(135deg,#FACC15,#F97316); border-radius:10px; text-align:center; color:#1A1A2E; font-weight:900; font-size:13px; }}
.url {{ color:#C0392B; font-size:14px; margin-top:2px; }}
</style></head><body>
<div class="header">
  <h1>🇰🇷 41 Chapters · Complete Roadmap</h1>
  <div class="sub">한국어 배우기 · 41장 완전 가이드 · 2026</div>
</div>
<div class="grid">{cards}
</div>
<div class="foot">
  📘 From Hangul Basics to Jeju Dialect · Bilingual EN/KR · Romanization · Cultural Notes
  <div class="url">krguide.com · study.krguide.com</div>
</div>
</body></html>"""

# Write all three HTML files
(PROJECT / "gumroad-cover.html").write_text(COVER_HTML, encoding="utf-8")
(PROJECT / "gumroad-features.html").write_text(FEATURES_HTML, encoding="utf-8")
(PROJECT / "gumroad-chapters.html").write_text(CHAPTERS_HTML, encoding="utf-8")

print("[OK] Wrote 3 HTML files. Now use render_images.js to convert to PNG.")
