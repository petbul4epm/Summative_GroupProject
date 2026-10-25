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

- [ ] Team reviews and merges the integration pull request.
- [ ] Run a brief add/edit/complete/delete check on the merged `main` commit and record that commit.
- [ ] Attach any retained manual screenshots and detailed test results for submission.
- [ ] Complete user-story traceability in #36.

Issues #34 and #35 remain open until merged integration is confirmed. This document replaces the placeholder QA description in #38 with the available verified and user-reported evidence.
