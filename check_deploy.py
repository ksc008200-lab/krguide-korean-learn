import requests
for url in ['https://krguide-vocab.pages.dev/vocab-hub.html']:
    try:
        r = requests.get(url, timeout=20, headers={'Cache-Control':'no-cache'})
        n9  = r.text.count('$9.90')
        n19 = r.text.count('$19.90')
        nview = r.text.count('온라인 학습')
        ndl   = r.text.count('PDF 다운로드')
        print(f'{url}')
        print(f'  status={r.status_code}  size={len(r.text)}')
        print(f'  $9.90={n9}  $19.90={n19}')
        print(f'  온라인학습 버튼={nview}  PDF다운로드 버튼={ndl}')
    except Exception as e:
        print(f'{url}: ERROR {e}')
