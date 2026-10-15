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
