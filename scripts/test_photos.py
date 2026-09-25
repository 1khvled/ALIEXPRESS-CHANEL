import httpx
import re
from bs4 import BeautifulSoup
from pathlib import Path

channels = ['ECKSDEAL', 'Pcgamingpart', 'BNDDEALS', 'zedstoreonline', 'lodydeals']
for ch in channels:
    r = httpx.get(f"https://t.me/s/{ch}")
    soup = BeautifulSoup(r.text, "html.parser")
    for wrap in soup.find_all("a", class_="tgme_widget_message_photo_wrap"):
        style = wrap.get("style", "")
        m = re.search(r"url\('([^']+)'\)", style)
        if m:
            img_url = m.group(1)
            img_resp = httpx.get(img_url)
            Path(f"test_{ch}.jpg").write_bytes(img_resp.content)
            print(f"Saved test_{ch}.jpg, size={len(img_resp.content)}")
            break
