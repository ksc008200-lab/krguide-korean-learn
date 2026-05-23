"""
Build a styled PDF from the adjectives/adverbs/idioms Google Doc.

Source format per entry (3 lines):
  단어 (English)
  한국어 예문1. (English translation.)
  한국어 예문2. (English translation.)
"""
import re, subprocess, time
from pathlib import Path
from html import escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "adjectives_adverbs.txt"
HTML_OUT = ROOT / "adjectives-adverbs-with-examples.html"
PDF_OUT  = ROOT / "adjectives-adverbs-with-examples.pdf"

raw_lines = SRC.read_text(encoding="utf-8").splitlines()
# Strip whitespace, drop empty lines
lines = [ln.strip() for ln in raw_lines if ln.strip()]

section_re = re.compile(r"^\d+\.\s+(.+?)\s+\((.+?)\)\s*$")
# Word line: "단어 (English meaning)"  — single line, ends with closing paren
# Example line: "한국어 (English).", probably with paren near end too
# Distinguish by content: word lines tend to be short. Use heuristic: a "word" line
# starts a new entry; the next two lines are examples.

# Strategy: scan sequentially. When we see a section header, set current.
# Else, peek 3 lines: first = word, second/third = examples (if available).
# To avoid mis-parsing, use the fact that example lines contain " ("  with English translation
# in parens AND usually end with ")", same as word lines.
# Best heuristic: word lines contain no Korean sentence punctuation like '.' ',' '?'
# inside the Korean part, while examples do.

def is_section_header(s):
    return bool(section_re.match(s))

def parse_word_line(s):
    """Return (korean_word, english_meaning) or None if it doesn't look like a word line."""
    m = re.match(r"^(.+?)\s+\((.+?)\)\s*$", s)
    if not m: return None
    ko = m.group(1).strip()
    en = m.group(2).strip()
    # Word line: Korean part is short (<= 20 chars) and contains no sentence-ending punctuation
    if len(ko) > 25:
        return None
    if any(c in ko for c in ".?!,"):
        return None
    # English meaning is short, no full sentence
    return (ko, en)

def parse_example_line(s):
    """Return (korean_sentence, english_sentence)."""
    # Match: "<Korean...>. (<English>.)" — split on the last " (...)"
    # Find rightmost " (" that opens the final paren group
    # Simple approach: regex
    m = re.match(r"^(.+?)\s+\((.+)\)\s*$", s)
    if not m:
        return (s, "")
    return (m.group(1).strip(), m.group(2).strip())

rows = []
current_sec = "(unknown)"
i = 0
while i < len(lines):
    line = lines[i]
    if is_section_header(line):
        m = section_re.match(line)
        ko_name = m.group(1).strip()
        en_paren = m.group(2).strip()
        # Strip range
        en_clean = re.sub(r",\s*\d+\s*~\s*\d+\s*$", "", en_paren).strip()
        current_sec = f"{ko_name} · {en_clean}"
        i += 1
        continue
    # Try to parse a word entry: next 3 lines = word, ex1, ex2
    wl = parse_word_line(line)
    if wl:
        ko_word, en_meaning = wl
        ex1_ko, ex1_en, ex2_ko, ex2_en = "", "", "", ""
        if i+1 < len(lines):
            ex1_ko, ex1_en = parse_example_line(lines[i+1])
        if i+2 < len(lines):
            # Make sure line i+2 isn't actually a new word line or section
            nxt = lines[i+2]
            if not is_section_header(nxt) and not parse_word_line(nxt):
                ex2_ko, ex2_en = parse_example_line(nxt)
                i += 3
            else:
                i += 2
        else:
            i += 2
        rows.append((current_sec, ko_word, en_meaning, ex1_ko, ex1_en, ex2_ko, ex2_en))
    else:
        # Skip introductory paragraphs
        i += 1

print(f"Parsed {len(rows)} entries across {len({r[0] for r in rows})} categories")

items = []
last = None
for i, (sec, ko, en, e1k, e1e, e2k, e2e) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="4">{escape(sec)}</td></tr>')
        last = sec
    ex_html = ""
    if e1k:
        ex_html += f'<div class="ex"><span class="ko">{escape(e1k)}</span><span class="en">{escape(e1e)}</span></div>'
    if e2k:
        ex_html += f'<div class="ex"><span class="ko">{escape(e2k)}</span><span class="en">{escape(e2e)}</span></div>'
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(ko)}</td>'
        f'<td class="en-mean">{escape(en)}</td>'
        f'<td class="ex-cell">{ex_html}</td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>한국어 형용사·부사·관용구 가이드</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:620px; margin:0 auto; line-height:1.7; }
  table { width:100%; border-collapse:collapse; font-size:11px; table-layout:fixed; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:30px;} th.k-col{width:85px;} th.en-col{width:110px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#1a1a2e; font-size:13px; }
  td.en-mean { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.ex-cell .ex { margin-bottom:3px; }
  td.ex-cell .ex .ko { display:block; color:#C0392B; font-size:10.5px; font-weight:600; }
  td.ex-cell .ex .en { display:block; color:#666; font-style:italic; font-size:10px; margin-top:1px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; letter-spacing:1.2px; padding:8px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
</style></head><body>

<div class="cover">
  <div class="label">Korean Adjectives · Adverbs · Idioms</div>
  <h1>한국어 형용사·부사·관용구 가이드</h1>
  <div class="kr">필수 표현 종합 · 예문 포함</div>
  <p class="desc">관형사·고급 형용사·부사·접속사·조사·관용구·속담·사자성어·의성·의태어까지 — 카테고리별 단어와 영어 의미, 한국어 예문 2개씩 정리.</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">한국어</th>
    <th class="en-col">English</th>
    <th>예문 Examples</th>
  </tr></thead>
  <tbody>
""" + "\n".join(items) + """
  </tbody>
</table>

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
