
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
