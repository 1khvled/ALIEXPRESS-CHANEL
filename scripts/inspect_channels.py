import urllib.request
import re
from bs4 import BeautifulSoup
import sys

channels = ['ECKSDEAL', 'zedstoreonline', 'Pcgamingpart', 'lodydeals', 'BNDDEALS', 'megaprix', 'aniscoupons']

with open("channel_samples.txt", "w", encoding="utf-8") as out:
    for ch in channels:
        out.write(f"\n=================== CHANNEL: {ch} ===================\n")
        url = f"https://t.me/s/{ch}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message_wrap')
            for msg in messages[-6:]:
                text_el = msg.find('div', class_='tgme_widget_message_text')
                photo_el = msg.find('a', class_='tgme_widget_message_photo_wrap')
                if text_el:
                    out.write("--- MESSAGE TEXT ---\n")
                    out.write(text_el.get_text(separator="\n").strip() + "\n")
                    links = [a.get('href') for a in text_el.find_all('a') if a.get('href')]
                    out.write(f"LINKS FOUND: {links}\n")
                    out.write(f"HAS PHOTO: {photo_el is not None}\n")
                    out.write("--------------------\n")
        except Exception as e:
            out.write(f"Error fetching {ch}: {e}\n")

print("Done writing channel_samples.txt")
