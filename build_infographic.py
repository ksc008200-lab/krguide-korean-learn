"""Build a sellable 41-chapter infographic poster.

Output:
  - learn-korean-infographic.html   (source)
  - learn-korean-infographic.pdf    (single-page A4 portrait)

Design:
  - Title banner across top
  - 41 chapter cards in 6-column grid, color-coded by section
  - Each card: chapter number, English title, Korean title (consistent format)
  - Footer with branding & URL
"""
import subprocess
from pathlib import Path

PROJECT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
OUT_HTML = PROJECT / "learn-korean-infographic.html"
OUT_PDF  = PROJECT / "learn-korean-infographic.pdf"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
edge = next((p for p in EDGE_CANDIDATES if Path(p).exists()), None)

# All 41 chapters: (num, English title, Korean title, section_id)
# Sections: F=Foundation, V=Vocabulary, G=Grammar, C=Conversation, D=Daily Life,
#           M=Modern Life, K=Deep Korean Culture, R=Reference
CHAPTERS = [
    (1,  "Birth of Hangul",                     "한글의 탄생",                 "F"),
    (2,  "Korean Consonants",                   "한국어 자음",                 "F"),
    (3,  "Korean Vowels",                       "한국어 모음",                 "F"),
    (4,  "Batchim — Bottom Sound",              "받침 — 아래 소리",            "F"),
    (5,  "Numbers — Two Systems",               "숫자 — 두 가지 체계",          "V"),
    (6,  "Essential 200 Words",                 "필수 단어 200",               "V"),
    (7,  "Sentence Structure",                  "문장 구조",                   "G"),
    (8,  "Verb Conjugation",                    "동사 활용",                   "G"),
    (9,  "Real Life Conversations",             "실생활 대화",                 "C"),
    (10, "존댓말 & 반말",                       "존댓말과 반말",                "G"),
    (11, "Tenses — Time Travel",                "시제 — 시간 여행",            "G"),
    (12, "Grammar Patterns",                    "문법 패턴",                   "G"),
    (13, "Particles — The Glue",                "조사 — 한국어의 접착제",       "G"),
    (14, "Question Words",                      "의문사",                      "C"),
    (15, "Food & Restaurants",                  "음식과 식당",                 "D"),
    (16, "Shopping & Money",                    "쇼핑과 돈",                   "D"),
    (17, "Transportation & Directions",         "교통과 길 찾기",              "D"),
    (18, "Family & Relationships",              "가족과 관계",                 "D"),
    (19, "Weather & Seasons",                   "날씨와 계절",                 "D"),
    (20, "Holidays & Culture",                  "명절과 문화",                 "D"),
    (21, "Adjectives",                          "형용사",                      "G"),
    (22, "Body & Health",                       "신체와 건강",                 "D"),
    (23, "K-pop & Hallyu",                      "K팝과 한류",                  "M"),
    (24, "Hobbies & Free Time",                 "취미와 여가",                 "D"),
    (25, "Work & School",                       "직장과 학교",                 "D"),
    (26, "Love & Dating",                       "사랑과 연애",                 "M"),
    (27, "Travel in Korea",                     "한국 여행",                   "D"),
    (28, "Korean Slang & Internet",             "한국어 슬랭과 인터넷",         "M"),
    (29, "Spelling Rules",                      "맞춤법",                      "G"),
    (30, "Using a Korean Dictionary",           "한국어 사전 사용법",          "G"),
    (31, "The 'Uri' Culture",                   "'우리' 문화",                 "K"),
    (32, "Speaking Without Subject",            "주어 없이 말하기",            "K"),
    (33, "Hanja & Pure Korean",                 "한자어와 고유어",             "K"),
    (34, "千字文 & Hanja Keys",                 "천자문과 한자",               "K"),
    (35, "Standard Korean & Dialects",          "표준어와 사투리",             "K"),
    (36, "5,000 Years of Korean History",       "한국 5,000년 역사",           "K"),
    (37, "BTS & K-Culture",                     "BTS와 K-컬처",                "K"),
    (38, "500 Essential Nouns",                 "필수 명사 500",               "R"),
    (39, "200 Essential Verbs",                 "필수 동사 200",               "R"),
    (40, "200 Essential Adverbs",               "필수 부사 200",               "R"),
    (41, "Jeju Dialect (제주어)",               "제주 방언",                   "K"),
]

# Section color palette
SECTIONS = {
    "F": ("#1A4A8A", "Foundation · 기초",     "🔤"),
    "V": ("#0EA5E9", "Vocabulary · 어휘",     "📚"),
    "G": ("#7C3AED", "Grammar · 문법",        "🧱"),
    "C": ("#F59E0B", "Conversation · 회화",   "💬"),
    "D": ("#10B981", "Daily Life · 일상",     "🏙️"),
    "M": ("#EC4899", "Modern Korea · 현대",   "🌟"),
    "K": ("#C0392B", "Deep Culture · 심층 문화", "🇰🇷"),
    "R": ("#6B7280", "Reference · 참고",      "📖"),
}

# Build chapter cards
cards_html = ""
for num, en, kr, sec in CHAPTERS:
    color, _, _ = SECTIONS[sec]
    cards_html += f"""
<div class="card" style="border-top:4px solid {color};">
  <div class="ch-num" style="color:{color};">CH {num:02d}</div>
  <div class="ch-en">{en}</div>
  <div class="ch-kr">{kr}</div>
</div>"""

# Section legend
legend_html = ""
for sec_id, (color, label, icon) in SECTIONS.items():
    legend_html += f"""
<div class="legend-item">
  <span class="legend-dot" style="background:{color};"></span>
  <span>{icon} {label}</span>
</div>"""

template = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>Learn Korean — 41-Chapter Complete Map</title>
<style>
@page {{
  size: A4 portrait;
  margin: 12mm;
}}
* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}
body {{
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Segoe UI', sans-serif;
  color: #222;
  background: #fff;
  font-size: 8.5pt;
  line-height: 1.4;
}}

.header {{
  background: linear-gradient(135deg, #1A4A8A 0%, #C0392B 100%);
  color: #fff;
  padding: 16px 20px;
  border-radius: 10px;
  text-align: center;
  margin-bottom: 12px;
}}
.header h1 {{
  font-size: 22pt;
  margin: 0;
  letter-spacing: -0.5px;
}}
.header .sub {{
  font-size: 11pt;
  margin-top: 4px;
  color: #FACC15;
  font-weight: 700;
  letter-spacing: 1px;
}}
.header .tag {{
  font-size: 9pt;
  margin-top: 6px;
  opacity: 0.92;
}}

.legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  justify-content: center;
  margin: 8px 0 12px;
  font-size: 8pt;
}}
.legend-item {{ display: flex; align-items: center; gap: 4px; }}
.legend-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 6px;
}}
.card {{
  background: #fff;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  padding: 6px 7px 7px;
  min-height: 56px;
  display: flex;
  flex-direction: column;
  page-break-inside: avoid;
}}
.ch-num {{
  font-size: 7pt;
  font-weight: 800;
  letter-spacing: 1.2px;
  margin-bottom: 2px;
}}
.ch-en {{
  font-size: 8pt;
  font-weight: 700;
  color: #1A1A2E;
  line-height: 1.25;
  margin-bottom: 2px;
}}
.ch-kr {{
  font-size: 7.5pt;
  color: #555;
  line-height: 1.25;
}}

.footer {{
  margin-top: 14px;
  padding: 10px 14px;
  background: linear-gradient(135deg, #FACC15 0%, #F97316 100%);
  border-radius: 10px;
  text-align: center;
  color: #1A1A2E;
  font-weight: 800;
  font-size: 9pt;
}}
.footer .url {{
  margin-top: 3px;
  font-size: 11pt;
  color: #C0392B;
}}
.footer .small {{
  margin-top: 3px;
  font-size: 7pt;
  font-weight: 500;
  opacity: 0.85;
}}
</style>
</head>
<body>

<div class="header">
  <h1>Learn Korean — Complete Roadmap</h1>
  <div class="sub">한국어 배우기 — 41장 완전 가이드</div>
  <div class="tag">41 Chapters · Bilingual EN/KR · Romanization · Cultural Notes</div>
</div>

<div class="legend">{legend_html}
</div>

<div class="grid">{cards_html}
</div>

<div class="footer">
  📘 Complete Korean Learning Journey · 한국어 학습 완전 가이드
  <div class="url">krguide.com · study.krguide.com</div>
  <div class="small">© 2026 krguide.com — From Hangul basics to Jeju dialect, bilingual throughout</div>
</div>

</body></html>"""

OUT_HTML.write_text(template, encoding="utf-8")
print(f"HTML written: {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")

if OUT_PDF.exists():
    try:
        OUT_PDF.unlink()
    except PermissionError:
        OUT_PDF = PROJECT / f"learn-korean-infographic-tmp.pdf"

print("Rendering infographic PDF via Edge headless...")
cmd = [
    edge,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUT_PDF}",
    OUT_HTML.as_uri(),
]
result = subprocess.run(cmd, capture_output=True, timeout=120)
if OUT_PDF.exists():
    print(f"PDF saved: {OUT_PDF}")
    print(f"Size: {OUT_PDF.stat().st_size / 1024:.1f} KB")
else:
    err = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
    print("FAIL:", err[:500])
