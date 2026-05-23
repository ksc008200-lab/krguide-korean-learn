"""
Build 500-honorifics PDF in the same style as the verbs/nouns/adverbs.
Source: honorifics_500.txt (downloaded from Google Docs).
"""
import re, subprocess, time
from pathlib import Path
from html import escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "honorifics_500.txt"
HTML_OUT = ROOT / "500-honorifics-with-meanings.html"
PDF_OUT  = ROOT / "500-honorifics-with-meanings.pdf"

text = SRC.read_text(encoding="utf-8")

# Find the start of the English-paired section (sections labeled with English in parentheses).
# Pattern: lines like "1. 일상적인 종결 어미 (Daily Ending Phrases, 1-20)"
start_match = re.search(r"^\s*1\.\s+일상적인 종결 어미\s+\(Daily Ending Phrases", text, re.M)
assert start_match, "Could not find start of English section"
body = text[start_match.start():]

# Walk line by line; track current section and accumulate entries
rows = []      # (section_label, ko_expr, en_meaning)
current_sec = ""
n = 0
sec_re = re.compile(r"^\s*(\d+)\.\s+(.+?)\s+\((.+?)\)\s*$")
for raw in body.splitlines():
    line = raw.strip()
    if not line:
        continue
    msec = sec_re.match(line)
    if msec:
        # Section header
        num, ko_name, en_name = msec.groups()
        # Strip trailing range like ", 401-420"
        en_clean = re.sub(r",\s*\d+\s*-\s*\d+\s*$", "", en_name)
        current_sec = f"{num}. {ko_name.strip()} · {en_clean.strip()}"
        continue
    # Entry: split on ' / '
    # Some lines: "안녕하세요? / Hello. / How are you?"
    # Some:       "고맙습니다 / 감사합니다. / Thank you. / I appreciate it."
    # Heuristic: split on " / ". The Korean parts are those that contain Hangul; English parts don't.
    parts = [p.strip() for p in line.split(" / ") if p.strip()]
    if len(parts) < 2:
        continue
    ko_parts, en_parts = [], []
    for p in parts:
        if re.search(r"[가-힣]", p):
            # If we've already started collecting English, this Korean snippet belongs to meanings (rare)
            if en_parts:
                en_parts.append(p)
            else:
                ko_parts.append(p)
        else:
            en_parts.append(p)
    if not ko_parts or not en_parts:
        continue
    ko_expr = " / ".join(ko_parts)
    en_meaning = " / ".join(en_parts)
    n += 1
    rows.append((current_sec, ko_expr, en_meaning))

print(f"Parsed {n} entries")

# Build HTML
items = []
last = None
for i, (sec, ko, en) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="3">{escape(sec)}</td></tr>')
        last = sec
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(ko)}</td>'
        f'<td class="en">{escape(en)}</td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>500 Korean Honorific Expressions · 존댓말 표현 500개</title>
<style>
  @page { size: A4; margin: 16mm 14mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.5; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:32px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:600px; margin:0 auto; line-height:1.7; }
  table { width:100%; border-collapse:collapse; font-size:11.5px; table-layout:fixed; }
  thead th { background:#1a1a2e; color:#fff; padding:8px 8px; font-size:10.5px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:40px;} th.k-col{width:42%;}
  td { padding:7px 9px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10.5px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:13px; line-height:1.5; }
  td.en  { color:#1A4A8A; font-size:11.5px; line-height:1.5; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; letter-spacing:1.2px; padding:9px 14px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
</style></head><body>

<div class="cover">
  <div class="label">Korean Honorific Expressions</div>
  <h1>500 Honorific Expressions</h1>
  <div class="kr">존댓말 표현 500개 · 격조 있는 한국어</div>
  <p class="desc">By category — Korean honorific expression and its English meaning, covering everyday speech, business etiquette, formal occasions, and poetic closings.</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">한국어 표현</th>
    <th>English Meaning</th>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=180)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
