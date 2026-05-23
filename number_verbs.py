"""
Extract & number all 200 verbs from Chapter 39 of learn-korean.html.

Outputs:
  chapters/ch39_numbered.txt        — full list 1~200
  chapters/ch39_from_81.txt         — only #81 onwards
"""
import re
from pathlib import Path
from html import unescape

SRC = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.html")
OUT = Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters")
OUT.mkdir(exist_ok=True)

html = SRC.read_text(encoding="utf-8")

# Find chapter 39 block
m = re.search(r'<div class="chapter" id="ch39">.*?(?=<div class="chapter" id="ch40")', html, re.S)
if not m:
    raise SystemExit("ch39 block not found")
block = m.group(0)

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = unescape(s)
    return s.strip()

# Each verb row: <tr><td class="hangul-cell">기본형</td><td>발음</td><td>English</td><td class="hangul-cell">해요체</td><td class="hangul-cell">과거형</td></tr>
# Skip category-header rows (which have colspan="5")
rows = []
current_section = ""
for m in re.finditer(
    r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = m.group(1)
    if 'colspan="5"' in row:
        # section header
        txt = clean(row)
        # skip the table header row ("기본형, 발음, English…")
        if txt and not txt.startswith("기본형"):
            current_section = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 5:
        continue
    gibon, pron, eng, polite, past = [clean(c) for c in cells]
    if gibon == "기본형":   # table header
        continue
    rows.append((current_section, gibon, pron, eng, polite, past))

print(f"Extracted {len(rows)} verbs")

# Write numbered list
lines_all = []
lines_81 = []
last_section = None
for i, (sec, gibon, pron, eng, polite, past) in enumerate(rows, 1):
    if sec != last_section:
        lines_all.append("")
        lines_all.append(f"━━━ {sec} ━━━")
        if i >= 81:
            lines_81.append("")
            lines_81.append(f"━━━ {sec} ━━━")
        last_section = sec
    line = f"{i:3}. {gibon}  ({pron}) — {eng}   |   해요체: {polite}  |  과거형: {past}"
    lines_all.append(line)
    if i >= 81:
        lines_81.append(line)

(OUT / "ch39_numbered.txt").write_text("\n".join(lines_all), encoding="utf-8")
(OUT / "ch39_from_81.txt").write_text("\n".join(lines_81), encoding="utf-8")
print(f"Wrote: ch39_numbered.txt  ({(OUT/'ch39_numbered.txt').stat().st_size:,} bytes)")
print(f"Wrote: ch39_from_81.txt   ({(OUT/'ch39_from_81.txt').stat().st_size:,} bytes)")
