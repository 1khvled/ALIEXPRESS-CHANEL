import sys, httpx, re
from bs4 import BeautifulSoup

url = 'https://www.aliexpress.com/item/1005010123517345.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
with httpx.Client(timeout=8.0, follow_redirects=True, verify=False, headers=headers) as client:
    r = client.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    og = soup.find('meta', property='og:image')
    print("Mobile OG Image:", og['content'] if og else None)
    imgs = re.findall(r'https?://[^\s\"\'<>]+\.alicdn\.com/kf/[A-Za-z0-9_-]+(?:\.jpg|\.png)', r.text)
    print("Found images:", len(imgs))
    if imgs:
        print("Sample:", imgs[0])
