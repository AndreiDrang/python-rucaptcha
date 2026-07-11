# AGENTS.md

## Scope and inheritance

Applies to: `docs/` and its descendants.

Inherits repository-wide guidance from `../AGENTS.md`.

This file defines only local differences for the Sphinx documentation subtree.

## What lives here

```text
docs/
├── conf.py             # Sphinx extensions, autodoc imports, theme, metadata
├── index.rst           # Main toctrees and documentation navigation
├── modules/             # Per-CAPTCHA examples and supporting Markdown/RST
├── _static/             # Images and other published assets
├── requirements.txt     # Documentation-only dependencies
└── Makefile             # Local Sphinx build wrapper
```

## Local boundaries and invariants

- Sphinx configuration imports the package's solver modules directly and uses autodoc; documentation builds therefore depend on importable, current Python modules.
- User-facing solver additions should have a matching example under `docs/modules/` and an entry in the appropriate `index.rst` toctree. Keep example parameter names aligned with the actual solver payload.
- Keep generated `_build/` output out of source edits. Static images belong in `docs/_static/` when they are part of the published docs.

## Validation

From the repository root, run `make doc`; it installs the package and invokes the Sphinx build in `docs/`. For a docs-only iteration, `cd docs && make html -e` uses the local documentation Makefile after its requirements are installed.

## Nearby docs

Read `docs/index.rst` when changing navigation and `docs/conf.py` when changing extensions, autodoc imports, theme settings, or published metadata.
