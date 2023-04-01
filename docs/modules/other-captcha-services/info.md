# Death By Captcha and other services

Using Death By Captcha and other services is possible by changing "service_type" and "url_request"\"url_response" parameters.


## Death By Captcha:
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
