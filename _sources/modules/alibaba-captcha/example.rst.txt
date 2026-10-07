Alibaba captcha
================

To import this module:

.. code-block:: python

    from python_rucaptcha.alibaba_captcha import AlibabaCaptcha
    from python_rucaptcha.core.enums import AlibabaEnm


.. autoclass:: python_rucaptcha.alibaba_captcha.AlibabaCaptcha
    :members:

The required ``sceneId`` and ``prefix`` values, together with optional values
such as ``userId``, ``verifyType``, ``region``, and ``userCertifyId``, are
page-specific and should be extracted from the captcha initialization
requests. ``apiGetLib`` may also be generated dynamically.

The result is a JSON string in ``solution.data.tokens``. Parse it with
``json.loads`` before resending the Alibaba verification request.
