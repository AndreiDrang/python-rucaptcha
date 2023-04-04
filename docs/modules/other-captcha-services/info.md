# DeathByCaptcha and other services

Using [Death By Captcha](https://deathbycaptcha.com?refid=1237267242) and other services is possible by changing "service_type" and "url_request"\"url_response" parameters.

More info about [Death By Captcha](https://deathbycaptcha.com?refid=1237267242) integration u can find in [service docs](https://deathbycaptcha.com/api/2captcha?refid=1237267242).


## DeathByCaptcha:
```python

from python_rucaptcha.control import Control
from python_rucaptcha.core.enums import ControlEnm, ServiceEnm

serv_username= 'your.username'
serv_password = 'your.passwordQq11'
deathbycaptcha_api_key = f"{serv_username}:{serv_password}"

result = Control(rucaptcha_key=deathbycaptcha_api_key,
                service_type=ServiceEnm.DEATHBYCAPTCHA,
                action=ControlEnm.GETBALANCE.value).additional_methods()
```

```python

from python_rucaptcha.control import Control
from python_rucaptcha.core.enums import ControlEnm, ServiceEnm

serv_username= 'your.username'
serv_password = 'your.passwordQq11'
deathbycaptcha_api_key = f"{serv_username}:{serv_password}"

result = Control(rucaptcha_key=deathbycaptcha_api_key,
                service_type=ServiceEnm.DEATHBYCAPTCHA,
                url_request='http://api.deathbycaptcha.com/2captcha/in.php',
                url_response='http://api.deathbycaptcha.com/2captcha/res.php',
                action=ControlEnm.GETBALANCE.value).additional_methods()
```

```python

from python_rucaptcha.re_captcha import ReCaptcha, ReCaptchaEnm

serv_username= 'your.username'
serv_password = 'your.passwordQq11'
deathbycaptcha_api_key = f"{serv_username}:{serv_password}"

result = ReCaptcha(rucaptcha_key=deathbycaptcha_api_key,
                 service_type="deathbycaptcha",
                 pageurl="https://rucaptcha.com/demo/recaptcha-v2",
                 googlekey="6LeIxboZAAAAAFQy7d8GPzgRZu2bV0GwKS8ue_cH",
                 method=ReCaptchaEnm.USER_RECAPTCHA.value
                 ).captcha_handler()
```

```python

from python_rucaptcha.hcaptcha import HCaptcha, HCaptchaEnm

serv_username= 'your.username'
serv_password = 'your.passwordQq11'
deathbycaptcha_api_key = f"{serv_username}:{serv_password}"

result = HCaptcha(rucaptcha_key=deathbycaptcha_api_key,
                  service_type="deathbycaptcha",
                  sitekey="3ceb8624-1970-4e6b-91d5-70317b70b651",
                  pageurl="https://rucaptcha.com/demo/hcaptcha",
                  method=HCaptchaEnm.HCAPTCHA.value
                 ).captcha_handler()
```

And etc, more info in [service docs](https://deathbycaptcha.com/api/2captcha?refid=1237267242).

## Or you can use other service which support RuCaptcha\2Captcha API-like requests 
```python

from python_rucaptcha.control import Control
from python_rucaptcha.core.enums import ControlEnm

result = Control(rucaptcha_key="someotherapikey",
                service_type='SomeOtherGoodService',
                url_request='http://some-good-server.com/in.php',
                url_response='http://some-good-server.com/res.php',
                action=ControlEnm.GETBALANCE.value).additional_methods()
```
