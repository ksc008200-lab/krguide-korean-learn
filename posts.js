/**
 * KR Guide - Post List
 *
 * How to add a new post:
 * 1. Copy post-template.html â save as post-[name].html
 * 2. Add an entry below
 * 3. Push to GitHub â auto deploy
 */

const POSTS = [
  {
    id: 'travel-conversations',
    title: 'Korean Travel Conversations â Real Dialogues for Every Situation',
    excerpt: 'Natural Korean dialogues for travelers: airport, hotel, restaurant, taxi, shopping, directions, numbers and emergency phrases â all with pronunciation guides.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'travel-conversations.html'
  },
  {
    id: 'korea-food-guide',
    title: 'Korean Food Guide â 30 Must-Try Dishes, Street Food & How to Order',
    excerpt: 'From Korean BBQ to street tteokbokki â a complete guide to eating in Korea with dish explanations, budget tips, vegetarian options and food phrases.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'post-korea-food-guide.html'
  },
  {
    id: 'korea-transport',
    title: 'Korea Transportation Guide â Subway, KTX, Bus & Taxi Explained',
    excerpt: 'T-money card, Seoul subway lines, KTX bullet train routes, airport transfer options and taxi apps â everything you need to get around Korea.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'post-korea-transport.html'
  },
  {
    id: 'busan-travel-guide',
    title: 'Busan Travel Guide 2026 â Beaches, Seafood & Korea\'s Coolest City',
    excerpt: 'Haeundae Beach, Gamcheon Culture Village, Jagalchi Fish Market, Gwangan Bridge â complete guide to Korea\'s second city including food, transport and best time to visit.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'post-busan-travel-guide.html'
  },
  {
    id: 'jeju-travel-guide',
    title: 'Jeju Island Travel Guide 2026 â Hallasan, Beaches & Volcanic Wonders',
    excerpt: 'Seongsan Ilchulbong, Manjanggul lava tube, black pork, tangerine farms â complete Jeju Island guide with area map, getting there, and best time to visit.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'post-jeju-travel-guide.html'
  },
  {
    id: 'korean-complete-guide',
    title: 'Korean Language Complete Guide â 41 Chapters (PDF + Online) $9.90',
    excerpt: 'Master Korean from zero â 41 chapters covering Hangul, grammar, daily life, culture, K-pop slang and more. Full PDF download + read online.',
    date: '2026-04-16',
    category: 'Learn Korean',
    thumbnail: '',
    file: 'ebook-landing.html'
  },
  {
    id: 'korea-daily-life',
    title: 'Daily Life in Korea for Foreigners â ARC, Trash, Budget & Culture',
    excerpt: 'ARC registration step-by-step, Korea\'s trash sorting system, realistic monthly budget, convenience store life, workplace culture and essential Korean etiquette.',
    date: '2026-04-16',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-daily-life.html'
  },
  {
    id: 'korea-phone-sim',
    title: 'Phone & SIM Card in Korea â Carriers, MVNO Plans & 10 Essential Apps',
    excerpt: 'How to get a Korean phone number, KT vs SKT vs LG U+ comparison, budget MVNO options, and the 10 apps you need to live in Korea.',
    date: '2026-04-16',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-phone-sim.html'
  },
  {
    id: 'korea-housing',
    title: 'Housing in Korea for Foreigners â Jeonse, Wolse & How to Rent',
    excerpt: 'Korea\'s unique jeonse vs wolse rental system explained, goshiwon to apartment options, how to find housing with Zigbang, contract tips and rent by area.',
    date: '2026-04-16',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-housing.html'
  },
  {
    id: 'korea-healthcare',
    title: 'Healthcare in Korea for Foreigners â NHI, Hospitals & Pharmacies',
    excerpt: 'National Health Insurance enrollment, clinic vs hospital vs general hospital, foreigner-friendly hospitals in Seoul, pharmacy tips and emergency numbers.',
    date: '2026-04-16',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-healthcare.html'
  },
  {
    id: 'korea-banking',
    title: 'Banking in Korea for Foreigners â How to Open a Bank Account',
    excerpt: 'Best banks for foreigners (IBK, KakaoBank, Shinhan), step-by-step account opening, international money transfers, ATM tips and banking Korean phrases.',
    date: '2026-04-16',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-banking.html'
  },
  {
    id: 'korea-travel-hub',
    title: 'Korea Travel Guide 2026 â Destinations, Tips & Everything You Need',
    excerpt: 'Complete Korea travel hub: top destinations (Seoul, Busan, Jeju, Gyeongju), best seasons, transport, budget tips, food, safety and essential Korean phrases for travelers.',
    date: '2026-04-16',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'travel.html'
  },
  {
    id: 'seoul-travel-guide',
    title: 'Seoul Travel Guide 2026 â Everything You Need to Know',
    excerpt: 'First time in Seoul? This complete guide covers the best neighborhoods, must-see attractions, transportation tips, and hidden gems to make your Seoul trip unforgettable.',
    date: '2026-03-31',
    category: 'Travel Guide',
    thumbnail: '',
    file: 'post-seoul-travel-guide.html'
  },
  {
    id: 'korea-visa-guide',
    title: 'Korea Visa Guide â Types, Requirements & How to Apply',
    excerpt: 'Planning to visit or live in Korea? This guide covers all visa types â tourist, working holiday, D-10 job seeker, E-2 English teacher â with step-by-step application tips.',
    date: '2026-03-28',
    category: 'Living in Korea',
    thumbnail: '',
    file: 'post-korea-visa-guide.html'
  },
  {
    id: 'korean-basics',
    title: 'Korean for Beginners â 50 Essential Phrases to Know Before You Go',
    excerpt: 'You don\'t need to be fluent to get around Korea. Learn these 50 essential Korean phrases for greetings, shopping, ordering food, and getting help â with pronunciation guides.',
    date: '2026-03-25',
    category: 'Learn Korean',
    thumbnail: '',
    file: 'post-korean-basics.html'
  },
  // Add new posts above (newest first)
];

// Category list (displayed in sidebar)
const CATEGORIES = ['Travel Guide', 'Living in Korea', 'Learn Korean'];

