# Automated test results

Run date: 9 October 2026. Environment: Python 3.12, Linux, FastAPI TestClient, temporary SQLite database. Command: python -m pytest -q. Result: 9 passed. Covers CRUD, validation, missing-record handling, data persistence through schema reinitialisation, literal HTML-like text storage, frontend serving and Swagger/OpenAPI routes. JavaScript syntax check: node --check frontend/script.js passed.

One dependency deprecation warning from Starlette TestClient/httpx was observed; it did not fail tests. Browser rendering, keyboard/screen-reader use and usability testing have not been performed. Complete the manual test plan with actual evidence before your final submission.
