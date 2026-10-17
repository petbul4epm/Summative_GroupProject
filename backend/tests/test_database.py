# Test 1: Database Connection
import sqlite3
from backend.database import (
    create_assignments_table,
    get_connection,
    create_assignment,
    get_assignments,
    get_assignment,
    update_assignment,
    delete_assignment
)

def test_database_connection():
    connection = get_connection()

    try:
        assert isinstance(connection, sqlite3.Connection)
    finally:
        connection.close()

#Test 2: Table Creation
def test_assignments_table_creation(tmp_path):
    test_db = tmp_path / "test_edutrack.db"

    create_assignments_table(test_db)
    connection = get_connection(test_db)

    try:
        result = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='assignments'"
        ).fetchone()

    finally:
        connection.close()
    assert result is not None
    assert result["name"] == "assignments"

# Test 3: Table Columns Validation
def test_table_columns(tmp_path):
    test_db = tmp_path / "test_edutrack.db"

    create_assignments_table(test_db)
    connection = get_connection(test_db)

    try:
        columns = connection.execute(
            "PRAGMA table_info(assignments)"    
        ).fetchall()

    finally:
        connection.close()
    actual_columns = [column["name"] for column in columns]

    expected_columns = [
        "id", 
        "title", 
        "description", 
        "due_date", 
        "status", 
        "module", 
        "priority"
    ]

    assert actual_columns == expected_columns
 
# Test 4: Default Status
def test_default_status(tmp_path):
    test_db = tmp_path / "test_edutrack.db"
    create_assignments_table(test_db)

    connection = get_connection(test_db)

    try:
        connection.execute(
            "INSERT INTO assignments (title, due_date) VALUES (?, ?)",
            ("Database Coursework", "2026-10-20")
        )
        connection.commit()

        result = connection.execute(
            "SELECT status FROM assignments WHERE title = ?",
            ("Database Coursework",)
        ).fetchone()

    finally:
        connection.close()
    assert result is not None
    assert result["status"] == "pending"



# Test 5 — CREATE Assignment
def test_create_assignment(tmp_path):
    test_db = tmp_path / "test_edutrack.db"

    create_assignments_table(test_db)

    assignment_id = create_assignment(
        "Python Coursework",
        "2026-11-15",
        database_path=test_db
    )

    connection = get_connection(test_db)

    try:
        assignment = connection.execute(
            "SELECT * FROM assignments WHERE id = ?",
            (assignment_id,)
        ).fetchone()

        assert assignment is not None
        assert assignment["title"] == "Python Coursework"
        assert assignment["due_date"] == "2026-11-15"
        assert assignment["status"] == "pending"

    finally:
        connection.close()


# Test 6 — READ all assignments
def test_get_assignments(tmp_path):
    test_db = tmp_path / "test_edutrack.db"
    create_assignments_table(test_db)

    create_assignment(
        "Python Coursework",
        "2026-11-15",
        database_path=test_db
    )

    assignments = get_assignments(database_path=test_db)

    assert len(assignments) == 1
    assert assignments[0]["title"] == "Python Coursework"
    assert assignments[0]["status"] == "pending"


# Test 7 — READ assignment by ID
def test_get_assignment_by_id(tmp_path):
    test_db = tmp_path / "test_edutrack.db"
    create_assignments_table(test_db)

    assignment_id = create_assignment(
        "Networking Coursework",
        "2026-11-20",
        database_path=test_db
    )

    assignment = get_assignment(
        assignment_id,
        database_path=test_db
    )

    assert assignment is not None
    assert assignment["id"] == assignment_id
    assert assignment["title"] == "Networking Coursework"

    missing_assignment = get_assignment(
        9999,
        database_path=test_db
    )

    assert missing_assignment is None


# Test 8 — UPDATE assignment
def test_update_assignment(tmp_path):
    test_db = tmp_path / "test_edutrack.db"
    create_assignments_table(test_db)

    assignment_id = create_assignment(
        "Python Coursework",
        "2026-11-15",
        database_path=test_db
    )

    updated = update_assignment(
        assignment_id,
        "Updated Python Coursework",
        "2026-11-20",
        "completed",
        database_path=test_db
    )

    assert updated is True

    assignment = get_assignment(
        assignment_id,
        database_path=test_db
    )

    assert assignment["title"] == "Updated Python Coursework"
    assert assignment["due_date"] == "2026-11-20"
    assert assignment["status"] == "completed"

    assert update_assignment(
        9999,
        "Missing Assignment",
        "2026-11-20",
        "completed",
        database_path=test_db
    ) is False


# Test 9 — DELETE assignment
def test_delete_assignment(tmp_path):
    test_db = tmp_path / "test_edutrack.db"
    create_assignments_table(test_db)

    assignment_id = create_assignment(
        "Assignment to Delete",
        "2026-11-25",
        database_path=test_db
    )

    deleted = delete_assignment(
        assignment_id,
        database_path=test_db
    )

    assert deleted is True

    assignment = get_assignment(
        assignment_id,
        database_path=test_db
    )

    assert assignment is None

    missing_deleted = delete_assignment(
        9999,
        database_path=test_db
    )

    assert missing_deleted is False




