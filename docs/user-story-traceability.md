# EduTrack user-story traceability review

Date: 22 October 2026  
Related issue: #36  
Source: EduTrack_User_Stories.docx, created 16 October 2026; original US1–US12 and acceptance criteria were read before this comparison. The issue attachment returned HTTP 404 through the available download route; the document copy was used instead.  
Code reviewed: PR #45 head `7a4ac573ca11606f3d9fe8768dc70da20e50018c`.

"Implemented" below means code is present, not that all browser acceptance criteria have individually passed. The recorded 22-test automated suite and Petya's overall reported browser pass are separate evidence; no unreported per-story pass is inferred.

| Story | Code evidence | Existing automated evidence | Assessment and remaining acceptance |
|---|---|---|---|
| US1 View assignments | script.js: load(), render(); GET /assignments | test_get_assignments_api; test_connected_frontend_assets | Implemented. Confirm populated and empty-list browser views on merged main. |
| US2 Create assignment | form submit POST; FastAPI add_assignment | test_create_assignment_api; test_create_assignment | Implemented. Module is optional in the actual API/UI: confirm this clarification. Verify one record per save and browser refresh persistence. |
| US3 View details | render() shows title/module/date/priority/status and expandable View description | test_get_assignment_by_id_api | Implemented as inline details, not a separate detail page. Confirm expand/collapse meets the intention of returning to the list. |
| US4 Edit assignment | edit(), form submit PUT; edit_assignment | test_update_assignment_api; test_update_all_assignment_fields_api; test_update_assignment | Implemented. Confirm correct selected record, optional fields and refresh. Null priority becomes medium when edited; confirm that default is intended. |
| US5 Delete assignment | confirmation, mutate(), API 204 handling | test_delete_assignment_api; test_delete_assignment; focused frontend 204 check | Implemented. Verify cancel, refresh and that deleting one of two records leaves the other unchanged. |
| US6 Correct invalid entries | HTML required/date constraints; displayed API validation errors; Pydantic models | test_invalid_assignment_api plus priority/length/status validation tests | Implemented in part; invalid-date/recovery browser cases need explicit evidence. Whitespace-only titles are not rejected by live Pydantic validation; demo trims them. Record as a validation gap for follow-up. |
| US7 Completion | Mark completed/Mark pending and edit status; PUT | test_update_assignment_api; test_update_all_assignment_fields_api | Implemented despite proposed label in original document. Confirm persistence after refresh and formally accept into delivered scope. |
| US8 Sort by deadline | No sorting control or chronological sort in script.js | None specific | Not implemented. Keep as proposed/deferred unless the team explicitly adds it. Do not claim complete. |
| US9 Search by title | No title-search input or search logic | None specific | Not implemented. Keep as proposed/deferred. |
| US10 Filter module or status | filter select: all/pending/completed/overdue; render() filters by status | No dedicated browser filter test | Partial: status/overdue filtering implemented; module filtering absent. Agree to narrow this release's acceptance criteria to status or retain module filtering as backlog. |
| US11 Overdue work | todayISO(), isOverdue(): pending and due_date before today | No dedicated overdue boundary test | Implemented. Explicitly check yesterday/pending, today/pending and yesterday/completed. Accept into delivered scope if agreed. |
| US12 Phone use | responsive style.css; preserved mobile/tablet changes from PR #31 | No automated viewport/layout acceptance test | Implemented CSS; PR #31 records Firefox responsive review. Confirm add/edit/delete and absence of horizontal scrolling at a named mobile width. |

## Decisions to record before closing #36

- Accept US7, US11 and US12 as delivered features rather than proposed items, subject to final acceptance.
- Keep US8 and US9 deferred unless scope is deliberately expanded.
- Confirm status-only filtering for US10 or plan module filtering separately.
- Confirm optional module (US2), inline details (US3), and priority default on editing.
- Track whitespace-only title validation as an existing gap; align live API and demo behaviour.
- Attach or link per-story manual evidence where available, then record the merged main commit.

## Test evidence and limits

- 22 automated tests passed locally with the combined validation and frontend-serving changes.
- JavaScript syntax and focused DELETE 204/GET/validation-error checks passed.
- Petya reported manual browser tests complete and passing. Browser version, exact tested commit, individual acceptance results and screenshots were not supplied, so this review does not manufacture those details.
- PR #44 is merged. PR #45 remains pending review/merge at the time of this record.
- The attendance/teacher/marks requirements described elsewhere do not match this assignment-tracker story baseline and need scope reconciliation.

This is a traceability review and proposed scope reconciliation, not a replacement for the original agreed user stories or an assertion of full acceptance.
