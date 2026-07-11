Basilisk captcha
=================

To import this module:

.. code-block:: python

    from python_rucaptcha.basilisk_captcha import BasiliskCaptcha
    from python_rucaptcha.core.enums import BasiliskEnm


.. autoclass:: python_rucaptcha.basilisk_captcha.BasiliskCaptcha
    :members:

The proxyless task requires ``websiteURL`` and ``websiteKey``. Use
``BasiliskEnm.BasiliskTask`` when the solve must use your own proxy and provide
``proxyType``, ``proxyAddress``, and ``proxyPort``.

The token is returned as ``solution.data.captcha_response``. If the response
contains ``solution.headers.User-Agent``, reuse that User-Agent in the request
to the target site.
