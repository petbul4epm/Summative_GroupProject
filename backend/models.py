
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


# CREATE - Validate new assignment data
class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_date: date
    description: str | None = None
    module: str | None = None
    priority: str | None = None


# UPDATE - Validate assignment changes
class AssignmentUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_date: date
    status: Literal["pending", "in_progress", "completed"]
    description: str | None = None
    module: str | None = None
    priority: str | None = None


# RESPONSE - Data returned by FastAPI
class AssignmentResponse(AssignmentCreate):
    id: int
    status: Literal["pending", "in_progress", "completed"] = "pending"
