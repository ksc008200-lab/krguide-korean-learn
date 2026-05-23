import requests, re

r = requests.get('https://krguide.com/post-sitemap.xml', timeout=30)
print('Status:', r.status_code, '| size:', len(r.text), 'chars')

urls = re.findall(r'<loc>([^<]+)</loc>', r.text)
print(f'Total URLs in post-sitemap.xml: {len(urls)}')

new_slugs = [
    '200-essential-korean-verbs',
    '200-korean-adverbs',
    '500-konglish-words',
    'ppalli-ppalli-culture',
    'seongsil-korean-diligence',
    'chaegimgam-korean-responsibility',
    'jeong-untranslatable',
    'han-korean-emotional-depth',
    'nunchi-korean-art',
    'chemyeon-korean-saving-face',
    'uri-korean-collective',
    'hyo-filial-piety',
    'hoesik-korean-company-dinner',
    'chuseok-korean-thanksgiving',
    'seolnal-korean-new-year',
    'hangul-vs-hanja',
]
print('\nNew-post slug check:')
for slug in new_slugs:
    found = any(slug in u for u in urls)
    mark = '[OK]  ' if found else '[MISS]'
    print(f'  {mark}  {slug}')

# Also fetch robots.txt
print('\n--- robots.txt ---')
r2 = requests.get('https://krguide.com/robots.txt', timeout=15)
print(r2.text[:600])
