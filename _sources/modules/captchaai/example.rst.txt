CaptchaAI
=========

CaptchaAI uses a classic multipart ``in.php`` / ``res.php`` API. Existing
high-level solvers can use ``service_type=ServiceEnm.CAPTCHAAI`` where a
compatibility profile is available. For every documented CaptchaAI method, use
the native client with provider field names.

Documented profile
------------------

A profile validates the documented required fields and supplies documented
defaults. The profile list is available through ``CaptchaAI.profiles()``.

.. code-block:: python

   from python_rucaptcha.captchaai import CaptchaAI

   result = CaptchaAI(
       rucaptcha_key="CAPTCHAAI_KEY",
       profile="cloudflare-challenge",
       params={
           "pageurl": "https://example.com/protected",
           "proxy": "user:pass@203.0.113.7:3128",
           "proxytype": "HTTPS",
       },
   ).captcha_handler()

Future provider methods
-----------------------

The client does not restrict the native ``method`` string. A newly released
CaptchaAI classic API method can be used before this package adds a profile.

.. code-block:: python

   from python_rucaptcha.captchaai import CaptchaAI

   result = CaptchaAI(
       rucaptcha_key="CAPTCHAAI_KEY",
       method="provider_future_method",
       params={"provider_field": "value"},
   ).captcha_handler()

File uploads and controls
-------------------------

Use ``CaptchaAIFile`` for API methods that require a real multipart file part,
such as Normal or Grid image CAPTCHA requests.

.. code-block:: python

   from python_rucaptcha.captchaai import CaptchaAI, CaptchaAIFile

   result = CaptchaAI(
       rucaptcha_key="CAPTCHAAI_KEY",
       profile="normal-solve-file",
       files={"file": CaptchaAIFile(b"... image bytes ...", "captcha.png", "image/png")},
   ).captcha_handler()

   client = CaptchaAI(rucaptcha_key="CAPTCHAAI_KEY", profile="turnstile", params={
       "sitekey": "SITE_KEY",
       "pageurl": "https://example.com",
   })
   balance = client.get_balance()
   threads = client.get_threads_info()
