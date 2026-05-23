"""
Split learn-korean.html into per-chapter markdown files.

Output: chapters/ch01.md, ch02.md, ... — each file holds the title and body
of one chapter, in markdown form, ready to paste into Google Docs.
"""
import re
from pathlib import Path
from html import unescape

SRC = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.html")
OUT = Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters")
OUT.mkdir(exist_ok=True)

html = SRC.read_text(encoding="utf-8")


def strip_tags(s: str) -> str:
    """Remove tags, decode entities, collapse whitespace."""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def md_from_chapter(block: str) -> str:
    out = []

    # Chapter header
    label = re.search(r"<div class=\"chapter-label\">(.*?)</div>", block, re.S)
    title = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
    krt   = re.search(r"<div class=\"kr-title\">(.*?)</div>", block, re.S)
    if label: out.append(f"*{strip_tags(label.group(1))}*")
    if title: out.append(f"# {strip_tags(title.group(1))}")
    if krt:   out.append(f"**{strip_tags(krt.group(1))}**")
    out.append("")

    # Body
    body_m = re.search(r"<div class=\"chapter-body\">(.*?)</div>\s*</div>\s*<!--", block, re.S)
    body = body_m.group(1) if body_m else block

    pos = 0
    for m in re.finditer(
        r"(<h3[^>]*>(?P<h3>.*?)</h3>)|"
        r"(<p[^>]*>(?P<p>.*?)</p>)|"
        r"(<blockquote[^>]*>(?P<bq>.*?)</blockquote>)|"
        r"(<div class=\"divider\"[^>]*>(?P<dv>.*?)</div>)|"
        r"(<div class=\"card[^\"]*\"[^>]*>(?P<card>.*?)</div>(?=\s*(<|$)))|"
        r"(<div class=\"tip\"[^>]*>(?P<tip>.*?)</div>(?=\s*(<|$)))|"
        r"(<div class=\"letter-grid\"[^>]*>(?P<lg>.*?)</div>\s*(?=<|$))|"
        r"(<div class=\"philosophy-grid\"[^>]*>(?P<pg>.*?)</div>\s*(?=<|$))",
        body, re.S):
        pos = m.end()
        if m.group("h3"):
            out.append(f"## {strip_tags(m.group('h3'))}")
            out.append("")
        elif m.group("p"):
            t = strip_tags(m.group("p"))
            if t: out.append(t); out.append("")
        elif m.group("bq"):
            for line in strip_tags(m.group("bq")).splitlines():
                line = line.strip()
                if line: out.append(f"> {line}")
            out.append("")
        elif m.group("dv"):
            out.append(f"### — {strip_tags(m.group('dv'))} —"); out.append("")
        elif m.group("card"):
            t = strip_tags(m.group("card"))
            for line in t.splitlines():
                line = line.strip()
                if line: out.append(f"> {line}")
            out.append("")
        elif m.group("tip"):
            t = strip_tags(m.group("tip"))
            out.append(f"💡 **Tip:** {t.replace(chr(10),' ')}"); out.append("")
        elif m.group("lg"):
            # Letter grid → simple list
            for card in re.finditer(
                r"<div class=\"letter-card\">\s*"
                r"<div class=\"letter-big\">(.*?)</div>\s*"
                r"<div class=\"letter-name\">(.*?)</div>\s*"
                r"<div class=\"letter-sound\">(.*?)</div>\s*"
                r"<div class=\"letter-examples\">(.*?)</div>",
                m.group("lg"), re.S):
                big, nm, snd, ex = [strip_tags(card.group(i)) for i in range(1, 5)]
                out.append(f"- **{big}** ({nm}) — sound: {snd} · example: {ex}")
            out.append("")
        elif m.group("pg"):
            for box in re.finditer(
                r"<div class=\"phil-box\">\s*"
                r"<div class=\"phil-symbol\">(.*?)</div>\s*"
                r"<div class=\"phil-name\">(.*?)</div>\s*"
                r"<div class=\"phil-name-kr\">(.*?)</div>\s*"
                r"<div class=\"phil-desc\">(.*?)</div>",
                m.group("pg"), re.S):
                sym, nm, krn, desc = [strip_tags(box.group(i)) for i in range(1, 5)]
                out.append(f"- **{sym}** {nm} ({krn}) — {desc}")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


count = 0
for m in re.finditer(
    r"<div class=\"chapter\"\s+id=\"ch(\d+)\"\s*>(.*?)</div>\s*</div>\s*(?=<!--|<div class=\"chapter\"|<script|<footer|</body>)",
    html, re.S):
    n = int(m.group(1))
    block = m.group(0)
    md = md_from_chapter(block)
    fname = OUT / f"ch{n:02d}.md"
    fname.write_text(md, encoding="utf-8")
    count += 1
    print(f"  ch{n:02d}.md   {fname.stat().st_size:>7,} bytes")

print(f"\n{count} chapters → {OUT}")
