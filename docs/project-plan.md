# Proposed project plan — confirm with your group

## Problem and scope
Learners can lose track of assignments across modules. EduTrack proposes one simple local planner. Research is needed to verify this need and evaluate usefulness. Primary SDG alignment: SDG 4. No measured education outcomes are claimed.

## Scrum and backlog
Assign a Scrum Master, product owner, frontend developer (Student 2), backend developer and documentation coordinator. Roles may overlap. Use a GitHub Project board: Backlog → In progress → Review → Done.

| ID | User story | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| US1 | As a learner, I can add a study assignment | Must | Valid title and date; optional module persist after restart |
| US2 | I can see deadlines | Must | Assignments ordered by date; overdue incomplete assignments identified |
| US3 | I can mark progress | Must | Completion and counts update consistently |
| US4 | I can filter assignments | Should | All, pending, completed and overdue views work |
| US5 | I can remove an assignment | Should | Confirmation before deletion |
| US7 | I can edit and view assignment details | Must | All fields editable and description available |
| US6 | I can use the planner on mobile | Must | No horizontal page overflow at 375px |

## Proposed milestones
| Sprint | SDLC focus | Deliverable |
| --- | --- | --- |
| 1 | Requirements and design | Agreed scope, research, wireframes, backlog |
| 2 | Implementation | Frontend and database/API integration |
| 3 | Testing and iteration | Functional tests, learner feedback, fixes |
| 4 | Review and defence | Final GitHub artefact, evidence, live demo |

Confirm dates against the timetable. Brief gives 9 November 2026 for assessment; verify Moodle and viva session details. Portfolio deadlines follow the weekly module schedule.

## Risks
| Risk | Response |
| --- | --- |
| Integration mismatch | Agree API contract and test together |
| Missing teamwork evidence | Record real stand-ups and link commits/PRs |
| Scope too large | Complete core planner before adding features |
| Loss of work | Push reviewed changes to GitHub regularly |
| Personal-data exposure | Synthetic records; do not publish SQLite database |

## Definition of done
Code reviewed; automated tests pass; relevant manual checks recorded; README accurate; evidence linked. Do not mark unperformed checks as passed.
