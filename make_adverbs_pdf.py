"""
Build 200-adverbs PDF — examples already in HTML, just restyle.
"""
import re, subprocess, time
from pathlib import Path
from html import unescape, escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "200-adverbs-with-examples.html"
PDF_OUT  = ROOT / "200-adverbs-with-examples.pdf"

html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch40">.*?(?=<div class="chapter" id="ch41")', html, re.S)
if not m:
    m = re.search(r'<div class="chapter" id="ch40">.*?(?=<!--|<script|<footer|</body>)', html, re.S)
block = m.group(0)

def clean(s):
    s = re.sub(r"<em>", "**", s)
    s = re.sub(r"</em>", "**", s)
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(s).strip()

rows = []
current = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="4"' in row:
        txt = clean(row)
        if txt and not txt.startswith("부사"):
            current = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 4: continue
    adv, pron, eng, ex = [clean(c) for c in cells]
    if adv == "부사": continue
    rows.append((current, adv, pron, eng, ex))

print(f"Extracted {len(rows)} adverbs")

items = []
last = None
for i, (sec, adv, pron, eng, ex) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="5">{escape(sec)}</td></tr>')
        last = sec
    # ex contains " — " separator between ko & en, with **bold** markers
    ex_html = escape(ex).replace("**", "<em>")
    # Toggle <em>: every odd occurrence opens, even closes
    parts = ex_html.split("<em>")
    rebuilt = parts[0]
    for j, p in enumerate(parts[1:], 1):
        rebuilt += ("<em>" if j % 2 == 1 else "</em>") + p
    # split into ko/en at " — " or " – "
    sep = None
    for s in [" — ", " – ", " - "]:
        if s in rebuilt:
            ex_ko, ex_en = rebuilt.split(s, 1)
            sep = s; break
    if sep is None:
        ex_ko, ex_en = rebuilt, ""
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(adv)}</td>'
        f'<td class="r">{escape(pron)}</td>'
        f'<td class="en">{escape(eng)}</td>'
        f'<td class="ex"><span class="ex-ko">{ex_ko.strip()}</span><span class="ex-en">{ex_en.strip()}</span></td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>200 Essential Korean Adverbs · 예문 포함</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:34px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:580px; margin:0 auto; line-height:1.7; }
  table { width:100%; border-collapse:collapse; font-size:11px; table-layout:fixed; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:30px;} th.k-col{width:85px;} th.r-col{width:75px;} th.en-col{width:130px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:13px; }
  td.r   { color:#6b6b6b; font-style:italic; font-size:11px; }
  td.en  { color:#1A4A8A; font-size:11px; }
  td.ex .ex-ko { display:block; color:#C0392B; font-weight:600; font-size:11px; }
  td.ex .ex-en { display:block; color:#666; font-style:italic; font-size:10px; margin-top:1px; }
  td.ex em { font-style:normal; background:#fef3c7; color:#92400e; padding:0 3px; border-radius:3px; font-weight:700; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; letter-spacing:1.2px; padding:8px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
</style></head><body>

<div class="cover">
  <div class="label">Korean Essential Adverbs · with Examples</div>
  <h1>200 Essential Korean Adverbs</h1>
  <div class="kr">필수 부사 200개 · 예문 포함</div>
  <p class="desc">By category — Korean adverb · Romanization · English meaning · Example sentence (예문)</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">부사</th>
    <th class="r-col">발음</th>
    <th class="en-col">English</th>
    <th>예문 Example</th>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=120)
time.sleep(2)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
