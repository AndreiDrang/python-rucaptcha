import asyncio

from src.python_rucaptcha.core.enums import KeyCaptchaEnm
from src.python_rucaptcha.key_captcha import KeyCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad9053f111111111111111fa758570"

s_s_c_user_id = "184015"
s_s_c_session_id = "0917788cad24ad3a69813c4fcd556061"
s_s_c_web_server_sign = "02f7f9669f1269595c4c69bcd4a3c52e"
s_s_c_web_server_sign2 = "d888700f6f324ec0f32b44c32c50bde1"
pageurl = "https://rucaptcha.com/demo/keycaptcha"

key_captcha = KeyCaptcha(
    rucaptcha_key=RUCAPTCHA_KEY,
    pageurl=pageurl,
    s_s_c_user_id=s_s_c_user_id,
    s_s_c_session_id=s_s_c_session_id,
    s_s_c_web_server_sign=s_s_c_web_server_sign,
    s_s_c_web_server_sign2=s_s_c_web_server_sign2,
    method=KeyCaptchaEnm.KEYCAPTCHA.value,
)
result = key_captcha.captcha_handler()

print(result)


async def run():
    try:
        key_captcha = await KeyCaptcha(
            rucaptcha_key=RUCAPTCHA_KEY,
            pageurl=pageurl,
            s_s_c_user_id=s_s_c_user_id,
            s_s_c_session_id=s_s_c_session_id,
            s_s_c_web_server_sign=s_s_c_web_server_sign,
            s_s_c_web_server_sign2=s_s_c_web_server_sign2,
            method=KeyCaptchaEnm.KEYCAPTCHA.value,
        ).aio_captcha_handler()
        print(key_captcha)
    except Exception as err:
        print(err)


asyncio.run(run())
