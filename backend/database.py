"""SQLite repository; parameterised SQL protects query boundaries."""
import os
import sqlite3
from pathlib import Path
DB_PATH = Path(os.environ.get("EDUTRACK_DB", Path(__file__).with_name("edutrack.db")))
FIELDS = ("title", "description", "due_date", "status", "module", "priority")
def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialise():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT '', due_date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('pending','completed')),
        module TEXT NOT NULL DEFAULT '',
        priority TEXT NOT NULL CHECK(priority IN ('low','medium','high')))""")

def list_assignments():
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM assignments ORDER BY due_date,id")]

def get_assignment(id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM assignments WHERE id=?",(id,)).fetchone()
        return dict(row) if row else None

def save_assignment(data, id=None):
    values = [data[k] for k in FIELDS]
    with connect() as conn:
        if id is None:
            cur = conn.execute("INSERT INTO assignments(title,description,due_date,status,module,priority) VALUES (?,?,?,?,?,?)",values)
            id = cur.lastrowid
        else:
            cur = conn.execute("UPDATE assignments SET title=?,description=?,due_date=?,status=?,module=?,priority=? WHERE id=?",values+[id])
            if not cur.rowcount: return None
        return dict(conn.execute("SELECT * FROM assignments WHERE id=?",(id,)).fetchone())

def delete_assignment(id):
    with connect() as conn:
        return conn.execute("DELETE FROM assignments WHERE id=?",(id,)).rowcount > 0
