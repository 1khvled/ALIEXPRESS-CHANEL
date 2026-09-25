import sys, httpx, re
from bs4 import BeautifulSoup

url = 'https://www.aliexpress.com/item/1005010123517345.html'
with httpx.Client(timeout=8.0, follow_redirects=True, verify=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}) as client:
    r = client.get(url)
    imgs = re.findall(r'//[^\s\"\'<>]+\.alicdn\.com/kf/[A-Za-z0-9_-]+(?:\.jpg|\.png)', r.text)
    print("Found Alicdn images:", len(imgs))
    for img in imgs[:5]:
        full_img = "https:" + img if img.startswith("//") else img
        print("Image:", full_img)
