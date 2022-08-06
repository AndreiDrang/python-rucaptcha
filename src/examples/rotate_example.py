from src.python_rucaptcha.enums import RotateCaptchaEnm
from src.python_rucaptcha.RotateCaptcha import RotateCaptcha

# Rucaptcha API Key from your account
RUCAPTCHA_KEY = "ad911111111111ca81755768608fa758570"


rotate_captcha = RotateCaptcha(rucaptcha_key=RUCAPTCHA_KEY, method=RotateCaptchaEnm.ROTATECAPTCHA.value)
# file URL
result = rotate_captcha.captcha_handler(
    captcha_link="https://rucaptcha.com/dist/web/b771cc7c5eb0c1a811fcb91d54e4443a.png"
)

print(result)

# file path
result = rotate_captcha.captcha_handler(captcha_link="src/examples/rotate/rotate_ex.png")

print(result)
