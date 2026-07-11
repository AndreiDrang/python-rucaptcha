# Knowledge Bundle Update Log

## 2026-07-12

* **Initialization**: Created an OKF v0.1 knowledge bundle for the repository root.
* **Creation**: Added concept documents for the architecture, solver adapters, request lifecycle, service contracts, CaptchaAI client, public usage surface, testing, and packaging/documentation.
* **Conflict**: The README contains examples importing solver classes from `python_rucaptcha`, while `src/python_rucaptcha/__init__.py` currently imports only `__version__`; this discrepancy is recorded in [Public usage surface](/public-usage-surface.md).
