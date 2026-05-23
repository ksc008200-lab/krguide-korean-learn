import requests, base64
SITE = 'https://krguide.com'
cred = base64.b64encode(b'admin_hu20is3:Cn5l oGV1 WkMD zbpa jJyx AplN').decode()
H = {'Authorization': f'Basic {cred}'}
r = requests.get(f'{SITE}/wp-json/wp/v2/media?search=learn-korean-v3&per_page=10', headers=H, timeout=30)
for m in r.json():
    print(f"ID {m['id']:>5} | {m['source_url']}")
