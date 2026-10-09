# EduTrack — Group Project

A local student assignment and progress tracker for CPU4106. Proposed alignment: UN SDG 4 (Quality Education), by helping learners organise study work. Educational impact is a hypothesis to evaluate, not a measured result.

## Run
Requires Python 3.10 or newer; install the dependencies in a virtual environment.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```
On Windows, use `py` instead of `python` if necessary. Open http://127.0.0.1:8000 in your browser. Do not open index.html directly: it needs the API. Stop with Ctrl+C. SQLite is created automatically in backend/edutrack.db. Tasks persist after restart.

## Features
Add assignments with title, description, due date, optional module and priority; view details; edit; filter by pending/completed/overdue; mark completion; delete with confirmation; show counts and completion percentage. Responsive layout with labelled inputs and status messages.

## Structure and proposed ownership
- frontend/index.html, style.css, script.js — Petya and Shahzad (Student 2): frontend and UI design.
- backend/main.py, database.py, requirements.txt — Sergiu (Student 1): backend, database and backend testing.
- tests/ — everyone: automated and manual validation.
- docs/ — Farah (Student 3) coordinates; everyone supplies evidence.
- README.md — everyone maintains setup and scope.

Roles are proposed; agree them with the group. Generated code is a starting implementation, not evidence that any student has already completed these contributions.

## Testing
```bash
python -m pytest -q
```
See tests/manual-test-plan.md for browser checks and docs/api.md for endpoints.

## GitHub upload
1. Use the existing petbul4epm/Summative_GroupProject repository. Clone it for routine teamwork. The init commands below apply only to a new local copy without Git history.
2. Open the extracted project folder in a terminal.
3. Run the commands below, replacing YOUR-USERNAME with the repository owner's username.

```bash
git init
git add .
git commit -m "Add EduTrack prototype and project documentation"
git branch -M main
git remote add origin https://github.com/petbul4epm/Summative_GroupProject.git
git push -u origin main
```
Invite group members in repository Settings → Collaborators. For your next changes:
```bash
git switch -c student2-frontend
git add frontend/
git commit -m "Improve frontend"
git push -u origin student2-frontend
```
Open a pull request on GitHub and ask a teammate to review. Other students use their own branches. Upload the extracted files, not just the ZIP. Never commit real learner data or credentials.

## Scope and limitations
Scope follows the supplied EduTrack Group Project Roadmap: single-user assignment tracking. Local single-user prototype, no login, roles, cloud hosting or notifications. The Uvicorn development server is for local demonstrations. Use synthetic data only. Accessibility requires manual testing; no compliance claim is made.

## Assessment work still required
Complete actual Scrum records, research, design decisions, usability testing and individual reflections. The included documents are templates/proposals, not completed evidence. Your brief requires a functional artefact, live defence, individual article and weekly portfolio. Review and understand the code, adapt it with your team, and follow your university's rules on acknowledging assistance. Do not claim generated work or invented activity as your own.

## API and team clarification
FastAPI documentation: http://127.0.0.1:8000/docs. Frontend and API use the same server, so CORS configuration is unnecessary for this setup. Launch from the project root. Sergiu is Student 1; Petya and Shahzad share Student 2; Farah is Student 3. Optional calendar and advanced analytics are excluded.

## Planning files
- docs/EduTrack_Gantt_Chart.xlsx uses roles only and preserves the supplied weekly schedule.
- docs/EduTrack_Project_Tracker.xlsx assigns named owners and retains the updated dates.
These workbooks currently have different schedule structures: Gantt uses Weeks 1–5; tracker contains four sprint summary rows, with tasks assigned to Sprints 1 and 2. Treat schedules as team planning inputs to reconcile, rather than verified deadlines.

## Frontend-only demo
Open frontend/index.html directly, or use ?demo=1 over HTTP, to try the separate localStorage demo. Without that flag, the served application calls FastAPI. Demo records do not transfer to SQLite.

## Team workflow
Use small feature branches and reviewed pull requests. Sergiu: backend and API tests; Petya and Shahzad: frontend; Farah: Scrum, GitHub Projects, QA coordination, Gantt and documentation. All members contribute requirements, integration tests and the live defence. The tracker and code are generated starting material: record actual commits, research, test results and contributions honestly.
