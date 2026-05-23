"""
Build 500 nouns (actual: 369) PDF with example sentences.
"""
import re, subprocess, time
from pathlib import Path
from html import unescape, escape

ROOT = Path(r"C:\Users\무지랭이\krguide-korean-learn")
SRC  = ROOT / "learn-korean.html"
HTML_OUT = ROOT / "essential-nouns-with-examples.html"
PDF_OUT  = ROOT / "essential-nouns-with-examples.pdf"

EX = {
1:("우리 가족은 다섯 명이에요.","My family has five people."),
2:("부모님께 전화해요.","I call my parents."),
3:("아버지는 회사에 가세요.","My father goes to work."),
4:("어머니가 요리해요.","My mother is cooking."),
5:("형은 대학생이에요.","My older brother is a college student."),
6:("누나가 결혼했어요.","My older sister got married."),
7:("동생이 학교에 가요.","My younger sibling goes to school."),
8:("할아버지께서 신문을 읽으세요.","Grandfather reads the newspaper."),
9:("할머니께서 김치를 만드세요.","Grandmother makes kimchi."),
10:("친척 집에 놀러 가요.","I go to visit my relatives."),
11:("남편과 영화를 봐요.","I watch a movie with my husband."),
12:("아내가 출근했어요.","My wife went to work."),
13:("아들이 운동해요.","My son exercises."),
14:("딸이 책을 읽어요.","My daughter reads a book."),
15:("이 사람은 누구예요?","Who is this person?"),
16:("인간은 사회적 동물이에요.","Humans are social animals."),
17:("친구를 만나러 가요.","I'm going to meet a friend."),
18:("회사 동료와 점심을 먹어요.","I have lunch with a coworker."),
19:("선배가 도와줬어요.","My senior helped me."),
20:("후배에게 조언해요.","I give advice to my junior."),
21:("이웃과 인사해요.","I greet my neighbor."),
22:("손님이 많이 와요.","Many guests are coming."),
23:("이 집 주인을 만났어요.","I met the owner of this house."),
24:("어른을 공경해요.","We respect adults."),
25:("아이가 놀고 있어요.","The child is playing."),
26:("아기가 자고 있어요.","The baby is sleeping."),
27:("저는 학생이에요.","I am a student."),
28:("선생님께 질문해요.","I ask the teacher."),
29:("교수님 수업이 재미있어요.","The professor's class is fun."),
30:("의사를 만나러 가요.","I'm going to see the doctor."),
31:("간호사가 친절해요.","The nurse is kind."),
32:("경찰이 도와줬어요.","The police helped me."),
33:("공무원 시험을 봐요.","I'm taking the civil servant exam."),
34:("회사원은 보통 9시에 출근해요.","Office workers usually go to work at 9."),
35:("가수의 노래가 좋아요.","I like the singer's song."),
36:("배우가 연기를 잘해요.","The actor performs well."),
37:("작가의 책을 읽어요.","I read the writer's book."),
38:("기자가 인터뷰해요.","The journalist conducts an interview."),
39:("몸이 안 좋아요.","My body doesn't feel well."),
40:("머리가 길어요.","My hair is long."),
41:("얼굴을 씻어요.","I wash my face."),
42:("눈이 예뻐요.","Your eyes are pretty."),
43:("코가 가려워요.","My nose is itchy."),
44:("입을 크게 벌려요.","Open your mouth wide."),
45:("귀를 잘 기울이세요.","Listen carefully."),
46:("목이 아파요.","My throat hurts."),
47:("어깨가 무거워요.","My shoulders feel heavy."),
48:("팔이 아파요.","My arm hurts."),
49:("손을 깨끗이 씻어요.","Wash your hands well."),
50:("손가락을 다쳤어요.","I hurt my finger."),
51:("허리가 아파요.","My back hurts."),
52:("다리가 길어요.","My legs are long."),
53:("발이 시려워요.","My feet are cold."),
54:("발가락이 아파요.","My toes hurt."),
55:("피부가 건조해요.","My skin is dry."),
56:("뼈가 부러졌어요.","I broke a bone."),
57:("피가 나요.","I'm bleeding."),
58:("심장이 빠르게 뛰어요.","My heart is racing."),
59:("건강이 제일 중요해요.","Health is the most important thing."),
60:("병에 걸렸어요.","I caught a disease."),
61:("감기가 심해요.","My cold is severe."),
62:("약을 먹어요.","I take medicine."),
63:("병원에 가요.","I'm going to the hospital."),
64:("약국에서 약을 사요.","I buy medicine at the pharmacy."),
65:("기침이 나요.","I have a cough."),
66:("열이 나요.","I have a fever."),
67:("통증이 심해요.","The pain is severe."),
68:("증상이 어떠세요?","What are your symptoms?"),
69:("수술을 받았어요.","I had surgery."),
70:("검사를 받으러 가요.","I'm going for a checkup."),
71:("운동이 건강에 좋아요.","Exercise is good for health."),
72:("다이어트 중이에요.","I'm on a diet."),
73:("휴식이 필요해요.","I need rest."),
74:("음식이 맛있어요.","The food is delicious."),
75:("밥 먹었어요?","Have you eaten?"),
76:("반찬이 다양해요.","There are many side dishes."),
77:("국이 따뜻해요.","The soup is warm."),
78:("찌개가 맛있어요.","The stew is delicious."),
79:("식사 시간이에요.","It's mealtime."),
80:("아침을 안 먹었어요.","I didn't eat breakfast."),
81:("점심 같이 먹어요.","Let's have lunch together."),
82:("저녁 메뉴가 뭐예요?","What's for dinner?"),
83:("간식을 먹어요.","I eat a snack."),
84:("야식은 건강에 안 좋아요.","Late-night snacks are unhealthy."),
85:("요리가 취미예요.","Cooking is my hobby."),
86:("메뉴를 보여 주세요.","Please show me the menu."),
87:("맛이 좋아요.","The flavor is good."),
88:("쌀을 씻어요.","I wash the rice."),
89:("고기를 좋아해요.","I like meat."),
90:("소고기 한 근 주세요.","One pound of beef, please."),
91:("돼지고기를 구워요.","I grill pork."),
92:("닭고기 요리를 만들어요.","I cook a chicken dish."),
93:("생선이 신선해요.","The fish is fresh."),
94:("채소를 많이 먹어요.","I eat a lot of vegetables."),
95:("과일이 달아요.","The fruit is sweet."),
96:("물을 마셔요.","I drink water."),
97:("우유 한 잔 주세요.","A glass of milk, please."),
98:("커피 마실래요?","Want to drink coffee?"),
99:("차 한 잔 어때요?","How about a cup of tea?"),
100:("음료수를 주문해요.","I order a drink."),
101:("술을 안 마셔요.","I don't drink alcohol."),
102:("계란을 삶아요.","I boil eggs."),
103:("설탕을 넣지 마세요.","Please don't add sugar."),
104:("소금이 부족해요.","Not enough salt."),
105:("기름이 많아요.","There's a lot of oil."),
106:("사과를 좋아해요.","I like apples."),
107:("바나나를 먹어요.","I eat a banana."),
108:("포도가 달아요.","The grapes are sweet."),
109:("딸기가 빨개요.","The strawberries are red."),
110:("수박은 여름 과일이에요.","Watermelon is a summer fruit."),
111:("배추로 김치를 만들어요.","I make kimchi with napa cabbage."),
112:("무 한 개 주세요.","One radish, please."),
113:("양파를 썰어요.","I slice an onion."),
114:("마늘을 다져요.","I mince garlic."),
115:("고추가 매워요.","The chili is spicy."),
116:("감자를 삶아요.","I boil potatoes."),
117:("고구마가 달아요.","Sweet potatoes are sweet."),
118:("이 식당이 유명해요.","This restaurant is famous."),
119:("카페에서 친구를 만나요.","I meet a friend at the café."),
120:("편의점에 가요.","I'm going to the convenience store."),
121:("시장에서 채소를 사요.","I buy vegetables at the market."),
122:("마트에서 장을 봐요.","I do shopping at the supermarket."),
123:("숟가락으로 먹어요.","I eat with a spoon."),
124:("젓가락을 사용해요.","I use chopsticks."),
125:("그릇에 담아 주세요.","Please put it in a bowl."),
126:("컵에 물을 따라요.","I pour water into a cup."),
127:("식탁에 앉아요.","I sit at the dining table."),
128:("시간이 없어요.","I don't have time."),
129:("5분 기다리세요.","Please wait 5 minutes."),
130:("1초만요.","Just one second."),
131:("3시에 만나요.","Let's meet at 3 o'clock."),
132:("오늘 무슨 날이에요?","What day is today?"),
133:("이번 주 바빠요.","I'm busy this week."),
134:("다음 달에 봐요.","See you next month."),
135:("내년에 결혼해요.","I'm getting married next year."),
136:("오전에 회의가 있어요.","I have a meeting in the morning."),
137:("오후에 만나요.","Let's meet in the afternoon."),
138:("낮에 일해요.","I work during the day."),
139:("밤에 별이 보여요.","Stars are visible at night."),
140:("새벽에 일어나요.","I wake up at dawn."),
141:("아침에 운동해요.","I exercise in the morning."),
142:("저녁에 가족과 식사해요.","I dine with family in the evening."),
143:("오늘 날씨가 좋아요.","The weather is good today."),
144:("어제 비가 왔어요.","It rained yesterday."),
145:("그저께 만났어요.","We met the day before yesterday."),
146:("내일 시험이에요.","I have an exam tomorrow."),
147:("모레 떠나요.","I leave the day after tomorrow."),
148:("이번 주말에 뭐 해요?","What are you doing this weekend?"),
149:("지난 주말에 영화 봤어요.","I watched a movie last weekend."),
150:("다음 시간에 봐요.","See you next time."),
151:("평일에 일해요.","I work on weekdays."),
152:("주말은 쉬어요.","I rest on weekends."),
153:("내일은 휴일이에요.","Tomorrow is a holiday."),
154:("방학 때 여행 가요.","I travel during vacation."),
155:("휴가 잘 보내세요.","Have a great vacation."),
156:("생일 축하해요.","Happy birthday."),
157:("결혼 기념일이에요.","It's our wedding anniversary."),
158:("어떤 계절을 좋아해요?","Which season do you like?"),
159:("봄에 꽃이 펴요.","Flowers bloom in spring."),
160:("여름은 더워요.","Summer is hot."),
161:("가을이 시원해요.","Autumn is cool."),
162:("겨울이 추워요.","Winter is cold."),
163:("날씨가 어때요?","How's the weather?"),
164:("하늘이 파래요.","The sky is blue."),
165:("해가 떴어요.","The sun has risen."),
166:("달이 밝아요.","The moon is bright."),
167:("별이 많아요.","There are many stars."),
168:("구름이 많아요.","There are lots of clouds."),
169:("비가 와요.","It's raining."),
170:("눈이 내려요.","It's snowing."),
171:("바람이 불어요.","The wind is blowing."),
172:("온도가 높아요.","The temperature is high."),
173:("집에 가요.","I'm going home."),
174:("거실에서 TV를 봐요.","I watch TV in the living room."),
175:("방을 청소해요.","I clean my room."),
176:("부엌에서 요리해요.","I cook in the kitchen."),
177:("화장실이 어디예요?","Where is the bathroom?"),
178:("현관에서 신발을 벗어요.","Take off your shoes at the entrance."),
179:("엘리베이터를 타요.","I take the elevator."),
180:("학교에 가요.","I'm going to school."),
181:("회사에서 일해요.","I work at a company."),
182:("공원에서 산책해요.","I take a walk in the park."),
183:("도서관에서 공부해요.","I study at the library."),
184:("박물관을 구경해요.","I'm looking around the museum."),
185:("은행에서 돈을 찾아요.","I withdraw money at the bank."),
186:("우체국에 편지를 보내요.","I send a letter at the post office."),
187:("경찰서에 신고해요.","I report it to the police station."),
188:("소방서에 전화해요.","I call the fire station."),
189:("공항으로 가요.","I'm heading to the airport."),
190:("역까지 걸어가요.","I walk to the station."),
191:("정류장에서 기다려요.","I wait at the bus stop."),
192:("백화점에서 옷을 사요.","I buy clothes at the department store."),
193:("쇼핑몰에 가요.","I'm going to the mall."),
194:("서점에서 책을 사요.","I buy a book at the bookstore."),
195:("약국에서 약을 받아요.","I pick up medicine at the pharmacy."),
196:("미용실에서 머리를 잘라요.","I get a haircut at the hair salon."),
197:("세탁소에 옷을 맡겨요.","I leave clothes at the laundry."),
198:("영화관에서 영화를 봐요.","I watch a movie at the cinema."),
199:("노래방에서 노래해요.","I sing at the karaoke room."),
200:("헬스장에서 운동해요.","I work out at the gym."),
201:("호텔에서 묵어요.","I stay at a hotel."),
202:("어느 나라에서 왔어요?","Which country are you from?"),
203:("한국에 살아요.","I live in Korea."),
204:("고향이 그리워요.","I miss my hometown."),
205:("서울은 큰 도시예요.","Seoul is a big city."),
206:("시골 생활이 좋아요.","I like country life."),
207:("이 거리는 조용해요.","This street is quiet."),
208:("산이 높아요.","The mountain is high."),
209:("바다가 넓어요.","The sea is vast."),
210:("강이 길어요.","The river is long."),
211:("섬으로 여행 가요.","I travel to an island."),
212:("호수가 아름다워요.","The lake is beautiful."),
213:("다리를 건너요.","I cross the bridge."),
214:("저 건물이 높아요.","That building is tall."),
215:("좋은 장소를 알아요?","Do you know a good place?"),
216:("컴퓨터를 켜요.","I turn on the computer."),
217:("노트북을 사고 싶어요.","I want to buy a laptop."),
218:("핸드폰이 어디 있어요?","Where is my phone?"),
219:("전화기가 울려요.","The phone is ringing."),
220:("텔레비전을 봐요.","I watch television."),
221:("냉장고 안에 있어요.","It's in the refrigerator."),
222:("세탁기를 돌려요.","I run the washing machine."),
223:("에어컨을 켜요.","I turn on the air conditioner."),
224:("전자레인지에 데워요.","I heat it in the microwave."),
225:("카메라로 찍어요.","I take a photo with the camera."),
226:("충전기 좀 빌려 주세요.","Please lend me a charger."),
227:("배터리가 없어요.","The battery is dead."),
228:("침대에 누워요.","I lie on the bed."),
229:("책상에서 일해요.","I work at the desk."),
230:("의자에 앉으세요.","Please have a seat."),
231:("옷장에 옷을 넣어요.","I put clothes in the wardrobe."),
232:("거울을 봐요.","I look in the mirror."),
233:("창문을 열어요.","I open the window."),
234:("문을 닫아 주세요.","Please close the door."),
235:("시계가 멈췄어요.","The clock stopped."),
236:("조명이 어두워요.","The lighting is dim."),
237:("안경을 써요.","I wear glasses."),
238:("우산을 가져가요.","Take an umbrella."),
239:("열쇠를 잃어버렸어요.","I lost my key."),
240:("지갑이 없어요.","I don't have my wallet."),
241:("가방이 무거워요.","The bag is heavy."),
242:("돈이 부족해요.","I don't have enough money."),
243:("카드로 결제해요.","I pay with a card."),
244:("영수증 주세요.","Receipt, please."),
245:("책을 읽어요.","I read a book."),
246:("공책에 적어요.","I write it in a notebook."),
247:("종이 한 장 주세요.","One sheet of paper, please."),
248:("펜으로 써요.","I write with a pen."),
249:("연필이 부러졌어요.","My pencil broke."),
250:("지우개로 지워요.","I erase it with an eraser."),
251:("가위로 잘라요.","I cut it with scissors."),
252:("풀로 붙여요.","I glue it together."),
253:("편지를 써요.","I write a letter."),
254:("봉투에 넣어요.","I put it in an envelope."),
255:("차를 운전해요.","I drive a car."),
256:("버스를 타요.","I take the bus."),
257:("지하철이 빨라요.","The subway is fast."),
258:("택시를 불러요.","I call a taxi."),
259:("기차로 여행해요.","I travel by train."),
260:("비행기를 타요.","I get on the airplane."),
261:("배를 타요.","I take a boat."),
262:("자전거를 타요.","I ride a bicycle."),
263:("오토바이 조심하세요.","Watch out for motorcycles."),
264:("킥보드를 빌려요.","I rent a kick scooter."),
265:("신호등이 빨개요.","The traffic light is red."),
266:("지도 좀 보여 주세요.","Show me the map, please."),
267:("표를 사요.","I buy a ticket."),
268:("요금이 얼마예요?","How much is the fare?"),
269:("주차장이 어디예요?","Where is the parking lot?"),
270:("인터넷이 느려요.","The internet is slow."),
271:("이메일을 보내요.","I send an email."),
272:("문자 받았어요.","I got a text message."),
273:("전화번호 알려 주세요.","Please tell me your phone number."),
274:("주소를 알려 주세요.","Please give me the address."),
275:("홈페이지에서 확인해요.","Check it on the website."),
276:("비밀번호를 잊었어요.","I forgot my password."),
277:("뉴스를 봐요.","I watch the news."),
278:("신문을 읽어요.","I read the newspaper."),
279:("잡지를 봐요.","I look at the magazine."),
280:("소문이 빨라요.","Rumors spread fast."),
281:("옷을 입어요.","I put on clothes."),
282:("티셔츠를 좋아해요.","I like T-shirts."),
283:("바지를 사요.","I'm buying pants."),
284:("치마가 예뻐요.","The skirt is pretty."),
285:("원피스를 입어요.","I'm wearing a dress."),
286:("셔츠를 다려요.","I iron the shirt."),
287:("코트를 입어요.","I wear a coat."),
288:("점퍼가 따뜻해요.","The jumper is warm."),
289:("속옷을 갈아입어요.","I change my underwear."),
290:("양말을 신어요.","I put on socks."),
291:("신발을 벗으세요.","Please take off your shoes."),
292:("운동화가 편해요.","Sneakers are comfortable."),
293:("구두가 예뻐요.","The dress shoes are pretty."),
294:("슬리퍼를 신어요.","I'm wearing slippers."),
295:("모자를 써요.","I wear a hat."),
296:("장갑을 끼세요.","Put on gloves."),
297:("목도리를 둘러요.","I wrap a scarf around my neck."),
298:("넥타이를 매요.","I tie a necktie."),
299:("안경을 닦아요.","I wipe my glasses."),
300:("액세서리가 예뻐요.","The accessory is pretty."),
301:("수업이 재미있어요.","The class is fun."),
302:("공부가 어려워요.","Studying is hard."),
303:("시험이 곧 시작해요.","The exam starts soon."),
304:("이 문제가 어려워요.","This problem is hard."),
305:("정답을 모르겠어요.","I don't know the answer."),
306:("숙제가 많아요.","I have a lot of homework."),
307:("이번 학기는 바빠요.","This semester is busy."),
308:("전공이 뭐예요?","What is your major?"),
309:("성적이 좋아요.","My grades are good."),
310:("졸업을 축하해요.","Congratulations on your graduation."),
311:("내년에 입학해요.","I'll enter school next year."),
312:("사전을 찾아봐요.","I look it up in the dictionary."),
313:("교육이 중요해요.","Education is important."),
314:("질문이 있어요.","I have a question."),
315:("대답을 들었어요.","I heard the answer."),
316:("일이 많아요.","I have a lot of work."),
317:("직업이 뭐예요?","What's your job?"),
318:("회의가 길어요.","The meeting is long."),
319:("서류를 정리해요.","I organize the documents."),
320:("보고서를 써요.","I write a report."),
321:("성공을 빌어요.","I wish you success."),
322:("실패해도 괜찮아요.","It's okay to fail."),
323:("계획이 있어요?","Do you have a plan?"),
324:("준비가 됐어요?","Are you ready?"),
325:("오늘 회식이에요.","We have a company dinner today."),
326:("월급을 받았어요.","I got my salary."),
327:("보너스를 받았어요.","I received a bonus."),
328:("출근 시간이에요.","It's time to go to work."),
329:("이제 퇴근해요.","I'm leaving work now."),
330:("내일 출장 가요.","I'm going on a business trip tomorrow."),
331:("기분이 좋아요.","I'm in a good mood."),
332:("사랑해요.","I love you."),
333:("마음이 따뜻해요.","My heart is warm."),
334:("좋은 생각이에요.","That's a good idea."),
335:("꿈이 있어요.","I have a dream."),
336:("희망을 가져요.","Have hope."),
337:("행복하세요.","Be happy."),
338:("슬픔을 이겨요.","Overcome the sadness."),
339:("걱정하지 마세요.","Don't worry."),
340:("화를 내지 마세요.","Don't get angry."),
341:("재미있어요.","It's fun."),
342:("약속을 지켜요.","I keep my promise."),
343:("좋은 추억이에요.","It's a good memory."),
344:("세상은 넓어요.","The world is wide."),
345:("사회가 변하고 있어요.","Society is changing."),
346:("경제가 어려워요.","The economy is tough."),
347:("문화 차이가 있어요.","There's a cultural difference."),
348:("역사를 공부해요.","I study history."),
349:("법을 지켜요.","I obey the law."),
350:("정치에 관심이 있어요.","I'm interested in politics."),
351:("평화를 원해요.","I want peace."),
352:("자유를 사랑해요.","I love freedom."),
353:("성격이 좋아요.","Your personality is great."),
354:("취미가 뭐예요?","What's your hobby?"),
355:("좋은 습관을 만들어요.","I build good habits."),
356:("특징이 뭐예요?","What's the feature?"),
357:("종류가 많아요.","There are many types."),
358:("좋은 방법이에요.","That's a good method."),
359:("이유가 뭐예요?","What's the reason?"),
360:("결과가 좋아요.","The result is good."),
361:("목적이 뭐예요?","What's the purpose?"),
362:("내용이 좋아요.","The content is good."),
363:("의미가 깊어요.","The meaning is deep."),
364:("사실이에요.","It's true."),
365:("가짜 뉴스예요.","It's fake news."),
366:("비밀이에요.","It's a secret."),
367:("이름이 뭐예요?","What's your name?"),
368:("번호를 알려 주세요.","Please tell me the number."),
369:("제목이 뭐예요?","What's the title?"),
}

# Extract noun list
html = SRC.read_text(encoding="utf-8")
m = re.search(r'<div class="chapter" id="ch38">.*?(?=<div class="chapter" id="ch39")', html, re.S)
block = m.group(0)
def clean(s): return unescape(re.sub(r"<[^>]+>", "", s)).strip()

rows = []
current = ""
for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', block, re.S):
    row = tr.group(1)
    if 'colspan="6"' in row:
        txt = clean(row)
        if txt and not txt.startswith("한글"):
            current = txt
        continue
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
    if len(cells) != 6: continue
    g1, p1, e1, g2, p2, e2 = [clean(c) for c in cells]
    if g1 == "한글": continue
    for g, p, e in [(g1, p1, e1), (g2, p2, e2)]:
        if not g: continue
        rows.append((current, g, p, e))

print(f"Extracted {len(rows)} nouns; have {len(EX)} examples")

items = []
last = None
for i, (sec, g, p, e) in enumerate(rows, 1):
    if sec != last:
        items.append(f'<tr class="section"><td colspan="5">{escape(sec)}</td></tr>')
        last = sec
    ex_ko, ex_en = EX.get(i, ("", ""))
    items.append(
        f'<tr>'
        f'<td class="num">{i}</td>'
        f'<td class="k">{escape(g)}</td>'
        f'<td class="r">{escape(p)}</td>'
        f'<td class="en">{escape(e)}</td>'
        f'<td class="ex"><span class="ex-ko">{escape(ex_ko)}</span><span class="ex-en">{escape(ex_en)}</span></td>'
        f'</tr>'
    )

OUT = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>Essential Korean Nouns · 예문 포함</title>
<style>
  @page { size: A4; margin: 16mm 12mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; color:#1a1a2e; margin:0; line-height:1.45; }
  .cover { text-align:center; padding:60px 20px 30px; border-bottom:4px solid #C0392B; margin-bottom:22px; }
  .cover .label { font-size:12px; font-weight:700; letter-spacing:3px; color:#C0392B; text-transform:uppercase; margin-bottom:14px; }
  .cover h1 { font-size:34px; margin:0 0 8px; color:#1a1a2e; font-weight:800; }
  .cover .kr { font-size:22px; color:#1A4A8A; font-weight:700; margin:0 0 18px; }
  .cover .desc { font-size:13px; color:#555; max-width:580px; margin:0 auto; line-height:1.7; }
  table { width:100%; border-collapse:collapse; font-size:11px; table-layout:fixed; }
  thead th { background:#1a1a2e; color:#fff; padding:7px 6px; font-size:10px; letter-spacing:0.4px; border-bottom:2px solid #C0392B; }
  th.num-col{width:32px;} th.k-col{width:90px;} th.r-col{width:80px;} th.en-col{width:130px;}
  td { padding:6px 8px; border-bottom:1px solid #e5e5ea; vertical-align:top; word-break:keep-all; }
  tr:nth-child(even) td { background:#fafafa; }
  td.num { text-align:center; color:#888; font-weight:600; font-size:10px; }
  td.k   { font-weight:600; color:#1a1a2e; font-size:13px; }
  td.r   { color:#6b6b6b; font-style:italic; font-size:11px; }
  td.en  { color:#1A4A8A; font-size:11px; }
  td.ex .ex-ko { display:block; color:#C0392B; font-weight:600; font-size:11px; }
  td.ex .ex-en { display:block; color:#666; font-style:italic; font-size:10px; margin-top:1px; }
  tr.section td { background:linear-gradient(135deg,#1a1a2e,#16213e) !important; color:#fff; font-weight:800; font-size:12px; letter-spacing:1.2px; padding:8px 12px; text-transform:uppercase; }
  tr.section td::before { content:"▸  "; color:#f97316; }
</style></head><body>

<div class="cover">
  <div class="label">Korean Essential Nouns · with Examples</div>
  <h1>Essential Korean Nouns</h1>
  <div class="kr">필수 명사 · 예문 포함</div>
  <p class="desc">By category — Korean noun · Romanization · English meaning · Example sentence (예문)</p>
</div>

<table>
  <thead><tr>
    <th class="num-col">#</th>
    <th class="k-col">한글</th>
    <th class="r-col">발음</th>
    <th class="en-col">English</th>
    <th>예문 Example</th>
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
                f"--print-to-pdf={PDF_OUT}", url], capture_output=True, timeout=180)
time.sleep(3)
if PDF_OUT.exists():
    print(f"PDF  → {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
