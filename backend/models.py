
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


# CREATE - Validate new assignment data
class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_date: date
    description: str | None = Field(default=None, max_length=2000)
    module: str | None = Field(default=None, max_length=100)
    priority: Literal["low", "medium", "high"] | None = None
     
# UPDATE - Validate assignment changes
class AssignmentUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_date: date
    status: Literal["pending", "completed"]
    description: str | None = Field(default=None, max_length=2000)
    module: str | None = Field(default=None, max_length=100)
    priority: Literal["low", "medium", "high"] | None = None


# RESPONSE - Data returned by FastAPI
class AssignmentResponse(AssignmentCreate):
    id: int
    status: Literal["pending", "completed"] = "pending"
