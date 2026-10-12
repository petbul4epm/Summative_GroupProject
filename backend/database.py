
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "edutrack.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ('pending', 'completed')),
                module TEXT DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'medium'
                    CHECK(priority IN ('low', 'medium', 'high'))
            )
        """)
        connection.commit()


def get_all_assignments():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM assignments ORDER BY due_date ASC"
        ).fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    init_db()
    print("EduTrack database created successfully!")
