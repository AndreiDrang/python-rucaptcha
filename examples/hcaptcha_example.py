import asyncio

from python_rucaptcha.HCaptcha import HCaptcha, aioHCaptcha

"""
HCaptcha docs - https://rucaptcha.com/api-rucaptcha#solving_hcaptcha
"""

RUCAPTCHA_KEY = "3ca91ab80ece74da44cfb7eec27493ed"
"""
website_link - The full URL of the page where you decide hCaptcha
data_sitekey - The value of the data-sitekey parameter that you found in the page code
"""
website_link = "https://secure2.e-konsulat.gov.pl/Uslugi/RejestracjaTerminu.aspx?IDUSLUGI=1&IDPlacowki=94"
data_sitekey = "39fccce0-e3e3-4f9d-a942-ea415c102beb"

# Sync example
client = HCaptcha(rucaptcha_key=RUCAPTCHA_KEY)

result = client.captcha_handler(site_key=data_sitekey, page_url=website_link)

print(result)

# Sync example with contextmanager
with HCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as h_captcha:
    result = h_captcha.captcha_handler(site_key=data_sitekey, page_url=website_link)
    print(result)

# Async example
async def aioexample():
    # with contextmanager
    with aioHCaptcha(rucaptcha_key=RUCAPTCHA_KEY) as h_captcha:
        result = await h_captcha.captcha_handler(
            site_key=data_sitekey, page_url=website_link
        )
        print(result)

    # without contextmanager
    client = aioHCaptcha(rucaptcha_key=RUCAPTCHA_KEY)
    result = await client.captcha_handler(site_key=data_sitekey, page_url=website_link)
    print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(aioexample())
loop.close()
