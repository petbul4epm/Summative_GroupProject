
# EduTrack - Automated FastAPI Tests

import pytest
from functools import partial
from fastapi.testclient import TestClient

import backend.main as api
from backend.database import (
    create_assignments_table,
    create_assignment,
    get_assignments,
    get_assignment,
    update_assignment,
    delete_assignment,
)


# Use a temporary SQLite database for every test
@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_api.db"

    database_functions = {
        "create_assignments_table": create_assignments_table,
        "create_assignment": create_assignment,
        "get_assignments": get_assignments,
        "get_assignment": get_assignment,
        "update_assignment": update_assignment,
        "delete_assignment": delete_assignment,
    }

    for name, function in database_functions.items():
        monkeypatch.setattr(
            api,
            name,
            partial(function, database_path=test_db)
        )

    with TestClient(api.app) as test_client:
        yield test_client


# Test 10 - POST: Create assignment
def test_create_assignment_api(client):
    response = client.post(
        "/assignments",
        json={
            "title": "Python Coursework",
            "due_date": "2026-11-15",
            "module": "CPU4106",
            "priority": "high"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Python Coursework"
    assert response.json()["status"] == "pending"


# Test 11 - GET: Retrieve all assignments
def test_get_assignments_api(client):
    client.post(
        "/assignments",
        json={
            "title": "Database Coursework",
            "due_date": "2026-11-20"
        }
    )

    response = client.get("/assignments")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Test 12 - GET: Retrieve assignment by ID
def test_get_assignment_by_id_api(client):
    created = client.post(
        "/assignments",
        json={
            "title": "Networking Coursework",
            "due_date": "2026-11-25"
        }
    )
    print("POST status:", created.status_code)
    print("POST response:", created.json())
    assignment_id = created.json()["id"]

    response = client.get(
        f"/assignments/{assignment_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == assignment_id


# Test 13 - GET: Assignment not found
def test_get_missing_assignment_api(client):
    response = client.get("/assignments/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Assignment not found"


# Test 14 - PUT: Update assignment
def test_update_assignment_api(client):
    created = client.post(
        "/assignments",
        json={
            "title": "Python Coursework",
            "due_date": "2026-11-15"
        }
    )

    assignment_id = created.json()["id"]

    response = client.put(
        f"/assignments/{assignment_id}",
        json={
            "title": "Updated Coursework",
            "due_date": "2026-11-20",
            "status": "completed"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Coursework"
    assert response.json()["status"] == "completed"


# Test 15 - DELETE: Remove assignment
def test_delete_assignment_api(client):
    created = client.post(
        "/assignments",
        json={
            "title": "Delete Test",
            "due_date": "2026-11-30"
        }
    )

    assignment_id = created.json()["id"]

    response = client.delete(
        f"/assignments/{assignment_id}"
    )

    assert response.status_code == 204

    check = client.get(
        f"/assignments/{assignment_id}"
    )

    assert check.status_code == 404


# Test 16 - POST: Invalid title
def test_invalid_assignment_api(client):
    response = client.post(
        "/assignments",
        json={
            "title": "",
            "due_date": "2026-11-15"
        }
    )

    assert response.status_code == 422


# Test 17 - PUT: Update all assignment fields
def test_update_all_assignment_fields_api(client):

    # Step 1 - Create an assignment
    created = client.post(
        "/assignments",
        json={
            "title": "Database Coursework",
            "due_date": "2026-11-20",
            "description": "Initial description",
            "module": "Databases",
            "priority": "low"
        }
    )

    assert created.status_code == 201
    assignment_id = created.json()["id"]

    # Step 2 - Update all fields
    response = client.put(
        f"/assignments/{assignment_id}",
        json={
            "title": "Updated Database Coursework",
            "due_date": "2026-12-01",
            "status": "completed",
            "description": "Updated description",
            "module": "CPU4106",
            "priority": "high"
        }
    )

    assert response.status_code == 200

    # Step 3 - Retrieve the updated assignment
    check = client.get(
        f"/assignments/{assignment_id}"
    )

    assert check.status_code == 200

    assignment = check.json()

    # Step 4 - Verify all updated fields
    assert assignment["title"] == "Updated Database Coursework"
    assert assignment["due_date"] == "2026-12-01"
    assert assignment["status"] == "completed"
    assert assignment["description"] == "Updated description"
    assert assignment["module"] == "CPU4106"
    assert assignment["priority"] == "high"

# Test 18 - POST: Invalid priority
def test_invalid_priority_api(client):
    response = client.post(
        "/assignments",
        json={
            "title": "Invalid Priority Test",
            "due_date": "2026-11-15",
            "priority": "urgent"  # Invalid priority
        }
    )        
    assert response.status_code == 422

# Test 19 - POST: Description exceeds maximum length
def test_invalid_description_length_api(client):
    long_description = "A" * 2001  # 2001 characters, exceeding the limit

    response = client.post(
        "/assignments",
        json={
            "title": "Long Description Test",
            "due_date": "2026-11-15",
            "description": long_description
        }
    )
    assert response.status_code == 422

# Test 20 - POST: Module exceeds maximum length
def test_invalid_module_length_api(client):
    long_module = "M" * 101  # 101 characters, exceeding the limit

    response = client.post(
        "/assignments",
        json={
            "title": "Long Module Test",
            "due_date": "2026-11-15",
            "module": long_module
        }
    )
    assert response.status_code == 422

# Test 21 - PUT: Invalid status
def test_invalid_status_api(client):
    created = client.post(
        "/assignments",
        json={
            "title": "Invalid Status Test",
            "due_date": "2026-11-15"
        }
    )

    assignment_id = created.json()["id"]

    response = client.put(
        f"/assignments/{assignment_id}",
        json={
            "title": "Invalid Status Test",
            "due_date": "2026-11-15",
            "status": "in_progress"  # Invalid status for update
        }
    )
    assert response.status_code == 422
