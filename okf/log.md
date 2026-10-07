# Knowledge Bundle Update Log

## 2026-07-12

* **Initialization**: Created an OKF v0.1 knowledge bundle for the repository root.
* **Creation**: Added concept documents for the architecture, solver adapters, request lifecycle, service contracts, CaptchaAI client, public usage surface, testing, and packaging/documentation.
* **Conflict**: The README contains examples importing solver classes from `python_rucaptcha`, while `src/python_rucaptcha/__init__.py` currently imports only `__version__`; this discrepancy is recorded in [Public usage surface](/public-usage-surface.md).

## 2026-10-07

* **Update**: Refreshed [packaging and documentation](/packaging-and-documentation.md) for the uv migration — dependency groups replace the requirements files, `uv.lock` is committed, and make/CI build steps run through uv.
* **Update**: Adjusted [testing and validation](/testing-and-validation.md) local-command descriptions and CI provisioning notes for uv.
* **Update**: Adjusted [public usage surface](/public-usage-surface.md) for the README install variants (pip and uv, plus the local development sync) and refreshed the bundle index description.
