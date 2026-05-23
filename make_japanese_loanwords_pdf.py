"""
Build Japanese-loanwords-in-Korean PDF in the same style as other guides.
Source: japanese_loanwords.txt
"""
import re, subprocess, time
from pathlib import Path
from html import escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "japanese_loanwords.txt"
HTML_OUT = ROOT / "japanese-loanwords-with-examples.html"
PDF_OUT  = ROOT / "japanese-loanwords-with-examples.pdf"

lines = SRC.read_text(encoding="utf-8").splitlines()

# Detect section headers (two patterns):
#   "1~20: 생활 및 일상 어휘"
#   "1. 법률 및 행정 용어 (1~40)"
section_re_a = re.compile(r"^\s*(\d+)~(\d+)\s*:\s*(.+?)\s*$")
section_re_b = re.compile(r"^\s*(\d+)\.\s+(.+?)\s+\((\d+)\s*~\s*(\d+)\)\s*$")

# Entry pattern: 단어(원래 의미): "예문1", "예문2"
entry_re = re.compile(
    r'^\s*([^\s(][^()]*?)\s*\(([^)]+)\)\s*:\s*"(.+?)"\s*[,，]\s*"(.+?)"',
)

rows = []
current = "(미분류)"
for raw in lines:
    line = raw.strip()
    if not line:
        continue
    # Skip intro/instructional paragraphs (very long, contain ':' but not entry format)
    if "(중복 제거)" in line or line.startswith("괄호 안에는"):
        continue
    if line.startswith("한국어 속에는"):
        continue
    if line.startswith("가장 딱딱하고"):
        continue
    ma = section_re_a.match(line)
    if ma:
        current = ma.group(3).strip()
        continue
    mb = section_re_b.match(line)
    if mb:
        current = mb.group(2).strip()
        continue
    me = entry_re.match(line)
    if me:
        word, orig, ex1, ex2 = me.groups()
        rows.append((current, word.strip(), orig.strip(), ex1.strip(), ex2.strip()))
        continue
    # Try a more permissive entry pattern (single example or different quotes)
    me2 = re.match(r'^\s*([^\s(][^()]*?)\s*\(([^)]+)\)\s*:\s*(.+)$', line)
    if me2:
        word, orig, rest = me2.groups()
        # split rest into examples by comma between quoted strings
        exs = re.findall(r'"([^"]+)"', rest)
        if len(exs) >= 1:
            ex1 = exs[0]
            ex2 = exs[1] if len(exs) >= 2 else ""
            rows.append((current, word.strip(), orig.strip(), ex1, ex2))

print(f"Parsed {len(rows)} entries across {len({r[0] for r in rows})} categories")

# Build HTML
items = []
last = None
for i, (sec, word, orig, ex1, ex2) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="5">{escape(sec)}</td></tr>')
        last = sec
    ex_html = f'<span class="ex-row">{escape(ex1)}</span>'
    if ex2:
        ex_html += f'<span class="ex-row">{escape(ex2)}</span>'
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(word)}</td>'
        f'<td class="en">{escape(orig)}</td>'
        f'<td class="ex">{ex_html}</td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>일본어 외래어 · Japanese Loanwords in Korean</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:32px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:600px; margin:0 auto; line-height:1.7; }
  table { width:100%; border-collapse:collapse; font-size:11px; table-layout:fixed; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:34px;} th.k-col{width:95px;} th.en-col{width:115px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#C0392B; font-size:13px; }
  td.en  { color:#1A4A8A; font-size:11.5px; font-weight:600; }
  td.ex .ex-row { display:block; color:#555; font-size:10.5px; line-height:1.4; margin-bottom:2px; }
  td.ex .ex-row:first-child { color:#1a1a2e; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; letter-spacing:1.2px; padding:8px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
</style></head><body>

<div class="cover">
  <div class="label">Japanese Loanwords in Korean</div>
  <h1>일본어 외래어 사전</h1>
  <div class="kr">우리말 속 일본어 표현 · 순화어 가이드</div>
  <p class="desc">By field — the Japanese-origin word used in Korean, its native Korean equivalent (순화어), and two example sentences for natural usage in context.</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">일본어 외래어</th>
    <th class="en-col">우리말 (순화어)</th>
    <th>예문 Example Sentences</th>
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
