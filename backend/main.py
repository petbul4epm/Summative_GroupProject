"""FastAPI assignment API and same-origin frontend for a local demo."""
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from . import database

class AssignmentInput(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)
    due_date: date
    status: Literal["pending", "completed"] = "pending"
    module: str = Field(default="", max_length=100)
    priority: Literal["low", "medium", "high"] = "medium"

    @field_validator("title", "module", "description", mode="before")
    @classmethod
    def trim(cls, value):
        return value.strip() if isinstance(value,str) else value

    def record(self):
        return self.model_dump(mode="json")

@asynccontextmanager
async def lifespan(app):
    database.initialise()
    yield

app = FastAPI(title="EduTrack API", lifespan=lifespan)

@app.get("/assignments")
def list_assignments():
    return database.list_assignments()

@app.get("/assignments/{id}")
def get_assignment(id: int):
    result = database.get_assignment(id)
    if result is None: raise HTTPException(404,"Assignment not found")
    return result

@app.post("/assignments", status_code=201)
def create_assignment(data: AssignmentInput):
    return database.save_assignment(data.record())

@app.put("/assignments/{id}")
def update_assignment(id: int, data: AssignmentInput):
    result = database.save_assignment(data.record(),id)
    if result is None: raise HTTPException(404,"Assignment not found")
    return result

@app.delete("/assignments/{id}")
def delete_assignment(id: int):
    if not database.delete_assignment(id): raise HTTPException(404,"Assignment not found")
    return {"deleted":True}

app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[1]/"frontend",html=True),name="frontend")
