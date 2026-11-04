# EduTrack integration QA record

Recorded: 22 October 2026  
Owner and manual tester: Petya Markova (`petbul4epm`)  
Branch: `petya/frontend-integration-qa`  
Code revision before this record: `43b036f913e428b5a8e94f436c4297a6e2fd34e4`

## Changes under test

- FastAPI serves the dashboard and its CSS/JavaScript at `/app/`.
- Frontend requests reach the API on the same origin.
- DELETE HTTP 204 is handled without JSON parsing.
- Creation starts pending; status is editable after creation.
- Optional null fields are handled when opening an assignment for editing.
- Existing responsive stylesheet is retained.

This branch starts at PR #44 head `e61e7e473c3e001ef69bea05d60b40b5c8ad83a5`, retaining Sergiu's validation models, tests and API documentation. PR #44 is independently approved; its changes are included in this branch until that PR is merged.

## Automated checks

| Check | Expected | Observed | Evidence |
|---|---|---|---|
| Database, API and frontend-serving tests | All tests pass | 22 passed, 0 failed; one Starlette/httpx deprecation warning | Local execution of `python -m pytest backend/tests -q` on the delivered code |
| JavaScript syntax | No syntax error | Passed | `node --check frontend/script.js` |
| Focused frontend response handling | 204 skips JSON; GET returns records; validation errors remain readable | Passed | Local Node VM checks of the frontend API function |

Environment: Python 3.12, FastAPI 0.143.0, Starlette 1.7.0, Pydantic 2.14.0. Automated execution was assistant-operated; it is separate from the manual testing below. Raw screenshots or test-output attachments are not supplied in this record.

## Manual browser test

Petya explicitly reported that browser testing worked and later confirmed tests complete in the project conversation. Record this as **PASS — reported by Petya**, not an independently executed assistant browser pass.

The precise browser version, tested commit, step-by-step actual results and screenshots were not supplied. This record does not invent them or claim that every proposed edge case passed.

## Remaining acceptance

- [x] Team reviews and merges the integration pull request — see 4 November addendum.
- [x] Run a brief add/edit/complete/delete check on the merged `main` commit and record that commit — see 4 November addendum.
- [x] Attach retained screenshots and detailed test results — see 4 November evidence; earlier manual-run metadata remains unknown.
- [x] Update user-story traceability in #36 — closed 29 October; remaining documented decisions tracked in #49.

Historical acceptance condition: issues #34 and #35 remain open until merged integration is confirmed. See the dated addendum below for the completed verification. This document replaces the placeholder QA description in #38 with the available verified and user-reported evidence.

## Post-merge verification — 4 November 2026

**Core integration acceptance: PASS** on merged `main` commit `9a988c769a5e181f714e059476a2d58f1759ae76`.

Executed by Codex on behalf of Petya Markova through authenticated GitHub account `petbul4epm`. These are newly executed assistant-operated checks, separate from Petya's earlier reported manual pass.

- PR #45 received backend approval from `dataconex94-collab` on 25 October and is merged at `92108de1faed8065b99214ed99a59a1a1f98d5e0`.
- The tested merged-main source was retrieved at the exact SHA above; backend and frontend source were unchanged during verification. Dependencies were installed from `backend/requirements.txt` in an isolated Python 3.12.14 environment.
- Automated suite: **22 passed, 0 failed, 1 Starlette/httpx deprecation warning**. `node --check frontend/script.js`: **PASS** (Node 24.22.1).
- Real FastAPI HTTP checks: **11 passed**, including CRUD, null optional fields, HTTP 201/200/204/404, retained edits/completion across process restart, and retained deletion across restart.
- Playwright 1.64.1, headless **Firefox 157.0**, desktop 1280×900 and mobile 390×844: **11 browser checks passed**, no page JavaScript errors. Checked connected mode at `http://127.0.0.1:8765/app/`, empty/populated views, create pending, view details, edit, complete, pending/completed/overdue filters, browser refresh, actual server restart, cancel deletion, successful DELETE 204, and deletion after refresh.
- At 390px the page had no horizontal overflow; deletion was exercised at that width. This is not a claim of full mobile or cross-browser acceptance.
- Fictional local SQLite test data only; the final test database was empty. No shared application data was changed.

Evidence and reproducible scripts: [merged-main verification](evidence/merged-main-2026-11-04/README.md). Raw [pytest output](evidence/merged-main-2026-11-04/pytest-output.txt), [HTTP results](evidence/merged-main-2026-11-04/api-smoke-results.json), [browser results](evidence/merged-main-2026-11-04/results.json), and desktop/mobile PNGs are retained there.

### Acceptance checklist status

- [x] PR #45 reviewed and merged.
- [x] Merged-main add/view/edit/complete/filter/refresh/restart/delete smoke verification completed and tested SHA recorded.
- [x] New screenshots and detailed test results retained for submission; earlier seven team screenshots are also present in [integration-testing](evidence/integration-testing/README.md), linked to #46.
- [x] Traceability record updated with this verification. #36 and #38 were already closed as completed on 29 October.
- [ ] Existing validation gaps and unrecorded user-story scope decisions are tracked separately in #49. Full acceptance of every original US1–US12 story is not asserted.

This dated addendum supersedes the stale review/merge and screenshot status in the historical 22 October record above. The earlier manual browser details remain unknown; no new detail is attributed retrospectively to Petya.
