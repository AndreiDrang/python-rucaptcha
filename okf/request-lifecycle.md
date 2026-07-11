---
type: Request Workflow
title: CAPTCHA request lifecycle
description: The common lifecycle from task construction through provider polling and normalized output.
tags: [workflow, polling, retries, http]
source_paths:
  - src/python_rucaptcha/core/base.py
  - src/python_rucaptcha/core/result_handler.py
  - src/python_rucaptcha/core/config.py
  - src/python_rucaptcha/core/serializer.py
confidence: observed
---

# CAPTCHA request lifecycle

## Standard task flow

1. A caller constructs a concrete adapter and invokes `captcha_handler()` or `aio_captcha_handler()` [1].
2. `BaseCaptcha` creates a `clientKey` plus typed task envelope, selects provider URLs, and adds adapter-supplied fields [1][2].
3. The sync or async path submits the create-task request and stores the returned task ID [1].
4. The result handler polls the result endpoint until it receives `processing`, `ready`, or an error response [3].
5. The response serializer converts the final result into a dictionary containing status, solution, task metadata, or error fields [2][3].

## Timing and retry behavior

HTTP sessions use a requests retry policy with five total retries, while async submission and URL reads use a tenacity policy with five attempts and fixed waits [4]. Result polling uses `attempts_generator()` with a default range of 19 attempts and sleeps between processing responses using the caller's `sleep_time` [3][4].

The lifecycle is bounded: an exhausted polling generator returns the latest normalized response rather than looping indefinitely [3]. Transport exceptions are represented as failed responses with error information [1][3].

## Optional file path

Image-oriented adapters may first read a local file, encode bytes, or fetch a URL and encode its content before task submission [1]. This is request preparation, not persistent application storage.

## Async parity

The async flow mirrors the sync flow: it submits through `aiohttp`, waits asynchronously, and calls the async result handler with the same task payload and result model [1][3].

## Relationships

* Provider URL and response fields are defined in [Service contracts](/service-contracts.md).
* Leaf payload preparation is owned by [standard solver adapters](/standard-solver-adapters.md).
* The separate CaptchaAI lifecycle is documented in [CaptchaAI native client](/captchaai-native-client.md).

# Citations

[1] `src/python_rucaptcha/core/base.py` — Implements task construction, sync/async submission, file preparation, and error mapping.
[2] `src/python_rucaptcha/core/serializer.py` — Defines request and response models plus dictionary conversion.
[3] `src/python_rucaptcha/core/result_handler.py` — Implements sync/async polling states and bounded result retrieval.
[4] `src/python_rucaptcha/core/config.py` — Defines request retry policies and the polling attempt generator.
