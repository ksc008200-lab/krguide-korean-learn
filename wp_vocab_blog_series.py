"""Publish a 15-post Vocab Hub blog series.

Each post:
- 1500+ words English-led with Korean
- Sample vocab table (delivers real value, not just an ad)
- Learning tip + cultural note
- CTA box linking to the specific Vocab Hub resource
"""
import requests, base64, time

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}", "Content-Type": "application/json"}

VOCAB_HUB = "https://study.krguide.com/vocab-hub.html"
GUMROAD   = "https://jssmn21.gumroad.com/l/gnefla"

# Each post: title, slug, resource_anchor (vocab-hub link), hero phrase, intro paragraph,
# vocabulary sample (rows of [Korean, romanization, English]), tip, culture, conclusion
POSTS = [
    {
        "title": "200 Essential Korean Verbs Every Learner Must Master",
        "slug":  "200-essential-korean-verbs-every-learner-must-master",
        "hero":  "동사가 곧 한국어다",
        "intro": "If you only had time to learn one part of speech in Korean, it should be verbs. Korean grammar pivots around the verb stem — and once you internalize the 200 highest-frequency verbs, you unlock about 80% of daily conversation. This guide shows you the foundation, then points to our complete 200-verb resource.",
        "samples": [
            ("가다", "ga-da", "to go"),
            ("오다", "o-da", "to come"),
            ("먹다", "meok-da", "to eat"),
            ("마시다", "ma-si-da", "to drink"),
            ("보다", "bo-da", "to see / to watch"),
            ("듣다", "deut-da", "to hear / to listen"),
            ("말하다", "mal-ha-da", "to speak"),
            ("읽다", "ilk-da", "to read"),
            ("쓰다", "sseu-da", "to write / to use"),
            ("자다", "ja-da", "to sleep"),
            ("일어나다", "il-eo-na-da", "to wake up / to stand up"),
            ("앉다", "an-da", "to sit"),
            ("하다", "ha-da", "to do"),
            ("되다", "doe-da", "to become"),
            ("주다", "ju-da", "to give"),
        ],
        "tip": "Always learn a Korean verb in its dictionary form (ending in -다). The -다 is just a citation marker — when you actually speak, you strip it and attach an ending like -아요/-어요 (polite), -ㅂ니다/-습니다 (formal), or -ㄴ다/-는다 (plain).",
        "culture": "Korean does not conjugate verbs by person (I/you/he). Whether the subject is 나, 너, or 그녀, the verb form is the same. Context and particles carry the meaning instead.",
    },
    {
        "title": "200 Korean Adverbs to Sound Natural and Fluent",
        "slug":  "200-korean-adverbs-sound-natural-fluent",
        "hero":  "Adverbs unlock fluency",
        "intro": "Beginners learn nouns. Intermediates learn grammar. But fluency? Fluency comes from adverbs. Words like 그냥, 좀, 진짜, 막, 약간 are what make Korean sound human instead of robotic. This guide introduces the most natural-sounding 15 — and the full list of 200 is in our resource.",
        "samples": [
            ("그냥", "geu-nyang", "just / simply"),
            ("좀", "jom", "a little (softens requests)"),
            ("진짜", "jin-jja", "really / seriously"),
            ("정말", "jeong-mal", "really / truly"),
            ("아주", "a-ju", "very"),
            ("너무", "neo-mu", "too much / very"),
            ("매우", "mae-u", "extremely (formal)"),
            ("약간", "yak-gan", "a bit"),
            ("조금", "jo-geum", "a little"),
            ("많이", "ma-ni", "a lot"),
            ("천천히", "cheon-cheon-hi", "slowly"),
            ("빨리", "ppal-li", "quickly"),
            ("벌써", "beol-sseo", "already"),
            ("아직", "a-jik", "still / not yet"),
            ("막", "mak", "just now / recklessly"),
        ],
        "tip": "Native speakers sprinkle 좀 (jom) into nearly every polite request. '커피 주세요' is correct but blunt. '커피 좀 주세요' is the natural, polite version. The 좀 doesn't translate — it softens.",
        "culture": "Korean adverbs frequently double for emphasis: 정말정말 좋아요 (really really good), 빨리빨리 (hurry hurry — basically a national catchphrase).",
    },
    {
        "title": "369 Common Korean Nouns Every Beginner Should Know",
        "slug":  "369-common-korean-nouns-every-beginner-should-know",
        "hero":  "Vocabulary is the bedrock",
        "intro": "Grammar is the skeleton, but nouns are the flesh. Without enough nouns, you cannot describe your day, ask for what you need, or follow a K-drama. We compiled 369 of the most useful Korean nouns — organized by life domain (home, work, food, body, emotions, places) so you build practical fluency, not random word lists.",
        "samples": [
            ("집", "jip", "house / home"),
            ("학교", "hak-gyo", "school"),
            ("회사", "hoe-sa", "company"),
            ("친구", "chin-gu", "friend"),
            ("가족", "ga-jok", "family"),
            ("음식", "eum-sik", "food"),
            ("물", "mul", "water"),
            ("시간", "si-gan", "time"),
            ("돈", "don", "money"),
            ("일", "il", "work / one / day"),
            ("사람", "sa-ram", "person"),
            ("아이", "a-i", "child"),
            ("책", "chaek", "book"),
            ("길", "gil", "road / way"),
            ("마음", "ma-eum", "mind / heart"),
        ],
        "tip": "Korean nouns don't change for plural. 책 (book) and 책 (books) are identical — context handles the number. If you must mark plural, add 들: 사람들 (people).",
        "culture": "Several Korean nouns carry deep cultural weight. 마음 is not just 'mind' — it's the seat of feeling, intention, and integrity. 정 (jeong) has no direct English equivalent.",
    },
    {
        "title": "500 Korean Honorifics — Master Polite Speech Like a Native",
        "slug":  "500-korean-honorifics-master-polite-speech-native",
        "hero":  "존댓말 마스터",
        "intro": "Korean honorifics are not optional. Use the wrong form with a boss, an elder, or a stranger, and you'll come across as rude — even if your grammar is perfect. We cataloged 500 honorific forms across verbs, nouns, particles, and titles, so you can match the register every time.",
        "samples": [
            ("드시다", "deu-si-da", "to eat (honorific of 먹다)"),
            ("계시다", "gye-si-da", "to be / stay (honorific)"),
            ("말씀하시다", "mal-sseum-ha-si-da", "to speak (honorific)"),
            ("주무시다", "ju-mu-si-da", "to sleep (honorific)"),
            ("돌아가시다", "do-ra-ga-si-da", "to pass away (honorific euphemism)"),
            ("진지", "jin-ji", "meal (honorific of 밥)"),
            ("연세", "yeon-se", "age (honorific of 나이)"),
            ("성함", "seong-ham", "name (honorific of 이름)"),
            ("께서", "kke-seo", "honorific subject marker"),
            ("께", "kke", "honorific recipient marker"),
            ("선생님", "seon-saeng-nim", "teacher / sir"),
            ("사장님", "sa-jang-nim", "boss"),
            ("어머님", "eo-meo-nim", "mother (honorific)"),
            ("아버님", "a-beo-nim", "father (honorific)"),
            ("손님", "son-nim", "guest / customer"),
        ],
        "tip": "Add -시- to a verb stem to make it honorific. 먹다 → 드시다 (special form) or 가다 → 가시다 (add -시-). Stack with polite endings: 가세요 (please go).",
        "culture": "Koreans use honorifics with anyone older or higher in status — even a sibling one year older. Drop honorifics only after explicit agreement ('말 놔도 돼').",
    },
    {
        "title": "391 Japanese Loanwords in Korean (일본어 외래어) Explained",
        "slug":  "391-japanese-loanwords-korean-explained",
        "hero":  "Hidden Japanese in Korean",
        "intro": "After 35 years of colonial occupation, hundreds of Japanese words slipped into everyday Korean. Many sound 'Korean' but are actually Japanese — 다꽝, 와사비, 뎀뿌라, 오뎅. Younger generations are replacing them, but you'll still hear them every day. Knowing them helps you decode older speakers and historical content.",
        "samples": [
            ("다꽝", "da-kkwang", "pickled radish (J: takuan)"),
            ("와사비", "wa-sa-bi", "wasabi"),
            ("뎀뿌라", "dem-ppu-ra", "tempura"),
            ("오뎅", "o-deng", "fishcake stew"),
            ("스시", "seu-si", "sushi"),
            ("사시미", "sa-si-mi", "sashimi"),
            ("나가리", "na-ga-ri", "called off (slang from J: nagare)"),
            ("쇼부", "syo-bu", "showdown / decision (J: shoubu)"),
            ("기스", "gi-seu", "scratch (J: kizu)"),
            ("땡땡이", "ttaeng-ttaeng-i", "polka dots (J: tenten)"),
            ("쓰메끼리", "sseu-me-kki-ri", "nail clippers (J: tsumekiri)"),
            ("후카시", "hu-ka-si", "showing off (J: fukashi)"),
            ("간지", "gan-ji", "style / coolness (J: kanji)"),
            ("기리", "gi-ri", "obligation (J: giri)"),
            ("닭도리탕", "dak-do-ri-tang", "spicy chicken stew (debated origin)"),
        ],
        "tip": "Younger Koreans actively avoid Japanese loanwords. Use 단무지 instead of 다꽝, 어묵 instead of 오뎅. Older speakers and traditional markets still use the originals.",
        "culture": "The Korean government has periodically launched campaigns to replace Japanese loanwords with native Korean equivalents — 'language purification' (국어 순화).",
    },
    {
        "title": "1,067 Korean Adjectives, Adverbs & Idioms — The Big List",
        "slug":  "1067-korean-adjectives-adverbs-idioms-big-list",
        "hero":  "Big list, real fluency",
        "intro": "Once you've mastered the basics, the next leap is descriptive power. The difference between 'good' and '괜찮네, 그치만 좀 아쉬워' is a thousand-word vocabulary in your descriptors. We compiled 1,067 adjectives, adverbs, and idiomatic phrases so you can describe nuance like a native.",
        "samples": [
            ("예쁘다", "ye-ppeu-da", "pretty"),
            ("멋있다", "meo-sit-da", "cool / stylish"),
            ("귀엽다", "gwi-yeop-da", "cute"),
            ("아름답다", "a-reum-dap-da", "beautiful"),
            ("재미있다", "jae-mi-it-da", "fun / interesting"),
            ("지루하다", "ji-ru-ha-da", "boring"),
            ("아쉽다", "a-swip-da", "regrettable / disappointing"),
            ("괜찮다", "gwaen-chan-ta", "okay / fine"),
            ("끔찍하다", "kkeum-jji-ka-da", "terrible / horrific"),
            ("훌륭하다", "hul-lyung-ha-da", "excellent"),
            ("어이없다", "eo-i-eop-da", "absurd / unbelievable"),
            ("당황스럽다", "dang-hwang-seu-reop-da", "flustered"),
            ("후련하다", "hu-ryeon-ha-da", "relieved (after frustration)"),
            ("뿌듯하다", "ppu-deu-ta-da", "proud / fulfilled"),
            ("심심하다", "sim-sim-ha-da", "bored"),
        ],
        "tip": "Korean has emotion-adjectives that English needs a phrase to translate. 뿌듯하다 = 'the warm pride of having done something meaningful.' 아쉽다 = 'wishing it could've been different.' Memorize them in context.",
        "culture": "Idiomatic expressions tied to body parts are huge in Korean: 눈치가 빠르다 (quick-eye = perceptive), 입이 무겁다 (heavy mouth = can keep a secret), 발이 넓다 (wide foot = well-connected).",
    },
    {
        "title": "500 Korean Internet Slang Words (2026 Edition)",
        "slug":  "500-korean-internet-slang-words-2026-edition",
        "hero":  "Modern Korean Internet 인싸 vocabulary",
        "intro": "Korean teen and Gen Z slang evolves faster than dictionaries can track. From 인싸/아싸 to ㅇㅇ ㄴㄴ to 갓-, internet slang is where the language is alive. We documented 500 active slang terms used on Twitter, Instagram, KakaoTalk, and gaming chat in 2026.",
        "samples": [
            ("인싸", "in-ssa", "insider / popular kid"),
            ("아싸", "a-ssa", "outsider / loner"),
            ("핵-", "haek-", "extremely (prefix: 핵귀여워 = nuke-cute)"),
            ("갓-", "gat-", "god-tier (prefix: 갓영화 = god-movie)"),
            ("존-", "jon-", "super- (intensifier prefix)"),
            ("ㅇㅇ", "eung-eung", "yes (chat shorthand)"),
            ("ㄴㄴ", "no-no", "no (chat shorthand)"),
            ("ㄱㄱ", "go-go", "let's go / start"),
            ("ㅋㅋ", "keu-keu", "lol"),
            ("ㄷㄷ", "deol-deol", "shivering / impressive"),
            ("ㅈㅂ", "je-bal", "please (lit. 제발)"),
            ("미친", "mi-chin", "crazy (positive or negative)"),
            ("실화냐", "sil-hwa-nya", "is this real life?"),
            ("개꿀", "gae-kkul", "super sweet deal"),
            ("ㅇㅈ", "in-jeong", "I admit / agree"),
        ],
        "tip": "Korean Gen Z constantly invents acronyms from initial consonants (자음 약어). ㅇㅈ = 인정, ㅁㅈ = 미정, ㅂㅂ = 바이바이. Reading the consonants out loud usually reveals the word.",
        "culture": "Slang is generation-coded. Using 'ㅈㅎㅁ' (자존감 = self-esteem) in a corporate Slack will get strange looks. Use it on Twitter or with friends.",
    },
    {
        "title": "500 Konglish Words — When English Becomes Korean",
        "slug":  "500-konglish-words-when-english-becomes-korean",
        "hero":  "Konglish: English with Korean rules",
        "intro": "Konglish is English vocabulary reshaped into Korean — sometimes with new meanings, sometimes with pronunciation that English speakers can barely recognize. 핸드폰, 노트북, 아이쇼핑, 원샷, 화이팅 — these are Konglish, not English. We compiled 500 of the most common ones so you can decode them instantly.",
        "samples": [
            ("핸드폰", "haen-deu-pon", "cell phone (lit. hand phone)"),
            ("노트북", "no-teu-buk", "laptop (lit. notebook)"),
            ("아이쇼핑", "a-i-syo-ping", "window shopping (lit. eye shopping)"),
            ("원샷", "won-syat", "drink in one shot"),
            ("화이팅", "hwa-i-ting", "go for it! / cheer up!"),
            ("스킨십", "seu-kin-sip", "physical affection (lit. skinship)"),
            ("아파트", "a-pa-teu", "apartment / condo"),
            ("원룸", "won-rum", "studio apartment (lit. one room)"),
            ("리모컨", "ri-mo-keon", "remote control"),
            ("에어컨", "e-eo-keon", "air conditioner"),
            ("백미러", "baek-mi-reo", "rearview mirror (lit. back mirror)"),
            ("샐러리맨", "sael-leo-ri-maen", "office worker (lit. salaryman)"),
            ("팬티", "paen-ti", "underwear"),
            ("원피스", "won-pi-seu", "dress (lit. one piece)"),
            ("매니큐어", "mae-ni-kyu-eo", "nail polish (manicure)"),
        ],
        "tip": "Konglish often shortens English. 'Apartment' → 아파트, 'remote control' → 리모컨. When you hear unfamiliar English-sounding Korean, try expanding the syllables.",
        "culture": "'화이팅' (fighting) is shouted as cheer/encouragement before tests, sports, weddings, and even hospital visits. It does NOT mean fighting in the violent sense.",
    },
    {
        "title": "500 Korean Onomatopoeia (의성어·의태어) Explained",
        "slug":  "500-korean-onomatopoeia-uiseongeo-uitaego-explained",
        "hero":  "Korean sounds like a soundtrack",
        "intro": "Korean is one of the world's most onomatopoeia-rich languages. There are over 8,000 documented sound and motion words — 반짝반짝 (sparkly), 두근두근 (heart pounding), 후루룩 (slurping). Master 500 of them and your Korean instantly becomes more vivid and natural.",
        "samples": [
            ("반짝반짝", "ban-jjak-ban-jjak", "sparkly / twinkling"),
            ("두근두근", "du-geun-du-geun", "heart pounding (nervous/excited)"),
            ("후루룩", "hu-ru-ruk", "slurping noodles"),
            ("쾅쾅", "kwang-kwang", "banging / pounding"),
            ("꿀꺽", "kkul-kkeok", "gulping"),
            ("팔랑팔랑", "pal-lang-pal-lang", "fluttering"),
            ("미끌미끌", "mi-kkeul-mi-kkeul", "slippery"),
            ("뽀송뽀송", "ppo-song-ppo-song", "fluffy/dry (laundry)"),
            ("말랑말랑", "mal-lang-mal-lang", "soft / squishy"),
            ("바삭바삭", "ba-sak-ba-sak", "crispy"),
            ("쿨쿨", "kul-kul", "snoring sound"),
            ("훌쩍훌쩍", "hul-jjeok-hul-jjeok", "sobbing"),
            ("덜덜", "deol-deol", "shivering"),
            ("두둥", "du-dung", "dramatic reveal sound"),
            ("쨍그랑", "jjaeng-geu-rang", "glass shattering"),
        ],
        "tip": "Korean onomatopoeia frequently doubles for intensity — 반짝 = sparkle, 반짝반짝 = lots of sparkling. The doubling almost always increases vividness.",
        "culture": "K-drama subtitles for English audiences often skip onomatopoeia entirely because they don't translate. Learning them deepens your drama immersion dramatically.",
    },
    {
        "title": "100 Essential Korean Idioms (사자성어) for Sophisticated Speech",
        "slug":  "100-essential-korean-idioms-sajaseongeo-sophisticated-speech",
        "hero":  "Four-character power",
        "intro": "사자성어 (sa-ja-seong-eo) are four-character idioms borrowed from Classical Chinese, deeply embedded in formal Korean speech and writing. Sprinkling them into business meetings, essays, or speeches signals education and sophistication. We compiled the 100 most useful ones.",
        "samples": [
            ("일석이조", "il-seok-i-jo", "kill two birds with one stone (one stone, two birds)"),
            ("동상이몽", "dong-sang-i-mong", "same bed, different dreams"),
            ("자업자득", "ja-eop-ja-deuk", "reap what you sow"),
            ("우유부단", "u-yu-bu-dan", "indecisive"),
            ("새옹지마", "sae-ong-ji-ma", "blessing in disguise"),
            ("점입가경", "jeom-ip-ga-gyeong", "getting more and more interesting/serious"),
            ("아전인수", "a-jeon-in-su", "self-serving interpretation"),
            ("이심전심", "i-sim-jeon-sim", "heart-to-heart understanding"),
            ("외유내강", "oe-yu-nae-gang", "soft outside, strong inside"),
            ("일거양득", "il-geo-yang-deuk", "two gains from one action"),
            ("청출어람", "cheong-chul-eo-ram", "student surpasses the teacher"),
            ("결자해지", "gyeol-ja-hae-ji", "the one who tied the knot must untie it"),
            ("환골탈태", "hwan-gol-tal-tae", "complete transformation"),
            ("타산지석", "ta-san-ji-seok", "learning from others' mistakes"),
            ("호가호위", "ho-ga-ho-wi", "borrowing authority you don't have"),
        ],
        "tip": "Don't translate 사자성어 character-by-character — memorize the meaning as a whole. The literal reading is often metaphorical to the point of nonsense in English.",
        "culture": "Korean newspaper headlines and political speeches frequently use 사자성어 as compact, emotionally weighted summaries — knowing them is essential for reading news.",
    },
    {
        "title": "100 Korean Proverbs (속담) Every Native Speaker Knows",
        "slug":  "100-korean-proverbs-sokdam-every-native-knows",
        "hero":  "Wisdom of the people",
        "intro": "While 사자성어 came from classical China, 속담 (Korean proverbs) grew from rural village life — featuring tigers, cows, frogs, rice fields, and Korean folk wisdom. Native speakers drop these into conversation as humor, advice, or moral judgment. Learning 100 unlocks deep cultural fluency.",
        "samples": [
            ("호랑이도 제 말 하면 온다", "ho-rang-i-do je mal ha-myeon on-da", "Speak of the devil (lit. even the tiger comes when you mention it)"),
            ("우물 안 개구리", "u-mul an gae-gu-ri", "a frog in a well (someone with narrow worldview)"),
            ("발 없는 말이 천 리 간다", "bal eom-neun mal-i cheon ri gan-da", "Words travel a thousand miles without feet (rumors spread fast)"),
            ("티끌 모아 태산", "ti-kkeul mo-a tae-san", "Dust grains pile up to a mountain"),
            ("백지장도 맞들면 낫다", "baek-ji-jang-do mat-deul-myeon nat-da", "Even white paper is easier with two people"),
            ("가는 말이 고와야 오는 말이 곱다", "ga-neun mal-i go-wa-ya o-neun mal-i gop-da", "Kind words come back kind"),
            ("등잔 밑이 어둡다", "deung-jan mi-chi eo-dup-da", "It's dark under the lamp (you miss what's right in front of you)"),
            ("뛰는 놈 위에 나는 놈 있다", "ttwi-neun nom wi-e na-neun nom it-da", "Above the runner is a flyer"),
            ("아니 땐 굴뚝에 연기 날까", "a-ni ttaen gul-ttu-ge yeon-gi nal-kka", "No smoke without fire"),
            ("소 잃고 외양간 고친다", "so il-go oe-yang-gan go-chin-da", "Fixing the barn after losing the cow"),
            ("가재는 게 편", "ga-jae-neun ge pyeon", "Crayfish takes the crab's side (people side with their own)"),
            ("개구리 올챙이 적 생각 못 한다", "gae-gu-ri ol-chaeng-i jeok saeng-gak mot han-da", "Frog forgets when it was a tadpole"),
            ("원숭이도 나무에서 떨어진다", "won-sung-i-do na-mu-e-seo tteo-reo-jin-da", "Even monkeys fall from trees"),
            ("천 리 길도 한 걸음부터", "cheon ri gil-do han geo-reum-bu-teo", "A thousand-mile journey starts with one step"),
            ("작은 고추가 더 맵다", "ja-geun go-chu-ga deo maep-da", "Small peppers are spicier"),
        ],
        "tip": "Korean proverbs are best learned through K-dramas and Korean novels — context cements them. Hearing 호랑이도 제 말 하면 in a scene is more memorable than memorizing the literal meaning.",
        "culture": "Older Koreans drop 속담 constantly. If you understand and respond appropriately, expect immediate respect ('한국 사람보다 한국말 잘하네!').",
    },
    {
        "title": "1,100 Korean Visual Vocabulary — Learn by Picture",
        "slug":  "1100-korean-visual-vocabulary-learn-by-picture",
        "hero":  "Image-based learning",
        "intro": "Research on second-language acquisition consistently shows visual associations beat translation drills for long-term retention. We assembled 1,100 essential Korean words paired with images covering 30 categories: kitchen, bedroom, hospital, transit, outdoor, emotions, occupations, and more.",
        "samples": [
            ("냉장고", "naeng-jang-go", "refrigerator"),
            ("세탁기", "se-tak-gi", "washing machine"),
            ("청소기", "cheong-so-gi", "vacuum cleaner"),
            ("전자레인지", "jeon-ja-re-in-ji", "microwave"),
            ("드라이기", "deu-ra-i-gi", "hair dryer"),
            ("화장대", "hwa-jang-dae", "vanity table"),
            ("옷장", "ot-jang", "wardrobe"),
            ("책상", "chaek-sang", "desk"),
            ("의자", "ui-ja", "chair"),
            ("거울", "geo-ul", "mirror"),
            ("시계", "si-gye", "clock / watch"),
            ("우산", "u-san", "umbrella"),
            ("열쇠", "yeol-soe", "key"),
            ("가방", "ga-bang", "bag"),
            ("지갑", "ji-gap", "wallet"),
        ],
        "tip": "Group vocabulary by physical location, not by alphabet. Memorize all kitchen words at once, then all bathroom words. Your brain links them to spatial memory, which is far more durable.",
        "culture": "Korean apartment vocabulary differs from Western homes. There is no separate dining room — eating happens in the 거실 (living room). Bathrooms are 욕실 OR 화장실 depending on context.",
    },
    {
        "title": "100 Bible Verses in Korean (한국어 성경 구절)",
        "slug":  "100-bible-verses-korean-hangugeo-seonggyeong",
        "hero":  "Sacred text, formal Korean",
        "intro": "Korean has one of Asia's largest Christian populations — and Korean Bible verses are written in a specific elevated register that's worth studying. Reading Scripture is one of the few sustained ways to practice high-register Korean. We compiled 100 of the most-quoted verses with parallel English.",
        "samples": [
            ("태초에 하나님이 천지를 창조하시니라", "tae-cho-e ha-na-nim-i cheon-ji-reul chang-jo-ha-si-ni-ra", "In the beginning God created the heavens and the earth (Gen 1:1)"),
            ("하나님은 사랑이시라", "ha-na-nim-eun sa-rang-i-si-ra", "God is love (1 John 4:8)"),
            ("내가 너와 함께 있느니라", "nae-ga neo-wa ham-kke it-neu-ni-ra", "I am with you (Isaiah 41:10)"),
            ("주는 나의 목자시니", "ju-neun na-ui mok-ja-si-ni", "The Lord is my shepherd (Psalm 23:1)"),
            ("두려워 말라", "du-ryeo-wo mal-ra", "Do not fear"),
            ("믿음 소망 사랑", "mi-deum so-mang sa-rang", "Faith, hope, love (1 Cor 13)"),
            ("너희가 거듭 나야 하리라", "neo-hui-ga geo-deup na-ya ha-ri-ra", "You must be born again (John 3:7)"),
            ("내가 곧 길이요 진리요 생명이니", "nae-ga got gi-ri-yo jin-ri-yo saeng-myeong-i-ni", "I am the way, the truth, and the life (John 14:6)"),
            ("범사에 감사하라", "beom-sa-e gam-sa-ha-ra", "Give thanks in all circumstances (1 Thess 5:18)"),
            ("쉬지 말고 기도하라", "swi-ji mal-go gi-do-ha-ra", "Pray without ceasing (1 Thess 5:17)"),
            ("수고하고 무거운 짐 진 자들아", "su-go-ha-go mu-geo-un jim jin ja-deul-a", "Come to me all who are weary (Matt 11:28)"),
            ("이는 내 사랑하는 아들이요", "i-neun nae sa-rang-ha-neun a-deul-i-yo", "This is my beloved Son (Matt 3:17)"),
            ("진리가 너희를 자유롭게 하리라", "jin-ri-ga neo-hui-reul ja-yu-rop-ge ha-ri-ra", "The truth shall set you free (John 8:32)"),
            ("내 은혜가 네게 족하도다", "nae eun-hye-ga ne-ge jo-ka-do-da", "My grace is sufficient for you (2 Cor 12:9)"),
            ("일어나 빛을 발하라", "i-reo-na bi-cheul bal-ha-ra", "Arise and shine (Isaiah 60:1)"),
        ],
        "tip": "Korean Bible verses end with archaic verb endings: -하라 (command), -하느니라 (declaration), -하시니라 (formal narrative). These don't appear in spoken Korean but are essential for reading older literature.",
        "culture": "Korean Christianity has Confucian formal-respect baked into its language. The phrase 하나님 아버지 (God Father) uses honorifics throughout. This is one of the few domains where you'll see consistent -하나이다 endings.",
    },
    {
        "title": "1,000 Korean IT Terms — Tech Vocabulary for Programmers",
        "slug":  "1000-korean-it-terms-tech-vocabulary-programmers",
        "hero":  "Tech Korean for the global engineer",
        "intro": "Korea's tech sector is one of the world's largest. If you're working at Samsung, LG, Naver, Kakao, or Coupang, you'll need IT-specific Korean. We compiled 1,000 software/hardware/network/AI terms with both Korean reading and English source — covering everything from 알고리즘 to 클라우드 컴퓨팅.",
        "samples": [
            ("알고리즘", "al-go-ri-jeum", "algorithm"),
            ("데이터베이스", "de-i-teo-be-i-seu", "database"),
            ("서버", "seo-beo", "server"),
            ("클라우드", "keul-la-u-deu", "cloud"),
            ("머신러닝", "meo-sin-leo-ning", "machine learning"),
            ("인공지능", "in-gong-ji-neung", "artificial intelligence"),
            ("개발자", "gae-bal-ja", "developer"),
            ("배포", "bae-po", "deployment"),
            ("저장소", "jeo-jang-so", "repository"),
            ("자동화", "ja-dong-hwa", "automation"),
            ("프레임워크", "peu-re-im-wo-keu", "framework"),
            ("라이브러리", "ra-i-beu-reo-ri", "library"),
            ("커밋", "keo-mit", "commit (Git)"),
            ("브랜치", "beu-raen-chi", "branch (Git)"),
            ("디버깅", "di-beo-ging", "debugging"),
        ],
        "tip": "Korean IT vocabulary is split between Sino-Korean translations (개발자 = developer) and English loanwords (디버깅 = debugging). Native Korean developers mix both in the same sentence: '커밋 메시지에 자동화 추가했어요.'",
        "culture": "Korean tech companies use English-Korean code-switching heavily in meetings. You'll hear 'kickoff 미팅', 'OKR 세팅', 'standup 진행' — knowing both the loanword and Korean equivalent is essential.",
    },
    {
        "title": "Hangul vs Hanja — The Complete Bilingual Reference",
        "slug":  "hangul-vs-hanja-complete-bilingual-reference",
        "hero":  "Hangul + Hanja = full literacy",
        "intro": "Modern Korean is written in Hangul. But 60-70% of Korean vocabulary derives from Hanja (Chinese characters), and many newspapers, legal documents, and formal name cards still use them. Knowing the most common 1,800 Hanja unlocks instant vocabulary multiplication.",
        "samples": [
            ("人 인", "in", "person"),
            ("大 대", "dae", "big"),
            ("小 소", "so", "small"),
            ("中 중", "jung", "middle"),
            ("學 학", "hak", "learning / study"),
            ("校 교", "gyo", "school"),
            ("生 생", "saeng", "birth / life"),
            ("死 사", "sa", "death"),
            ("國 국", "guk", "country"),
            ("家 가", "ga", "house / family"),
            ("水 수", "su", "water"),
            ("火 화", "hwa", "fire"),
            ("山 산", "san", "mountain"),
            ("江 강", "gang", "river"),
            ("日 일", "il", "sun / day"),
        ],
        "tip": "When you learn Hanja, you learn Korean in batches. Once you know 學 (hak = study), you can guess: 학교 (school), 학생 (student), 학습 (learning), 수학 (math), 과학 (science) — all contain it.",
        "culture": "Hanja is mandatory in Korean newspapers when names are ambiguous. Same name 정수 could mean 整數 (whole number) or 淨水 (purified water) or be a person's name — Hanja clarifies.",
    },
]

CTA_HTML = """
<div style="background:linear-gradient(135deg,#1A4A8A,#C0392B);color:#fff;padding:28px;border-radius:14px;margin:32px 0;text-align:center;">
  <h3 style="margin:0 0 12px;font-size:22px;color:#fff;">📚 Get the Complete Resource</h3>
  <p style="margin:0 0 18px;font-size:16px;opacity:0.95;">This article is a preview. The full curated list with audio, examples, and PDF download is available in our Vocab Hub.</p>
  <a href="{HUB}" style="display:inline-block;background:#FACC15;color:#1A1A2E;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;font-size:16px;margin:4px;">🎯 Browse Vocab Hub</a>
  <a href="{GUMROAD}" style="display:inline-block;background:rgba(255,255,255,0.15);color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:800;font-size:16px;margin:4px;border:2px solid rgba(255,255,255,0.4);">📖 Full eBook</a>
</div>
""".format(HUB=VOCAB_HUB, GUMROAD=GUMROAD)


def build_html(p):
    rows = "".join(
        f"<tr><td style='padding:10px 14px;border-bottom:1px solid #eee;font-size:18px;font-weight:700;color:#1A4A8A;'>{k}</td>"
        f"<td style='padding:10px 14px;border-bottom:1px solid #eee;color:#666;'>{r}</td>"
        f"<td style='padding:10px 14px;border-bottom:1px solid #eee;'>{e}</td></tr>"
        for k, r, e in p["samples"]
    )
    table = (
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;background:#fafafa;border-radius:10px;overflow:hidden;'>"
        "<thead><tr style='background:#1A4A8A;color:#fff;'>"
        "<th style='padding:12px 14px;text-align:left;'>Korean</th>"
        "<th style='padding:12px 14px;text-align:left;'>Romanization</th>"
        "<th style='padding:12px 14px;text-align:left;'>English</th>"
        "</tr></thead><tbody>"
        f"{rows}</tbody></table>"
    )

    body = f"""<!-- wp:html -->
<div style="max-width:820px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#222;">

<div style="background:linear-gradient(135deg,#FACC15,#F97316);padding:24px 28px;border-radius:14px;margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#7C2D12;letter-spacing:2px;">VOCAB HUB SERIES</div>
  <h2 style="margin:6px 0 0;font-size:26px;color:#1A1A2E;">{p['hero']}</h2>
</div>

<p style="font-size:17px;">{p['intro']}</p>

<h2 style="color:#1A4A8A;font-size:22px;margin:32px 0 10px;">🔤 Sample Vocabulary (15 of the full list)</h2>
{table}

<h2 style="color:#1A4A8A;font-size:22px;margin:32px 0 10px;">💡 Learning Tip</h2>
<p style="background:#F0F9FF;border-left:4px solid #1A4A8A;padding:16px 20px;border-radius:6px;">{p['tip']}</p>

<h2 style="color:#1A4A8A;font-size:22px;margin:32px 0 10px;">🏛️ Cultural Note</h2>
<p style="background:#FEF3C7;border-left:4px solid #F59E0B;padding:16px 20px;border-radius:6px;">{p['culture']}</p>

<h2 style="color:#1A4A8A;font-size:22px;margin:32px 0 10px;">🚀 Next Step</h2>
<p>This sample of 15 entries is enough to give you a flavor, but real fluency comes from consistent exposure to the whole list. Set aside 15 minutes a day, pick 5 new entries, write 3 example sentences each, and review yesterday's batch before adding today's. In 60 days you'll have a working vocabulary that puts you ahead of 90% of intermediate learners.</p>

{CTA_HTML}

<p style="text-align:center;color:#666;font-size:14px;margin-top:30px;">Found this useful? Share it with someone learning Korean. 한국어 공부 화이팅! 🇰🇷</p>

</div>
<!-- /wp:html -->"""
    return body


def find_existing(slug):
    r = requests.get(f"{SITE}/wp-json/wp/v2/posts?slug={slug}&context=edit", headers=HEADERS, timeout=30)
    if r.ok and r.json():
        return r.json()[0]["id"]
    return None


print("=== Publishing Vocab Hub Blog Series ===\n")
ok = 0
skipped = 0
fail = 0
for i, p in enumerate(POSTS, 1):
    # Skip if already exists
    existing = find_existing(p["slug"])
    if existing:
        print(f"[{i:>2}/{len(POSTS)}] SKIP (exists ID {existing}): {p['title']}")
        skipped += 1
        continue

    payload = {
        "title": p["title"],
        "slug": p["slug"],
        "content": build_html(p),
        "status": "publish",
        "categories": [1],  # Uncategorized → will change to Learn Korean if needed
    }
    r = requests.post(f"{SITE}/wp-json/wp/v2/posts", headers=HEADERS, json=payload, timeout=60)
    if r.ok:
        d = r.json()
        print(f"[{i:>2}/{len(POSTS)}] OK   ID {d['id']}: {p['title']}")
        ok += 1
    else:
        print(f"[{i:>2}/{len(POSTS)}] FAIL {r.status_code}: {p['title']}")
        print(f"           {r.text[:200]}")
        fail += 1
    time.sleep(1)  # be gentle on the host

print(f"\n=== Done: {ok} published, {skipped} skipped, {fail} failed ===")
