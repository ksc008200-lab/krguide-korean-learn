"""Just regenerate the combined HTML from current MD chapters — no PDF step.
Use this if Edge headless is hanging."""
import re, sys
sys.path.insert(0, r"C:\Users\무지랭이\krguide-korean-learn")

# Run the HTML-only portion of build_pdf_from_md.py
import markdown
from pathlib import Path

PROJECT  = Path(r"C:\Users\무지랭이\krguide-korean-learn")
CHAPTERS = PROJECT / "chapters"
OUT_HTML = PROJECT / "learn-korean-v3.html"

md_files = sorted(CHAPTERS.glob("ch*.md"))
print(f"Loading {len(md_files)} chapters...")

def clean_chapter(text, ch_num):
    text = re.sub(r"^\s*\*Chapter\s+\d+\s*·\s*제\d+장\*\s*\n+", "", text, flags=re.M)
    text = re.sub(
        r"^#\s+(.+?)$",
        f"# Chapter {ch_num} · \\1",
        text, count=1, flags=re.M,
    )
    return text.strip() + "\n"

parts = []
for f in md_files:
    ch_num = int(re.search(r"ch(\d+)", f.stem).group(1))
    parts.append(clean_chapter(f.read_text(encoding="utf-8"), ch_num))

combined_md = "\n\n".join(parts)
html_body = markdown.markdown(
    combined_md,
    extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
)

# Use same template as build_pdf_from_md.py
template = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>Learn Korean — Complete Guide (41 Chapters)</title>
<style>
@page { size: A4; margin: 1.6cm 1.8cm; }
body { font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Segoe UI', sans-serif; line-height: 1.65; color: #222; font-size: 12.5pt; max-width: 760px; margin: 0 auto; padding: 0 6px; }
.cover { text-align: center; padding: 100px 20px 60px; page-break-after: always; }
.cover-title { font-size: 38pt; color: #1A4A8A; margin: 0 0 12px; font-weight: 700; }
.cover-kr { font-size: 22pt; color: #C0392B; margin-bottom: 40px; }
.cover-subtitle { font-size: 13pt; color: #555; margin-top: 50px; }
.cover-brand { font-size: 10pt; color: #888; margin-top: 100px; }
h1 { color: #1A4A8A; border-bottom: 3px solid #C0392B; padding-bottom: 10px; margin-top: 0; font-size: 26pt; page-break-before: always; page-break-after: avoid; }
h1:first-of-type { page-break-before: avoid; }
h2 { color: #1A4A8A; margin-top: 32px; font-size: 18pt; page-break-after: avoid; }
h3 { color: #C0392B; margin-top: 24px; font-size: 14pt; page-break-after: avoid; }
p { margin: 10px 0 14px; }
strong { color: #C0392B; font-weight: 700; }
em { color: #1A4A8A; }
h2 strong, h3 strong, h1 strong { color: inherit; }
table { border-collapse: collapse; width: 100%; margin: 16px auto; font-size: 11.5pt; page-break-inside: avoid; }
th { background: #1A4A8A; color: white; padding: 9px 11px; text-align: center; font-weight: 600; }
td { border: 1px solid #ddd; padding: 8px 11px; vertical-align: middle; text-align: center; }
tr:nth-child(even) td { background: #FAFAFA; }
blockquote { background: #F0F9FF; border-left: 4px solid #1A4A8A; padding: 12px 18px; margin: 10px 0; border-radius: 0 5px 5px 0; page-break-inside: avoid; font-size: 12pt; }
blockquote p { margin: 6px 0; }
ul, ol { margin: 8px 0 12px 18px; }
li { font-size: 12.5pt; margin: 5px 0; }
hr { border: none; border-top: 2px solid #FACC15; margin: 30px 0; }
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', monospace; font-size: 11pt; }
.closing { text-align: center; padding: 80px 20px; color: #666; page-break-before: always; }
.closing h2 { color: #1A4A8A; border: none; page-break-before: avoid; }
</style>
</head>
<body>
<div class="cover">
  <div class="cover-title">Learn Korean</div>
  <div class="cover-kr">한국어 배우기 — 완전 가이드</div>
  <div class="cover-subtitle">41 Chapters · Bilingual · Romanization · Cultural Notes</div>
  <div class="cover-brand">krguide.com · study.krguide.com</div>
</div>
""" + html_body + """
<div class="closing">
  <h2>감사합니다 · Thank You</h2>
  <p style="margin-top:18px;">For the complete vocabulary resources and audio, visit:</p>
  <p style="font-size:13pt;color:#C0392B;margin-top:10px;">study.krguide.com</p>
  <p style="margin-top:50px;font-size:9pt;">© 2026 krguide.com — All rights reserved</p>
</div>
</body></html>"""

OUT_HTML.write_text(template, encoding="utf-8")
print(f"HTML written: {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")
