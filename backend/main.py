
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db, get_all_assignments

app = FastAPI(
    title="EduTrack API",
    description="Student Assignment and Progress Tracker",
    version="1.0.0"
)

# Allow the EduTrack frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to EduTrack API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

init_db()

@app.get("/assignments")
def list_assignments():
    return get_all_assignments()

from pydantic import BaseModel, Field
from datetime import date
from typing import Literal


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    due_date: date
    status: Literal["pending", "completed"] = "pending"
    module: str = ""
    priority: Literal["low", "medium", "high"] = "medium"


@app.post("/assignments", status_code=201)
def create_assignment(assignment: AssignmentCreate):
    from backend.database import get_connection

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO assignments
            (title, description, due_date, status, module, priority)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                assignment.title.strip(),
                assignment.description,
                assignment.due_date.isoformat(),
                assignment.status,
                assignment.module,
                assignment.priority
            )
        )
        connection.commit()
        new_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM assignments WHERE id = ?",
            (new_id,)
        ).fetchone()

    return dict(row)

from fastapi import HTTPException

@app.put("/assignments/{assignment_id}")
def update_assignment(
    assignment_id: int,
    assignment: AssignmentCreate
):
    from backend.database import get_connection

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM assignments WHERE id = ?",
            (assignment_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found"
            )

        connection.execute(
            """
            UPDATE assignments
            SET title = ?, description = ?, due_date = ?,
                status = ?, module = ?, priority = ?
            WHERE id = ?
            """,
            (
                assignment.title.strip(),
                assignment.description,
                assignment.due_date.isoformat(),
                assignment.status,
                assignment.module,
                assignment.priority,
                assignment_id
            )
        )
        connection.commit()

        updated = connection.execute(
            "SELECT * FROM assignments WHERE id = ?",
            (assignment_id,)
        ).fetchone()

    return dict(updated)

@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int):
    from backend.database import get_connection

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM assignments WHERE id = ?",
            (assignment_id,)
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found"
            )

    return {"deleted": True}

