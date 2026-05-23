"""Upload the 3 Gumroad PNG images to WordPress media library."""
import requests, base64
from pathlib import Path

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()

IMAGES = [
    Path(r"C:\Users\무지랭이\krguide-korean-learn\gumroad-cover.png"),
    Path(r"C:\Users\무지랭이\krguide-korean-learn\gumroad-features.png"),
    Path(r"C:\Users\무지랭이\krguide-korean-learn\gumroad-chapters.png"),
]

for img in IMAGES:
    print(f"\nUploading {img.name} ({img.stat().st_size/1024:.1f} KB) ...")
    with open(img, "rb") as f:
        data = f.read()
    headers = {
        "Authorization": f"Basic {cred}",
        "Content-Type": "image/png",
        "Content-Disposition": f'attachment; filename="{img.name}"',
    }
    r = requests.post(f"{SITE}/wp-json/wp/v2/media", headers=headers, data=data, timeout=120)
    if r.ok:
        d = r.json()
        print(f"  [OK] ID {d['id']}: {d['source_url']}")
    else:
        print(f"  [FAIL] {r.status_code}: {r.text[:200]}")
