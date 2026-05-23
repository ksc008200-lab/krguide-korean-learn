"""
Build a clean standalone HTML for the 200 verbs (numbered) and print to PDF.
"""
import re
import subprocess
from pathlib import Path
from html import unescape, escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "200-verbs-numbered.html"
PDF_OUT  = ROOT / "200-verbs-numbered.pdf"

html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch39">.*?(?=<div class="chapter" id="ch40")', html, re.S)
block = m.group(0)

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(s).strip()

rows = []
current = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="5"' in row:
        txt = clean(row)
        if txt and not txt.startswith("기본형"):
            current = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 5:
        continue
    g, p, e, pol, pa = [clean(c) for c in cells]
    if g == "기본형":
        continue
    rows.append((current, g, p, e, pol, pa))

# Build HTML
items = []
last = None
n = 0
for sec, g, p, e, pol, pa in rows:
    if sec != last:
        items.append(f'<tr class="section"><td colspan="6">{escape(sec)}</td></tr>')
        last = sec
    n += 1
    items.append(
        f'<tr>'
        f'<td class="num">{n}</td>'
        f'<td class="k">{escape(g)}</td>'
        f'<td class="r">{escape(p)}</td>'
        f'<td class="en">{escape(e)}</td>'
        f'<td class="k">{escape(pol)}</td>'
        f'<td class="k">{escape(pa)}</td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>200 Essential Korean Verbs · 필수 동사 200개</title>
<style>
  @page { size: A4; margin: 18mm 16mm; }
  * { box-sizing: border-box; }
  body {
    font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
    color: #1a1a2e;
    margin: 0;
    line-height: 1.5;
  }
  .cover {
    text-align: center;
    padding: 60px 20px 30px;
    border-bottom: 4px solid #C0392B;
    margin-bottom: 24px;
  }
  .cover .label {
    font-size: 12px; font-weight: 700; letter-spacing: 3px;
    color: #C0392B; text-transform: uppercase; margin-bottom: 14px;
  }
  .cover h1 {
    font-size: 36px; margin: 0 0 8px;
    color: #1a1a2e; font-weight: 800;
  }
  .cover .kr {
    font-size: 22px; color: #1A4A8A; font-weight: 700; margin: 0 0 22px;
  }
  .cover .desc {
    font-size: 13px; color: #555; max-width: 540px; margin: 0 auto;
    line-height: 1.7;
  }
  table {
    width: 100%; border-collapse: collapse; font-size: 12px;
    table-layout: fixed;
  }
  thead th {
    background: #1a1a2e; color: #fff; padding: 9px 8px;
    font-size: 11px; letter-spacing: 0.5px;
    border-bottom: 2px solid #C0392B;
  }
  th.num-col { width: 36px; }
  th.k-col { width: 80px; }
  th.r-col { width: 70px; }
  th.en-col { width: 110px; }
  td {
    padding: 6px 8px; border-bottom: 1px solid #e5e5ea;
    vertical-align: top; word-break: keep-all;
  }
  tr:nth-child(even) td { background: #fafafa; }
  td.num { text-align: center; color: #888; font-weight: 600; font-size: 11px; }
  td.k { font-weight: 600; color: #1a1a2e; font-size: 13px; }
  td.r { color: #6b6b6b; font-style: italic; font-size: 11px; }
  td.en { color: #1A4A8A; }
  tr.section td {
    background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
    color: #fff; font-weight: 800; font-size: 12px;
    letter-spacing: 1.2px; padding: 8px 12px;
    text-transform: uppercase;
  }
  tr.section td::before { content: "▸  "; color: #f97316; }
</style>
</head><body>

<div class="cover">
  <div class="label">Korean Essential Verbs</div>
  <h1>200 Essential Korean Verbs</h1>
  <div class="kr">필수 동사 200개 · 카테고리별 완전 참고표</div>
  <p class="desc">By category — Korean dictionary form · Romanization · English meaning · Polite form (해요체) · Past tense (과거형)</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">기본형</th>
    <th class="r-col">발음</th>
    <th class="en-col">English</th>
    <th class="k-col">해요체</th>
    <th class="k-col">과거형</th>
  </tr></thead>
  <tbody>
""" + "\n".join(items) + """
  </tbody>
</table>

</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML  → {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

# Print to PDF via Edge
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url  = f"file:///{HTML_OUT.as_posix()}"
if PDF_OUT.exists(): PDF_OUT.unlink()
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url],
               capture_output=True, timeout=120)
import time; time.sleep(2)
if PDF_OUT.exists():
    print(f"PDF   → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
else:
    print("PDF generation failed")
