"""
Enhanced PDF builder for internet_500.txt and konglish_500.txt.

Both files share a block format:
  #NNN  단어
        field1: value
        field2: value
        예문...
        💡 tip line
Sections separated by `====` lines with header `A. KO — EN  (N items)`.
"""
import re, subprocess, time, io, base64, random, urllib.parse, sys
from pathlib import Path
from html import escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def qr_png_data_url(text):
    qr = qrcode.QRCode(box_size=2, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def parse_entries(text):
    """Return list of (section_label, word, fields_dict, tip)."""
    lines = text.splitlines()
    sec_re = re.compile(r"^\s+([A-Z])\.\s+(.+?)\s+—\s+(.+?)\s+\((\d+)\s*items?\)\s*$")
    entry_re = re.compile(r"^#(\d+)\s+(.+?)\s*$")
    rows = []
    current_sec = ""
    cur_word = None
    cur_fields = {}
    cur_tip = ""
    cur_fields_order = []

    def flush():
        nonlocal cur_word, cur_fields, cur_tip, cur_fields_order
        if cur_word is not None:
            rows.append((current_sec, cur_word, cur_fields.copy(), cur_tip, list(cur_fields_order)))
        cur_word = None
        cur_fields = {}
        cur_tip = ""
        cur_fields_order = []

    for raw in lines:
        line = raw.rstrip()
        ms = sec_re.match(line)
        if ms:
            flush()
            current_sec = f"{ms.group(1)}. {ms.group(2)} · {ms.group(3)}"
            continue
        me = entry_re.match(line)
        if me:
            flush()
            cur_word = me.group(2).strip()
            continue
        if cur_word is None:
            continue
        s = line.strip()
        if not s: continue
        if s.startswith("💡"):
            cur_tip = s.lstrip("💡").strip()
            continue
        mf = re.match(r"^([^:]+?):\s*(.+)$", s)
        if mf:
            k, v = mf.group(1).strip(), mf.group(2).strip()
            cur_fields[k] = v
            cur_fields_order.append(k)
        else:
            # continuation of last field
            if cur_fields_order:
                last = cur_fields_order[-1]
                cur_fields[last] = (cur_fields[last] + " " + s).strip()
    flush()
    return rows

def build(file_key, config):
    src = ROOT / config["src"]
    html_out = ROOT / config["html_out"]
    pdf_out  = ROOT / config["pdf_out"]
    title    = config["title"]
    subtitle = config["subtitle"]
    desc     = config["desc"]

    text = src.read_text(encoding="utf-8")
    rows = parse_entries(text)
    print(f"[{file_key}] parsed {len(rows)} entries")

    def get_theme(sec):
        for theme_name, prefixes in config["themes"]:
            for prefix in prefixes:
                if prefix in sec: return theme_name
        return "기타"

    SCEN = config["scenarios"]; COMP = config["compares"]

    # quizzes (every 20)
    random.seed(42)
    quizzes = []
    eng_field = config["eng_field"]
    for start in range(0, len(rows), 20):
        chunk = rows[start:start+20]
        qs = []
        sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
        for s in sampled:
            sec, word, fields, tip, order = chunk[s]
            correct = fields.get(eng_field, "")
            if not correct: continue
            wrong_pool = [r[2].get(eng_field, "") for r in rows if r[2].get(eng_field, "") and r[2].get(eng_field, "") != correct]
            if len(wrong_pool) < 3: continue
            distractors = random.sample(wrong_pool, 3)
            options = distractors + [correct]; random.shuffle(options)
            qs.append((word, options, options.index(correct)))
        if qs:
            quizzes.append((start+1, min(start+20, len(rows)), qs))

    def cat_intro(theme):
        blocks = []
        if theme in SCEN:
            ls = "".join(f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> <span class="dl-text">{escape(ko)}</span></div>' for spk, ko in SCEN[theme])
            blocks.append(f'<div class="scenario-box"><div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>{ls}</div>')
        if theme in COMP:
            ps = "".join(f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span><span class="cb-en">{escape(p[1])}</span></div>' for p in COMP[theme])
            blocks.append(f'<div class="compare-box"><div class="cb-title">🔍 비교 박스 · Comparison</div>{ps}</div>')
        return "".join(blocks)

    items = []
    last_theme = None; last_sec = None
    quiz_idx = 0
    for i, (sec, word, fields, tip, order) in enumerate(rows, 1):
        theme = get_theme(sec)
        if theme != last_theme:
            items.append('</tbody></table>'); items.append('<div class="page-break"></div>')
            items.append(f'<h2 class="cat-h">{escape(theme)}</h2>')
            items.append(cat_intro(theme))
            items.append('<table><thead><tr><th class="num-col">#</th><th class="k-col">' + config["word_label"] + '</th><th class="en-col">' + config["en_label"] + '</th><th>예문 / 설명</th><th class="qr-col">🔊</th></tr></thead><tbody>')
            last_theme = theme; last_sec = None
        if sec != last_sec:
            items.append(f'<tr class="section"><td colspan="5">{escape(sec)}</td></tr>')
            last_sec = sec
        # main fields
        main_eng = fields.get(eng_field, "")
        # build the rest column (예문 + tip + other fields)
        rest_lines = []
        # show ex/tip first
        for k in order:
            if k == eng_field: continue
            v = fields[k]
            rest_lines.append(f'<div class="r-line"><span class="r-label">{escape(k)}:</span> <span class="r-val">{escape(v)}</span></div>')
        if tip:
            rest_lines.append(f'<div class="r-tip">💡 {escape(tip)}</div>')
        qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(word)}"
        qr_data = qr_png_data_url(qr_url)
        items.append(
            f'<tr><td class="num">{i}</td><td class="k">{escape(word)}</td>'
            f'<td class="en">{escape(main_eng)}</td>'
            f'<td class="rest">{"".join(rest_lines)}</td>'
            f'<td class="qr"><img src="{qr_data}" alt="QR"/></td></tr>'
        )
        if i % 20 == 0 and quiz_idx < len(quizzes):
            a, b, qs = quizzes[quiz_idx]; quiz_idx += 1
            qh = [f'<tr class="quiz-row"><td colspan="5"><div class="quiz">',
                  f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>',
                  f'<div class="q-sub">{escape(config["quiz_sub"])}</div>']
            for qi, (w, opts, _) in enumerate(qs, 1):
                opt_html = "".join(f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>' for oi, o in enumerate(opts))
                qh.append(f'<div class="q-item"><span class="q-num">Q{qi}.</span> <span class="q-word">{escape(w)}</span> = ? {opt_html}</div>')
            qh.append('</div></td></tr>')
            items.extend(qh)
    items.append('</tbody></table>')

    answer_html = ['<div class="page-break"></div>', '<h2 class="cat-h">📚 정답 · Answer Key</h2>', '<div class="answer-key">']
    for qi, (a, b, qs) in enumerate(quizzes, 1):
        line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
        answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
    answer_html.append('</div>')

    OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>""" + title + """ · Enhanced</title>
<style>
  @page { size: A4; margin: 16mm 12mm; } * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:620px; margin:0 auto; line-height:1.7; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }
  h2.cat-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:14px 22px; margin:0 0 14px; font-size:18px; border-left:6px solid #C0392B; }
  .scenario-box { background:#fff8f0; border-left:4px solid #f97316; padding:14px 18px; margin-bottom:14px; border-radius:6px; }
  .scenario-box .sb-title { font-weight:800; color:#9a3412; font-size:13px; margin-bottom:8px; }
  .scenario-box .dl-line { font-size:12px; margin:3px 0; }
  .scenario-box .dl-speaker { color:#C0392B; font-weight:700; margin-right:6px; }
  .compare-box { background:#f0f5ff; border-left:4px solid #1A4A8A; padding:14px 18px; margin-bottom:16px; border-radius:6px; }
  .compare-box .cb-title { font-weight:800; color:#1e3a8a; font-size:13px; margin-bottom:8px; }
  .compare-box .cb-pair { font-size:12px; margin:3px 0; display:flex; gap:12px; }
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:200px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; border-bottom:2px solid #C0392B; }
  th.num-col{width:30px;} th.k-col{width:85px;} th.en-col{width:130px;} th.qr-col{width:34px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:700; color:#C0392B; font-size:13px; }
  td.en  { color:#1A4A8A; font-size:11px; font-weight:600; }
  td.rest .r-line { font-size:10px; margin:1px 0; }
  td.rest .r-label { color:#888; font-weight:700; margin-right:3px; font-size:9.5px; }
  td.rest .r-val { color:#333; }
  td.rest .r-tip { font-size:9.5px; color:#666; font-style:italic; margin-top:3px; padding:2px 4px; background:#fefce8; border-left:2px solid #f59e0b; }
  td.qr { text-align:center; padding:3px; } td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:11px; padding:7px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
  tr.quiz-row td { padding:0; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:6px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-word { font-weight:800; color:#1a1a2e; font-size:13px; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; }
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>
<div class="cover">
  <div class="label">""" + title + """ · Enhanced</div>
  <h1>""" + title + """</h1>
  <div class="kr">""" + subtitle + """</div>
  <p class="desc">""" + desc + """</p>
  <div class="features">
    <span class="feat">🎭 시나리오</span><span class="feat">🔍 비교</span><span class="feat">📝 퀴즈</span><span class="feat">🔊 QR</span>
  </div>
</div>
""" + "\n".join(items) + "\n".join(answer_html) + """
</body></html>"""

    html_out.write_text(OUT, encoding="utf-8")
    print(f"[{file_key}] HTML → {html_out} ({html_out.stat().st_size:,} bytes)")

    if pdf_out.exists(): pdf_out.unlink()
    url = f"file:///{html_out.as_posix()}"
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_out}", url], capture_output=True, timeout=300)
    time.sleep(3)
    if pdf_out.exists():
        print(f"[{file_key}] PDF  → {pdf_out} ({pdf_out.stat().st_size:,} bytes)")

# ====== INTERNET CONFIG ======
INTERNET = dict(
    src="internet_500.txt",
    html_out="internet-500-enhanced.html",
    pdf_out="internet-500-enhanced.pdf",
    title="500 Korean Internet & Chat Expressions",
    subtitle="인터넷·채팅 한국어 500 · 향상판",
    desc="ㅋㅋㅋ부터 K-pop·게임 신조어까지 — 카테고리·예문·시나리오·미니 퀴즈·발음 QR 포함.",
    word_label="단어/표현",
    en_label="English",
    eng_field="English",
    quiz_sub="단어의 영어 뜻을 고르세요.",
    themes=[
        ("🔤 자음·줄임말", ["자음·기호", "두 글자 줄임", "세 글자"]),
        ("📱 SNS·인터넷 문화", ["SNS·인터넷 문화", "인터넷 밈"]),
        ("🎤 K-pop·게임", ["K-pop·팬덤", "게임·온라인"]),
        ("👥 세대·사회", ["세대·사회"]),
    ],
    scenarios={
        "🔤 자음·줄임말": [
            ("친구1", "야 ㅋㅋㅋ 그 영상 봤어?"),
            ("친구2", "ㅋㅋㅋㅋ 진짜 ㅁㅊ"),
            ("친구1", "ㄱㅅㄱㅅ 알려줘서"),
            ("친구2", "ㄴㄴ 별거 아니야 ㅎㅎ"),
            ("친구1", "ㅇㅋ ㄱㄱ"),
        ],
        "📱 SNS·인터넷 문화": [
            ("친구1", "오늘 인스타 피드 봤어? 완전 인생샷이야!"),
            ("친구2", "디엠 보냈는데 답이 없네."),
            ("친구1", "잠금장치 풀고 좋아요 눌러줘."),
            ("친구2", "ㅇㅋ 팔로우도 했어."),
            ("친구1", "역시 인친 최고!"),
        ],
        "🎤 K-pop·게임": [
            ("팬1", "신곡 컴백 떴어! 데뷔 무대 봤어?"),
            ("팬2", "ㄹㅇ 미쳤어 ㅠㅠ 그 직캠 봐줘"),
            ("팬1", "최애 표정 진짜 살벌해 ㅋㅋ"),
            ("팬2", "팬싸 갔다 왔다며? 부럽 ㅠㅠ"),
            ("팬1", "ㅇㅇ 다음에 같이 가자"),
        ],
        "👥 세대·사회": [
            ("MZ", "꼰대 마인드 어쩔..."),
            ("친구", "ㅋㅋ 라떼는 말이야~"),
            ("MZ", "워라밸 챙기는 게 중요해."),
            ("친구", "그래도 욜로 살아야지."),
            ("MZ", "갓생 살자!"),
        ],
    },
    compares={
        "🔤 자음·줄임말": [
            ("ㅋㅋㅋ (lol) / ㅎㅎ (hehe)", "loud laugh / soft laugh"),
            ("ㅠㅠ / ㅜㅜ", "crying (interchangeable)"),
            ("ㅇㅇ (yes) ↔ ㄴㄴ (no)", "yes ↔ no"),
            ("ㄱㄱ (go go) / ㅇㅋ (ok)", "let's go / ok"),
            ("ㅁㅊ (crazy) / ㅈㄴ (very)", "crazy / super"),
        ],
        "📱 SNS·인터넷 문화": [
            ("좋아요 ↔ 싫어요", "like ↔ dislike"),
            ("팔로우 / 팔로워 / 팔로잉", "follow / follower / following"),
            ("디엠 (DM) / 멘션 / 알림", "DM / mention / notification"),
        ],
        "🎤 K-pop·게임": [
            ("최애 / 차애", "favorite / 2nd favorite"),
            ("덕질 / 입덕 / 탈덕", "fandom / start being fan / quit fan"),
            ("팬싸 / 팬미 / 팬콘", "fansign / fanmeet / fancon"),
        ],
        "👥 세대·사회": [
            ("MZ ↔ 꼰대", "MZ generation ↔ outdated boomer"),
            ("워라밸 / 욜로 / 갓생", "work-life-balance / YOLO / god-like life"),
            ("N포세대 / 흙수저", "give-up generation / poor background"),
        ],
    },
)

# ====== KONGLISH CONFIG ======
KONGLISH = dict(
    src="konglish_500.txt",
    html_out="konglish-500-enhanced.html",
    pdf_out="konglish-500-enhanced.pdf",
    title="500 Konglish: Korean-English Expressions",
    subtitle="콩글리시 500 · 향상판",
    desc="한국에서만 통하는 영어식 표현과 진짜 영어 — 잘못된 영어 vs 올바른 영어, 예문, 시나리오, 비교, 미니 퀴즈, 발음 QR 포함.",
    word_label="콩글리시",
    en_label="올바른 영어",
    eng_field="올바른 영어",
    quiz_sub="콩글리시의 올바른 영어 표현을 고르세요.",
    themes=[
        ("🏠 일상·집·교통", ["일상생활", "자동차·교통"]),
        ("💼 직장·교육", ["직장·비즈니스", "학교·교육"]),
        ("🍔 음식·패션", ["음식·식음료", "의류·패션"]),
        ("🎬 미디어·운동", ["미디어·연예", "운동·스포츠"]),
        ("💻 IT·기타·신조어", ["IT·기술", "기타·신조어"]),
    ],
    scenarios={
        "🏠 일상·집·교통": [
            ("외국인",  "Where do you live?"),
            ("한국인",  "I live in a one-room… ah, I mean a studio apartment."),
            ("외국인",  "What's your handphone number?"),
            ("한국인",  "We say 'cell phone' in English!"),
            ("외국인",  "Oh, got it. Let me give you my cell phone number."),
        ],
        "💼 직장·교육": [
            ("직원1", "오늘 회식 가요?"),
            ("직원2", "응. 영어로는 'company dinner'야, 'hoeshik' 아니고."),
            ("직원1", "아 그렇구나. '미팅'은 영어로 'meeting' 맞지?"),
            ("직원2", "비즈니스에선 OK, 근데 데이트의 '미팅'은 'blind date'야."),
            ("직원1", "와 헷갈리네 ㅋㅋ"),
        ],
        "🍔 음식·패션": [
            ("손님", "원샷 하자! 영어로 뭐라고 해?"),
            ("친구", "'Bottoms up!' 또는 'Cheers!'야."),
            ("손님", "사이다 한 잔!"),
            ("친구", "영어로 'cider'는 사과주! 'Sprite'나 'soda'라고 해."),
            ("손님", "헐 진짜?"),
        ],
        "🎬 미디어·운동": [
            ("팬", "내가 좋아하는 아이돌이 컴백했어!"),
            ("외국친구", "Comeback! 영어로도 같은 말이야 (return)."),
            ("팬", "그 가수 'CF' 찍었대."),
            ("외국친구", "CF는 콩글리시야. 영어는 'commercial' 또는 'ad'."),
            ("팬", "또 배웠다!"),
        ],
        "💻 IT·기타·신조어": [
            ("후배", "노트북 좀 빌려도 될까요?"),
            ("선배", "영어로는 'laptop'이야, 'notebook' 아니야."),
            ("후배", "아하 'notebook'은 종이 공책이군요."),
            ("선배", "맞아. '핸드폰'도 'cell phone'이지."),
            ("후배", "콩글리시 진짜 헷갈려요 ㅋㅋ"),
        ],
    },
    compares={
        "🏠 일상·집·교통": [
            ("핸드폰 → cell phone", "NOT 'handphone'"),
            ("노트북 → laptop", "NOT 'notebook'"),
            ("원룸 → studio apartment", "NOT 'one-room'"),
            ("오토바이 → motorcycle", "NOT 'auto-bi'"),
        ],
        "💼 직장·교육": [
            ("회식 → company dinner", "NOT 'hoeshik'"),
            ("선임/후임 → senior/junior colleague", "NOT 'sun-im'"),
            ("학원 → cram school / private academy", "NOT 'hakwon'"),
        ],
        "🍔 음식·패션": [
            ("사이다 → Sprite / soda", "NOT 'cider' (apple juice)"),
            ("원샷 → Bottoms up! / Cheers!", "NOT 'one shot'"),
            ("아이쇼핑 → window shopping", "NOT 'eye shopping'"),
        ],
        "🎬 미디어·운동": [
            ("CF → commercial / ad", "NOT 'CF'"),
            ("탤런트 → TV actor", "NOT 'talent'"),
            ("개그맨 → comedian", "NOT 'gag man'"),
        ],
        "💻 IT·기타·신조어": [
            ("USB → flash drive / thumb drive", "USB is plug type, not the device"),
            ("핸드폰 케이스 → phone case", "OK"),
            ("리모컨 → remote control", "NOT 'remocon'"),
        ],
    },
)

for key, cfg in [("INTERNET", INTERNET), ("KONGLISH", KONGLISH)]:
    build(key, cfg)
