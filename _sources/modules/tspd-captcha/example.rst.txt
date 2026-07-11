TSPD
====

To import this module:

.. code-block:: python

    from python_rucaptcha.tspd_captcha import TSPDCaptcha


.. autoclass:: python_rucaptcha.tspd_captcha.TSPDCaptcha
    :members:

Usage notes
-----------

TSPD requires a static proxy session. Obtain the challenge HTML and cookies
through that proxy immediately before creating the task, then keep the same
outbound IP when applying the returned cookies.

``htmlPageBase64`` must contain the complete challenge HTML encoded as Base64.
The solution cookies are returned under ``solution.Domains`` and
``solution.Domains[domain].Cookies``.
