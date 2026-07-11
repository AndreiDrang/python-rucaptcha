# Architecture

## 1. High-Level Overview

`python-rucaptcha` is a Python 3.9+ library that adapts multiple CAPTCHA-solving task types to the 2Captcha, RuCaptcha, DeathByCaptcha, and CaptchaAI service APIs. Its source is a `src/`-layout setuptools package (`pyproject.toml`) with synchronous and asyncio entry points, rather than a standalone server, worker, or command-line application. The user-facing purpose and supported providers are stated in `README.md` and `docs/index.rst`.

The primary architecture is a family of thin, flat solver adapters over a shared task engine. A concrete solver prepares provider task fields and delegates request creation, polling, retries, serialization, and response normalization to `src/python_rucaptcha/core/`. CaptchaAI is a deliberate second path: `src/python_rucaptcha/captchaai.py` and `src/python_rucaptcha/core/captchaai.py` submit its classic multipart protocol using packaged JSON profiles. External service calls are the system boundary; no database or long-running application runtime is defined in the repository. The executable package boundary is module-based: `src/python_rucaptcha/__init__.py` currently imports only the version, despite some root-level import examples in `README.md`.

## 2. System Architecture (Logical)

Dependency direction:

```text
Library caller
    ├──> flat solver adapters ──> shared task engine ──> provider task APIs
    └──> CaptchaAI native client ──> CaptchaAI classic multipart API
Tests / Sphinx / build checks ──> package source and packaging metadata
```

### Public solver adapters

- Responsibility: Expose one adapter per supported CAPTCHA or control operation, validate task-method choices, add task-specific fields, and provide sync/async handlers.
- Code locations: `src/python_rucaptcha/*_captcha.py`, `src/python_rucaptcha/control.py`.
- Entry points: Concrete `captcha_handler` and `aio_captcha_handler` methods; representative implementations are `src/python_rucaptcha/hcaptcha.py` and `src/python_rucaptcha/image_captcha.py`.
- Depends on: `core.base.BaseCaptcha` and the relevant enum in `core.enums`.
- Must not depend on: Provider-specific transport implementations in leaf modules; shared HTTP and polling behavior belongs in `core/`.
- Owns: CAPTCHA-specific task names, task fields, validation, and input-shaping decisions such as image/file handling.
- State and external boundaries: Holds an in-memory task payload and delegates all provider HTTP calls to the shared core.
- Evidence: `src/python_rucaptcha/hcaptcha.py`, `src/python_rucaptcha/image_captcha.py`, `src/python_rucaptcha/AGENTS.md`.

### Shared task engine and contracts

- Responsibility: Build create-task and result payloads, select service URLs, execute sync/async HTTP requests, retry connections, poll task results, and normalize errors/results.
- Code locations: `src/python_rucaptcha/core/base.py`, `src/python_rucaptcha/core/result_handler.py`, `src/python_rucaptcha/core/config.py`.
- Entry points: `BaseCaptcha._processing_response`, `BaseCaptcha._aio_processing_response`, `get_sync_result`, and `get_async_result`.
- Depends on: `requests`, `aiohttp`, `tenacity`, and the serializer/enums in `core/`.
- Must not depend on: Individual CAPTCHA modules for task-specific behavior; the base flow accepts generic task data and the leaf adapter supplies its fields.
- Owns: Shared task lifecycle, request sessions, retry/poll timing, task IDs, and common failure mapping.
- State and external boundaries: Keeps request state in Python objects; crosses HTTP boundaries to JSON task APIs, classic CaptchaAI delegation, and optional source-image URLs.
- Evidence: `src/python_rucaptcha/core/base.py`, `src/python_rucaptcha/core/result_handler.py`, `src/python_rucaptcha/core/config.py`.

### Serialization and service contract layer

- Responsibility: Define the structured request/response shapes, serialized field names, service selection, and task-method enums used by adapters and transport.
- Code locations: `src/python_rucaptcha/core/serializer.py`, `src/python_rucaptcha/core/enums.py`.
- Entry points: `MyBaseModel.to_dict()` and `CaptchaOptionsSer.urls_set()`.
- Depends on: `msgspec` and the shared service enum values.
- Must not depend on: Concrete solver modules; contract types are consumed by them rather than encoding their individual payload rules.
- Owns: `TaskSer`, create-task/result models, service endpoint selection, and the canonical enum vocabulary.
- State and external boundaries: Produces dictionaries consumed by remote APIs; it does not persist data or perform network I/O.
- Evidence: `src/python_rucaptcha/core/serializer.py`, `src/python_rucaptcha/core/enums.py`, `pyproject.toml`.

### CaptchaAI native and compatibility path

- Responsibility: Support CaptchaAI’s classic `in.php`/`res.php` multipart protocol, including native methods, optional profile validation, control operations, legacy task translation, and sync/async polling.
- Code locations: `src/python_rucaptcha/captchaai.py`, `src/python_rucaptcha/core/captchaai.py`, `src/python_rucaptcha/core/data/captchaai_profiles.json`, `src/python_rucaptcha/core/data/captchaai_legacy_profiles.json`.
- Entry points: `CaptchaAI.captcha_handler`, `CaptchaAI.aio_captcha_handler`, and the corresponding native transport functions in `core/captchaai.py`.
- Depends on: `core.serializer.GetTaskResultResponseSer`, `core.config.attempts_generator`, and packaged profile metadata; direct `CaptchaAI` does not inherit `BaseCaptcha`.
- Must not depend on: Per-method branches in Python transport code; documented method behavior is represented in profile data. Legacy generic tasks may delegate into this path through the explicit CaptchaAI service branch in `core/base.py`.
- Owns: Provider-native multipart fields, profile defaults/validation, response aliases, and CaptchaAI control-operation mappings.
- State and external boundaries: Uses in-memory mappings and packaged JSON metadata, then crosses CaptchaAI submission and polling endpoints.
- Evidence: `src/python_rucaptcha/captchaai.py`, `src/python_rucaptcha/core/captchaai.py`, `src/python_rucaptcha/core/data/`, `src/python_rucaptcha/core/AGENTS.md`.

## 3. Code Map (Physical)

```text
.
├── src/python_rucaptcha/
│   ├── *_captcha.py, re_captcha.py, hcaptcha.py, ...  # concrete solver adapters
│   ├── captchaai.py                                   # native CaptchaAI client
│   ├── control.py                                     # balance/report-style operations
│   └── core/
│       ├── base.py, result_handler.py, config.py      # shared lifecycle and polling
│       ├── serializer.py, enums.py                    # wire models and vocabulary
│       └── captchaai.py, data/*.json                  # native transport and profiles
├── tests/
│   ├── conftest.py                                    # credential-dependent fixtures
│   ├── test_core.py                                   # shared foundation checks
│   └── test_by_solver.py                              # solver-oriented coverage
├── docs/
│   ├── index.rst, conf.py                             # Sphinx navigation and imports
│   └── modules/                                       # user-facing solver examples
├── pyproject.toml, Makefile                           # package, format, test, build, docs tasks
└── .github/workflows/                                 # install, lint, test, build, and docs CI
```

## 4. Life of a Request / Primary Data Flow

### Standard solver task

1. Trigger: A library caller constructs a concrete adapter and invokes its synchronous or asynchronous handler.
2. Entry point: A leaf method such as `HCaptcha.captcha_handler` / `aio_captcha_handler` in `src/python_rucaptcha/hcaptcha.py`.
3. Coordination: `BaseCaptcha` builds the generic create-task envelope and selects endpoints through `CaptchaOptionsSer.urls_set()`.
4. Core or domain processing: The leaf adapter has already supplied its method-specific task fields; `BaseCaptcha` submits the task and records the returned task ID.
5. Persistence or external interaction: The shared engine polls `getTaskResult` (or the DeathByCaptcha-compatible classic endpoints) through `get_sync_result` or `get_async_result`, with retry and delay settings from `core/config.py`.
6. Output or side effect: `GetTaskResultResponseSer.to_dict()` returns a normalized ready/error mapping to the caller; image adapters may also read a local file or fetch and optionally save a source image.

Architectural boundaries crossed:
- Caller API → concrete solver adapter → shared core → remote provider HTTP API.
- Optional local filesystem or source-image URL → encoded task payload.

Evidence:
- `src/python_rucaptcha/hcaptcha.py`
- `src/python_rucaptcha/core/base.py`
- `src/python_rucaptcha/core/result_handler.py`
- `src/python_rucaptcha/core/serializer.py`

### CaptchaAI native task

1. Trigger: A caller constructs `CaptchaAI` with a provider-native method or a packaged profile and invokes `captcha_handler` or `aio_captcha_handler`.
2. Entry point: `src/python_rucaptcha/captchaai.py` delegates to `solve_native` or `aio_solve_native` in `src/python_rucaptcha/core/captchaai.py`.
3. Coordination: Profile metadata supplies defaults, required fields, file-field rules, aliases, and polling behavior; unprofiled calls pass provider-native parameters through validation.
4. Core or domain processing: The native transport builds multipart form fields, submits `in.php`/profile-specific paths, and interprets the provider’s response contract.
5. Persistence or external interaction: The transport optionally polls `res.php` using the provider task ID; binary parts remain request-local and profile JSON is read from the installed package.
6. Output or side effect: The transport maps provider success/error values into the common result shape, or returns a control-operation response.

Architectural boundaries crossed:
- Caller → native CaptchaAI façade → data-driven transport → CaptchaAI classic HTTP API.
- Installed package metadata → request validation and response aliasing.

Evidence:
- `src/python_rucaptcha/captchaai.py`
- `src/python_rucaptcha/core/captchaai.py`
- `src/python_rucaptcha/core/data/captchaai_profiles.json`

## 5. Architectural Invariants & Constraints

### 1. Leaf adapters own provider task semantics

- Rule: CAPTCHA-specific method names, fields, validation, and input preparation stay in the concrete modules; shared core code remains generic.
- Rationale: One transport/polling implementation can serve the flat family of solver adapters without accumulating solver-specific branches.
- Enforcement / Signals: Import direction and repeated inheritance in `src/python_rucaptcha/*.py`; explicitly documented in `src/python_rucaptcha/AGENTS.md` and `src/python_rucaptcha/core/AGENTS.md`.

### 2. Sync and async paths have parallel task semantics

- Rule: A solver that exposes both modes must use the same task contract and normalized response shape while selecting blocking or asyncio I/O.
- Rationale: Consumers can change execution model without changing provider task meaning.
- Enforcement / Signals: Paired handlers in `src/python_rucaptcha/hcaptcha.py`, paired core processing methods in `src/python_rucaptcha/core/base.py`, and sync/async result handlers in `src/python_rucaptcha/core/result_handler.py`.

### 3. Service endpoint selection is centralized

- Rule: Service names and endpoint selection flow through `ServiceEnm` and `CaptchaOptionsSer.urls_set()` rather than being reimplemented by each solver.
- Rationale: 2Captcha/RuCaptcha JSON APIs, DeathByCaptcha-compatible URLs, and CaptchaAI classic URLs have distinct wire boundaries.
- Enforcement / Signals: `src/python_rucaptcha/core/enums.py` and `src/python_rucaptcha/core/serializer.py`; `BaseCaptcha` calls `urls_set()` during initialization.

### 4. Shared responses are normalized at the core boundary

- Rule: Generic task creation/results and transport failures use `GetTaskResultResponseSer` and its `to_dict()` representation.
- Rationale: Different adapters and services present one stable library-facing result contract.
- Enforcement / Signals: `src/python_rucaptcha/core/serializer.py`, `src/python_rucaptcha/core/base.py`, and `src/python_rucaptcha/core/result_handler.py` construct or return the serializer.

### 5. Polling and connection retries are bounded and configurable

- Rule: Remote submission and result retrieval use the configured retry policies, polling attempt generator, and caller-visible sleep interval.
- Rationale: The library is a client of asynchronous human-solving services and must tolerate delayed results without an unbounded local loop.
- Enforcement / Signals: `RETRIES`, `ASYNC_RETRIES`, and `attempts_generator()` in `src/python_rucaptcha/core/config.py`; polling loops in `src/python_rucaptcha/core/result_handler.py` and `src/python_rucaptcha/core/captchaai.py`.

### 6. CaptchaAI’s native path remains data-driven and separate

- Rule: Direct CaptchaAI calls use `CaptchaAI` plus packaged profiles; new provider methods must not require per-method branches in the native transport or conversion into `BaseCaptcha`.
- Rationale: CaptchaAI’s classic multipart contract differs from the generic JSON task API and is intentionally extensible through metadata.
- Enforcement / Signals: Separate façade/transport modules, profile lookups in `src/python_rucaptcha/core/captchaai.py`, packaged data declaration in `pyproject.toml`, and local guidance in `src/python_rucaptcha/core/AGENTS.md`.

### 7. Runtime profile metadata is part of the package contract

- Rule: Both CaptchaAI profile JSON files must ship with the installed wheel when the native path is used.
- Rationale: Profile validation, compatibility translation, and control mappings load these files at runtime.
- Enforcement / Signals: `tool.setuptools.package-data` in `pyproject.toml`, file reads in `src/python_rucaptcha/core/captchaai.py`, and the files under `src/python_rucaptcha/core/data/`.

### 8. The repository has no internal persistence or service runtime

- Rule: Task state is request-local/in-memory, with optional local image files; solving state and results remain on the external provider APIs.
- Rationale: The package is an SDK boundary for consumer applications, not a server or worker owning a task database.
- Enforcement / Signals: Runtime dependencies and source layout contain HTTP clients but no database, web-server, queue, or worker framework; `src/python_rucaptcha/core/base.py` stores payloads and task IDs on instances.

## 6. Documentation Strategy

`ARCHITECTURE.md` owns the global architecture map, dependency direction, representative flows, and durable invariants. It should remain a navigation document rather than an API reference, usage tutorial, deployment runbook, or per-solver catalog.

- `AGENTS.md` defines repository-wide contribution and context-routing rules; child `AGENTS.md` files refine those rules for `src/python_rucaptcha/`, `core/`, `tests/`, and `docs/`.
- `README.md` owns the public overview, installation/usage examples, supported services, and high-level feature claims.
- `docs/index.rst`, `docs/conf.py`, and `docs/modules/` own the Sphinx navigation, autodoc configuration, and per-CAPTCHA examples.
- `okf/` contains the project-local OKF v0.1 knowledge bundle: concept-oriented architecture and operational knowledge, stable cross-links, update history, and citation-backed repository evidence. It complements this document and should not duplicate the global architecture map.
- `tests/AGENTS.md` and the test modules define test-fixture and validation conventions; they are evidence for behavior, not replacements for this architecture map.
- Provider API contracts remain external service documentation; repository schemas are represented by `src/python_rucaptcha/core/serializer.py` and the packaged CaptchaAI profile data.
- No repository-local ADR, runbook, or `DESIGN.md` is present in the active tracked layout; if such documents are added, they should own decisions, operations, or visual design rather than duplicating this map.
