"""Scan all 41 chapter MD files for:
  - Title format consistency
  - Empty sections (H2 followed immediately by another H2 or end-of-chapter)
  - Emoji-only blockquote placeholders (> 🚇 with no content following)
  - Word count per chapter (catch thin chapters)
"""
import re
from pathlib import Path

CHAPTERS = Path(r"C:\Users\무지랭이\krguide-korean-learn\chapters")
files = sorted(CHAPTERS.glob("ch*.md"))

print(f"{'Ch':>3} | {'Lines':>5} | {'Words':>5} | Title format")
print("-" * 100)

issues = []
for f in files:
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    word_count = sum(len(line.split()) for line in lines)

    # Title format detection
    label = ""
    h1 = ""
    krsub = ""
    for i, ln in enumerate(lines[:6]):
        ln_strip = ln.strip()
        if ln_strip.startswith("*Chapter"):
            label = "✓"
        elif ln_strip.startswith("# "):
            h1 = ln_strip[2:][:50]
        elif ln_strip.startswith("**") and ln_strip.endswith("**"):
            krsub = "✓"

    fmt = f"L:{label or '_'}  H1:{'✓' if h1 else '_'}  KR:{krsub or '_'}"
    ch_num = int(re.search(r"ch(\d+)", f.stem).group(1))

    # Detect placeholder issues
    chapter_issues = []
    # Empty H2 sections — H2 followed by blank or another H2
    h2_indices = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    for idx in h2_indices:
        # Check if next non-blank line is another H2 or end
        next_content = None
        for j in range(idx + 1, len(lines)):
            if lines[j].strip():
                next_content = lines[j].strip()
                break
        if next_content is None or next_content.startswith("## "):
            section = lines[idx].strip()[:40]
            chapter_issues.append(f"empty section: '{section}'")

    # Emoji-only blockquotes (> 🚇 with nothing else)
    for i, ln in enumerate(lines):
        if re.match(r"^>\s+[\U0001F300-\U0001FAFF\U00002600-\U000027BF]+\s*$", ln):
            chapter_issues.append(f"line {i+1}: emoji-only placeholder '{ln.strip()}'")

    # Short chapters (likely incomplete)
    if word_count < 200:
        chapter_issues.append(f"thin content ({word_count} words)")

    if chapter_issues:
        issues.append((ch_num, h1, chapter_issues))

    print(f"{ch_num:>3} | {len(lines):>5} | {word_count:>5} | {fmt}  →  {h1}")

print("\n=== Issues found ===\n")
for ch_num, h1, ch_issues in issues:
    print(f"Ch {ch_num} ({h1}):")
    for issue in ch_issues:
        print(f"  - {issue}")
    print()

print(f"Total chapters with issues: {len(issues)}/41")
