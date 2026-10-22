
# EduTrack — FastAPI Backend
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException, status
from backend.models import AssignmentCreate, AssignmentResponse
from backend.database import create_assignment, get_assignment
from fastapi import FastAPI
from backend.database import get_assignments
from backend.models import AssignmentUpdate
from backend.database import update_assignment
from backend.database import create_assignments_table
from backend.database import delete_assignment

# Initialise SQLite when FastAPI starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_assignments_table()
    yield

#Create FastAPI application
app = FastAPI(
    title="EduTrack API",
    description="Student Assignment & Progress Tracker",
    version="1.0.0",
    lifespan=lifespan
)


# Root endpoint
@app.get("/")
def home():
    return {"message": "EduTrack API is running"}


# POST — Create a new assignment
@app.post(
    "/assignments",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_assignment(assignment: AssignmentCreate):
    assignment_id = create_assignment(
        title=assignment.title,
        due_date=assignment.due_date,
        description=assignment.description,
        module=assignment.module,
        priority=assignment.priority
    )

    created_assignment = get_assignment(assignment_id)

    if created_assignment is None:
        raise HTTPException(
            status_code=500,
            detail="Assignment could not be retrieved"
        )

    return created_assignment



# GET — Retrieve all assignments
@app.get(
    "/assignments",
    response_model=list[AssignmentResponse]
)
def list_assignments():
    return get_assignments()



# GET — Retrieve a single assignment by ID
@app.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse
)
def read_assignment(assignment_id: int):
    assignment = get_assignment(assignment_id)

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return assignment



# PUT — Update an existing assignment
@app.put(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse
)
def edit_assignment(assignment_id: int, assignment: AssignmentUpdate):

    updated = update_assignment(
        assignment_id,
        assignment.title,
        assignment.due_date,
        assignment.status,
        description=assignment.description,
        module=assignment.module,
        priority=assignment.priority
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return get_assignment(assignment_id)


# DELETE — Remove an assignment by ID
@app.delete(
    "/assignments/{assignment_id}",
    status_code=204
)
def remove_assignment(assignment_id: int):
    deleted = delete_assignment(assignment_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return None



# Serve only frontend assets; API endpoints and Swagger remain available.
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")



