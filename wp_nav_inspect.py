import requests, base64, re

SITE = "https://krguide.com"
USER = "admin_hu20is3"
APP_PASS = "Cn5l oGV1 WkMD zbpa jJyx AplN"
cred = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {cred}"}

r = requests.get(f"{SITE}/wp-json/wp/v2/navigation/4?context=edit", headers=HEADERS, timeout=30)
nav = r.json()
raw = nav["content"]["raw"]

print(f"=== Navigation '{nav['title']['rendered']}' (ID {nav['id']}) ===\n")
print("Full raw content:")
print("-" * 60)
print(raw)
print("-" * 60)

# Extract all menu items with labels and hrefs
print("\n=== Menu items summary ===")
items = re.findall(r'<a[^>]*href="([^"]*)"[^>]*><span[^>]*>([^<]*)</span></a>', raw)
for href, label in items:
    print(f"  '{label}'  →  {href}")
