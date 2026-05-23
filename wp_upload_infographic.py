"""Upload the 41-chapter infographic PDF to WordPress media library."""
import requests, base64
from pathlib import Path

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"

PDF = Path(r"C:\Users\무지랭이\krguide-korean-learn\learn-korean-infographic.pdf")
assert PDF.exists(), f"PDF not found: {PDF}"

cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()

print(f"Uploading {PDF.name} ({PDF.stat().st_size/1024:.1f} KB) ...")

with open(PDF, "rb") as f:
    data = f.read()

headers = {
    "Authorization": f"Basic {cred}",
    "Content-Type": "application/pdf",
    "Content-Disposition": f'attachment; filename="learn-korean-infographic.pdf"',
}

r = requests.post(
    f"{SITE}/wp-json/wp/v2/media",
    headers=headers,
    data=data,
    timeout=300,
)

if r.ok:
    d = r.json()
    print(f"\n[OK] Uploaded successfully")
    print(f"  ID:        {d['id']}")
    print(f"  URL:       {d['source_url']}")
else:
    print(f"[FAIL] {r.status_code}")
    print(r.text[:500])
