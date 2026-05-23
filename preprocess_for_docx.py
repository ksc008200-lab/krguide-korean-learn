"""
Preprocess learn-korean.html for DOCX conversion (aggressive v2).
"""
import re
from pathlib import Path

SRC  = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.html")
DST  = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean.preprocessed.html")

html = SRC.read_text(encoding="utf-8")

# 1. Clean head
html = re.sub(r"<head>.*?</head>",
              "<head><meta charset='UTF-8'><title>Learn Korean</title></head>",
              html, flags=re.S)

# 2. Remove UI chrome entirely
for pat in [
    r"<div id=\"unlock-modal\".*?</div>\s*</div>",     # modal has nested div
    r"<div id=\"paywall-bar\".*?</div>",
    r"<div class=\"top-search-bar\".*?</div>",
    r"<div class=\"top-search-results\".*?(?:</div>|/>)",
    r"<aside.*?</aside>",
    r"<nav.*?</nav>",
    r"<footer.*?</footer>",
    r"<div id=\"google_translate_element\".*?</div>",
    r"<script.*?</script>",
    r"<style.*?</style>",
    r"<noscript.*?</noscript>",
    r"<input[^>]*/?>",
    r"<button[^>]*>.*?</button>",
]:
    html = re.sub(pat, "", html, flags=re.S | re.I)

# 3. Strip all <br>
html = re.sub(r"<br\s*/?>\s*", " ", html)

# 4. Cover block → simple centered title block
def conv_cover(m):
    inner = m.group(1)
    title    = re.search(r"<h1>(.*?)</h1>", inner, flags=re.S)
    kr_title = re.search(r"<div class=\"cover-korean\">(.*?)</div>", inner, flags=re.S)
    desc     = re.search(r"<p class=\"cover-desc\">(.*?)</p>", inner, flags=re.S)
    badge    = re.search(r"<div class=\"cover-badge\">(.*?)</div>", inner, flags=re.S)
    out = []
    if badge: out.append(f"<p style='text-align:center'><em>{badge.group(1).strip()}</em></p>")
    if title: out.append(f"<h1 style='text-align:center'>{re.sub(r'<.*?>','',title.group(1)).strip()}</h1>")
    if kr_title: out.append(f"<p style='text-align:center'><strong>{kr_title.group(1).strip()}</strong></p>")
    if desc: out.append(f"<p style='text-align:center'>{desc.group(1).strip()}</p>")
    out.append("<p style='text-align:center'>Korea Guide Team · krguide.com</p>")
    return "\n".join(out)

html = re.sub(r"<div class=\"cover\">(.*?)</div>\s*<!--", conv_cover, html, flags=re.S)

# 5. TOC: replace whole <div class="toc">…</div> block with a clean table
def conv_toc(m):
    inner = m.group(1)
    # Match either toc-part divs or toc-item links in order
    out = ['<h2>Table of Contents · 목차</h2>',
           '<p><em>37 Chapters · 한글부터 한국 문화까지 완전 학습 가이드</em></p>',
           '<table>',
           '<thead><tr><th>#</th><th>Title</th><th>제목</th></tr></thead>',
           '<tbody>']
    parts = re.split(r"(<div class=\"toc-part\">.*?</div>|<a href=\"#ch\d+\".*?</a>)", inner, flags=re.S)
    for chunk in parts:
        if not chunk.strip():
            continue
        m_part = re.match(r"<div class=\"toc-part\">(.*?)</div>", chunk, flags=re.S)
        m_item = re.match(r"<a href=\"#ch\d+\".*?<div class=\"toc-num\">(.*?)</div><div><div class=\"toc-title\">(.*?)</div><div class=\"toc-title-kr\">(.*?)</div></div>", chunk, flags=re.S)
        if m_part:
            label = re.search(r"<span class=\"toc-part-label\">(.*?)</span>", chunk)
            title = re.search(r"<span class=\"toc-part-title\">(.*?)</span>", chunk)
            kr    = re.search(r"<span class=\"toc-part-kr\">(.*?)</span>", chunk)
            row = f"<tr><td colspan='3'><strong>{label.group(1) if label else ''} — {title.group(1) if title else ''} ({kr.group(1) if kr else ''})</strong></td></tr>"
            out.append(row)
        elif m_item:
            num, en, kr = m_item.group(1).strip(), m_item.group(2).strip(), m_item.group(3).strip()
            out.append(f"<tr><td>{num}</td><td>{en}</td><td>{kr}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)

html = re.sub(r"<div class=\"toc\">(.*?)</div>\s*<!--", conv_toc, html, flags=re.S)

# 6. philosophy-grid → table
def conv_phil_grid(m):
    inner = m.group(1)
    rows = re.findall(
        r"<div class=\"phil-box\">\s*"
        r"<div class=\"phil-symbol\">(.*?)</div>\s*"
        r"<div class=\"phil-name\">(.*?)</div>\s*"
        r"<div class=\"phil-name-kr\">(.*?)</div>\s*"
        r"<div class=\"phil-desc\">(.*?)</div>\s*"
        r"</div>", inner, flags=re.S)
    if not rows:
        return ""
    out = ['<table><thead><tr><th>기호</th><th>Name</th><th>이름</th><th>Description</th></tr></thead><tbody>']
    for sym, nm, krn, desc in rows:
        out.append(f"<tr><td><strong>{sym.strip()}</strong></td><td>{nm.strip()}</td><td>{krn.strip()}</td><td>{desc.strip()}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)

html = re.sub(r"<div class=\"philosophy-grid\">(.*?)</div>\s*(?=<|$)",
              conv_phil_grid, html, flags=re.S)

# 7. letter-grid → table
def conv_letter_grid(m):
    inner = m.group(1)
    rows = re.findall(
        r"<div class=\"letter-card\">\s*"
        r"<div class=\"letter-big\">(.*?)</div>\s*"
        r"<div class=\"letter-name\">(.*?)</div>\s*"
        r"<div class=\"letter-sound\">(.*?)</div>\s*"
        r"<div class=\"letter-examples\">(.*?)</div>\s*"
        r"</div>", inner, flags=re.S)
    if not rows:
        return ""
    out = ['<table><thead><tr><th>글자</th><th>이름</th><th>소리</th><th>예시</th></tr></thead><tbody>']
    for big, nm, snd, ex in rows:
        ex_clean = re.sub(r"<span>(.*?)</span>", r" — \1", ex).strip()
        out.append(f"<tr><td><strong>{big.strip()}</strong></td><td>{nm.strip()}</td><td>{snd.strip()}</td><td>{ex_clean}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)

html = re.sub(r"<div class=\"letter-grid\">(.*?)</div>\s*(?=<|$)",
              conv_letter_grid, html, flags=re.S)

# 8. card / tip blocks → blockquote
def conv_card(m):
    inner = m.group(1).strip()
    inner = re.sub(r"<div class=\"card-title\">(.*?)</div>",
                   r"<p><strong>\1</strong></p>", inner, flags=re.S)
    return f"<blockquote>{inner}</blockquote>"

html = re.sub(r"<div class=\"card(?:\s+[a-z]+)?\">(.*?)</div>\s*(?=<|$)",
              conv_card, html, flags=re.S)

def conv_tip(m):
    inner = m.group(1)
    inner = re.sub(r"<div class=\"tip-icon\">.*?</div>", "", inner, flags=re.S)
    inner = re.sub(r"<div class=\"tip-content\">(.*?)</div>\s*$", r"\1", inner.strip(), flags=re.S)
    return f"<blockquote><p><strong>💡 Tip</strong></p>{inner}</blockquote>"

html = re.sub(r"<div class=\"tip\">(.*?)</div>\s*(?=<|$)",
              conv_tip, html, flags=re.S)

# 9. divider, chapter-label, kr-title → small centered text
html = re.sub(r"<div class=\"divider\">(.*?)</div>",
              r"<p style='text-align:center'><strong>— \1 —</strong></p>", html, flags=re.S)
html = re.sub(r"<div class=\"chapter-label\">(.*?)</div>",
              r"<p style='text-align:center'><em>\1</em></p>", html, flags=re.S)
html = re.sub(r"<div class=\"kr-title\">(.*?)</div>",
              r"<p style='text-align:center'><strong>\1</strong></p>", html, flags=re.S)

# 10. Strip empty link tags & empty divs
html = re.sub(r"<a\s+href=\"#[^\"]+\"[^>]*></a>", "", html)
html = re.sub(r"<a\s+[^>]*>\s*</a>", "", html)
for _ in range(6):
    html = re.sub(r"<div[^>]*>\s*</div>", "", html)
    html = re.sub(r"<p[^>]*>\s*</p>", "", html)
    html = re.sub(r"<span[^>]*>\s*</span>", "", html)

# 11. Collapse multiple blank lines
html = re.sub(r"(\s*\n){2,}", "\n", html)

DST.write_text(html, encoding="utf-8")
print(f"Wrote {DST}  ({DST.stat().st_size:,} bytes)")
