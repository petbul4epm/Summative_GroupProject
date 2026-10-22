# EduTrack – Student Assignment & Progress Tracker

## 1. Project Overview

EduTrack is a student assignment and progress tracking web application developed for the **CPU4106 Group Project** at Bath Spa University / GBS.

The project supports **UN Sustainable Development Goal 4 (SDG 4) – Quality Education** by aiming to help students organise assignments, manage deadlines and monitor academic task completion.

EduTrack is being developed as a local, single-user prototype over four development weeks, followed by a group presentation in Week 5.

## 2. Project Aim and Objectives

The aim is to develop a simple, responsive web application for managing academic assignments.

The objectives are to:

- Create and view assignments.
- Edit assignment details.
- Mark assignments as completed.
- Delete assignments.
- Track deadlines and completion progress.
- Store assignment data in SQLite.
- Connect the frontend and backend through a REST API.
- Test the application's core functionality.

## 3. Project Scope

### In Scope

- Student assignment dashboard.
- Add, view, edit and delete assignments.
- Assignment deadlines and completion status.
- Optional assignment module and priority, subject to team approval.
- SQLite database storage.
- REST API using Python and FastAPI.
- Responsive frontend using HTML, CSS and JavaScript.
- Input validation and functional testing.

### Out of Scope

- Online course delivery or learning materials.
- Student attendance tracking.
- Assignment grading by lecturers.
- Student–lecturer messaging.
- Online assignment file submissions.
- Advanced analytics or AI recommendations.
- Complex authentication and role management.

## 4. Technology Stack

| Technology | Purpose |
| --- | --- |
| HTML, CSS, JavaScript | Frontend and User Interface |
| Python | Backend development |
| FastAPI | REST API |
| SQLite | Database |
| Pydantic | Data validation |
| Uvicorn | Local development server |
| VS Code | Development environment |
| Git and GitHub | Version control and collaboration |
| GitHub Projects | Task management |
| Microsoft Excel | Gantt Chart and milestones |
| diagrams.net | Technical diagrams |

## 5. System Architecture

EduTrack uses a proposed three-tier architecture:

1. Presentation Tier – Frontend and User Interface.
2. Application Tier – Python and FastAPI.
3. Data Tier – SQLite database.

The frontend communicates with the backend through HTTP requests and JSON responses. The backend accesses SQLite using SQL queries.

![EduTrack System Architecture](docs/system-architecture.png)

## 6. Project Structure

The planned repository structure is:

```text
Summative_GroupProject/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
├── docs/
│   ├── README.md
│   ├── database-design.md
│   ├── database-erd.png
│   ├── system-architecture.png
│   └── api-specification.md
├── .gitignore
└── README.md
```

Some backend files and functionality are planned and may not yet exist on the main branch.

## 7. Local Development

Run these commands from the project root using Python, FastAPI and SQLite:

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then install dependencies and start the server:

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```

- Connected application: **http://127.0.0.1:8000/app/** (include the trailing slash).
- API documentation: http://127.0.0.1:8000/docs
- API health message: http://127.0.0.1:8000/

FastAPI serves the frontend and API from the same origin. No separate frontend server or CORS configuration is needed. Keep the terminal running while using the application. If a different port is selected, use that port in the browser address too.

Opening `frontend/index.html` directly, or adding `?demo=1` to the application URL, enables browser demo mode. Demo records use browser storage and are separate from SQLite; they do not demonstrate API integration.

New assignments start as pending. Use Edit or Mark completed to change status after creation. A successful DELETE returns HTTP 204 without JSON; the frontend then reloads the assignment list.

To check integration, add an assignment, edit it, mark it completed, refresh, restart the server and verify it remains, then delete it and refresh again. Record actual results in the QA log; this procedure is not itself evidence of a pass.

## 8. Team Responsibilities

| Role | Responsibility |
| --- | --- |
| Backend Developer – Sergiu | SQLite, Python, FastAPI, REST API and backend testing |
| Frontend Developers – Petya and Shahzad | UI design, dashboard, HTML, CSS, JavaScript and frontend testing |
| Project Coordinator – Farah | Scrum coordination, Gantt Chart, GitHub Projects and documentation |

All team members contribute to requirements review, integration, testing and the final presentation.

## 9. Technical Documentation

The `docs/` folder contains the proposed technical design.

- [Database Design](docs/database-design.md)
- [Entity Relationship Diagram](docs/database-erd.png)
- [System Architecture Diagram](docs/system-architecture.png)
- [REST API Specification](docs/api-specification.md)

The API specification describes the proposed endpoints and expected data formats. It must be reviewed with the frontend team before being treated as the final contract.

## 10. Project Schedule

| Week | Main Activities |
| --- | --- |
| Week 1 | Project planning, scope, GitHub setup and Gantt Chart |
| Week 2 | Database and API design, development |
| Week 3 | Frontend/backend implementation and integration |
| Week 4 | Testing, debugging, integration verification and documentation |
| Week 5 | Group presentation and viva |

The detailed Gantt Chart and milestone tracker are maintained separately and will be added to the repository after review.

## 11. Development and Testing Status

The project is under active development.

Database design, ERD, system architecture and API specification have been prepared for team review. The backend implementation and frontend integration must be verified through actual code review and testing.

Testing will include CRUD operations, input validation, frontend interaction, responsive layouts and error handling.

No unverified functionality or test result should be reported as completed.

## 12. Collaboration Workflow

Team members work on separate Git branches and submit Pull Requests for review.

Changes should be checked before merging into `main`. GitHub Issues and Projects are used to record task ownership and progress.

The team will maintain evidence of actual contributions, implementation decisions, testing and project meetings.

---

**EduTrack | CPU4106 Group Project | SDG 4 – Quality Education**

