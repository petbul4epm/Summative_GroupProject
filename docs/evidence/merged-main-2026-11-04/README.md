# Merged-main verification — 4 November 2026

Owner: Petya Markova (`petbul4epm`). Execution: Codex-operated HTTP and Playwright checks on her behalf.
Tested source: `9a988c769a5e181f714e059476a2d58f1759ae76`, after PR #45 merge.

| Check | Actual result |
|---|---|
| `python -m pytest backend/tests -q` | 22 passed; one Starlette/httpx deprecation warning |
| `node --check frontend/script.js` | Passed; Node 24.22.1 |
| [Live HTTP smoke results](api-smoke-results.json) | 11 passed, including actual process restart and SQLite persistence |
| [Firefox browser results](results.json) | 11 passed; Firefox 157.0, Playwright 1.64.1; no page errors |
| Desktop/mobile | 1280×900 and 390×844; no horizontal overflow at 390px |

Python 3.12.14; exact pinned backend dependencies installed from `backend/requirements.txt`. FastAPI 0.143.0, Starlette 1.7.0, Pydantic 2.14.0.
The source files fetched from the tested commit were not modified. The evidence commit changes documentation/evidence only.

## Screenshots

- [Desktop after server restart](desktop-persisted.png)
- [Mobile retained record](mobile-persisted.png)
- [Mobile after deletion](mobile-deleted.png)

Seven earlier team screenshots remain under [integration-testing](../integration-testing/README.md). Their original browser/build metadata is not supplied here.

## Reproduce

Run in a disposable checkout of the tested source using fictional data: the scripts start a real uvicorn process on port 8765 and use the checkout's `backend/edutrack.db`. Start with an empty local database; do not point at shared or production data.

Install the pinned backend requirements and Playwright, then install Playwright Firefox. From the repository root:

```bash
python -m pytest backend/tests -q
node --check frontend/script.js
python docs/evidence/merged-main-2026-11-04/api-smoke.py
MOZ_DISABLE_CONTENT_SANDBOX=1 MOZ_DISABLE_RDD_SANDBOX=1 MOZ_DISABLE_GMP_SANDBOX=1 python docs/evidence/merged-main-2026-11-04/browser-smoke.py
```

The Firefox environment flags were needed in the managed test container after its first page creation crashed; the subsequent complete browser run passed. Chromium downloads were unusable, so no Chromium pass is claimed.

The stored scripts have repository-relative paths for reuse; the executed scratch copies used the equivalent isolated checkout path. Results and PNGs are overwritten when scripts are rerun; retain dated evidence before doing so.

Core integrated CRUD acceptance passed. Known validation and scope follow-ups remain in #49; this is not full US1–US12 acceptance.
