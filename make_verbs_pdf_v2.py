"""
Build a richer 200-verbs PDF with example sentences.
"""
import re, subprocess, time
from pathlib import Path
from html import unescape, escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "200-verbs-with-examples.html"
PDF_OUT  = ROOT / "200-verbs-with-examples.pdf"

# Example sentences (ko, en) for each of the 200 verbs.
EX = {
1: ("학교에 가요.", "I go to school."),
2: ("친구가 와요.", "My friend is coming."),
3: ("공원에서 걸어요.", "I walk in the park."),
4: ("아침마다 뛰어요.", "I run every morning."),
5: ("버스를 타요.", "I take the bus."),
6: ("다음 역에서 내려요.", "I get off at the next station."),
7: ("의자에 앉아요.", "I sit on the chair."),
8: ("줄을 서요.", "I stand in line."),
9: ("침대에 누워요.", "I lie down on the bed."),
10: ("주말에 집에서 쉬어요.", "I rest at home on weekends."),
11: ("김치를 먹어요.", "I eat kimchi."),
12: ("커피를 마셔요.", "I drink coffee."),
13: ("일찍 자요.", "I sleep early."),
14: ("7시에 일어나요.", "I wake up at 7."),
15: ("손을 씻어요.", "I wash my hands."),
16: ("이를 닦아요.", "I brush my teeth."),
17: ("코트를 입어요.", "I wear a coat."),
18: ("운동화를 신어요.", "I wear sneakers."),
19: ("모자를 써요.", "I wear a hat."),
20: ("옷을 벗어요.", "I take off my clothes."),
21: ("친구를 만나요.", "I meet a friend."),
22: ("친구와 헤어져요.", "I part with my friend."),
23: ("한국어로 말해요.", "I speak in Korean."),
24: ("가족과 이야기해요.", "I talk with my family."),
25: ("음악을 들어요.", "I listen to music."),
26: ("영화를 봐요.", "I watch a movie."),
27: ("책을 읽어요.", "I read a book."),
28: ("편지를 써요.", "I write a letter."),
29: ("케이크를 만들어요.", "I make a cake."),
30: ("친구와 놀아요.", "I hang out with my friend."),
31: ("저녁을 요리해요.", "I cook dinner."),
32: ("빵을 구워요.", "I bake bread."),
33: ("야채를 볶아요.", "I stir-fry vegetables."),
34: ("물을 끓여요.", "I boil water."),
35: ("재료를 섞어요.", "I mix the ingredients."),
36: ("방을 청소해요.", "I clean my room."),
37: ("주말에 빨래해요.", "I do laundry on weekends."),
38: ("옷을 널어요.", "I hang the clothes."),
39: ("빨래를 개요.", "I fold the laundry."),
40: ("식탁을 치워요.", "I clear the table."),
41: ("쓰레기를 버려요.", "I throw away the trash."),
42: ("책상을 정리해요.", "I organize my desk."),
43: ("컴퓨터를 고쳐요.", "I fix the computer."),
44: ("불을 켜요.", "I turn on the light."),
45: ("TV를 꺼요.", "I turn off the TV."),
46: ("창문을 열어요.", "I open the window."),
47: ("문을 닫아요.", "I close the door."),
48: ("사과를 사요.", "I buy apples."),
49: ("가게에서 책을 팔아요.", "I sell books at the store."),
50: ("카드로 돈을 내요.", "I pay with a card."),
51: ("도서관에서 책을 빌려요.", "I borrow a book from the library."),
52: ("친구에게 펜을 빌려줘요.", "I lend a pen to my friend."),
53: ("선물을 줘요.", "I give a gift."),
54: ("편지를 받아요.", "I receive a letter."),
55: ("돈을 바꿔요.", "I exchange money."),
56: ("매일 한국어를 공부해요.", "I study Korean every day."),
57: ("피아노를 배워요.", "I learn the piano."),
58: ("영어를 가르쳐요.", "I teach English."),
59: ("선생님께 질문해요.", "I ask the teacher."),
60: ("질문에 대답해요.", "I answer the question."),
61: ("발음을 연습해요.", "I practice pronunciation."),
62: ("단어를 외워요.", "I memorize words."),
63: ("설명을 이해해요.", "I understand the explanation."),
64: ("답을 알아요.", "I know the answer."),
65: ("길을 몰라요.", "I don't know the way."),
66: ("가족을 생각해요.", "I think of my family."),
67: ("여행지를 결정해요.", "I decide on a destination."),
68: ("회사에서 일해요.", "I work at a company."),
69: ("9시에 출근해요.", "I go to work at 9."),
70: ("6시에 퇴근해요.", "I leave work at 6."),
71: ("회의를 준비해요.", "I prepare for the meeting."),
72: ("휴가를 계획해요.", "I plan a vacation."),
73: ("매주 월요일에 회의해요.", "We have a meeting every Monday."),
74: ("서류를 결재해요.", "I approve the documents."),
75: ("결과를 보고해요.", "I report the results."),
76: ("친구를 도와줘요.", "I help my friend."),
77: ("도움을 부탁해요.", "I ask for help."),
78: ("제안을 거절해요.", "I reject the offer."),
79: ("시험에 성공해요.", "I succeed in the exam."),
80: ("도전에 실패해요.", "I fail at the challenge."),
81: ("일을 끝내요.", "I finish the work."),
82: ("수업을 시작해요.", "I start the class."),
83: ("친구에게 연락해요.", "I contact my friend."),
84: ("엄마에게 전화해요.", "I call my mom."),
85: ("중요한 일을 메모해요.", "I take notes on important things."),
86: ("아기가 웃어요.", "The baby is laughing."),
87: ("영화를 보고 울어요.", "I cry watching a movie."),
88: ("합격해서 기뻐해요.", "I'm happy because I passed."),
89: ("동생이 화나요.", "My sibling gets angry."),
90: ("친구가 떠나서 슬퍼해요.", "I'm sad because my friend is leaving."),
91: ("가족을 사랑해요.", "I love my family."),
92: ("한국 음식을 좋아해요.", "I like Korean food."),
93: ("매운 음식을 싫어해요.", "I hate spicy food."),
94: ("생일을 축하해요.", "I celebrate the birthday."),
95: ("시험을 걱정해요.", "I worry about the exam."),
96: ("어두운 곳을 무서워해요.", "I'm afraid of dark places."),
97: ("깜짝 놀라요.", "I'm startled."),
98: ("행복을 느껴요.", "I feel happiness."),
99: ("화를 참아요.", "I hold back my anger."),
100: ("버스를 기다려요.", "I wait for the bus."),
101: ("이름을 잊어요.", "I forget the name."),
102: ("추억을 기억해요.", "I remember the memories."),
103: ("결과를 기대해요.", "I look forward to the result."),
104: ("결정을 후회해요.", "I regret the decision."),
105: ("결과에 만족해요.", "I'm satisfied with the result."),
106: ("매일 운동해요.", "I exercise every day."),
107: ("강아지와 산책해요.", "I walk with my dog."),
108: ("주말에 등산해요.", "I hike on weekends."),
109: ("바다에서 수영해요.", "I swim in the sea."),
110: ("공을 던져요.", "I throw a ball."),
111: ("공을 받아요.", "I catch a ball."),
112: ("문을 밀어요.", "I push the door."),
113: ("짐을 끌어요.", "I pull the luggage."),
114: ("가방을 들어요.", "I lift the bag."),
115: ("책을 책상에 놓아요.", "I put the book on the desk."),
116: ("손을 잡아요.", "I hold hands."),
117: ("고양이를 만져요.", "I touch the cat."),
118: ("문을 두드려요.", "I knock on the door."),
119: ("천천히 움직여요.", "I move slowly."),
120: ("차가 멈춰요.", "The car stops."),
121: ("미끄러져서 넘어져요.", "I slip and fall."),
122: ("운동하다 다쳐요.", "I get hurt while exercising."),
123: ("머리가 아파요.", "My head hurts."),
124: ("감기가 나아요.", "My cold gets better."),
125: ("깊게 숨쉬어요.", "I breathe deeply."),
126: ("다음 달에 결혼해요.", "I'm getting married next month."),
127: ("서울로 이사해요.", "I move to Seoul."),
128: ("친구와 싸워요.", "I fight with my friend."),
129: ("친구와 화해해요.", "I make up with my friend."),
130: ("실수를 사과해요.", "I apologize for the mistake."),
131: ("잘못을 용서해요.", "I forgive the mistake."),
132: ("시간을 약속해요.", "I make an appointment."),
133: ("친구를 소개해요.", "I introduce my friend."),
134: ("할머니 댁을 방문해요.", "I visit grandmother's house."),
135: ("집에 친구를 초대해요.", "I invite a friend home."),
136: ("꽃을 선물해요.", "I give flowers as a gift."),
137: ("아이를 칭찬해요.", "I praise the child."),
138: ("팀을 응원해요.", "I cheer for the team."),
139: ("지하철을 이용해요.", "I use the subway."),
140: ("컴퓨터를 사용해요.", "I use the computer."),
141: ("잃어버린 열쇠를 찾아요.", "I look for the lost key."),
142: ("지갑을 잃어버려요.", "I lose my wallet."),
143: ("약속을 지켜요.", "I keep my promise."),
144: ("규칙을 어겨요.", "I break the rule."),
145: ("회의에 참석해요.", "I attend the meeting."),
146: ("행사에 참여해요.", "I participate in the event."),
147: ("새로운 문화를 경험해요.", "I experience a new culture."),
148: ("가격을 비교해요.", "I compare the prices."),
149: ("메뉴를 선택해요.", "I choose from the menu."),
150: ("꿈을 포기해요.", "I give up the dream."),
151: ("의사가 돼요.", "I become a doctor."),
152: ("날씨가 바뀌어요.", "The weather changes."),
153: ("시간이 지나면 마음이 변해요.", "Feelings change with time."),
154: ("학생 수가 늘어요.", "The number of students increases."),
155: ("무게가 줄어요.", "My weight decreases."),
156: ("한국에서 태어나요.", "I was born in Korea."),
157: ("꽃이 죽어요.", "The flower dies."),
158: ("서울에 살아요.", "I live in Seoul."),
159: ("시간이 남아요.", "Time remains."),
160: ("문제가 생겨요.", "A problem arises."),
161: ("안개가 사라져요.", "The fog disappears."),
162: ("별이 나타나요.", "Stars appear."),
163: ("잎이 떨어져요.", "Leaves fall."),
164: ("가격이 올라요.", "The price rises."),
165: ("방이 밝아요.", "The room is bright."),
166: ("밖이 어두워요.", "It's dark outside."),
167: ("아버지를 닮아요.", "I resemble my father."),
168: ("이 옷이 잘 어울려요.", "These clothes suit you well."),
169: ("시간이 부족해요.", "There's not enough time."),
170: ("돈이 충분해요.", "There's enough money."),
171: ("선물을 골라요.", "I pick a gift."),
172: ("행복을 빌어요.", "I wish for happiness."),
173: ("사람을 속여요.", "I deceive someone."),
174: ("친구를 믿어요.", "I trust my friend."),
175: ("결과를 의심해요.", "I doubt the result."),
176: ("더 나은 미래를 꿈꿔요.", "I dream of a better future."),
177: ("매일 노력해요.", "I make an effort every day."),
178: ("문제를 해결해요.", "I solve the problem."),
179: ("기술이 발전해요.", "Technology develops."),
180: ("아이가 성장해요.", "The child grows."),
181: ("휴가를 즐겨요.", "I enjoy my vacation."),
182: ("환경을 보호해요.", "I protect the environment."),
183: ("차를 조심해요.", "I'm careful of cars."),
184: ("이메일을 확인해요.", "I check my email."),
185: ("예약을 취소해요.", "I cancel the reservation."),
186: ("장학금을 신청해요.", "I apply for a scholarship."),
187: ("유럽을 여행해요.", "I travel in Europe."),
188: ("음식을 배달해요.", "I deliver the food."),
189: ("시장을 구경해요.", "I look around the market."),
190: ("일기를 기록해요.", "I keep a diary."),
191: ("결과를 발표해요.", "I announce the results."),
192: ("새로운 약을 연구해요.", "We research new medicine."),
193: ("감정을 표현해요.", "I express my feelings."),
194: ("메시지를 전해요.", "I deliver the message."),
195: ("답이 맞아요.", "The answer is correct."),
196: ("답이 틀려요.", "The answer is wrong."),
197: ("친구를 불러요.", "I call my friend."),
198: ("한국을 떠나요.", "I leave Korea."),
199: ("공항에 도착해요.", "I arrive at the airport."),
200: ("길을 헤매요.", "I'm lost on the street."),
}

# Extract verbs
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

assert len(rows) == 200, f"Expected 200 verbs, got {len(rows)}"

items = []
last = None
for i, (sec, g, p, e, pol, pa) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="7">{escape(sec)}</td></tr>')
        last = sec
    ex_ko, ex_en = EX[i]
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(g)}</td>'
        f'<td class="r">{escape(p)}</td>'
        f'<td class="en">{escape(e)}</td>'
        f'<td class="k">{escape(pol)}</td>'
        f'<td class="k">{escape(pa)}</td>'
        f'<td class="ex"><span class="ex-ko">{escape(ex_ko)}</span><span class="ex-en">{escape(ex_en)}</span></td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>200 Essential Korean Verbs · 예문 포함</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; color: #1a1a2e; margin: 0; line-height: 1.45; }
  .cover { text-align: center; padding: 60px 20px 30px; border-bottom: 4px solid #C0392B; margin-bottom: 22px; }
  .cover .label { font-size: 12px; font-weight: 700; letter-spacing: 3px; color: #C0392B; text-transform: uppercase; margin-bottom: 14px; }
  .cover h1 { font-size: 34px; margin: 0 0 8px; color: #1a1a2e; font-weight: 800; }
  .cover .kr { font-size: 22px; color: #1A4A8A; font-weight: 700; margin: 0 0 18px; }
  .cover .desc { font-size: 13px; color: #555; max-width: 580px; margin: 0 auto; line-height: 1.7; }
  table { width: 100%; border-collapse: collapse; font-size: 11px; table-layout: fixed; }
  thead th { background: #1a1a2e; color: #fff; padding: 7px 6px; font-size: 10px; letter-spacing: 0.4px; border-bottom: 2px solid #C0392B; }
  th.num-col { width: 28px; }
  th.k-col   { width: 65px; }
  th.r-col   { width: 60px; }
  th.en-col  { width: 90px; }
  th.ex-col  { width: 220px; }
  td { padding: 5px 6px; border-bottom: 1px solid #e5e5ea; vertical-align: top; word-break: keep-all; }
  tr:nth-child(even) td { background: #fafafa; }
  td.num { text-align: center; color: #888; font-weight: 600; font-size: 10px; }
  td.k   { font-weight: 600; color: #1a1a2e; font-size: 12px; }
  td.r   { color: #6b6b6b; font-style: italic; font-size: 10px; }
  td.en  { color: #1A4A8A; font-size: 11px; }
  td.ex  { font-size: 11px; }
  td.ex .ex-ko { display: block; color: #C0392B; font-weight: 600; }
  td.ex .ex-en { display: block; color: #666; font-style: italic; font-size: 10px; margin-top: 1px; }
  tr.section td { background: linear-gradient(135deg, #1a1a2e, #16213e) !important; color: #fff; font-weight: 800; font-size: 12px; letter-spacing: 1.2px; padding: 8px 12px; text-transform: uppercase; }
  tr.section td::before { content: "▸  "; color: #f97316; }
</style>
</head><body>

<div class="cover">
  <div class="label">Korean Essential Verbs · with Examples</div>
  <h1>200 Essential Korean Verbs</h1>
  <div class="kr">필수 동사 200개 · 예문 포함</div>
  <p class="desc">By category — Korean dictionary form · Romanization · English meaning · Polite form (해요체) · Past tense (과거형) · Example sentence (예문)</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">기본형</th>
    <th class="r-col">발음</th>
    <th class="en-col">English</th>
    <th class="k-col">해요체</th>
    <th class="k-col">과거형</th>
    <th class="ex-col">예문 Example</th>
  </tr></thead>
  <tbody>
""" + "\n".join(items) + """
  </tbody>
</table>

</body></html>"""

HTML_OUT.write_text(OUT, encoding="utf-8")
print(f"HTML → {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url = f"file:///{HTML_OUT.as_posix()}"
if PDF_OUT.exists(): PDF_OUT.unlink()
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=120)
time.sleep(2)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
