Imperva (Incapsula)
====================

To import this module:

.. code-block:: python

    from python_rucaptcha.incapsula_captcha import IncapsulaCaptcha
    from python_rucaptcha.core.enums import IncapsulaEnm


.. autoclass:: python_rucaptcha.incapsula_captcha.IncapsulaCaptcha
    :members:

Provide the Incapsula script resource and cookies captured from the challenge
page. The optional ``reese84UrlEndpoint`` is the endpoint used to submit the
Reese84 fingerprint. Keep the same proxy session while solving and using the
returned cookies.

Cookies are returned under ``solution.domains[domain].cookies``. Reuse any
User-Agent included in the solution headers when making the target request.
