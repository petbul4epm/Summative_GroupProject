# Test 1: Database Connection
import sqlite3
from backend.database import create_assignments_table, get_connection

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

        
        
