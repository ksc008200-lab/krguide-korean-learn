"""Merge consecutive bilingual H2 headers into a single line.

Pattern detected:
    ## English Header
    (blank line)
    ## Korean Header

Replaced with:
    ## English Header · Korean Header

Skips H2s that already contain · (already merged).
"""
import re
from pathlib import Path

CHAPTERS = Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters")
files = sorted(CHAPTERS.glob("ch*.md"))

total_merged = 0
for f in files:
    text = f.read_text(encoding="utf-8")
    # Match: ## A\n(blank lines)## B
    # Capture A and B, skip if A already has '·'
    def merge(m):
        a = m.group(1).strip()
        b = m.group(2).strip()
        # If either already contains middle dot or em-dash separator, skip
        if "·" in a or "·" in b:
            return m.group(0)
        return f"## {a} · {b}"

    pattern = re.compile(r"^##\s+(.+?)\s*\n\s*\n##\s+(.+?)\s*$", re.M)
    new_text, count = pattern.subn(merge, text)

    # Same for H3 pairs
    def merge_h3(m):
        a = m.group(1).strip()
        b = m.group(2).strip()
        if "·" in a or "·" in b:
            return m.group(0)
        return f"### {a} · {b}"

    pattern3 = re.compile(r"^###\s+(.+?)\s*\n\s*\n###\s+(.+?)\s*$", re.M)
    new_text, count3 = pattern3.subn(merge_h3, new_text)

    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        total = count + count3
        total_merged += total
        print(f"  {f.name}: merged {count} H2 + {count3} H3 pairs")

print(f"\nTotal bilingual header pairs merged: {total_merged}")
