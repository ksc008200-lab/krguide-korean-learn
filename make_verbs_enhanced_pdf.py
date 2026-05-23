"""
Enhanced 200-verbs PDF:
  - per-row QR code → Google Translate (TTS playable)
  - per-category scenario dialogue + comparison box
  - every 20 verbs: mini quiz page (5 Q's)
  - end: full answer key
"""
import re, subprocess, time, io, base64, random, urllib.parse
from pathlib import Path
from html import unescape, escape
import qrcode

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "200-verbs-enhanced.html"
PDF_OUT  = ROOT / "200-verbs-enhanced.pdf"

# Example sentences (from previous version, copied here)
EX = {
1:("학교에 가요.","I go to school."),2:("친구가 와요.","My friend is coming."),3:("공원에서 걸어요.","I walk in the park."),
4:("아침마다 뛰어요.","I run every morning."),5:("버스를 타요.","I take the bus."),6:("다음 역에서 내려요.","I get off at the next station."),
7:("의자에 앉아요.","I sit on the chair."),8:("줄을 서요.","I stand in line."),9:("침대에 누워요.","I lie down on the bed."),
10:("주말에 집에서 쉬어요.","I rest at home on weekends."),11:("김치를 먹어요.","I eat kimchi."),12:("커피를 마셔요.","I drink coffee."),
13:("일찍 자요.","I sleep early."),14:("7시에 일어나요.","I wake up at 7."),15:("손을 씻어요.","I wash my hands."),
16:("이를 닦아요.","I brush my teeth."),17:("코트를 입어요.","I wear a coat."),18:("운동화를 신어요.","I wear sneakers."),
19:("모자를 써요.","I wear a hat."),20:("옷을 벗어요.","I take off my clothes."),21:("친구를 만나요.","I meet a friend."),
22:("친구와 헤어져요.","I part with my friend."),23:("한국어로 말해요.","I speak in Korean."),24:("가족과 이야기해요.","I talk with my family."),
25:("음악을 들어요.","I listen to music."),26:("영화를 봐요.","I watch a movie."),27:("책을 읽어요.","I read a book."),
28:("편지를 써요.","I write a letter."),29:("케이크를 만들어요.","I make a cake."),30:("친구와 놀아요.","I hang out with my friend."),
31:("저녁을 요리해요.","I cook dinner."),32:("빵을 구워요.","I bake bread."),33:("야채를 볶아요.","I stir-fry vegetables."),
34:("물을 끓여요.","I boil water."),35:("재료를 섞어요.","I mix the ingredients."),36:("방을 청소해요.","I clean my room."),
37:("주말에 빨래해요.","I do laundry on weekends."),38:("옷을 널어요.","I hang the clothes."),39:("빨래를 개요.","I fold the laundry."),
40:("식탁을 치워요.","I clear the table."),41:("쓰레기를 버려요.","I throw away the trash."),42:("책상을 정리해요.","I organize my desk."),
43:("컴퓨터를 고쳐요.","I fix the computer."),44:("불을 켜요.","I turn on the light."),45:("TV를 꺼요.","I turn off the TV."),
46:("창문을 열어요.","I open the window."),47:("문을 닫아요.","I close the door."),48:("사과를 사요.","I buy apples."),
49:("가게에서 책을 팔아요.","I sell books at the store."),50:("카드로 돈을 내요.","I pay with a card."),51:("도서관에서 책을 빌려요.","I borrow a book from the library."),
52:("친구에게 펜을 빌려줘요.","I lend a pen to my friend."),53:("선물을 줘요.","I give a gift."),54:("편지를 받아요.","I receive a letter."),
55:("돈을 바꿔요.","I exchange money."),56:("매일 한국어를 공부해요.","I study Korean every day."),57:("피아노를 배워요.","I learn the piano."),
58:("영어를 가르쳐요.","I teach English."),59:("선생님께 질문해요.","I ask the teacher."),60:("질문에 대답해요.","I answer the question."),
61:("발음을 연습해요.","I practice pronunciation."),62:("단어를 외워요.","I memorize words."),63:("설명을 이해해요.","I understand the explanation."),
64:("답을 알아요.","I know the answer."),65:("길을 몰라요.","I don't know the way."),66:("가족을 생각해요.","I think of my family."),
67:("여행지를 결정해요.","I decide on a destination."),68:("회사에서 일해요.","I work at a company."),69:("9시에 출근해요.","I go to work at 9."),
70:("6시에 퇴근해요.","I leave work at 6."),71:("회의를 준비해요.","I prepare for the meeting."),72:("휴가를 계획해요.","I plan a vacation."),
73:("매주 월요일에 회의해요.","We have a meeting every Monday."),74:("서류를 결재해요.","I approve the documents."),75:("결과를 보고해요.","I report the results."),
76:("친구를 도와줘요.","I help my friend."),77:("도움을 부탁해요.","I ask for help."),78:("제안을 거절해요.","I reject the offer."),
79:("시험에 성공해요.","I succeed in the exam."),80:("도전에 실패해요.","I fail at the challenge."),81:("일을 끝내요.","I finish the work."),
82:("수업을 시작해요.","I start the class."),83:("친구에게 연락해요.","I contact my friend."),84:("엄마에게 전화해요.","I call my mom."),
85:("중요한 일을 메모해요.","I take notes on important things."),86:("아기가 웃어요.","The baby is laughing."),87:("영화를 보고 울어요.","I cry watching a movie."),
88:("합격해서 기뻐해요.","I'm happy because I passed."),89:("동생이 화나요.","My sibling gets angry."),90:("친구가 떠나서 슬퍼해요.","I'm sad because my friend is leaving."),
91:("가족을 사랑해요.","I love my family."),92:("한국 음식을 좋아해요.","I like Korean food."),93:("매운 음식을 싫어해요.","I hate spicy food."),
94:("생일을 축하해요.","I celebrate the birthday."),95:("시험을 걱정해요.","I worry about the exam."),96:("어두운 곳을 무서워해요.","I'm afraid of dark places."),
97:("깜짝 놀라요.","I'm startled."),98:("행복을 느껴요.","I feel happiness."),99:("화를 참아요.","I hold back my anger."),
100:("버스를 기다려요.","I wait for the bus."),101:("이름을 잊어요.","I forget the name."),102:("추억을 기억해요.","I remember the memories."),
103:("결과를 기대해요.","I look forward to the result."),104:("결정을 후회해요.","I regret the decision."),105:("결과에 만족해요.","I'm satisfied with the result."),
106:("매일 운동해요.","I exercise every day."),107:("강아지와 산책해요.","I walk with my dog."),108:("주말에 등산해요.","I hike on weekends."),
109:("바다에서 수영해요.","I swim in the sea."),110:("공을 던져요.","I throw a ball."),111:("공을 받아요.","I catch a ball."),
112:("문을 밀어요.","I push the door."),113:("짐을 끌어요.","I pull the luggage."),114:("가방을 들어요.","I lift the bag."),
115:("책을 책상에 놓아요.","I put the book on the desk."),116:("손을 잡아요.","I hold hands."),117:("고양이를 만져요.","I touch the cat."),
118:("문을 두드려요.","I knock on the door."),119:("천천히 움직여요.","I move slowly."),120:("차가 멈춰요.","The car stops."),
121:("미끄러져서 넘어져요.","I slip and fall."),122:("운동하다 다쳐요.","I get hurt while exercising."),123:("머리가 아파요.","My head hurts."),
124:("감기가 나아요.","My cold gets better."),125:("깊게 숨쉬어요.","I breathe deeply."),126:("다음 달에 결혼해요.","I'm getting married next month."),
127:("서울로 이사해요.","I move to Seoul."),128:("친구와 싸워요.","I fight with my friend."),129:("친구와 화해해요.","I make up with my friend."),
130:("실수를 사과해요.","I apologize for the mistake."),131:("잘못을 용서해요.","I forgive the mistake."),132:("시간을 약속해요.","I make an appointment."),
133:("친구를 소개해요.","I introduce my friend."),134:("할머니 댁을 방문해요.","I visit grandmother's house."),135:("집에 친구를 초대해요.","I invite a friend home."),
136:("꽃을 선물해요.","I give flowers as a gift."),137:("아이를 칭찬해요.","I praise the child."),138:("팀을 응원해요.","I cheer for the team."),
139:("지하철을 이용해요.","I use the subway."),140:("컴퓨터를 사용해요.","I use the computer."),141:("잃어버린 열쇠를 찾아요.","I look for the lost key."),
142:("지갑을 잃어버려요.","I lose my wallet."),143:("약속을 지켜요.","I keep my promise."),144:("규칙을 어겨요.","I break the rule."),
145:("회의에 참석해요.","I attend the meeting."),146:("행사에 참여해요.","I participate in the event."),147:("새로운 문화를 경험해요.","I experience a new culture."),
148:("가격을 비교해요.","I compare the prices."),149:("메뉴를 선택해요.","I choose from the menu."),150:("꿈을 포기해요.","I give up the dream."),
151:("의사가 돼요.","I become a doctor."),152:("날씨가 바뀌어요.","The weather changes."),153:("시간이 지나면 마음이 변해요.","Feelings change with time."),
154:("학생 수가 늘어요.","The number of students increases."),155:("무게가 줄어요.","My weight decreases."),156:("한국에서 태어나요.","I was born in Korea."),
157:("꽃이 죽어요.","The flower dies."),158:("서울에 살아요.","I live in Seoul."),159:("시간이 남아요.","Time remains."),
160:("문제가 생겨요.","A problem arises."),161:("안개가 사라져요.","The fog disappears."),162:("별이 나타나요.","Stars appear."),
163:("잎이 떨어져요.","Leaves fall."),164:("가격이 올라요.","The price rises."),165:("방이 밝아요.","The room is bright."),
166:("밖이 어두워요.","It's dark outside."),167:("아버지를 닮아요.","I resemble my father."),168:("이 옷이 잘 어울려요.","These clothes suit you well."),
169:("시간이 부족해요.","There's not enough time."),170:("돈이 충분해요.","There's enough money."),171:("선물을 골라요.","I pick a gift."),
172:("행복을 빌어요.","I wish for happiness."),173:("사람을 속여요.","I deceive someone."),174:("친구를 믿어요.","I trust my friend."),
175:("결과를 의심해요.","I doubt the result."),176:("더 나은 미래를 꿈꿔요.","I dream of a better future."),177:("매일 노력해요.","I make an effort every day."),
178:("문제를 해결해요.","I solve the problem."),179:("기술이 발전해요.","Technology develops."),180:("아이가 성장해요.","The child grows."),
181:("휴가를 즐겨요.","I enjoy my vacation."),182:("환경을 보호해요.","I protect the environment."),183:("차를 조심해요.","I'm careful of cars."),
184:("이메일을 확인해요.","I check my email."),185:("예약을 취소해요.","I cancel the reservation."),186:("장학금을 신청해요.","I apply for a scholarship."),
187:("유럽을 여행해요.","I travel in Europe."),188:("음식을 배달해요.","I deliver the food."),189:("시장을 구경해요.","I look around the market."),
190:("일기를 기록해요.","I keep a diary."),191:("결과를 발표해요.","I announce the results."),192:("새로운 약을 연구해요.","We research new medicine."),
193:("감정을 표현해요.","I express my feelings."),194:("메시지를 전해요.","I deliver the message."),195:("답이 맞아요.","The answer is correct."),
196:("답이 틀려요.","The answer is wrong."),197:("친구를 불러요.","I call my friend."),198:("한국을 떠나요.","I leave Korea."),
199:("공항에 도착해요.","I arrive at the airport."),200:("길을 헤매요.","I'm lost on the street."),
}

# Comparison pairs — manually curated opposites & similar verbs
COMPARE_BOX = {
    "기본 일상 활동": [
        ("가다 / 오다", "go ↔ come"),
        ("타다 / 내리다", "ride ↔ get off"),
        ("앉다 / 서다", "sit ↔ stand"),
        ("자다 / 일어나다", "sleep ↔ wake up"),
        ("입다 / 벗다", "wear ↔ take off"),
    ],
    "가사 및 생활": [
        ("열다 / 닫다", "open ↔ close"),
        ("켜다 / 끄다", "turn on ↔ turn off"),
        ("사다 / 팔다", "buy ↔ sell"),
        ("주다 / 받다", "give ↔ receive"),
        ("빌리다 / 빌려주다", "borrow ↔ lend"),
    ],
    "학습 및 업무": [
        ("질문하다 / 대답하다", "ask ↔ answer"),
        ("알다 / 모르다", "know ↔ not know"),
        ("출근하다 / 퇴근하다", "go to work ↔ leave work"),
        ("성공하다 / 실패하다", "succeed ↔ fail"),
        ("부탁하다 / 거절하다", "request ↔ reject"),
    ],
    "감정 및 감각": [
        ("웃다 / 울다", "laugh ↔ cry"),
        ("기뻐하다 / 슬퍼하다", "rejoice ↔ grieve"),
        ("좋아하다 / 싫어하다", "like ↔ dislike"),
        ("잊다 / 기억하다", "forget ↔ remember"),
    ],
    "신체 활동 및 운동": [
        ("던지다 / 받다", "throw ↔ catch"),
        ("밀다 / 끌다", "push ↔ pull"),
        ("움직이다 / 멈추다", "move ↔ stop"),
        ("다치다 / 낫다", "get hurt ↔ recover"),
    ],
    "관계 및 사회 생활": [
        ("만나다 / 헤어지다", "meet ↔ part"),
        ("싸우다 / 화해하다", "fight ↔ reconcile"),
        ("사과하다 / 용서하다", "apologize ↔ forgive"),
        ("이용하다 / 사용하다", "use (service) vs use (object)"),
    ],
    "상태 변화 및 현상": [
        ("늘다 / 줄다", "increase ↔ decrease"),
        ("태어나다 / 죽다", "be born ↔ die"),
        ("생기다 / 사라지다", "arise ↔ disappear"),
        ("나타나다 / 사라지다", "appear ↔ disappear"),
        ("오르다 / 떨어지다", "rise ↔ fall"),
        ("밝다 / 어둡다", "bright ↔ dark"),
    ],
    "기타 추상적 행위": [
        ("믿다 / 의심하다", "believe ↔ doubt"),
        ("맞다 / 틀리다", "correct ↔ wrong"),
        ("도착하다 / 떠나다", "arrive ↔ leave"),
        ("부족하다 / 충분하다", "insufficient ↔ sufficient"),
    ],
}

# Scenario dialogues per category — 5~6 lines
SCENARIO = {
    "기본 일상 활동": [
        ("민수", "오늘 어디 가요?"),
        ("지영", "공원에 가요. 같이 걸을래요?"),
        ("민수", "좋아요. 버스를 타고 갈까요?"),
        ("지영", "아니요, 천천히 걸어요."),
        ("민수", "그래요. 오늘 날씨가 좋네요!"),
    ],
    "가사 및 생활": [
        ("엄마", "방을 좀 청소해 줄래?"),
        ("아들", "네, 책상부터 정리할게요."),
        ("엄마", "쓰레기도 버려 줘."),
        ("아들", "알겠어요. 빨래는요?"),
        ("엄마", "그건 내가 할게. 고마워."),
    ],
    "학습 및 업무": [
        ("선생님", "오늘은 새 단어를 배워요."),
        ("학생",   "선생님, 질문이 있어요."),
        ("선생님", "네, 말해보세요."),
        ("학생",   "이 단어는 어떻게 발음해요?"),
        ("선생님", "이렇게요. 같이 연습해 봅시다."),
    ],
    "감정 및 감각": [
        ("친구1", "왜 그렇게 슬퍼해?"),
        ("친구2", "시험에 실패해서…"),
        ("친구1", "걱정하지 마. 다음에 잘하면 돼."),
        ("친구2", "응, 고마워. 기분이 좀 나아졌어."),
        ("친구1", "같이 영화 볼래? 기분 풀어 줄게."),
    ],
    "신체 활동 및 운동": [
        ("동료1", "오늘 같이 운동할래요?"),
        ("동료2", "좋아요! 어디서요?"),
        ("동료1", "공원에서 뛰어요. 아니면 등산 어때요?"),
        ("동료2", "등산이 좋겠어요. 조심해서 가요."),
        ("동료1", "네, 다치지 않게 조심해요."),
    ],
    "관계 및 사회 생활": [
        ("호스트", "어서 오세요. 들어오세요."),
        ("손님",   "초대해 주셔서 감사해요."),
        ("호스트", "이쪽은 제 친구 민수예요. 소개할게요."),
        ("손님",   "안녕하세요, 반갑습니다."),
        ("민수",   "잘 부탁드려요!"),
    ],
    "상태 변화 및 현상": [
        ("기자",  "요즘 도시 인구가 어떻게 변하고 있나요?"),
        ("전문가","서울 인구는 줄고, 지방 도시는 늘어요."),
        ("기자",  "왜 그런 일이 생기나요?"),
        ("전문가","집값이 오르고 직장이 변하기 때문이에요."),
        ("기자",  "흥미로운 분석이네요. 감사합니다."),
    ],
    "기타 추상적 행위": [
        ("상사", "이 보고서 좀 확인해 주세요."),
        ("직원", "네, 바로 확인하겠습니다."),
        ("상사", "예약도 취소했나요?"),
        ("직원", "방금 취소했어요. 다른 거 있나요?"),
        ("상사", "고생했어요. 일찍 퇴근하세요."),
    ],
}

# Generate QR code as base64 inline image
def qr_png_data_url(text):
    qr = qrcode.QRCode(version=None, box_size=2, border=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Extract verbs from HTML
html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch39">.*?(?=<div class="chapter" id="ch40")', html, re.S)
block = m.group(0)
def clean(s): return unescape(re.sub(r"<[^>]+>", "", s)).strip()

rows = []
current = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="5"' in row:
        txt = clean(row)
        if txt and not txt.startswith("기본형"):
            current = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 5: continue
    g, p, e, pol, pa = [clean(c) for c in cells]
    if g == "기본형": continue
    rows.append((current, g, p, e, pol, pa))

# Map verb row index → primary category (단어 → top-level category)
# Group by header-level (대분류, e.g. "1. 기본 일상 활동")
# In HTML these are wrapped in div with id="v1"~"v8" — let's detect from sequence: 30/25/30/20/20/25/25/25 = 200
category_assignments = []
for i, r in enumerate(rows, 1):
    if i <= 30: category_assignments.append("기본 일상 활동")
    elif i <= 55: category_assignments.append("가사 및 생활")
    elif i <= 85: category_assignments.append("학습 및 업무")
    elif i <= 105: category_assignments.append("감정 및 감각")
    elif i <= 125: category_assignments.append("신체 활동 및 운동")
    elif i <= 150: category_assignments.append("관계 및 사회 생활")
    elif i <= 175: category_assignments.append("상태 변화 및 현상")
    else: category_assignments.append("기타 추상적 행위")

# Generate quizzes (every 20 verbs)
random.seed(42)
quizzes = []  # list of (start_idx, [(question, options, correct_idx)])
for start in range(0, 200, 20):
    chunk = rows[start:start+20]
    qs = []
    sampled = random.sample(range(len(chunk)), min(5, len(chunk)))
    for s in sampled:
        sec, g, p, e, pol, pa = chunk[s]
        # Question: "X의 영어 뜻은?"
        # Wrong options: random from other rows
        wrong_pool = [r[3] for r in rows if r[3] != e]
        distractors = random.sample(wrong_pool, 3)
        options = distractors + [e]
        random.shuffle(options)
        correct_idx = options.index(e)
        qs.append((g, options, correct_idx))
    quizzes.append((start+1, start+20, qs))

# Build HTML
def cat_intro_block(cat):
    """Category-level scenario + comparison box."""
    blocks = []
    # Scenario
    if cat in SCENARIO:
        lines = "".join(
            f'<div class="dl-line"><span class="dl-speaker">{escape(spk)}:</span> '
            f'<span class="dl-text">{escape(ko)}</span></div>'
            for spk, ko in SCENARIO[cat])
        blocks.append(
            f'<div class="scenario-box">'
            f'<div class="sb-title">🎭 시나리오 대화 · Scenario Dialogue</div>'
            f'{lines}</div>'
        )
    # Comparison
    if cat in COMPARE_BOX:
        pairs = "".join(
            f'<div class="cb-pair"><span class="cb-ko">{escape(p[0])}</span>'
            f'<span class="cb-en">{escape(p[1])}</span></div>'
            for p in COMPARE_BOX[cat])
        blocks.append(
            f'<div class="compare-box">'
            f'<div class="cb-title">🔍 헷갈리지 마세요 · Easy-to-confuse Pairs</div>'
            f'{pairs}</div>'
        )
    return "".join(blocks)

items = []
last_cat = None
verb_section_label_last = None

quiz_idx = 0
for i, ((sec, g, p, e, pol, pa), top_cat) in enumerate(zip(rows, category_assignments), 1):
    # New top-level category? Emit intro block before the section row
    if top_cat != last_cat:
        items.append(f'</tbody></table>')
        items.append(f'<div class="page-break"></div>')
        items.append(f'<h2 class="cat-h">🌟 {escape(top_cat)}</h2>')
        items.append(cat_intro_block(top_cat))
        items.append('<table><thead><tr>'
                     '<th class="num-col">#</th>'
                     '<th class="k-col">기본형</th>'
                     '<th class="r-col">발음</th>'
                     '<th class="en-col">English</th>'
                     '<th class="k-col">해요체</th>'
                     '<th class="k-col">과거형</th>'
                     '<th>예문 Example</th>'
                     '<th class="qr-col">🔊</th>'
                     '</tr></thead><tbody>')
        last_cat = top_cat
        verb_section_label_last = None
    # New sub-section?
    if sec != verb_section_label_last:
        items.append(f'<tr class="section"><td colspan="8">{escape(sec)}</td></tr>')
        verb_section_label_last = sec

    ex_ko, ex_en = EX.get(i, ("", ""))
    # QR URL: Google Translate with the verb base form
    qr_url = f"https://translate.google.com/?sl=ko&tl=en&op=translate&text={urllib.parse.quote(g)}"
    qr_data = qr_png_data_url(qr_url)
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(g)}</td>'
        f'<td class="r">{escape(p)}</td>'
        f'<td class="en">{escape(e)}</td>'
        f'<td class="k">{escape(pol)}</td>'
        f'<td class="k">{escape(pa)}</td>'
        f'<td class="ex"><span class="ex-ko">{escape(ex_ko)}</span><span class="ex-en">{escape(ex_en)}</span></td>'
        f'<td class="qr"><img src="{qr_data}" alt="QR" /></td>'
        f'</tr>'
    )

    # After every 20 entries, emit a quiz
    if i % 20 == 0:
        a, b, qs = quizzes[quiz_idx]
        quiz_idx += 1
        qhtml = []
        qhtml.append(f'<tr class="quiz-row"><td colspan="8"><div class="quiz">')
        qhtml.append(f'<div class="q-title">📝 미니 퀴즈 · Mini Quiz ({a}~{b})</div>')
        qhtml.append('<div class="q-sub">다음 동사의 영어 뜻을 고르세요. · Choose the correct English meaning.</div>')
        for qi, (word, opts, _) in enumerate(qs, 1):
            opt_html = "".join(
                f'<span class="q-opt">{chr(0x2460+oi)} {escape(o)}</span>'
                for oi, o in enumerate(opts))
            qhtml.append(f'<div class="q-item">'
                         f'<span class="q-num">Q{qi}.</span> '
                         f'<span class="q-word">{escape(word)}</span> = ? '
                         f'{opt_html}</div>')
        qhtml.append('</div></td></tr>')
        items.extend(qhtml)

items.append('</tbody></table>')

# Answer key at end
answer_html = ['<div class="page-break"></div>',
               '<h2 class="cat-h">📚 정답 · Answer Key</h2>',
               '<div class="answer-key">']
for qi, (a, b, qs) in enumerate(quizzes, 1):
    line = ", ".join(f"Q{j}: {chr(0x2460+correct)}" for j, (_, _, correct) in enumerate(qs, 1))
    answer_html.append(f'<div class="ak-row"><strong>Quiz {qi} ({a}~{b}):</strong> {line}</div>')
answer_html.append('</div>')

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>200 Essential Korean Verbs · Enhanced Edition</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR','Malgun Gothic',sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .page-break { page-break-before: always; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:30px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:600px; margin:0 auto; line-height:1.7; }
  .cover .features { margin-top:24px; display:flex; justify-content:center; gap:14px; flex-wrap:wrap; }
  .cover .feat { background:#1a1a2e; color:#fff; padding:6px 14px; border-radius:18px; font-size:11px; font-weight:600; }
  h2.cat-h { background:linear-gradient(135deg,#1a1a2e,#16213e); color:#fff; padding:14px 22px; margin:0 0 14px; font-size:18px; border-left:6px solid #C0392B; }
  .scenario-box { background:#fff8f0; border-left:4px solid #f97316; padding:14px 18px; margin-bottom:14px; border-radius:6px; }
  .scenario-box .sb-title { font-weight:800; color:#9a3412; font-size:13px; margin-bottom:8px; letter-spacing:0.5px; }
  .scenario-box .dl-line { font-size:12px; margin:3px 0; }
  .scenario-box .dl-speaker { color:#C0392B; font-weight:700; margin-right:6px; }
  .scenario-box .dl-text { color:#1a1a2e; }
  .compare-box { background:#f0f5ff; border-left:4px solid #1A4A8A; padding:14px 18px; margin-bottom:16px; border-radius:6px; }
  .compare-box .cb-title { font-weight:800; color:#1e3a8a; font-size:13px; margin-bottom:8px; letter-spacing:0.5px; }
  .compare-box .cb-pair { font-size:12px; margin:3px 0; display:flex; gap:12px; }
  .compare-box .cb-ko { color:#1a1a2e; font-weight:700; min-width:180px; }
  .compare-box .cb-en { color:#666; font-style:italic; }
  table { width:100%; border-collapse:collapse; font-size:10.5px; table-layout:fixed; margin-bottom:14px; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 5px; font-size:9.5px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:26px;} th.k-col{width:58px;} th.r-col{width:54px;} th.en-col{width:90px;} th.qr-col{width:32px;}
  td { padding:5px 6px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:12px; }
  td.r   { color:#6b6b6b; font-style:italic; font-size:10px; }
  td.en  { color:#1A4A8A; font-size:10.5px; }
  td.ex  { font-size:10.5px; }
  td.ex .ex-ko { display:block; color:#C0392B; font-weight:600; }
  td.ex .ex-en { display:block; color:#666; font-style:italic; font-size:9.5px; margin-top:1px; }
  td.qr { text-align:center; padding:3px; }
  td.qr img { width:30px; height:30px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:11px; letter-spacing:1.2px; padding:7px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
  /* Quiz */
  tr.quiz-row td { padding:0; }
  .quiz { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:2px solid #f59e0b; border-radius:10px; padding:14px 18px; margin:14px 0; }
  .quiz .q-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:6px; }
  .quiz .q-sub { font-size:11px; color:#78350f; margin-bottom:10px; font-style:italic; }
  .quiz .q-item { font-size:11px; margin:6px 0; padding:6px 10px; background:#fff; border-radius:6px; }
  .quiz .q-num { font-weight:800; color:#C0392B; margin-right:6px; }
  .quiz .q-word { font-weight:800; color:#1a1a2e; font-size:13px; }
  .quiz .q-opt { display:inline-block; margin-right:12px; color:#444; }
  /* Answer key */
  .answer-key { background:#f9fafb; padding:20px 24px; border-radius:8px; }
  .ak-row { padding:6px 0; border-bottom:1px solid #e5e5ea; font-size:12px; }
  .ak-row strong { color:#C0392B; }
</style></head><body>

<div class="cover">
  <div class="label">Korean Essential Verbs · Enhanced Edition</div>
  <h1>200 Essential Korean Verbs</h1>
  <div class="kr">필수 동사 200개 · 향상판</div>
  <p class="desc">By category — dictionary form · romanization · English meaning · polite form (해요체) · past tense (과거형) · example sentence — plus scenario dialogues, comparison boxes, mini quizzes, and pronunciation QR codes.</p>
  <div class="features">
    <span class="feat">🎭 시나리오 대화</span>
    <span class="feat">🔍 비교 박스</span>
    <span class="feat">📝 미니 퀴즈</span>
    <span class="feat">🔊 발음 QR</span>
  </div>
</div>

""" + "\n".join(items) + "\n".join(answer_html) + """

</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML → {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url = f"file:///{HTML_OUT.as_posix()}"
if PDF_OUT.exists(): PDF_OUT.unlink()
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=240)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
