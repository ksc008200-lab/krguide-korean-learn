"""Publish 2 SEO-optimized blog series:
  Series A — Vocab Hub deep-dives (15 posts)
  Series B — Korean Culture deep-dives (12 posts)

SEO features per post:
- Targeted focus keyword in title, first paragraph, H2, URL, meta description
- Excerpt = SEO meta description (155 chars)
- JSON-LD Article schema + FAQPage schema (featured snippet target)
- Table of contents (anchor links)
- 3 FAQ questions per post (Google PAA target)
- Internal cross-links between posts
- Outbound links to Vocab Hub & Gumroad with rel="noopener"
- Semantic H2/H3, alt text, structured data
"""
import requests, base64, time, json, html

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

VOCAB_HUB = "https://study.krguide.com/vocab-hub.html"
GUMROAD   = "https://jssmn21.gumroad.com/l/gnefla"
SITE_NAME = "KRGuide"

# ============================================================
# SERIES A — VOCAB HUB (15 posts)
# ============================================================
VOCAB_POSTS = [
    {
        "title": "200 Essential Korean Verbs Every Learner Must Master in 2026",
        "slug":  "200-essential-korean-verbs-every-learner-must-master",
        "kw":    "Korean verbs",
        "meta":  "Master the 200 most essential Korean verbs with romanization, examples, and conjugation tips. Free preview of our complete verb learning resource.",
        "hero":  "동사가 곧 한국어다",
        "intro": "If you only learn one part of speech in Korean, make it <strong>Korean verbs</strong>. Korean grammar pivots entirely around the verb stem — internalize the 200 highest-frequency verbs and you unlock about 80% of daily conversation.",
        "samples": [
            ("가다","ga-da","to go"),("오다","o-da","to come"),("먹다","meok-da","to eat"),
            ("마시다","ma-si-da","to drink"),("보다","bo-da","to see / watch"),
            ("듣다","deut-da","to hear / listen"),("말하다","mal-ha-da","to speak"),
            ("읽다","ilk-da","to read"),("쓰다","sseu-da","to write / use"),
            ("자다","ja-da","to sleep"),("일어나다","il-eo-na-da","to wake up"),
            ("앉다","an-da","to sit"),("하다","ha-da","to do"),
            ("되다","doe-da","to become"),("주다","ju-da","to give"),
        ],
        "tip": "Always learn a Korean verb in its dictionary form (-다 ending). The -다 is just a citation marker — when speaking, strip it and attach an ending: -아요/-어요 (polite), -ㅂ니다 (formal), -ㄴ다 (plain).",
        "culture": "Korean does not conjugate by person (I/you/he). Whether the subject is 나, 너, or 그녀, the verb form stays the same. Particles and context carry the meaning.",
        "faqs": [
            ("How many Korean verbs do I need to be conversational?",
             "Around 200 high-frequency verbs cover roughly 80% of daily conversation. Mastering these gives you functional fluency for travel, ordering food, basic work, and social interactions."),
            ("Are Korean verbs hard to conjugate?",
             "Korean verb conjugation is simpler than European languages — there is no person agreement. You only need to learn tense, formality level, and a few irregular patterns."),
            ("What's the most common Korean verb?",
             "하다 (ha-da, 'to do') is the single most common — it attaches to thousands of nouns to form verbs (공부하다 = to study, 일하다 = to work, 사랑하다 = to love)."),
        ],
        "related": ["200-korean-adverbs-sound-natural-fluent", "369-common-korean-nouns-every-beginner-should-know"],
    },
    {
        "title": "200 Korean Adverbs to Sound Natural & Fluent (Native Tips)",
        "slug":  "200-korean-adverbs-sound-natural-fluent",
        "kw":    "Korean adverbs",
        "meta":  "Learn 200 essential Korean adverbs like 그냥, 좀, 진짜 that make your Korean sound natural. Sample list, learning tips, and free resource.",
        "hero":  "Adverbs unlock fluency",
        "intro": "Beginners learn nouns. Intermediates learn grammar. But fluency comes from <strong>Korean adverbs</strong>. Words like 그냥, 좀, 진짜, 막, 약간 transform robotic Korean into natural human speech.",
        "samples": [
            ("그냥","geu-nyang","just / simply"),("좀","jom","a little (softener)"),
            ("진짜","jin-jja","really"),("정말","jeong-mal","truly"),
            ("아주","a-ju","very"),("너무","neo-mu","too / very"),
            ("매우","mae-u","extremely (formal)"),("약간","yak-gan","a bit"),
            ("조금","jo-geum","a little"),("많이","ma-ni","a lot"),
            ("천천히","cheon-cheon-hi","slowly"),("빨리","ppal-li","quickly"),
            ("벌써","beol-sseo","already"),("아직","a-jik","still / not yet"),
            ("막","mak","just now / recklessly"),
        ],
        "tip": "Native speakers sprinkle 좀 (jom) into nearly every polite request. '커피 주세요' is correct but blunt. '커피 좀 주세요' is the natural, polite version. The 좀 softens.",
        "culture": "Korean adverbs frequently double for emphasis: 정말정말 좋아요 (really really good), 빨리빨리 (Korea's unofficial national catchphrase).",
        "faqs": [
            ("What's the difference between 진짜 and 정말?",
             "정말 (jeong-mal) is slightly more polite and formal. 진짜 (jin-jja) is more casual and emphatic. Use 정말 with strangers and elders, 진짜 with friends."),
            ("How is 너무 different from 아주?",
             "너무 originally meant 'excessive' (too much, negative) but modern usage allows positive ('너무 좋아요' = really good). 아주 is purely 'very' and neutral."),
            ("Why do Koreans say 좀 so often?",
             "좀 softens requests, makes statements less direct, and adds politeness. It's the conversational lubricant of polite Korean."),
        ],
        "related": ["200-essential-korean-verbs-every-learner-must-master", "369-common-korean-nouns-every-beginner-should-know"],
    },
    {
        "title": "369 Common Korean Nouns Every Beginner Should Know in 2026",
        "slug":  "369-common-korean-nouns-every-beginner-should-know",
        "kw":    "Korean nouns",
        "meta":  "Build core Korean vocabulary with 369 essential nouns organized by life domain — home, food, work, family, emotions. Free sample list and study tips.",
        "hero":  "Vocabulary is the bedrock",
        "intro": "Grammar is the skeleton, but <strong>Korean nouns</strong> are the flesh. Without enough nouns, you can't describe your day, ask for what you need, or follow a K-drama. We organized 369 of the most useful nouns by life domain.",
        "samples": [
            ("집","jip","house / home"),("학교","hak-gyo","school"),
            ("회사","hoe-sa","company"),("친구","chin-gu","friend"),
            ("가족","ga-jok","family"),("음식","eum-sik","food"),
            ("물","mul","water"),("시간","si-gan","time"),
            ("돈","don","money"),("일","il","work / day"),
            ("사람","sa-ram","person"),("아이","a-i","child"),
            ("책","chaek","book"),("길","gil","road / way"),
            ("마음","ma-eum","mind / heart"),
        ],
        "tip": "Korean nouns don't change for plural. 책 (book) and 책 (books) are identical — context handles the number. Add -들 only when plural must be marked: 사람들 (people).",
        "culture": "Several Korean nouns carry deep cultural weight. 마음 is not just 'mind' — it's the seat of feeling, intention, and integrity. 정 (jeong) has no direct English equivalent.",
        "faqs": [
            ("How many Korean nouns should I learn first?",
             "Start with 300–500 high-frequency nouns covering daily life domains: home, food, family, work, time, money. This base supports basic conversation."),
            ("Do Korean nouns have gender?",
             "No. Korean nouns have no grammatical gender — unlike Spanish, French, or German. This is one of the easier aspects of Korean for English speakers."),
            ("Why does Korean have so many words for the same family member?",
             "Korean kinship terms encode the speaker's gender and relative age. 형/오빠 both mean 'older brother' but 형 is used by males, 오빠 by females."),
        ],
        "related": ["200-essential-korean-verbs-every-learner-must-master", "500-korean-honorifics-master-polite-speech-native"],
    },
    {
        "title": "500 Korean Honorifics — Master 존댓말 Like a Native",
        "slug":  "500-korean-honorifics-master-polite-speech-native",
        "kw":    "Korean honorifics",
        "meta":  "Master 500 Korean honorific forms (존댓말) across verbs, nouns, and titles. Avoid social mistakes — speak respectfully like a native.",
        "hero":  "존댓말 마스터",
        "intro": "<strong>Korean honorifics</strong> (존댓말) are not optional. Use the wrong form with a boss, elder, or stranger and you'll seem rude — even with perfect grammar. We cataloged 500 honorific forms across verbs, nouns, particles, and titles.",
        "samples": [
            ("드시다","deu-si-da","to eat (honorific of 먹다)"),
            ("계시다","gye-si-da","to be / stay (honorific)"),
            ("말씀하시다","mal-sseum-ha-si-da","to speak (honorific)"),
            ("주무시다","ju-mu-si-da","to sleep (honorific)"),
            ("돌아가시다","do-ra-ga-si-da","to pass away (euphemism)"),
            ("진지","jin-ji","meal (honorific of 밥)"),
            ("연세","yeon-se","age (honorific of 나이)"),
            ("성함","seong-ham","name (honorific of 이름)"),
            ("께서","kke-seo","honorific subject marker"),
            ("께","kke","honorific recipient marker"),
            ("선생님","seon-saeng-nim","teacher / sir"),
            ("사장님","sa-jang-nim","boss"),
            ("어머님","eo-meo-nim","mother (honorific)"),
            ("아버님","a-beo-nim","father (honorific)"),
            ("손님","son-nim","guest / customer"),
        ],
        "tip": "Add -시- to a verb stem to make it honorific. 먹다 → 드시다 (special) or 가다 → 가시다 (add -시-). Stack with polite endings: 가세요 (please go).",
        "culture": "Koreans use honorifics with anyone older or higher in status — even a sibling one year older. Drop honorifics only after explicit agreement ('말 놔도 돼').",
        "faqs": [
            ("When do I use 존댓말?",
             "Always with strangers, customers, elders (1+ year older), bosses, teachers, and in business. Drop only after explicit permission from the senior party."),
            ("What's the difference between 반말 and 존댓말?",
             "반말 (informal speech) is used between close friends, family, and to younger people. 존댓말 (formal speech) is used with everyone else by default."),
            ("Is using -님 always honorific?",
             "Yes. -님 is the universal honorific suffix attached to titles: 선생님 (teacher), 의사선생님 (doctor), 사장님 (CEO), 손님 (customer)."),
        ],
        "related": ["369-common-korean-nouns-every-beginner-should-know", "100-essential-korean-idioms-sajaseongeo-sophisticated-speech"],
    },
    {
        "title": "391 Japanese Loanwords in Korean (일본어 외래어) Explained",
        "slug":  "391-japanese-loanwords-korean-explained",
        "kw":    "Japanese loanwords in Korean",
        "meta":  "391 Japanese loanwords still used in everyday Korean — 다꽝, 와사비, 오뎅, 간지, 기스. History, modern alternatives, and cultural context.",
        "hero":  "Hidden Japanese in Korean",
        "intro": "After 35 years of colonial occupation (1910–1945), hundreds of <strong>Japanese loanwords in Korean</strong> embedded into daily speech. 다꽝, 와사비, 뎀뿌라, 오뎅 sound Korean but are Japanese. Younger generations replace them, but you'll still hear them daily.",
        "samples": [
            ("다꽝","da-kkwang","pickled radish (J: takuan)"),
            ("와사비","wa-sa-bi","wasabi"),
            ("뎀뿌라","dem-ppu-ra","tempura"),
            ("오뎅","o-deng","fishcake stew"),
            ("스시","seu-si","sushi"),("사시미","sa-si-mi","sashimi"),
            ("나가리","na-ga-ri","called off (J: nagare)"),
            ("쇼부","syo-bu","showdown (J: shoubu)"),
            ("기스","gi-seu","scratch (J: kizu)"),
            ("땡땡이","ttaeng-ttaeng-i","polka dots (J: tenten)"),
            ("쓰메끼리","sseu-me-kki-ri","nail clippers (J: tsumekiri)"),
            ("후카시","hu-ka-si","showing off (J: fukashi)"),
            ("간지","gan-ji","style / cool (J: kanji)"),
            ("기리","gi-ri","obligation (J: giri)"),
            ("닭도리탕","dak-do-ri-tang","spicy chicken stew (debated)"),
        ],
        "tip": "Younger Koreans avoid Japanese loanwords. Use 단무지 instead of 다꽝, 어묵 instead of 오뎅. Older speakers and traditional markets still use originals.",
        "culture": "Korean government has periodically run '국어 순화' campaigns — language purification — to replace Japanese loanwords with native Korean equivalents.",
        "faqs": [
            ("Why are there Japanese words in Korean?",
             "From 1910–1945, Korea was under Japanese colonial rule. Japanese became the official language in schools and government, embedding hundreds of words that survived liberation."),
            ("Are Japanese loanwords disappearing from Korean?",
             "Slowly. Government and media campaigns promote native alternatives, and younger speakers actively avoid Japanese loanwords. But everyday speech still contains many."),
            ("Is using Japanese loanwords considered offensive?",
             "Generally no, but in formal/political contexts they're frowned upon. Older Koreans use them naturally; younger Koreans prefer Sino-Korean or pure Korean alternatives."),
        ],
        "related": ["500-konglish-words-when-english-becomes-korean", "hangul-vs-hanja-complete-bilingual-reference"],
    },
    {
        "title": "1,067 Korean Adjectives, Adverbs & Idioms — The Complete List",
        "slug":  "1067-korean-adjectives-adverbs-idioms-big-list",
        "kw":    "Korean adjectives",
        "meta":  "1,067 essential Korean adjectives, adverbs, and idioms for advanced fluency. Express emotion and nuance like a native speaker.",
        "hero":  "Big list, real fluency",
        "intro": "Once you've mastered basics, the next leap is descriptive power. The gap between 'good' and '괜찮네, 그치만 좀 아쉬워' is a thousand-word descriptor vocabulary. <strong>Korean adjectives</strong> and adverbs are where nuance lives.",
        "samples": [
            ("예쁘다","ye-ppeu-da","pretty"),("멋있다","meo-sit-da","cool / stylish"),
            ("귀엽다","gwi-yeop-da","cute"),("아름답다","a-reum-dap-da","beautiful"),
            ("재미있다","jae-mi-it-da","fun / interesting"),
            ("지루하다","ji-ru-ha-da","boring"),("아쉽다","a-swip-da","regrettable"),
            ("괜찮다","gwaen-chan-ta","okay / fine"),
            ("끔찍하다","kkeum-jji-ka-da","terrible"),
            ("훌륭하다","hul-lyung-ha-da","excellent"),
            ("어이없다","eo-i-eop-da","absurd / unbelievable"),
            ("당황스럽다","dang-hwang-seu-reop-da","flustered"),
            ("후련하다","hu-ryeon-ha-da","relieved"),
            ("뿌듯하다","ppu-deu-ta-da","proud / fulfilled"),
            ("심심하다","sim-sim-ha-da","bored"),
        ],
        "tip": "Korean has emotion-adjectives English needs a phrase to translate. 뿌듯하다 = 'warm pride of having done something meaningful.' 아쉽다 = 'wishing it could've been different.'",
        "culture": "Body-part idioms are huge: 눈치가 빠르다 (quick-eye = perceptive), 입이 무겁다 (heavy mouth = can keep a secret), 발이 넓다 (wide foot = well-connected).",
        "faqs": [
            ("Are Korean adjectives really verbs?",
             "Yes — Korean adjectives conjugate exactly like verbs (descriptive verbs / 형용사). 예쁘다 conjugates as 예뻐요, 예뻤어요, 예쁠 거예요."),
            ("Why don't Korean adjectives need 'is/are'?",
             "Because they ARE verbs. '꽃이 예쁘다' literally is 'the flower is-pretty.' No separate copula needed."),
            ("How do I know if something is an adjective or verb in Korean?",
             "Try a present-tense -는 ending: verbs accept it (먹는 = eating), adjectives reject it (예쁘는 ✗ → 예쁜 ✓)."),
        ],
        "related": ["500-korean-onomatopoeia-uiseongeo-uitaego-explained", "100-essential-korean-idioms-sajaseongeo-sophisticated-speech"],
    },
    {
        "title": "500 Korean Internet Slang Words You'll Hear in 2026",
        "slug":  "500-korean-internet-slang-words-2026-edition",
        "kw":    "Korean internet slang",
        "meta":  "500 Korean internet slang words used by Gen Z on KakaoTalk, Twitter, and Instagram in 2026 — 인싸, 갓-, 핵-, ㅇㅈ, and more.",
        "hero":  "Modern Internet 인싸 vocabulary",
        "intro": "<strong>Korean internet slang</strong> evolves faster than dictionaries can track. 인싸/아싸, ㅇㅇ, ㄴㄴ, 갓-, 핵-, 미쳤다 — slang is where the language is alive. We documented 500 active terms used on Twitter, KakaoTalk, Instagram, and gaming chat.",
        "samples": [
            ("인싸","in-ssa","insider / popular"),
            ("아싸","a-ssa","outsider / loner"),
            ("핵-","haek-","nuke- (intensifier prefix)"),
            ("갓-","gat-","god-tier (prefix)"),
            ("존-","jon-","super- (intensifier)"),
            ("ㅇㅇ","eung-eung","yes"),("ㄴㄴ","no-no","no"),
            ("ㄱㄱ","go-go","let's go"),("ㅋㅋ","keu-keu","lol"),
            ("ㄷㄷ","deol-deol","impressive / shivering"),
            ("ㅈㅂ","je-bal","please (제발)"),
            ("미친","mi-chin","crazy (good or bad)"),
            ("실화냐","sil-hwa-nya","is this real life?"),
            ("개꿀","gae-kkul","super sweet deal"),
            ("ㅇㅈ","in-jeong","I admit / agree"),
        ],
        "tip": "Korean Gen Z constantly invents acronyms from initial consonants (자음 약어). ㅇㅈ = 인정, ㅁㅈ = 미정, ㅂㅂ = 바이바이. Reading consonants aloud usually reveals the word.",
        "culture": "Slang is generation-coded. Using 'ㅈㅎㅁ' (자존감) in a corporate Slack will get strange looks. Use it on Twitter or with friends.",
        "faqs": [
            ("Is Korean internet slang used in speech?",
             "Yes — younger Koreans often pronounce slang aloud. 'ㅋㅋ' becomes 'keu-keu' said out loud. 'ㅇㅈ?' becomes 'in-jeong?'"),
            ("Can I use Korean slang at work?",
             "Be cautious. Tech startups and creative agencies tolerate slang in casual chats. Traditional corporations and formal emails — never."),
            ("What's 갓-과 핵-의 difference?",
             "갓- (god) marks excellence: 갓영화 = god-tier movie. 핵- (nuclear) marks intensity: 핵귀여워 = nuke-cute. Both are positive intensifiers."),
        ],
        "related": ["500-konglish-words-when-english-becomes-korean", "500-korean-onomatopoeia-uiseongeo-uitaego-explained"],
    },
    {
        "title": "500 Konglish Words — Korean English That Confuses Everyone",
        "slug":  "500-konglish-words-when-english-becomes-korean",
        "kw":    "Konglish",
        "meta":  "500 Konglish words explained — Korean-English hybrid vocabulary like 핸드폰, 노트북, 화이팅. Decode Korea's unique English instantly.",
        "hero":  "Konglish: English with Korean rules",
        "intro": "<strong>Konglish</strong> is English vocabulary reshaped into Korean — sometimes with new meanings, sometimes with pronunciation English speakers can barely recognize. 핸드폰, 노트북, 아이쇼핑, 원샷, 화이팅 — Konglish, not English.",
        "samples": [
            ("핸드폰","haen-deu-pon","cell phone (lit. hand phone)"),
            ("노트북","no-teu-buk","laptop (lit. notebook)"),
            ("아이쇼핑","a-i-syo-ping","window shopping (eye shopping)"),
            ("원샷","won-syat","drink in one shot"),
            ("화이팅","hwa-i-ting","go for it!"),
            ("스킨십","seu-kin-sip","physical affection"),
            ("아파트","a-pa-teu","apartment"),
            ("원룸","won-rum","studio apartment"),
            ("리모컨","ri-mo-keon","remote control"),
            ("에어컨","e-eo-keon","air conditioner"),
            ("백미러","baek-mi-reo","rearview mirror"),
            ("샐러리맨","sael-leo-ri-maen","office worker"),
            ("팬티","paen-ti","underwear"),
            ("원피스","won-pi-seu","dress"),
            ("매니큐어","mae-ni-kyu-eo","nail polish"),
        ],
        "tip": "Konglish often shortens English. 'Apartment' → 아파트, 'remote control' → 리모컨. When you hear unfamiliar English-sounding Korean, try expanding the syllables.",
        "culture": "'화이팅' (fighting) is shouted as cheer/encouragement before tests, sports, weddings, and hospital visits. It does NOT mean fighting in any violent sense.",
        "faqs": [
            ("Why is Korean English called Konglish?",
             "Konglish is a portmanteau of 'Korean' and 'English' — describing English-origin words that have been integrated into Korean with shifted meanings, pronunciation, or grammar."),
            ("Can I use English words instead of Konglish in Korea?",
             "Saying 'cell phone' instead of 핸드폰 may not be understood. Native Konglish forms are often the only forms Koreans recognize."),
            ("What's the most confusing Konglish word?",
             "스킨십 (skin-ship) — coined in Korea, means 'physical affection between non-romantic partners.' English speakers find it surprising."),
        ],
        "related": ["500-korean-internet-slang-words-2026-edition", "391-japanese-loanwords-korean-explained"],
    },
    {
        "title": "500 Korean Onomatopoeia (의성어·의태어) Make Your Korean Vivid",
        "slug":  "500-korean-onomatopoeia-uiseongeo-uitaego-explained",
        "kw":    "Korean onomatopoeia",
        "meta":  "Master 500 Korean onomatopoeia (의성어 의태어) — sound and motion words like 반짝반짝, 두근두근, 후루룩 that make Korean vivid and natural.",
        "hero":  "Korean sounds like a soundtrack",
        "intro": "<strong>Korean onomatopoeia</strong> is one of the world's richest — over 8,000 documented sound and motion words. 반짝반짝 (sparkly), 두근두근 (heart pounding), 후루룩 (slurping). Master 500 and your Korean instantly becomes vivid and natural.",
        "samples": [
            ("반짝반짝","ban-jjak-ban-jjak","sparkly / twinkling"),
            ("두근두근","du-geun-du-geun","heart pounding"),
            ("후루룩","hu-ru-ruk","slurping noodles"),
            ("쾅쾅","kwang-kwang","banging"),
            ("꿀꺽","kkul-kkeok","gulping"),
            ("팔랑팔랑","pal-lang-pal-lang","fluttering"),
            ("미끌미끌","mi-kkeul-mi-kkeul","slippery"),
            ("뽀송뽀송","ppo-song-ppo-song","fluffy/dry"),
            ("말랑말랑","mal-lang-mal-lang","soft / squishy"),
            ("바삭바삭","ba-sak-ba-sak","crispy"),
            ("쿨쿨","kul-kul","snoring"),
            ("훌쩍훌쩍","hul-jjeok-hul-jjeok","sobbing"),
            ("덜덜","deol-deol","shivering"),
            ("두둥","du-dung","dramatic reveal sound"),
            ("쨍그랑","jjaeng-geu-rang","glass shattering"),
        ],
        "tip": "Korean onomatopoeia frequently doubles for intensity — 반짝 = sparkle, 반짝반짝 = lots of sparkling. Doubling almost always increases vividness.",
        "culture": "K-drama subtitles for English audiences often skip onomatopoeia entirely because they don't translate. Learning them deepens your drama immersion dramatically.",
        "faqs": [
            ("What's the difference between 의성어 and 의태어?",
             "의성어 (uiseongeo) imitates actual sounds (멍멍 = woof, 쾅 = bang). 의태어 (uitaego) describes manner or appearance without sound (반짝반짝 = sparkly)."),
            ("Are Korean onomatopoeia used in formal writing?",
             "Less than in casual speech, but Korean literature and journalism use them more freely than English would. They're not 'childish' in Korean culture."),
            ("How do I learn them efficiently?",
             "Pair each onomatopoeia with a vivid image or short K-drama clip. Repetition + visual context cements them in long-term memory."),
        ],
        "related": ["1067-korean-adjectives-adverbs-idioms-big-list", "500-korean-internet-slang-words-2026-edition"],
    },
    {
        "title": "100 Korean Idioms (사자성어) for Sophisticated Speech",
        "slug":  "100-essential-korean-idioms-sajaseongeo-sophisticated-speech",
        "kw":    "Korean idioms 사자성어",
        "meta":  "100 essential Korean four-character idioms (사자성어) for advanced speech and writing. Boost your fluency with classical wisdom.",
        "hero":  "Four-character power",
        "intro": "<strong>사자성어 (sa-ja-seong-eo)</strong> are four-character idioms borrowed from Classical Chinese, embedded in formal Korean speech and writing. Sprinkling them into business meetings, essays, or speeches signals education and sophistication.",
        "samples": [
            ("일석이조","il-seok-i-jo","two birds one stone"),
            ("동상이몽","dong-sang-i-mong","same bed, different dreams"),
            ("자업자득","ja-eop-ja-deuk","reap what you sow"),
            ("우유부단","u-yu-bu-dan","indecisive"),
            ("새옹지마","sae-ong-ji-ma","blessing in disguise"),
            ("점입가경","jeom-ip-ga-gyeong","getting more interesting"),
            ("아전인수","a-jeon-in-su","self-serving interpretation"),
            ("이심전심","i-sim-jeon-sim","heart-to-heart understanding"),
            ("외유내강","oe-yu-nae-gang","soft outside, strong inside"),
            ("일거양득","il-geo-yang-deuk","two gains from one action"),
            ("청출어람","cheong-chul-eo-ram","student surpasses the teacher"),
            ("결자해지","gyeol-ja-hae-ji","tie it, untie it"),
            ("환골탈태","hwan-gol-tal-tae","complete transformation"),
            ("타산지석","ta-san-ji-seok","learning from others"),
            ("호가호위","ho-ga-ho-wi","borrowing authority"),
        ],
        "tip": "Don't translate 사자성어 character-by-character — memorize as a whole. Literal readings are metaphorical to the point of nonsense in English.",
        "culture": "Korean newspaper headlines and political speeches frequently use 사자성어 as compact, emotionally weighted summaries — essential for reading news.",
        "faqs": [
            ("Are 사자성어 still used in everyday Korean?",
             "Yes — in news, formal speeches, essays, and educated conversation. Native speakers use 20–30 high-frequency ones regularly."),
            ("What's the difference between 사자성어 and 속담?",
             "사자성어 are 4-character Sino-Korean idioms (classical). 속담 are native Korean proverbs (folk wisdom). Different origin, similar function."),
            ("How many 사자성어 should I learn?",
             "Start with the top 100 most-used. This covers nearly all you'll encounter in news and formal writing."),
        ],
        "related": ["100-korean-proverbs-sokdam-every-native-knows", "hangul-vs-hanja-complete-bilingual-reference"],
    },
    {
        "title": "100 Korean Proverbs (속담) Every Native Speaker Knows",
        "slug":  "100-korean-proverbs-sokdam-every-native-knows",
        "kw":    "Korean proverbs 속담",
        "meta":  "100 Korean proverbs (속담) every native knows — wisdom from tigers, frogs, and rice fields. Cultural fluency in one resource.",
        "hero":  "Wisdom of the people",
        "intro": "While 사자성어 came from classical China, <strong>Korean proverbs (속담)</strong> grew from village life — featuring tigers, cows, frogs, rice fields, and folk wisdom. Native speakers drop these into conversation as humor, advice, or moral judgment.",
        "samples": [
            ("호랑이도 제 말 하면 온다","ho-rang-i-do je mal ha-myeon on-da","Speak of the devil"),
            ("우물 안 개구리","u-mul an gae-gu-ri","frog in a well"),
            ("발 없는 말이 천 리 간다","bal eom-neun mal-i cheon ri gan-da","rumors spread fast"),
            ("티끌 모아 태산","ti-kkeul mo-a tae-san","dust grains become a mountain"),
            ("백지장도 맞들면 낫다","baek-ji-jang-do mat-deul-myeon nat-da","two hands lift even paper"),
            ("가는 말이 고와야 오는 말이 곱다","ga-neun mal-i go-wa-ya o-neun mal-i gop-da","kind words come back kind"),
            ("등잔 밑이 어둡다","deung-jan mi-chi eo-dup-da","dark under the lamp"),
            ("뛰는 놈 위에 나는 놈 있다","ttwi-neun nom wi-e na-neun nom it-da","above runner, a flyer"),
            ("아니 땐 굴뚝에 연기 날까","a-ni ttaen gul-ttu-ge yeon-gi nal-kka","no smoke without fire"),
            ("소 잃고 외양간 고친다","so il-go oe-yang-gan go-chin-da","fix barn after losing cow"),
            ("가재는 게 편","ga-jae-neun ge pyeon","crayfish sides with crab"),
            ("개구리 올챙이 적 생각 못 한다","gae-gu-ri ol-chaeng-i jeok saeng-gak mot han-da","frog forgets tadpole days"),
            ("원숭이도 나무에서 떨어진다","won-sung-i-do na-mu-e-seo tteo-reo-jin-da","monkeys fall from trees"),
            ("천 리 길도 한 걸음부터","cheon ri gil-do han geo-reum-bu-teo","journey of a thousand miles"),
            ("작은 고추가 더 맵다","ja-geun go-chu-ga deo maep-da","small peppers spicier"),
        ],
        "tip": "Korean proverbs are best learned through K-dramas and novels — context cements them. Hearing 호랑이도 제 말 하면 in a scene is more memorable than the literal meaning.",
        "culture": "Older Koreans drop 속담 constantly. Understanding and responding appropriately earns immediate respect ('한국 사람보다 한국말 잘하네!').",
        "faqs": [
            ("Are Korean proverbs still used today?",
             "Very much yes. Older generations use 속담 constantly. Younger speakers know them passively and use them for humor or emphasis."),
            ("What's the most famous Korean proverb?",
             "'호랑이도 제 말 하면 온다' (speak of the devil) and '티끌 모아 태산' (small things add up) are likely the most-quoted."),
            ("Can foreigners use Korean proverbs?",
             "Absolutely — and Koreans love when you do. It signals deep cultural engagement. Just verify the meaning and context first."),
        ],
        "related": ["100-essential-korean-idioms-sajaseongeo-sophisticated-speech", "500-korean-onomatopoeia-uiseongeo-uitaego-explained"],
    },
    {
        "title": "1,100 Korean Visual Vocabulary — Learn 30 Categories by Picture",
        "slug":  "1100-korean-visual-vocabulary-learn-by-picture",
        "kw":    "Korean visual vocabulary",
        "meta":  "Learn 1,100 essential Korean words through pictures across 30 daily-life categories — kitchen, bedroom, hospital, transit, emotions, occupations.",
        "hero":  "Image-based learning",
        "intro": "Research on second-language acquisition consistently shows visual associations beat translation drills for long-term retention. <strong>Korean visual vocabulary</strong> learning groups 1,100 essential words with images across 30 categories.",
        "samples": [
            ("냉장고","naeng-jang-go","refrigerator"),
            ("세탁기","se-tak-gi","washing machine"),
            ("청소기","cheong-so-gi","vacuum cleaner"),
            ("전자레인지","jeon-ja-re-in-ji","microwave"),
            ("드라이기","deu-ra-i-gi","hair dryer"),
            ("화장대","hwa-jang-dae","vanity table"),
            ("옷장","ot-jang","wardrobe"),
            ("책상","chaek-sang","desk"),
            ("의자","ui-ja","chair"),("거울","geo-ul","mirror"),
            ("시계","si-gye","clock / watch"),
            ("우산","u-san","umbrella"),("열쇠","yeol-soe","key"),
            ("가방","ga-bang","bag"),("지갑","ji-gap","wallet"),
        ],
        "tip": "Group vocabulary by physical location, not alphabet. Memorize all kitchen words at once, then all bathroom words. Your brain links them to spatial memory — far more durable.",
        "culture": "Korean apartment vocabulary differs from Western homes. No separate dining room — eating happens in 거실 (living room). Bathrooms are 욕실 OR 화장실 depending on context.",
        "faqs": [
            ("Why is visual vocabulary more effective?",
             "Brain research shows dual-coding (image + word) creates two retrieval pathways vs. translation alone. Visual learners retain 2–3× more long-term."),
            ("How long until I can use these words?",
             "With 15 minutes/day of visual review, expect functional use within 30 days for a 200-word batch."),
            ("Can I use this for TOPIK preparation?",
             "Yes — the 1,100 words map closely to TOPIK I and II vocabulary categories. Visual learning helps with the listening section."),
        ],
        "related": ["369-common-korean-nouns-every-beginner-should-know", "1000-korean-it-terms-tech-vocabulary-programmers"],
    },
    {
        "title": "100 Bible Verses in Korean (한국어 성경 구절)",
        "slug":  "100-bible-verses-korean-hangugeo-seonggyeong",
        "kw":    "Korean Bible verses",
        "meta":  "100 Korean Bible verses (성경 구절) with romanization and English translation. Practice high-register Korean through Scripture.",
        "hero":  "Sacred text, formal Korean",
        "intro": "Korea has one of Asia's largest Christian populations — and <strong>Korean Bible verses</strong> are written in elevated register. Reading Scripture is one of the few sustained ways to practice high-register Korean. We compiled 100 most-quoted verses with parallel English.",
        "samples": [
            ("태초에 하나님이 천지를 창조하시니라","tae-cho-e ha-na-nim-i cheon-ji-reul chang-jo-ha-si-ni-ra","In the beginning God created (Gen 1:1)"),
            ("하나님은 사랑이시라","ha-na-nim-eun sa-rang-i-si-ra","God is love (1 John 4:8)"),
            ("내가 너와 함께 있느니라","nae-ga neo-wa ham-kke it-neu-ni-ra","I am with you (Isaiah 41:10)"),
            ("주는 나의 목자시니","ju-neun na-ui mok-ja-si-ni","The Lord is my shepherd (Psalm 23)"),
            ("두려워 말라","du-ryeo-wo mal-ra","Do not fear"),
            ("믿음 소망 사랑","mi-deum so-mang sa-rang","Faith, hope, love (1 Cor 13)"),
            ("너희가 거듭 나야 하리라","neo-hui-ga geo-deup na-ya ha-ri-ra","You must be born again (John 3:7)"),
            ("내가 곧 길이요 진리요 생명이니","nae-ga got gi-ri-yo jin-ri-yo saeng-myeong-i-ni","I am the way (John 14:6)"),
            ("범사에 감사하라","beom-sa-e gam-sa-ha-ra","Give thanks always (1 Thess 5:18)"),
            ("쉬지 말고 기도하라","swi-ji mal-go gi-do-ha-ra","Pray without ceasing (1 Thess 5:17)"),
            ("수고하고 무거운 짐 진 자들아","su-go-ha-go mu-geo-un jim jin ja-deul-a","Come, weary ones (Matt 11:28)"),
            ("이는 내 사랑하는 아들이요","i-neun nae sa-rang-ha-neun a-deul-i-yo","This is my beloved Son (Matt 3:17)"),
            ("진리가 너희를 자유롭게 하리라","jin-ri-ga neo-hui-reul ja-yu-rop-ge ha-ri-ra","Truth shall set you free (John 8:32)"),
            ("내 은혜가 네게 족하도다","nae eun-hye-ga ne-ge jo-ka-do-da","My grace is sufficient (2 Cor 12:9)"),
            ("일어나 빛을 발하라","i-reo-na bi-cheul bal-ha-ra","Arise and shine (Isaiah 60:1)"),
        ],
        "tip": "Korean Bible verses end with archaic verb endings: -하라 (command), -하느니라 (declaration), -하시니라 (formal narrative). Essential for reading older literature.",
        "culture": "Korean Christianity has Confucian formal-respect baked into language. 하나님 아버지 uses honorifics throughout. One of few domains with consistent -하나이다 endings.",
        "faqs": [
            ("Which Korean Bible translation should I use?",
             "개역개정 (revised version) is most common. 새번역 (new translation) is easier for modern speakers. Both are widely accepted."),
            ("Are Korean Bible verses good for learning?",
             "Excellent for high-register Korean, but not for daily speech. Use them alongside conversational practice — not as a replacement."),
            ("Why are Korean Bible endings so different?",
             "They preserve 17–19th century literary Korean. Modern translations smooth them out, but classic versions retain archaic endings."),
        ],
        "related": ["500-korean-honorifics-master-polite-speech-native", "hangul-vs-hanja-complete-bilingual-reference"],
    },
    {
        "title": "1,000 Korean IT Terms — Tech Vocabulary for Developers in Korea",
        "slug":  "1000-korean-it-terms-tech-vocabulary-programmers",
        "kw":    "Korean IT terms",
        "meta":  "1,000 Korean IT terms for developers, engineers, and tech professionals working at Samsung, Naver, Kakao. Software, AI, cloud, DevOps vocabulary.",
        "hero":  "Tech Korean for the global engineer",
        "intro": "Korea's tech sector is one of the world's largest. If you work at Samsung, LG, Naver, Kakao, or Coupang, you need <strong>Korean IT terms</strong>. We compiled 1,000 software, hardware, network, and AI terms — 알고리즘 to 클라우드 컴퓨팅.",
        "samples": [
            ("알고리즘","al-go-ri-jeum","algorithm"),
            ("데이터베이스","de-i-teo-be-i-seu","database"),
            ("서버","seo-beo","server"),("클라우드","keul-la-u-deu","cloud"),
            ("머신러닝","meo-sin-leo-ning","machine learning"),
            ("인공지능","in-gong-ji-neung","artificial intelligence"),
            ("개발자","gae-bal-ja","developer"),
            ("배포","bae-po","deployment"),
            ("저장소","jeo-jang-so","repository"),
            ("자동화","ja-dong-hwa","automation"),
            ("프레임워크","peu-re-im-wo-keu","framework"),
            ("라이브러리","ra-i-beu-reo-ri","library"),
            ("커밋","keo-mit","commit (Git)"),
            ("브랜치","beu-raen-chi","branch (Git)"),
            ("디버깅","di-beo-ging","debugging"),
        ],
        "tip": "Korean IT vocabulary splits between Sino-Korean translations (개발자 = developer) and English loanwords (디버깅 = debugging). Developers mix both: '커밋 메시지에 자동화 추가했어요.'",
        "culture": "Korean tech companies use heavy English-Korean code-switching in meetings. 'Kickoff 미팅', 'OKR 세팅', 'standup 진행' — knowing both forms is essential.",
        "faqs": [
            ("Do Korean developers code in English?",
             "Variables and comments are mostly English. Meetings and Slack are mostly Korean with English tech terms mixed in. Documentation varies by company."),
            ("How important is Korean for working at Naver/Kakao?",
             "Very important. Most internal meetings, code reviews, and design docs are in Korean. Strong Korean significantly impacts promotion potential."),
            ("Can I work in Korean tech without Korean?",
             "Possible at foreign-led teams (Google Korea, AWS Korea) but limited at domestic giants. TOPIK 4+ recommended for Naver/Kakao."),
        ],
        "related": ["1100-korean-visual-vocabulary-learn-by-picture", "hangul-vs-hanja-complete-bilingual-reference"],
    },
    {
        "title": "Hangul vs Hanja — Why You Should Learn Both",
        "slug":  "hangul-vs-hanja-complete-bilingual-reference",
        "kw":    "Hangul vs Hanja",
        "meta":  "Hangul vs Hanja explained — when Koreans use Chinese characters and how learning 1,800 Hanja multiplies your Korean vocabulary instantly.",
        "hero":  "Hangul + Hanja = full literacy",
        "intro": "Modern Korean is written in Hangul, but 60–70% of Korean vocabulary derives from <strong>Hanja</strong> (Chinese characters). Many newspapers, legal documents, and formal name cards still use them. Knowing the top 1,800 Hanja unlocks instant vocabulary multiplication.",
        "samples": [
            ("人 인","in","person"),("大 대","dae","big"),
            ("小 소","so","small"),("中 중","jung","middle"),
            ("學 학","hak","learning"),("校 교","gyo","school"),
            ("生 생","saeng","life"),("死 사","sa","death"),
            ("國 국","guk","country"),("家 가","ga","house/family"),
            ("水 수","su","water"),("火 화","hwa","fire"),
            ("山 산","san","mountain"),("江 강","gang","river"),
            ("日 일","il","sun/day"),
        ],
        "tip": "When you learn Hanja, you learn Korean in batches. Once you know 學 (hak = study), you can guess: 학교 (school), 학생 (student), 학습 (learning), 수학 (math), 과학 (science).",
        "culture": "Hanja is mandatory in Korean newspapers for ambiguous names. Same name 정수 could mean 整數 (whole number), 淨水 (purified water), or be a person's name — Hanja clarifies.",
        "faqs": [
            ("Do Koreans still write Hanja?",
             "Daily life is 99% Hangul. Hanja appears in name cards, legal documents, newspaper name disambiguation, and traditional contexts."),
            ("Should foreign learners learn Hanja?",
             "Yes — for vocabulary growth. Learning 500–1000 Hanja roots dramatically accelerates Sino-Korean vocabulary acquisition."),
            ("How many Hanja are taught in Korean schools?",
             "1,800 'basic Chinese characters' (한문 교육용 기초 한자) — covers nearly all academic and journalistic vocabulary."),
        ],
        "related": ["391-japanese-loanwords-korean-explained", "100-essential-korean-idioms-sajaseongeo-sophisticated-speech"],
    },
]

# ============================================================
# SERIES B — KOREAN CULTURE (12 posts)
# ============================================================
CULTURE_POSTS = [
    {
        "title": "빨리빨리 Culture — Why Koreans Always Hurry (And Why It Works)",
        "slug":  "ppalli-ppalli-culture-why-koreans-always-hurry",
        "kw":    "빨리빨리 culture",
        "meta":  "Decode Korea's 빨리빨리 (hurry hurry) culture — its post-war origins, modern impact, and what it says about Korean society today.",
        "hero":  "Korea's national speed",
        "intro": "If you've spent a day in Korea, you've heard <strong>빨리빨리</strong> (ppalli-ppalli) — literally 'fast fast.' It's Korea's unofficial national motto, the engine behind its post-war miracle and the everyday rhythm of life from Seoul to Busan.",
        "samples": [
            ("빨리","ppal-li","quickly"),
            ("서두르다","seo-du-reu-da","to rush"),
            ("재촉하다","jae-chok-ha-da","to urge / press"),
            ("급하다","geu-pa-da","urgent"),
            ("바쁘다","ba-ppeu-da","busy"),
            ("느긋하다","neu-geu-ta-da","relaxed (opposite)"),
            ("효율","hyo-yul","efficiency"),
            ("속도","sok-do","speed"),
            ("순간","sun-gan","moment"),
            ("즉시","jeuk-si","immediately"),
            ("당장","dang-jang","right now"),
            ("얼른","eol-leun","quickly (colloquial)"),
            ("후딱","hu-ttak","in a flash"),
            ("빠릿빠릿","ppa-rit-ppa-rit","sharp / quick-witted"),
            ("시간 없어","si-gan eop-seo","no time!"),
        ],
        "tip": "When ordering at a Korean restaurant, '빨리 주세요' is acceptable, even expected. Servers don't take it personally — speed is the standard.",
        "culture": "빨리빨리 originated in the 1960s–80s rapid industrialization era. Korea rebuilt from a war-devastated nation to a global economy in 40 years — speed was survival. Today it manifests as: 30-min food delivery, same-day clothes alteration, instant 5G everywhere, subway arriving every 2 minutes.",
        "faqs": [
            ("Is 빨리빨리 culture a positive or negative trait?",
             "Both. It drove Korea's economic miracle and produces unmatched efficiency, but also contributes to high stress, accidents from rushing, and the world's longest work hours."),
            ("Do Koreans want to slow down?",
             "Slowly yes. The '소확행' (small certain happiness) movement and rising interest in mindfulness signal a generational shift, especially among Gen Z."),
            ("How fast is Korean food delivery really?",
             "Average 25–35 minutes from order to door, even at 2 AM. Apps like 배달의민족 and 쿠팡이츠 made this an industry standard."),
        ],
        "related": ["seongsil-korean-diligence-work-ethic", "chaegimgam-korean-responsibility-culture"],
    },
    {
        "title": "성실성 — The Korean Diligence That Powers a Nation",
        "slug":  "seongsil-korean-diligence-work-ethic",
        "kw":    "Korean diligence 성실성",
        "meta":  "성실성 (seongsil-seong) — Korea's deep cultural value of diligence and sincerity. Why Koreans work so hard and how it shapes society.",
        "hero":  "Diligence as identity",
        "intro": "Ask a Korean parent what virtue matters most in a child, and 9 out of 10 will say <strong>성실 (seongsil)</strong> — diligence and sincerity combined. It's the bedrock of Korea's education system, work culture, and self-image.",
        "samples": [
            ("성실","seong-sil","diligence / sincerity"),
            ("근면","geun-myeon","industriousness"),
            ("부지런하다","bu-ji-reon-ha-da","diligent"),
            ("노력","no-ryeok","effort"),
            ("꾸준히","kku-jun-hi","steadily"),
            ("열심히","yeol-sim-hi","hard / earnestly"),
            ("최선","choe-seon","one's best"),
            ("끈기","kkeun-gi","perseverance"),
            ("인내","in-nae","patience"),
            ("성취","seong-chwi","achievement"),
            ("자기관리","ja-gi-gwan-ri","self-management"),
            ("자기계발","ja-gi-gye-bal","self-development"),
            ("도전","do-jeon","challenge"),
            ("극복","geuk-bok","overcome"),
            ("실력","sil-lyeok","skill / ability"),
        ],
        "tip": "Saying '성실해 보여요' (you seem diligent) is one of the highest compliments in Korean. It signals trustworthy, hardworking, sincere — far more flattering than 'smart' or 'talented.'",
        "culture": "Korean job interviews ask not just about skills but about 'effort stories.' Stories of overcoming hardship (극복 사례) carry more weight than natural talent. The proverb 노력은 배신하지 않는다 (effort never betrays you) is gospel.",
        "faqs": [
            ("Why do Koreans study so much?",
             "Confucian heritage values education as social mobility, plus modern competitive job market. The result: highest education spending per GDP and longest study hours globally."),
            ("Is 성실 more important than talent in Korea?",
             "Culturally yes. Stories of diligent strivers beating talented prodigies are deeply celebrated — see athletes like Son Heung-min and businessman Lee Byung-chul."),
            ("Does 성실 culture cause burnout?",
             "Yes — Korea has one of the highest burnout rates and suicide rates among OECD countries. The dark side of diligence-worship is increasingly discussed."),
        ],
        "related": ["ppalli-ppalli-culture-why-koreans-always-hurry", "chaegimgam-korean-responsibility-culture"],
    },
    {
        "title": "책임감 — Korean Responsibility Culture & Its Hidden Weight",
        "slug":  "chaegimgam-korean-responsibility-culture",
        "kw":    "책임감 Korean responsibility",
        "meta":  "책임감 (chaegim-gam) — Korea's intense culture of responsibility. Why Korean workers, parents, and students carry weight Westerners rarely see.",
        "hero":  "The weight Koreans carry",
        "intro": "<strong>책임감 (chaegim-gam)</strong> — a sense of responsibility — is not just a personal trait in Korea. It's a social obligation, a moral weight, and the unspoken expectation behind every role: student, employee, parent, citizen.",
        "samples": [
            ("책임","chae-gim","responsibility"),
            ("책임감","chae-gim-gam","sense of responsibility"),
            ("의무","ui-mu","duty"),
            ("도리","do-ri","moral duty"),
            ("역할","yeok-hal","role"),
            ("맡다","mat-da","to take on / be in charge"),
            ("담당","dam-dang","being in charge"),
            ("희생","hui-saeng","sacrifice"),
            ("부담","bu-dam","burden"),
            ("의리","ui-ri","loyalty / duty"),
            ("신뢰","sin-roe","trust"),
            ("신용","sin-yong","credit / trustworthiness"),
            ("진심","jin-sim","sincerity"),
            ("성의","seong-ui","goodwill effort"),
            ("자세","ja-se","attitude / posture"),
        ],
        "tip": "If a Korean manager says '책임감 있게 해주세요' (please handle it responsibly), they mean: own it completely, fix all problems silently, and never escalate unless absolutely critical.",
        "culture": "Korean responsibility is collective. A subordinate's mistake reflects on the manager. A student's failure reflects on the parents. This produces extraordinary diligence — but also covers up failures to protect group reputation.",
        "faqs": [
            ("How is 책임감 different from Western responsibility?",
             "Western responsibility is often individual and contractual. Korean 책임감 is collective and moral — extending to your team's failures, your family's reputation, and unspoken expectations."),
            ("Why do Korean managers apologize for subordinates' mistakes?",
             "Because 책임감 culture holds the senior accountable for the junior. A team leader publicly apologizes; the actual offender often stays anonymous."),
            ("Can 책임감 culture be harmful?",
             "Yes — it discourages reporting problems, hides failures, and produces immense stress. Many Korean reform movements target this dark side."),
        ],
        "related": ["seongsil-korean-diligence-work-ethic", "nunchi-korean-art-of-reading-the-room"],
    },
    {
        "title": "정 (Jeong) — The Untranslatable Korean Bond",
        "slug":  "jeong-untranslatable-korean-bond",
        "kw":    "Korean jeong 정",
        "meta":  "정 (jeong) — Korea's most untranslatable concept. The deep emotional bond beyond friendship, family, or love that defines Korean relationships.",
        "hero":  "Beyond friendship, beyond love",
        "intro": "<strong>정 (jeong)</strong> is the single most untranslatable word in Korean. It's not love, not friendship, not loyalty — but a slow-built emotional attachment that grows between people, places, and even objects through shared time and small kindnesses.",
        "samples": [
            ("정","jeong","emotional bond"),
            ("정이 들다","jeong-i deul-da","to become attached"),
            ("정이 많다","jeong-i man-ta","to be warm-hearted"),
            ("미운 정","mi-un jeong","bond despite annoyance"),
            ("고운 정","go-un jeong","tender bond"),
            ("우정","u-jeong","friendship"),
            ("애정","ae-jeong","affection"),
            ("정성","jeong-seong","heartfelt effort"),
            ("정나미","jeong-na-mi","feeling of attachment"),
            ("정겹다","jeong-gyeop-da","heartwarming"),
            ("그립다","geu-rip-da","to miss / yearn"),
            ("따뜻하다","tta-tteu-ta-da","warm"),
            ("끈끈하다","kkeun-kkeun-ha-da","tightly bonded"),
            ("애틋하다","ae-teut-ha-da","tender / poignant"),
            ("아끼다","a-kki-da","to cherish"),
        ],
        "tip": "When Koreans give you extra food at a restaurant '서비스' (service), it's 정 — small, unprompted generosity that builds an invisible thread of relationship.",
        "culture": "Even 'mi-un jeong' (bond despite annoyance) exists — the deep attachment to a friend or sibling you constantly fight with. Korean grandmothers say '미운 정도 정이다' — even bitter bond is bond.",
        "faqs": [
            ("Can 정 exist with strangers?",
             "Yes — between regular shop owners and customers, neighbors who never speak but recognize each other, even between you and the convenience store ajumma."),
            ("How is 정 different from love?",
             "Love (사랑) is intense and romantic. 정 is quiet, gradual, accumulated through small interactions — sometimes between people who don't even like each other."),
            ("Is 정 disappearing in modern Korea?",
             "Some say yes, due to urbanization and apartment life. But food gifting, '서비스' generosity, and online communities suggest 정 just changes form."),
        ],
        "related": ["han-korean-emotional-depth-untranslatable", "uri-korean-collective-we-mindset"],
    },
    {
        "title": "한 (Han) — Korea's Untranslatable Sorrow",
        "slug":  "han-korean-emotional-depth-untranslatable",
        "kw":    "Korean han 한",
        "meta":  "한 (han) — Korea's untranslatable emotion of accumulated sorrow, longing, and unresolved injustice. Understanding K-drama and pansori depth.",
        "hero":  "Sorrow that becomes strength",
        "intro": "<strong>한 (han)</strong> is the dark twin of 정. Where 정 is warm accumulated attachment, han is accumulated sorrow — generations of unresolved injustice, frustrated dreams, separations, and quiet rage transformed into endurance.",
        "samples": [
            ("한","han","accumulated sorrow"),
            ("한이 맺히다","han-i maet-chi-da","sorrow takes root"),
            ("억울하다","eok-ul-ha-da","wronged / unjust"),
            ("서럽다","seo-reop-da","heart-aching sorrow"),
            ("애통하다","ae-tong-ha-da","grief"),
            ("비통","bi-tong","deep grief"),
            ("슬픔","seul-peum","sadness"),
            ("그리움","geu-ri-um","longing"),
            ("회한","hoe-han","regret"),
            ("원망","won-mang","resentment"),
            ("한탄","han-tan","lamentation"),
            ("탄식","tan-sik","sigh"),
            ("응어리","eung-eo-ri","emotional knot"),
            ("응어리지다","eung-eo-ri-ji-da","to be knotted (with sorrow)"),
            ("풀다","pul-da","to release / untie"),
        ],
        "tip": "In Korean cinema and K-drama, when a character has '한이 맺힌 눈빛' (eyes knotted with sorrow), they're carrying generational, unresolved pain. It's narrative shorthand for deep character.",
        "culture": "Pansori (traditional Korean opera) is built on han — the singer's voice is roughened by years of practice to embody this aesthetic. Korean modern artists like director Park Chan-wook explicitly call themselves 'directors of han.'",
        "faqs": [
            ("Is 한 always negative?",
             "No — han transforms. Many Koreans see han as the source of perseverance, art, and national identity. Korea's 20th-century survival is often attributed to han transmuted into endurance."),
            ("Do younger Koreans still feel 한?",
             "Less than older generations, but it's embedded in cultural products — songs, films, even K-pop ballads. Younger Koreans recognize and value it even if they don't personally carry it."),
            ("What's the difference between 한 and depression?",
             "Han is collective, intergenerational, and culturally productive. Depression is individual and clinical. Han can coexist with high functioning; depression generally impairs it."),
        ],
        "related": ["jeong-untranslatable-korean-bond", "uri-korean-collective-we-mindset"],
    },
    {
        "title": "눈치 — The Korean Art of Reading the Room",
        "slug":  "nunchi-korean-art-of-reading-the-room",
        "kw":    "Korean nunchi 눈치",
        "meta":  "눈치 (nunchi) — the Korean art of reading social cues. Why Koreans value emotional intelligence above almost any other skill.",
        "hero":  "Emotional radar, 24/7",
        "intro": "<strong>눈치 (nunchi)</strong> literally means 'eye measure' — the ability to read a room, sense others' moods, and adjust your behavior accordingly. It's perhaps the single most prized social skill in Korea, taught from childhood.",
        "samples": [
            ("눈치","nun-chi","social awareness"),
            ("눈치가 빠르다","nun-chi-ga ppa-reu-da","quick to read situations"),
            ("눈치가 없다","nun-chi-ga eop-da","socially oblivious"),
            ("눈치를 보다","nun-chi-reul bo-da","watch for cues"),
            ("눈치채다","nun-chi-chae-da","to notice / catch on"),
            ("분위기","bun-wi-gi","atmosphere / mood"),
            ("분위기 파악","bun-wi-gi pa-ak","reading the atmosphere"),
            ("센스","sen-seu","tact / wit"),
            ("센스 있다","sen-seu it-da","tactful"),
            ("배려","bae-ryeo","consideration"),
            ("공감","gong-gam","empathy"),
            ("어색하다","eo-sae-ka-da","awkward"),
            ("부담스럽다","bu-dam-seu-reop-da","burdensome"),
            ("불편하다","bul-pyeon-ha-da","uncomfortable"),
            ("적절하다","jeok-jeol-ha-da","appropriate"),
        ],
        "tip": "If a Korean group goes silent after your comment, that's a 눈치 signal — something was inappropriate. Skilled 눈치 readers immediately pivot the topic or apologize lightly.",
        "culture": "Korean children are praised for 눈치 from age 5. Western individualism encourages 'be yourself.' Korean collectivism encourages 'sense the group, then respond.' Both have merit — different optimization targets.",
        "faqs": [
            ("Can 눈치 be learned?",
             "Yes — through immersion. Korean reality shows, K-dramas, and live conversation practice teach 눈치 implicitly. Westerners often need 2–3 years of immersion to develop strong 눈치."),
            ("Is high 눈치 always good?",
             "Not always — extreme 눈치 can mean people-pleasing and self-suppression. Modern Korean self-help books increasingly advocate balanced 눈치 — sensitive but not subservient."),
            ("How does 눈치 affect Korean meetings?",
             "Heavily. Junior members rarely speak first. Disagreement is signaled through subtle pauses or '음...' Lacking 눈치 in Korean meetings is a career limiter."),
        ],
        "related": ["chemyeon-korean-saving-face-culture", "uri-korean-collective-we-mindset"],
    },
    {
        "title": "체면 — Korean Saving Face & Why It Still Matters",
        "slug":  "chemyeon-korean-saving-face-culture",
        "kw":    "체면 Korean face culture",
        "meta":  "체면 (chemyeon) — Korea's saving-face culture explained. How honor, dignity, and public image shape every Korean social interaction.",
        "hero":  "Dignity is currency",
        "intro": "<strong>체면 (chemyeon)</strong> — Korea's saving-face culture — governs how Koreans dress, speak, host, and even pay restaurant bills. Lose 체면 publicly and you damage not just yourself but your family's standing.",
        "samples": [
            ("체면","che-myeon","face / dignity"),
            ("체면 차리다","che-myeon cha-ri-da","keep up appearances"),
            ("체면이 깎이다","che-myeon-i kkak-i-da","lose face"),
            ("자존심","ja-jon-sim","pride / self-respect"),
            ("위신","wi-sin","prestige"),
            ("명예","myeong-ye","honor"),
            ("창피하다","chang-pi-ha-da","embarrassing"),
            ("부끄럽다","bu-kkeu-reop-da","ashamed"),
            ("쪽팔리다","jjok-pal-li-da","embarrassed (slang)"),
            ("망신","mang-sin","public humiliation"),
            ("품위","pum-wi","grace / dignity"),
            ("점잖다","jeom-jan-ta","dignified / refined"),
            ("의젓하다","ui-jeot-ha-da","mature / composed"),
            ("내색","nae-saek","showing one's feelings"),
            ("드러내다","deu-reo-nae-da","to reveal"),
        ],
        "tip": "When a Korean colleague offers to pay for everyone's meal, they're partly performing 체면. Refusing flatly damages their face. Accept gracefully — then return the favor next time.",
        "culture": "Korean restaurant bills are famously fought over — '내가 살게' (I'll pay) shouted while physically blocking each other. Whoever pays gains 체면. This isn't just kindness; it's social currency.",
        "faqs": [
            ("Is 체면 superficial?",
             "Critics say yes — but defenders argue it enforces civility, generosity, and social cooperation. Without 체면, Korean public spaces would be far ruder."),
            ("How is 체면 different from Western pride?",
             "Western pride is internal. 체면 is collective and external — you save face for your family, your team, your company. Loss of face ripples outward."),
            ("Are younger Koreans abandoning 체면?",
             "Slowly. Gen Z values authenticity more. But 체면 remains powerful in workplaces, family events, and wedding/funeral etiquette."),
        ],
        "related": ["nunchi-korean-art-of-reading-the-room", "uri-korean-collective-we-mindset"],
    },
    {
        "title": "우리 — The Korean 'We' That Replaces 'I'",
        "slug":  "uri-korean-collective-we-mindset",
        "kw":    "Korean uri 우리",
        "meta":  "우리 (uri) — Korea's collective 'we' mindset that shapes language, family, and identity. Why Koreans say 'our country' instead of 'my country.'",
        "hero":  "From 'I' to 'we'",
        "intro": "Koreans rarely say 'my' — they say <strong>우리 (uri)</strong>, meaning 'our.' 우리 나라 (our country), 우리 엄마 (our mom), 우리 집 (our house), even 우리 남편 (our husband — even though the speaker has only one). This linguistic habit reveals a deep collective identity.",
        "samples": [
            ("우리","u-ri","we / our"),
            ("우리나라","u-ri-na-ra","our country (Korea)"),
            ("우리집","u-ri-jip","our house"),
            ("우리 가족","u-ri ga-jok","our family"),
            ("공동체","gong-dong-che","community"),
            ("단체","dan-che","group / organization"),
            ("소속","so-sok","belonging / affiliation"),
            ("팀워크","tim-wo-keu","teamwork"),
            ("동료","dong-ryo","colleague"),
            ("동기","dong-gi","same-year peer"),
            ("선배","seon-bae","senior"),
            ("후배","hu-bae","junior"),
            ("회식","hoe-sik","company dinner"),
            ("화합","hwa-hap","harmony"),
            ("협력","hyeop-ryeok","cooperation"),
        ],
        "tip": "Saying '내 엄마' (my mom) instead of '우리 엄마' sounds oddly individualistic to Korean ears — almost selfish. The default is 우리.",
        "culture": "The 우리 mindset extends to economic behavior — Koreans famously gave gold jewelry to the government during the 1997 IMF crisis to save 'our country.' Western individualist economies would never produce that response.",
        "faqs": [
            ("Why do Koreans say 우리 even for 'my husband'?",
             "It's a linguistic habit signaling that family relationships are shared with the whole family — your husband is also your parents' son-in-law, your siblings' brother-in-law. Saying 우리 acknowledges all those bonds."),
            ("Does 우리 mindset hurt individualism?",
             "It can — Korean creatives and entrepreneurs sometimes struggle with self-promotion that feels natural to Western counterparts. Gen Z is shifting this, but slowly."),
            ("Is 우리 mindset weakening?",
             "Family 우리 remains strong. Workplace 우리 (회식 culture, lifetime employment) has weakened significantly post-2010."),
        ],
        "related": ["jeong-untranslatable-korean-bond", "hoesik-korean-company-dinner-culture"],
    },
    {
        "title": "효 (Hyo) — Filial Piety in Modern Korean Society",
        "slug":  "hyo-filial-piety-korean-family-culture",
        "kw":    "효 Korean filial piety",
        "meta":  "효 (hyo) — Korea's filial piety tradition. How Confucian respect for parents and elders shapes modern Korean families, careers, and decisions.",
        "hero":  "Confucius lives in Korean kitchens",
        "intro": "<strong>효 (hyo)</strong> — filial piety — is Korea's most ancient and persistent virtue. Rooted in 600 years of Confucian state ideology, hyo remains the unspoken framework for parent-child relationships even in 2026 Seoul.",
        "samples": [
            ("효","hyo","filial piety"),
            ("효도","hyo-do","acts of filial piety"),
            ("효자","hyo-ja","dutiful son"),
            ("효녀","hyo-nyeo","dutiful daughter"),
            ("부모님","bu-mo-nim","parents (honorific)"),
            ("어른","eo-reun","elder"),
            ("공경","gong-gyeong","respect for elders"),
            ("예절","ye-jeol","etiquette"),
            ("도덕","do-deok","morality"),
            ("유교","yu-gyo","Confucianism"),
            ("성묘","seong-myo","grave-visiting"),
            ("제사","je-sa","ancestral rites"),
            ("명절","myeong-jeol","traditional holiday"),
            ("세배","se-bae","New Year deep bow"),
            ("부양","bu-yang","supporting (parents)"),
        ],
        "tip": "Sending parents regular money — even when they don't need it — is a modern 효 expression. 용돈 to parents (yes, allowance) is normal for working adults.",
        "culture": "Korean filial piety extends beyond parents' lifetimes. Annual 제사 (ancestral rites), 추석 grave-visiting, and memorial ceremonies (기일) maintain the bond across generations. Skipping these damages family standing.",
        "faqs": [
            ("Is 효 declining in modern Korea?",
             "Forms are shifting. Living with parents is less common, but financial support, calls, and holiday visits remain strong. Pure abandonment of parents is still socially taboo."),
            ("What if I disagree with my Korean parents?",
             "Direct confrontation is rare. Indirect signaling, gradual persuasion, and waiting for the right moment are 효-respecting strategies."),
            ("Do Koreans inherit obligations from their parents?",
             "Yes — both literal (debts, business obligations) and figurative (career expectations, marriage timelines). Western 'I'm my own person' rhetoric clashes with Korean reality."),
        ],
        "related": ["uri-korean-collective-we-mindset", "seolnal-korean-new-year-traditions"],
    },
    {
        "title": "회식 — Korean Company Dinner Culture & Survival Guide",
        "slug":  "hoesik-korean-company-dinner-culture",
        "kw":    "회식 Korean company dinner",
        "meta":  "회식 (hoesik) — Korea's company dinner culture explained. Drinking etiquette, the round system, and how to survive Korean work socials.",
        "hero":  "Work doesn't end at 6 PM",
        "intro": "<strong>회식 (hoesik)</strong> — the Korean company dinner — is half team-bonding, half political theater, and often mandatory. Refusing damages your standing; surviving with grace builds your career.",
        "samples": [
            ("회식","hoe-sik","company dinner"),
            ("1차","il-cha","first round"),
            ("2차","i-cha","second round"),
            ("3차","sam-cha","third round"),
            ("건배","geon-bae","cheers"),
            ("한잔","han-jan","one drink"),
            ("따르다","tta-reu-da","to pour"),
            ("받다","bat-da","to receive"),
            ("폭탄주","pok-tan-ju","beer-soju bomb"),
            ("소맥","so-maek","soju + beer"),
            ("주량","ju-ryang","alcohol tolerance"),
            ("취하다","chwi-ha-da","get drunk"),
            ("숙취","suk-chwi","hangover"),
            ("해장국","hae-jang-guk","hangover soup"),
            ("노래방","no-rae-bang","karaoke (3rd round)"),
        ],
        "tip": "When a senior pours you a drink, hold the glass with both hands and turn your head away to drink. This dual gesture signals respect — failing to do it is a serious 눈치 fail.",
        "culture": "The famous 'round system' (1차 → 2차 → 3차): start with dinner+soju, move to a bar/pojangmacha, end at noraebang. Each round filters out the responsible — and reveals who really belongs.",
        "faqs": [
            ("Can I refuse to attend 회식?",
             "Possible but costly. Citing health or family reasons works occasionally. Frequent refusal signals you're not a team player — career consequences likely."),
            ("How do I survive heavy drinking?",
             "Eat first (very Korean — drinking on empty stomach is taboo), pace yourself, decline 2차 if needed, drink water between soju shots. Saying '오늘은 컨디션이 안 좋아요' often works."),
            ("Is 회식 disappearing?",
             "Slowly. Post-COVID and younger generations have weakened 회식 culture, especially mandatory after-hours drinking. Lunch 회식 is rising."),
        ],
        "related": ["uri-korean-collective-we-mindset", "ppalli-ppalli-culture-why-koreans-always-hurry"],
    },
    {
        "title": "추석 — Korean Thanksgiving Traditions & Greetings",
        "slug":  "chuseok-korean-thanksgiving-traditions",
        "kw":    "Chuseok Korean Thanksgiving 추석",
        "meta":  "Chuseok (추석) — Korea's harvest holiday explained. Traditional foods, ancestral rites, family travel, and essential phrases for the holiday.",
        "hero":  "Korea's harvest moon",
        "intro": "<strong>추석 (Chuseok)</strong> — Korean Thanksgiving — falls on the 15th day of the 8th lunar month. It's Korea's largest holiday: 30+ million people travel home, ancestors are honored, and the moon is full above mountain graves.",
        "samples": [
            ("추석","chu-seok","Chuseok / Korean Thanksgiving"),
            ("한가위","han-ga-wi","Chuseok (native term)"),
            ("송편","song-pyeon","half-moon rice cake"),
            ("차례","cha-rye","ancestral rite"),
            ("성묘","seong-myo","grave visiting"),
            ("벌초","beol-cho","grave grass cutting"),
            ("귀성","gwi-seong","traveling home"),
            ("고향","go-hyang","hometown"),
            ("보름달","bo-reum-dal","full moon"),
            ("강강술래","gang-gang-sul-lae","circle folk dance"),
            ("한복","han-bok","traditional dress"),
            ("전","jeon","Korean pancakes"),
            ("나물","na-mul","seasoned vegetables"),
            ("토란국","to-ran-guk","taro soup"),
            ("새옷","sae-ot","new clothes (for elders)"),
        ],
        "tip": "Standard Chuseok greeting: '추석 잘 보내세요' (have a good Chuseok) or '풍성한 한가위 되세요' (may you have an abundant Chuseok). Avoid '메리 추석' — that's NOT a thing.",
        "culture": "Chuseok 차례 (ancestor rite) is performed at dawn on the holiday. Families bow to portraits or empty seats representing ancestors, present food, and 'share' the meal. Increasingly simplified or skipped by Gen Z.",
        "faqs": [
            ("When is Chuseok in 2026?",
             "Chuseok 2026 falls on September 25 (lunar Aug 15). The 3-day holiday extends Sep 24–26."),
            ("Is Chuseok like American Thanksgiving?",
             "Similar in concept (harvest gratitude, family gathering, traveling home), but different rituals — ancestor rites instead of turkey, songpyeon instead of pie."),
            ("What do I say to Korean friends during Chuseok?",
             "'추석 잘 보내세요' is safe and warm. To business contacts, '풍성한 한가위 되세요' is more formal."),
        ],
        "related": ["seolnal-korean-new-year-traditions", "hyo-filial-piety-korean-family-culture"],
    },
    {
        "title": "설날 — Korean New Year Traditions & 세배 Phrases",
        "slug":  "seolnal-korean-new-year-traditions",
        "kw":    "Seolnal Korean New Year 설날",
        "meta":  "설날 (Seolnal) — Korean Lunar New Year traditions, 세배 bowing ritual, tteokguk soup, and essential New Year greetings.",
        "hero":  "First day of the lunar year",
        "intro": "<strong>설날 (Seolnal)</strong> — Korean Lunar New Year — is the country's other massive holiday, when families gather, children perform 세배 (deep bow) to elders, and everyone eats tteokguk to officially gain a year of age.",
        "samples": [
            ("설날","seol-nal","Lunar New Year"),
            ("새해","sae-hae","new year"),
            ("세배","se-bae","New Year deep bow"),
            ("세뱃돈","se-baet-don","New Year money"),
            ("떡국","tteok-guk","rice cake soup (age soup)"),
            ("한복","han-bok","traditional dress"),
            ("덕담","deok-dam","blessing words"),
            ("새해 복 많이 받으세요","sae-hae bok ma-ni ba-deu-se-yo","Happy New Year (most common)"),
            ("나이","na-i","age"),
            ("어른","eo-reun","elder"),
            ("절","jeol","bow"),
            ("윷놀이","yut-no-ri","traditional yut game"),
            ("연날리기","yeon-nal-li-gi","kite flying"),
            ("차례","cha-rye","ancestral rite"),
            ("귀성길","gwi-seong-gil","journey home"),
        ],
        "tip": "Korean age math: on 설날, every Korean traditionally turns one year older — regardless of birthday. As of 2023, Korea officially adopted international age, but traditional age still lives socially.",
        "culture": "세배 ritual: children bow deeply to seated elders. Elders give 덕담 (blessing words) and 세뱃돈 (cash, usually crisp bills in a clean envelope). The exchange creates a yearly contract of family bond.",
        "faqs": [
            ("When is Seolnal in 2026?",
             "Seolnal 2026 falls on February 17 (lunar Jan 1). The 3-day holiday extends Feb 16–18."),
            ("What's the difference between 새해 and 설날?",
             "새해 refers to January 1 (solar new year). 설날 refers specifically to the Lunar New Year — and is the bigger family holiday in Korea."),
            ("How much 세뱃돈 do Korean kids get?",
             "Varies widely: ₩10,000 for small kids, ₩50,000+ for teens, sometimes ₩100,000+ from grandparents. Crisp bills in clean envelopes are expected."),
        ],
        "related": ["chuseok-korean-thanksgiving-traditions", "hyo-filial-piety-korean-family-culture"],
    },
]

ALL_POSTS = [(p, "vocab") for p in VOCAB_POSTS] + [(p, "culture") for p in CULTURE_POSTS]

# ============================================================
# HELPERS
# ============================================================
def find_existing(slug):
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts?slug={slug}&context=edit", headers=HEADERS, timeout=30)
    if r.ok and r.json():
        return r.json()[0]["id"]
    return None


def build_table(samples):
    rows = "".join(
        f"<tr><td style='padding:10px 14px;border-bottom:1px solid #eee;font-size:18px;font-weight:700;color:#1A4A8A;'>{k}</td>"
        f"<td style='padding:10px 14px;border-bottom:1px solid #eee;color:#666;'>{r}</td>"
        f"<td style='padding:10px 14px;border-bottom:1px solid #eee;'>{e}</td></tr>"
        for k, r, e in samples
    )
    return (
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;background:#fafafa;border-radius:10px;overflow:hidden;'>"
        "<thead><tr style='background:#1A4A8A;color:#fff;'>"
        "<th style='padding:12px 14px;text-align:left;'>Korean</th>"
        "<th style='padding:12px 14px;text-align:left;'>Romanization</th>"
        "<th style='padding:12px 14px;text-align:left;'>English</th>"
        "</tr></thead><tbody>"
        f"{rows}</tbody></table>"
    )


def build_faq_html(faqs):
    items = ""
    for q, a in faqs:
        items += (
            f"<details style='background:#F8FAFC;border-left:4px solid #1A4A8A;padding:14px 20px;margin:10px 0;border-radius:6px;'>"
            f"<summary style='cursor:pointer;font-weight:700;font-size:17px;color:#1A1A2E;'>{q}</summary>"
            f"<p style='margin:10px 0 0;'>{a}</p></details>"
        )
    return items


def build_faq_jsonld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ]
    }


def build_article_jsonld(p, url):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "description": p["meta"],
        "keywords": p["kw"],
        "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": "en-US",
    }


CTA_HTML = f"""
<div style="background:linear-gradient(135deg,#1A4A8A,#C0392B);color:#fff;padding:28px;border-radius:14px;margin:32px 0;text-align:center;">
  <h3 style="margin:0 0 12px;font-size:22px;color:#fff;">📚 Get the Complete Resource</h3>
  <p style="margin:0 0 18px;font-size:16px;opacity:0.95;">This is a preview. The full curated content with audio, examples, and PDF download is in our Vocab Hub.</p>
  <a href="{VOCAB_HUB}" rel="noopener" style="display:inline-block;background:#FACC15;color:#1A1A2E;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;font-size:16px;margin:4px;">🎯 Browse Vocab Hub</a>
  <a href="{GUMROAD}" rel="noopener" style="display:inline-block;background:rgba(255,255,255,0.15);color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;font-size:16px;margin:4px;border:2px solid rgba(255,255,255,0.4);">📖 Full eBook</a>
</div>
"""


def build_html(p, series):
    url = f"{SITE}/{p['slug']}/"
    table = build_table(p["samples"])
    faq_html = build_faq_html(p["faqs"])
    article_ld = build_article_jsonld(p, url)
    faq_ld = build_faq_jsonld(p["faqs"])

    series_label = "VOCAB HUB SERIES" if series == "vocab" else "KOREAN CULTURE SERIES"
    series_color = "#FACC15,#F97316" if series == "vocab" else "#10B981,#3B82F6"

    related_links = "".join(
        f'<li><a href="{SITE}/{slug}/" style="color:#1A4A8A;text-decoration:underline;">{slug.replace("-"," ").title()}</a></li>'
        for slug in p.get("related", [])
    )

    toc = (
        '<div style="background:#F8FAFC;border:1px solid #E2E8F0;padding:16px 22px;border-radius:10px;margin:20px 0;">'
        '<strong style="color:#1A4A8A;">📋 In this article:</strong>'
        '<ul style="margin:8px 0 0;padding-left:20px;">'
        '<li><a href="#vocab" style="color:#1A4A8A;">Sample Vocabulary</a></li>'
        '<li><a href="#tip" style="color:#1A4A8A;">Learning Tip</a></li>'
        '<li><a href="#culture" style="color:#1A4A8A;">Cultural Note</a></li>'
        '<li><a href="#faq" style="color:#1A4A8A;">FAQ</a></li>'
        '</ul></div>'
    )

    body = f"""<!-- wp:html -->
<div style="max-width:820px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#222;">

<script type="application/ld+json">{json.dumps(article_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>

<div style="background:linear-gradient(135deg,{series_color});padding:24px 28px;border-radius:14px;margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#7C2D12;letter-spacing:2px;">{series_label}</div>
  <h2 style="margin:6px 0 0;font-size:26px;color:#1A1A2E;">{p['hero']}</h2>
</div>

<p style="font-size:18px;line-height:1.65;">{p['intro']}</p>

{toc}

<h2 id="vocab" style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">🔤 Sample {p['kw'].title()} (15 of the full list)</h2>
{table}

<h2 id="tip" style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">💡 Learning Tip</h2>
<p style="background:#F0F9FF;border-left:4px solid #1A4A8A;padding:16px 20px;border-radius:6px;font-size:16px;">{p['tip']}</p>

<h2 id="culture" style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">🏛️ Cultural Note</h2>
<p style="background:#FEF3C7;border-left:4px solid #F59E0B;padding:16px 20px;border-radius:6px;font-size:16px;">{p['culture']}</p>

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">🚀 How to Apply This</h2>
<p>This sample of 15 entries is enough to give you a flavor, but real fluency comes from consistent exposure to the whole list. Set aside 15 minutes a day, pick 5 new entries, write 3 example sentences each, and review yesterday's batch before adding today's. In 60 days you'll have a working vocabulary that puts you ahead of 90% of intermediate learners.</p>

<h2 id="faq" style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">❓ Frequently Asked Questions</h2>
{faq_html}

<h2 style="color:#1A4A8A;font-size:24px;margin:36px 0 10px;">📖 Related Posts</h2>
<ul style="font-size:16px;">{related_links}</ul>

{CTA_HTML}

<p style="text-align:center;color:#666;font-size:14px;margin-top:30px;">Found this useful? Share it with someone learning Korean. 한국어 공부 화이팅! 🇰🇷</p>

</div>
<!-- /wp:html -->"""
    return body


# ============================================================
# PUBLISH
# ============================================================
print(f"=== Publishing {len(ALL_POSTS)} SEO-optimized posts ===\n")
ok = 0; skipped = 0; fail = 0

for i, (p, series) in enumerate(ALL_POSTS, 1):
    existing = find_existing(p["slug"])
    if existing:
        print(f"[{i:>2}/{len(ALL_POSTS)}] SKIP (exists ID {existing}): {p['title'][:60]}")
        skipped += 1
        continue

    payload = {
        "title":   p["title"],
        "slug":    p["slug"],
        "content": build_html(p, series),
        "excerpt": p["meta"],
        "status":  "publish",
        "categories": [1],
    }
    r = requests.post(f"{SITE}/wp-json/wp/v2/posts", headers=HEADERS, json=payload, timeout=60)
    if r.ok:
        d = r.json()
        print(f"[{i:>2}/{len(ALL_POSTS)}] OK   ID {d['id']}: {p['title'][:60]}")
        ok += 1
    else:
        print(f"[{i:>2}/{len(ALL_POSTS)}] FAIL {r.status_code}: {p['title'][:60]}")
        print(f"           {r.text[:200]}")
        fail += 1
    time.sleep(1)

print(f"\n=== Done: {ok} published, {skipped} skipped, {fail} failed ===")
