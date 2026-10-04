import pytest
from app.aliexpress.parser import extract_telegram_html_text, extract_prices, compute_title_compatibility
from app.aliexpress.product import product_extractor
from bs4 import BeautifulSoup

def test_extract_telegram_html_text_preserves_numbers_and_codes():
    html_raw = """<blockquote>⚡️<b>ألحـــــــــــــــق</b>🚨</blockquote><br/>
⭐️ <b>ATTACK SHARK G300</b><br/><br/>
💵 االسعر  : 1<b>1.7<i class="emoji"><b>💲</b></i><i class="emoji"><b>🔥</b></i></b><br/><br/>
🎟️ كوبـــون 2/15$ : <br/><br/>
👊كوبون 2$:  O<code>TPRD02 </code><br/><br/>
🔗 رابــط  :  <a href="https://s.click.aliexpress.com/e/_c2JpSWfB">https://s.click.aliexpress.com/e/_c2JpSWfB</a><br/>
🔗 مباشر : <a href="https://s.click.aliexpress.com/e/_c3ar3tq9">https://s.click.aliexpress.com/e/_c3ar3tq9</a>"""

    soup = BeautifulSoup(html_raw, "html.parser")
    clean_text = extract_telegram_html_text(soup)

    # Must preserve 11.7 contiguous and OTPRD02 contiguous
    assert "11.7" in clean_text
    assert "OTPRD02" in clean_text

    usd, eur = extract_prices(clean_text)
    assert usd == 11.7
    # Must NOT be 1.7
    assert usd != 1.7

def test_title_compatibility_detects_mismatch():
    post_title = "ATTACK SHARK G300"
    mismatched_api_title = "[World Premiere] POCO X8 5G Smartphone Global Version 8340mAh"
    matching_api_title = "ATTACK SHARK G300 Foldable Wireless Gaming Headset, Active Noise Reduction"

    score_mismatch = compute_title_compatibility(post_title, mismatched_api_title)
    score_match = compute_title_compatibility(post_title, matching_api_title)

    assert score_mismatch == 0.0
    assert score_match >= 0.5

@pytest.mark.asyncio
async def test_multi_link_prefers_matching_product():
    # Message with 2 links: link 1 is wrong phone, link 2 is correct headset
    msg_text = """⭐️ ATTACK SHARK G300
💵 االسعر : 11.7💲🔥
🎟️ كوبون : OTPRD02
🔗 رابط : https://s.click.aliexpress.com/e/_c2JpSWfB
🔗 مباشر : https://s.click.aliexpress.com/e/_c3ar3tq9"""

    extracted = await product_extractor.extract_from_message(msg_text)
    assert extracted is not None
    # Must select the headset product ID (1005008390562391), NOT POCO phone (1005013152491360)
    assert extracted.product_id == "1005008390562391"
    assert extracted.current_price == 11.7
