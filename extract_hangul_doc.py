from docx import Document
from pathlib import Path

src = Path(r"C:\Users\무지랭이\krguide-korean-learn\한글의 언어 문화적 특징과 한자와의 비교.docx")
dst = Path(r"C:\Users\무지랭이\krguide-korean-learn\hangul-vs-hanja.txt")

d = Document(src)
lines = []
for p in d.paragraphs:
    txt = p.text.strip()
    if txt:
        lines.append(txt)

dst.write_text("\n\n".join(lines), encoding="utf-8")
print(f"Wrote {len(lines)} paragraphs to {dst}")
print(f"Size: {dst.stat().st_size} bytes")
