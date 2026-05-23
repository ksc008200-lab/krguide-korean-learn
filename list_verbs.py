import re
from pathlib import Path
from html import unescape

html = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.html").read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch39">.*?(?=<div class="chapter" id="ch40")', html, re.S)
block = m.group(0)

def clean(s): return unescape(re.sub(r"<[^>]+>", "", s)).strip()

out_lines = []
n = 0
for tr in re.finditer(r"<tr[^>]*>(.*?)</tr>", block, re.S):
    row = tr.group(1)
    if 'colspan="5"' in row: continue
    cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
    if len(cells) != 5: continue
    g, p, e, pol, pa = [clean(c) for c in cells]
    if g == "기본형": continue
    n += 1
    out_lines.append(f"{n}|{g}|{e}|{pol}")

Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters\verbs_list.txt").write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {n} verbs")
