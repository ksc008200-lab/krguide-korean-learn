import re
from pathlib import Path
from html import unescape

html = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.html").read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch38">.*?(?=<div class="chapter" id="ch39")', html, re.S)
block = m.group(0)

def clean(s): return unescape(re.sub(r"<[^>]+>", "", s)).strip()

out = []
n = 0
current = ""
for tr in re.finditer(r"<tr[^>]*>(.*?)</tr>", block, re.S):
    row = tr.group(1)
    if 'colspan="6"' in row:
        txt = clean(row)
        if txt and not txt.startswith("한글"):
            current = txt
        continue
    cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
    if len(cells) != 6: continue
    g1, p1, e1, g2, p2, e2 = [clean(c) for c in cells]
    if g1 == "한글": continue
    for g, p, e in [(g1, p1, e1), (g2, p2, e2)]:
        if not g: continue
        n += 1
        out.append(f"{n}|{current}|{g}|{p}|{e}")

Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters\nouns_list.txt").write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {n} nouns")
