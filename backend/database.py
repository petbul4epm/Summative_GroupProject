import sqlite3
from pathlib import Path

# Location of our SQLite database
DATABASE_PATH = Path(__file__).parent / "edutrack.db"

def get_connection(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row  # This allows us to access columns by name
    return connection

# Create the assignments table
def create_assignments_table(database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                module TEXT,
                priority TEXT   
            )
        """)

        connection.commit()

    finally:
        connection.close()


# CREATE — Add a new assignment
def create_assignment(title, due_date, database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            """
            INSERT INTO assignments (title, due_date)
            VALUES (?, ?)
            """,
            (title, due_date)
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()



# READ — Get all assignments
def get_assignments(database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            "SELECT * FROM assignments"
        )

        assignments = cursor.fetchall()

        return [dict(row) for row in assignments]

    finally:
        connection.close()



# READ — Get a single assignment by ID
def get_assignment(assignment_id, database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            "SELECT * FROM assignments WHERE id = ?",
            (assignment_id,)
        )

        assignment = cursor.fetchone()

        return dict(assignment) if assignment else None

    finally:
        connection.close()



# UPDATE — Modify an existing assignment
def update_assignment(assignment_id, title, due_date, status, database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            """
            UPDATE assignments
            SET title = ?, due_date = ?, status = ?
            WHERE id = ?
            """,
            (title, due_date, status, assignment_id)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()



# DELETE — Remove an assignment by ID
def delete_assignment(assignment_id, database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    try:
        cursor = connection.execute(
            "DELETE FROM assignments WHERE id = ?",
            (assignment_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


        
