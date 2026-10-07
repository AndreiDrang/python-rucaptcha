---
type: Delivery Workflow
title: Packaging and documentation

description: Setuptools packaging, uv-driven dependency and build workflow, runtime metadata inclusion, and Sphinx publication.
tags: [packaging, sphinx, setuptools, uv, release]
source_paths:
  - pyproject.toml
  - Makefile
  - uv.lock
  - docs/index.rst
  - docs/conf.py
  - .github/workflows/sphinx.yml
  - .github/workflows/build_sphinx.yml
confidence: observed
---

# Packaging and documentation

## Package layout

The project uses setuptools with a `src/` layout, discovers packages matching `python_rucaptcha*`, requires Python 3.9 or newer, and declares HTTP, async HTTP, serialization, and retry dependencies [1]. The package version is loaded dynamically from `python_rucaptcha.__version__` [1].

## Dependency management and build (uv)

Development, test, and documentation dependencies are declared as `dev` and `docs` dependency groups in `pyproject.toml`; the former `requirements.style.txt`, `requirements.test.txt`, and `docs/requirements.txt` files were removed [1]. The `uv.lock` lockfile is committed for reproducible environments [2]. Make targets run through uv: `make install` executes `uv sync --all-groups`, `make build` runs `uv build`, and `make upload` publishes with `uv publish` reading the gitignored `.pypi-token` file [3]. The `docs` group caps Sphinx below 9 because `enum-tools` used by `docs/conf.py` cannot import from Sphinx 9 [1].

## Runtime package data

`pyproject.toml` includes `core/data/*.json` as package data. These files are required by the [CaptchaAI native client](/captchaai-native-client.md) at runtime, so package builds must preserve them [1].

## Sphinx documentation

`docs/index.rst` is the navigation root. It publishes general information pages, a broad set of CAPTCHA examples, CaptchaAI and control examples, and enum/serializer references [4]. `docs/conf.py` enables MyST, Napoleon, enum tooling, and the project theme, and imports solver modules for documentation configuration [5].

## Delivery checks

The Makefile provides the uv-driven build and documentation entry points (`make build`, `make doc`) [3]. CI workflows provision interpreters through `astral-sh/setup-uv` with `uv python install`. The Sphinx workflow runs `make doc` and deploys `docs/_build/html/` to the `gh-pages` branch on release pushes, while the master-branch docs workflow rebuilds documentation as a check [6].

## Relationships

* Validation commands and CI matrices are summarized in [testing and validation](/testing-and-validation.md).
* Public navigation and examples are summarized in [public usage surface](/public-usage-surface.md).
* Runtime profile data is part of the [CaptchaAI native client](/captchaai-native-client.md) contract.

# Citations

[1] `pyproject.toml` — Defines Python support, package discovery, dependencies, dynamic versioning, package data, and uv dependency groups.
[2] `uv.lock` — Locks exact resolved versions for all dependency groups.
[3] `Makefile` — Defines uv-driven install, refactor, lint, build, publish, test, and documentation commands.
[4] `docs/index.rst` — Defines the published Sphinx navigation and example entries.
[5] `docs/conf.py` — Defines Sphinx extensions, theme configuration, and imported package modules.
[6] `.github/workflows/sphinx.yml` and `.github/workflows/build_sphinx.yml` — Define release documentation deployment and master-branch documentation checks with setup-uv.
