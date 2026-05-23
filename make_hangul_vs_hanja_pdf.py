"""
Build bilingual (Korean + English) PDF: Hangul Cultural Features & Comparison with Hanja.
"""
import subprocess, time, urllib.parse
from pathlib import Path
from html import escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
HTML_OUT = ROOT / "hangul-vs-hanja-enhanced.html"
PDF_OUT  = ROOT / "hangul-vs-hanja-enhanced.pdf"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 5 features of Hangul (Korean + English)
FEATURES = [
    {
        "no": 1, "icon": "🔬",
        "title_ko": "발음 기관을 본떠 만든 세계 유일의 과학적 문자",
        "title_en": "The Only Scientifically Designed Alphabet Based on Vocal Organs",
        "body_ko": [
            "자음은 입·혀·목구멍의 모양을, 모음은 천(·)·지(ㅡ)·인(ㅣ) 삼재 사상을 본떠 만들어졌습니다.",
            "ㄱ: 혀뿌리가 목구멍을 막는 모양",
            "ㄴ: 혀끝이 윗잇몸에 닿는 모양",
            "ㅁ: 입술이 다물어진 모양",
            "ㅅ: 이의 모양",
            "→ 글자만 봐도 어떻게 발음해야 하는지 알 수 있는 세계에서 유일한 알파벳입니다. UNESCO는 한글의 이런 우수성을 기려 \"세종대왕 문해상(King Sejong Literacy Prize)\"을 제정했습니다.",
        ],
        "body_en": [
            "Consonants are shaped after the form of the mouth, tongue, and throat. Vowels are based on the Three Powers cosmology: Heaven (·), Earth (ㅡ), and Human (ㅣ).",
            "ㄱ: tongue root blocking the throat",
            "ㄴ: tongue tip touching the upper gum",
            "ㅁ: lips pressed together (closed mouth)",
            "ㅅ: shape of a tooth",
            "→ It is the only alphabet in the world where the shape of the letter itself shows you how to pronounce it. UNESCO honored this excellence by establishing the King Sejong Literacy Prize.",
        ],
    },
    {
        "no": 2, "icon": "🔊",
        "title_ko": "한 글자 = 한 소리 (완벽한 음소문자)",
        "title_en": "One Letter = One Sound (Perfect Phonemic Script)",
        "body_ko": [
            "영어처럼 \"though, through, thought\"가 제각각 다르게 읽히는 일이 없습니다. 한글은 글자대로 소리 나고, 소리대로 글자가 적히는 가장 투명한 표음문자입니다.",
            "→ 그래서 세종대왕이 \"지혜로운 자는 아침나절이면 깨우치고, 어리석은 자도 열흘이면 배운다(智者不終朝而會, 愚者可浹旬而學)\"라고 자신 있게 말할 수 있었던 것입니다.",
        ],
        "body_en": [
            "Unlike English, where 'though, through, thought' are all read differently, Hangul letters always sound exactly as written. It is the most transparent phonemic script in the world.",
            "→ This is why King Sejong could confidently say: \"The wise can master it before morning ends, and even the foolish can learn it within ten days.\"",
        ],
    },
    {
        "no": 3, "icon": "🧩",
        "title_ko": "모아쓰기 — 음절 단위 모듈 구조",
        "title_en": "Syllable-Block Composition — A Modular Structure",
        "body_ko": [
            "자음과 모음을 옆·아래로 조합해 하나의 네모 블록(음절)을 만드는 것이 한글의 독특한 시각적 특징입니다.",
            "한 (ㅎ + ㅏ + ㄴ) / 글 (ㄱ + ㅡ + ㄹ)",
            "→ 음소문자의 정밀함 + 음절문자의 가독성을 동시에 갖춘 유일한 문자 체계입니다. 한자 문화권에서 자란 한국인의 시각 인지 구조에도 자연스럽게 맞습니다.",
        ],
        "body_en": [
            "Consonants and vowels are combined horizontally and vertically into a single square syllable block — Hangul's unique visual feature.",
            "한 (ㅎ + ㅏ + ㄴ) / 글 (ㄱ + ㅡ + ㄹ)",
            "→ Hangul uniquely combines the precision of an alphabet with the visual readability of a syllabic script. It also fits the Korean cognitive structure shaped by the Hanja cultural sphere.",
        ],
    },
    {
        "no": 4, "icon": "📜",
        "title_ko": "창제자·창제 시기·창제 의도가 모두 기록된 유일한 문자",
        "title_en": "The Only Script with Recorded Creator, Date, and Intent",
        "body_ko": [
            "세계의 거의 모든 문자(라틴·한자·아랍·인도)는 자연 발생적으로 진화했습니다. 그러나 한글만은:",
            "누가: 세종대왕과 집현전 학자들",
            "언제: 1443년 창제, 1446년 반포",
            "왜: 『훈민정음 해례본』 서문 — \"백성이 말하고자 하는 바가 있어도 그 뜻을 펴지 못하는 자가 많기에 내가 이를 가엾이 여겨…\"",
            "어떻게: 28자의 구성·원리·예시까지 모두 기록",
            "→ 『훈민정음 해례본』은 UNESCO 세계기록유산(1997년 등재)입니다. 인류 문자 역사상 전무후무한 사례입니다.",
        ],
        "body_en": [
            "Almost every writing system in the world (Latin, Chinese, Arabic, Indic) evolved naturally over centuries. Hangul alone has all of:",
            "WHO: King Sejong the Great and scholars of the Hall of Worthies (Jiphyeonjeon).",
            "WHEN: Created in 1443, promulgated in 1446.",
            "WHY: Preface to Hunminjeongeum — \"There are many who, having something they wish to put into words, are in the end unable to express themselves. I am greatly distressed because of this.\"",
            "HOW: All 28 letters' structure, principles, and examples documented.",
            "→ The Hunminjeongeum Haeryebon was inscribed in UNESCO's Memory of the World Register in 1997 — unprecedented in the history of human writing.",
        ],
    },
    {
        "no": 5, "icon": "📱",
        "title_ko": "디지털·AI 시대에 가장 적합한 문자",
        "title_en": "The Most Digital- and AI-Friendly Script",
        "body_ko": [
            "뜻밖에도 한글은 현대 정보 기술 시대에 더 빛나는 문자입니다.",
            "스마트폰 입력 속도: 천지인·쿼티 모두 영어 못지않게 빠르며, 자음·모음 24자로 11,172개 음절을 표현",
            "유니코드 효율성: 한글 음절 하나가 영어 단어 하나만큼의 정보를 담음",
            "음성 인식·합성 정확도: 표음문자라 AI가 한글 ↔ 음성 변환을 매우 정확하게 처리",
            "한류 콘텐츠의 핵심: K-팝·K-드라마·웹툰의 글로벌 확산과 함께 한글 학습자 폭증",
            "→ \"세종대왕이 600년 후 디지털 시대를 예견하고 만든 것 같다\"는 말이 나올 정도로, 시간이 갈수록 그 우수성이 더 드러나는 문자입니다.",
        ],
        "body_en": [
            "Surprisingly, Hangul shines even brighter in the digital era.",
            "Mobile typing speed: Cheonjiin and QWERTY layouts are as fast as English typing. 24 letters generate 11,172 possible syllables.",
            "Unicode efficiency: One Korean syllable carries as much information as an entire English word.",
            "Voice recognition & synthesis: Because Hangul is phonemic, AI handles Korean ↔ speech conversion with high accuracy.",
            "Core of the Hallyu wave: K-pop, K-drama, and webtoons drive a global surge in Korean learners.",
            "→ \"It feels like Sejong foresaw the digital age 600 years ago.\" Hangul's brilliance only grows with time.",
        ],
    },
]

# 5 comparisons Hangul vs Hanja
COMPARISONS = [
    {
        "no": 1, "icon": "🔤",
        "title_ko": "표음문자 vs 표의문자 — 가장 본질적 차이",
        "title_en": "Phonemic vs Logographic — The Most Fundamental Difference",
        "rows_ko": [
            ("한글", "소리를 적는 문자. 글자만 보면 어떻게 읽는지 안다. 모든 글자가 자기 소리를 가짐."),
            ("한자", "뜻을 적는 문자. 어떤 뜻인지 안다. 글자와 소리가 별개 — 따로 외워야 함."),
        ],
        "rows_en": [
            ("Hangul", "Records sounds. The letter shows you how to read it. Every letter carries its own sound."),
            ("Hanja", "Records meanings. The character shows you what it means. Sound is separate — must be memorized."),
        ],
        "note_ko": "→ 한자 \"山\"을 보면 산이라는 뜻은 알지만, 한국에선 \"산\", 중국에선 \"샨(shān)\", 일본에선 \"야마(やま)\" 또는 \"산(さん)\"으로 다르게 읽힙니다. 반면 한글 \"산\"은 누가 봐도 무조건 \"san\" 소리로만 읽힙니다.",
        "note_en": "→ The Hanja '山' means mountain in every East Asian language, but it's pronounced 'san' in Korean, 'shān' in Chinese, and 'yama' or 'san' in Japanese. The same character is read differently across countries. Meanwhile, the Hangul '산' is always read as 'san' — the sound is built into the letters themselves.",
    },
    {
        "no": 2, "icon": "🔢",
        "title_ko": "글자 수: 24자 vs 5만~8만 자",
        "title_en": "Number of Characters: 24 vs 50,000~80,000",
        "rows_ko": [
            ("한글", "기본 자모 24자 (자음 14 + 모음 10). 음절 블록 11,172개 (이론상). 하루 만에 다 외울 수 있음."),
            ("한자", "강희자전 기준 약 47,000자. 현대 중국 일상 약 3,500~5,000자. 평생 배워도 다 모름."),
        ],
        "rows_en": [
            ("Hangul", "24 basic letters (14 consonants + 10 vowels). 11,172 possible syllable blocks. Learnable in a single day."),
            ("Hanja", "About 47,000 characters in the Kangxi Dictionary. ~3,500–5,000 used in daily modern Chinese. Lifetime is not enough to master all."),
        ],
        "note_ko": "→ 중국 소학교 6년에 약 3,000자, 신문 읽으려면 최소 3,500자, 고전 읽으려면 8,000자 이상 필요. 한글은 단 24자.",
        "note_en": "→ Chinese elementary students learn about 3,000 characters over 6 years. Reading newspapers requires 3,500+. Classical Chinese requires 8,000+. Hangul: only 24 letters.",
    },
    {
        "no": 3, "icon": "⏱️",
        "title_ko": "학습 난이도: 하루~열흘 vs 수십 년",
        "title_en": "Learning Difficulty: A Day to Ten Days vs Decades",
        "rows_ko": [
            ("한글", "약 2~5시간이면 모든 자모를 익히고 글자를 읽을 수 있음."),
            ("한자", "HSK 6급(고급) 도달까지 평균 2,000~3,000시간 필요. 간체자만 해도 3,000자 이상 암기 필수."),
        ],
        "rows_en": [
            ("Hangul", "About 2–5 hours to master all the letters and start reading."),
            ("Hanja/Chinese", "On average, 2,000–3,000 hours to reach HSK 6 (advanced). Even simplified characters require memorizing 3,000+ characters."),
        ],
        "note_ko": "→ 세종대왕 훈민정음 서문: \"슬기로운 사람은 아침이 끝나기도 전에 깨치고, 어리석은 사람도 열흘이면 배울 수 있다.\" 이 학습 효율의 차이가 한국의 세계 최고 수준 문해율을 만들어냈습니다.",
        "note_en": "→ Sejong's Hunminjeongeum preface: \"The wise can master it before morning ends, and even the foolish can learn it within ten days.\" This dramatic difference in learning efficiency made Korea one of the most literate countries in the world.",
    },
    {
        "no": 4, "icon": "🔨",
        "title_ko": "창제 방식: 인공 설계 vs 자연 발생",
        "title_en": "Creation: Engineered Design vs Natural Evolution",
        "rows_ko": [
            ("한글", "1443년 세종대왕이 의도적으로 설계. 24자 모든 글자가 일정한 원리에 따라 만들어짐."),
            ("한자", "약 3,300년 전 갑골문에서 자연 발생해 진화. 누가·언제·왜 만들었는지 명확하지 않음. 상형(象形) → 회의(會意) → 형성(形聲)으로 진화."),
        ],
        "rows_en": [
            ("Hangul", "Deliberately engineered in 1443 by King Sejong. All 24 letters follow consistent design principles."),
            ("Hanja", "Naturally evolved from oracle bone script ~3,300 years ago. Creator, date, and purpose unclear. Evolved from pictographs → ideographs → phono-semantic compounds."),
        ],
        "note_ko": "→ 한자는 약 3,000년에 걸쳐 자연스럽게 진화한 결과이고, 한글은 한 시점에 한 사람(과 그의 집현전 학자들)이 공학적으로 설계한 작품입니다. 그래서 한글에는 \"버려진 글자\"가 없고, 한자에는 잘 안 쓰는 글자가 수만 자 쌓여 있습니다.",
        "note_en": "→ Hanja is the result of 3,000 years of natural evolution. Hangul is an engineered work designed at a single point in time by one person (and his royal scholars). That's why Hangul has no \"abandoned letters,\" while Hanja accumulates tens of thousands of rarely-used characters.",
    },
    {
        "no": 5, "icon": "💻",
        "title_ko": "디지털·입력 효율성: 직관적 조합 vs 변환 필수",
        "title_en": "Digital Input: Intuitive Composition vs Required Conversion",
        "rows_ko": [
            ("한글", "자음·모음 24자만 키보드에 있으면 됨. 천지인 입력법(8키), 쿼티 입력법(22키) 모두 직접 타이핑. 자모 → 즉시 글자가 완성."),
            ("한자", "한자를 직접 입력할 방법이 없어 반드시 변환 과정을 거쳐야 함. 병음 입력: 알파벳으로 발음 친 뒤 후보 한자 중 선택 → 동음이의어 처리 필요. 창힐·오필 입력: 부수·획을 분해 입력 → 학습이 매우 어려움. 한글보다 약 30~40% 느림."),
        ],
        "rows_en": [
            ("Hangul", "Only 24 letters needed on a keyboard. Cheonjiin (8-key) or QWERTY (22-key) — both allow direct typing. Letters → instant syllables."),
            ("Hanja/Chinese", "Cannot type characters directly — conversion is always required. Pinyin: type alphabetic pronunciation, then pick from homophone candidates. Cangjie/Wubi: decompose radicals and strokes — very steep learning curve. 30–40% slower than Hangul."),
        ],
        "note_ko": "→ 모바일·SNS·AI 음성 인식 시대에 한글이 압도적으로 빠르고 정확합니다. 한국이 IT 강국이 된 이면에는 한글의 디지털 친화성이라는 숨은 자산이 있습니다.",
        "note_en": "→ In the era of mobile messaging, social media, and AI voice recognition, Hangul is dramatically faster and more accurate. Korea's rise as an IT powerhouse owes much to Hangul's hidden digital advantage.",
    },
]

# Summary table
SUMMARY_ROWS = [
    ("문자 성격 · Script Type",   "표음 (소리) · Phonemic (sound)",       "표의 (뜻) · Logographic (meaning)"),
    ("글자 수 · Characters",      "24자 · 24 letters",                     "5만~8만 자 · 50,000~80,000"),
    ("학습 기간 · Learning",      "하루~열흘 · 1 day – 10 days",          "수십 년 · Decades"),
    ("창제 · Origin",             "1443년 인공 설계 · 1443 engineered",   "자연 진화 · Natural evolution"),
    ("디지털 입력 · Digital Input","직관적·즉시 · Direct & instant",       "변환 필요·복잡 · Conversion required"),
    ("창제 기록 · Records",       "『훈민정음 해례본』 (UNESCO)",          "명확한 기록 없음 · No clear records"),
]

def feature_block(f):
    body_ko = "".join(f"<p class='body-ko'>{escape(line)}</p>" for line in f['body_ko'])
    body_en = "".join(f"<p class='body-en'>{escape(line)}</p>" for line in f['body_en'])
    return f"""
<div class="feature-card">
  <div class="feature-header">
    <span class="feature-num">{f['no']}</span>
    <span class="feature-icon">{f['icon']}</span>
    <div class="feature-titles">
      <div class="title-ko">{escape(f['title_ko'])}</div>
      <div class="title-en">{escape(f['title_en'])}</div>
    </div>
  </div>
  <div class="feature-body">
    <div class="lang-col"><div class="lang-label">한국어</div>{body_ko}</div>
    <div class="lang-col"><div class="lang-label">English</div>{body_en}</div>
  </div>
</div>
"""

def comparison_block(c):
    rows_ko = "".join(f"<tr><td class='lbl'>{escape(label)}</td><td>{escape(text)}</td></tr>" for label, text in c['rows_ko'])
    rows_en = "".join(f"<tr><td class='lbl'>{escape(label)}</td><td>{escape(text)}</td></tr>" for label, text in c['rows_en'])
    return f"""
<div class="comp-card">
  <div class="comp-header">
    <span class="comp-num">{c['no']}</span>
    <span class="comp-icon">{c['icon']}</span>
    <div class="comp-titles">
      <div class="title-ko">{escape(c['title_ko'])}</div>
      <div class="title-en">{escape(c['title_en'])}</div>
    </div>
  </div>
  <div class="comp-tables">
    <table class="comp-table"><tbody>{rows_ko}</tbody></table>
    <table class="comp-table en"><tbody>{rows_en}</tbody></table>
  </div>
  <div class="comp-note"><strong>한국어:</strong> {escape(c['note_ko'])}</div>
  <div class="comp-note en"><strong>English:</strong> {escape(c['note_en'])}</div>
</div>
"""

summary_html = "".join(
    f"<tr><td class='lbl'>{escape(item)}</td><td class='hg'>{escape(hg)}</td><td class='hj'>{escape(hj)}</td></tr>"
    for item, hg, hj in SUMMARY_ROWS
)

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>한글 vs 한자 — 언어 문화적 특징과 비교 / Hangul vs Hanja</title>
<style>
  @page { size: A4; margin: 16mm 14mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color: #1a1a2e; margin: 0; line-height: 1.6; }
  .page-break { page-break-before: always; }

  .cover { text-align:center; padding:80px 20px 40px; border-bottom:4px solid #C0392B; margin-bottom:30px; }
  .cover .label { font-size:13px; font-weight:700; letter-spacing:4px; color:#C0392B; text-transform:uppercase; margin-bottom:18px; }
  .cover h1 { font-size:38px; margin:0 0 10px; color:#1a1a2e; font-weight:800; line-height:1.2; }
  .cover .h1-en { font-size:24px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:14px; color:#555; max-width:620px; margin:0 auto; line-height:1.8; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }

  h2.section-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:18px 24px; margin:40px 0 22px; font-size:22px; border-left:6px solid #C0392B; border-radius:6px; }
  h2.section-h .en { display:block; font-size:14px; font-weight:600; opacity:0.8; margin-top:4px; }

  .feature-card { background:#fff; border-radius:14px; padding:20px 22px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border-top:4px solid #C0392B; }
  .feature-header { display:flex; align-items:center; gap:14px; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #f1ede5; }
  .feature-num { background:#C0392B; color:#fff; font-weight:800; font-size:18px; min-width:36px; height:36px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; }
  .feature-icon { font-size:30px; }
  .feature-titles .title-ko { font-size:16px; font-weight:800; color:#1a1a2e; }
  .feature-titles .title-en { font-size:13px; color:#1A4A8A; font-weight:600; font-style:italic; margin-top:2px; }
  .feature-body { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
  .lang-col { background:#fafafa; padding:14px 16px; border-radius:8px; }
  .lang-label { font-size:10px; font-weight:800; letter-spacing:2px; color:#C0392B; margin-bottom:8px; }
  .lang-col .body-ko { font-size:12.5px; line-height:1.65; margin:0 0 6px; color:#1a1a2e; }
  .lang-col .body-en { font-size:12px; line-height:1.65; margin:0 0 6px; color:#1A4A8A; font-style:italic; }

  .comp-card { background:#fff; border-radius:14px; padding:20px 22px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border-top:4px solid #1A4A8A; }
  .comp-header { display:flex; align-items:center; gap:14px; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #f1ede5; }
  .comp-num { background:#1A4A8A; color:#fff; font-weight:800; font-size:18px; min-width:36px; height:36px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; }
  .comp-icon { font-size:30px; }
  .comp-titles .title-ko { font-size:16px; font-weight:800; color:#1a1a2e; }
  .comp-titles .title-en { font-size:13px; color:#1A4A8A; font-weight:600; font-style:italic; margin-top:2px; }
  .comp-tables { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:10px; }
  .comp-table { width:100%; border-collapse:collapse; font-size:11.5px; background:#fafafa; border-radius:8px; overflow:hidden; }
  .comp-table.en td { color:#1A4A8A; font-style:italic; }
  .comp-table td { padding:7px 10px; border-bottom:1px solid #ececec; vertical-align:top; line-height:1.5; }
  .comp-table td.lbl { font-weight:800; color:#C0392B; width:80px; }
  .comp-table tr:last-child td { border-bottom:none; }
  .comp-note { font-size:12px; color:#1a1a2e; background:#fef3c7; padding:8px 12px; border-radius:6px; margin-top:8px; line-height:1.6; }
  .comp-note.en { color:#1A4A8A; font-style:italic; background:#f0f5ff; }

  .summary-section { background:#fff; border-radius:14px; padding:24px; margin-top:30px; box-shadow:0 4px 16px rgba(0,0,0,0.07); }
  .summary-section h3 { font-size:22px; color:#1a1a2e; margin:0 0 6px; }
  .summary-section .en-sub { font-size:13px; color:#1A4A8A; font-style:italic; margin-bottom:18px; }
  .summary-table { width:100%; border-collapse:collapse; font-size:12.5px; }
  .summary-table th { background:#1a1a2e; color:#fff; padding:10px; font-weight:700; }
  .summary-table td { padding:9px 12px; border-bottom:1px solid #ececec; vertical-align:top; }
  .summary-table td.lbl { font-weight:800; color:#1a1a2e; background:#fafafa; }
  .summary-table td.hg { color:#C0392B; font-weight:600; }
  .summary-table td.hj { color:#1A4A8A; font-weight:600; }

  .end-note { text-align:center; margin:40px 0 20px; padding:30px 24px; background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; border-radius:14px; }
  .end-note p { margin:6px 0; font-size:14px; opacity:0.92; }
  .end-note .ko { font-size:16px; font-weight:700; color:#fbbf24; }
</style></head><body>

<div class="cover">
  <div class="label">KR GUIDE · Bilingual Reference</div>
  <h1>한글의 언어 문화적 특징과<br>한자와의 비교</h1>
  <div class="h1-en">Hangul: Cultural Features &amp; Comparison with Hanja</div>
  <p class="desc">세종대왕이 1443년 창제한 한글의 5가지 언어 문화적 특징과, 동아시아 한자와의 5가지 본질적 차이를 한국어·영어 병기로 정리한 자료입니다.<br>
  A bilingual reference (Korean &amp; English) on Hangul's 5 cultural-linguistic features and 5 fundamental differences from Chinese Hanja.</p>
  <div class="features">
    <span class="feat">5 Hangul Features</span>
    <span class="feat">5 Hangul vs Hanja Comparisons</span>
    <span class="feat">Summary Table</span>
    <span class="feat">한·영 병기</span>
  </div>
</div>

<h2 class="section-h">🌟 한글의 언어 문화적 특징 5가지<span class="en">5 Cultural-Linguistic Features of Hangul</span></h2>
""" + "".join(feature_block(f) for f in FEATURES) + """

<div class="page-break"></div>

<h2 class="section-h">⚖️ 한자와의 본질적 차이 5가지<span class="en">5 Fundamental Differences from Hanja (Chinese Characters)</span></h2>
""" + "".join(comparison_block(c) for c in COMPARISONS) + """

<div class="summary-section">
  <h3>📊 한눈에 보는 핵심 비교</h3>
  <div class="en-sub">At-a-Glance Summary</div>
  <table class="summary-table">
    <thead><tr><th>비교 항목 · Category</th><th>한글 · Hangul</th><th>한자 · Hanja</th></tr></thead>
    <tbody>""" + summary_html + """</tbody>
  </table>
</div>

<div class="end-note">
  <p class="ko">"슬기로운 사람은 아침이 끝나기도 전에 깨치고,<br>어리석은 사람도 열흘이면 배울 수 있다."</p>
  <p>"The wise can master it before morning ends, and even the foolish can learn it within ten days."</p>
  <p style="opacity:0.7;font-size:12px;margin-top:14px;">— 세종대왕 · 『훈민정음 해례본』 (1446) / King Sejong · Hunminjeongeum Haeryebon</p>
</div>

</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML -> {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

if PDF_OUT.exists(): PDF_OUT.unlink()
url = f"file:///{HTML_OUT.as_posix()}"
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=180)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  -> {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
