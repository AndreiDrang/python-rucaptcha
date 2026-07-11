---
type: Delivery Workflow
title: Packaging and documentation

description: Setuptools packaging, runtime metadata inclusion, and Sphinx publication workflow.
tags: [packaging, sphinx, setuptools, release]
source_paths:
  - pyproject.toml
  - Makefile
  - docs/index.rst
  - docs/conf.py
  - .github/workflows/sphinx.yml
confidence: observed
---

# Packaging and documentation

## Package layout

The project uses setuptools with a `src/` layout, discovers packages matching `python_rucaptcha*`, requires Python 3.9 or newer, and declares HTTP, async HTTP, serialization, and retry dependencies [1]. The package version is loaded dynamically from `python_rucaptcha.__version__` [1].

## Runtime package data

`pyproject.toml` includes `core/data/*.json` as package data. These files are required by the [CaptchaAI native client](/captchaai-native-client.md) at runtime, so package builds must preserve them [1].

## Sphinx documentation

`docs/index.rst` is the navigation root. It publishes general information pages, a broad set of CAPTCHA examples, CaptchaAI and control examples, and enum/serializer references [2]. `docs/conf.py` enables MyST, Napoleon, enum tooling, and the project theme, and imports solver modules for documentation configuration [3].

## Delivery checks

The Makefile provides the local build and documentation entry points [4]. The Sphinx workflow installs documentation requirements, runs `make doc`, and deploys `docs/_build/html/` to the `gh-pages` branch on release pushes [5].

## Relationships

* Validation commands and CI matrices are summarized in [testing and validation](/testing-and-validation.md).
* Public navigation and examples are summarized in [public usage surface](/public-usage-surface.md).
* Runtime profile data is part of the [CaptchaAI native client](/captchaai-native-client.md) contract.

# Citations

[1] `pyproject.toml` — Defines Python support, package discovery, dependencies, dynamic versioning, and package data.
[2] `docs/index.rst` — Defines the published Sphinx navigation and example entries.
[3] `docs/conf.py` — Defines Sphinx extensions, theme configuration, and imported package modules.
[4] `Makefile` — Defines build and documentation commands.
[5] `.github/workflows/sphinx.yml` — Defines the release documentation build and deployment workflow.
