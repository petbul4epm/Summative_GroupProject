# EduTrack – Database Design

**Project:** EduTrack – Student Assignment & Progress Tracker  
**Module:** CPU4106 Group Project  
**Document Version:** 1.1  
**Database:** SQLite3  
**Responsible Role:** Backend Developer  
**Implementation Status:** Implemented and Tested

---

## 1. Database Overview

EduTrack uses SQLite to store and manage student assignments in a local, single-user application.

The database consists of one table named `assignments`. It supports the creation, retrieval, updating and deletion of assignment records through CRUD operations.

The implemented table contains seven fields: `id`, `title`, `description`, `due_date`, `status`, `module` and `priority`.

SQLite database operations are implemented in `backend/database.py`, while the database file is stored locally as `backend/edutrack.db`.

The database is initialised automatically when the FastAPI application starts.

---

## 2. Database Table Specification

The `assignments` table uses the following schema:

| Field | SQLite Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique assignment identifier |
| `title` | TEXT | NOT NULL | Assignment title |
| `description` | TEXT | Nullable | Additional assignment information |
| `due_date` | TEXT | NOT NULL | Assignment deadline |
| `status` | TEXT | NOT NULL DEFAULT 'pending' | Assignment progress status |
| `module` | TEXT | Nullable | Associated academic module |
| `priority` | TEXT | Nullable | Assignment priority |

### 2.1 Primary Key

The `id` column is the primary key of the `assignments` table.

SQLite automatically generates a unique integer for each new assignment using `AUTOINCREMENT`.

The primary key is used to identify individual records during SELECT, UPDATE and DELETE operations.

### 2.2 Required and Optional Fields

The database requires values for `title`, `due_date` and `status`.

The `description`, `module` and `priority` columns allow NULL values.

When an assignment is created without an explicit status, SQLite automatically assigns `pending`.

### 2.3 Date Storage

The `due_date` column uses SQLite's TEXT data type.

The application stores dates as strings in the ISO format `YYYY-MM-DD`.

FastAPI uses a Pydantic date field to validate dates received through the API.

---

## 3. Data Integrity and Validation

Data integrity is maintained through SQLite constraints, parameterised SQL queries and application-level validation.

### 3.1 SQLite Constraints

The implemented database enforces:

- `id` as an automatically generated primary key.
- `title` as NOT NULL.
- `due_date` as NOT NULL.
- `status` as NOT NULL with the default value `pending`.

The current table definition does not contain CHECK constraints for permitted status or priority values, or maximum text lengths.

### 3.2 Application-Level Validation

FastAPI uses Pydantic models to validate API requests before database operations are executed.

The implemented API requires:

- A title containing between 1 and 200 characters.
- A valid due date.
- A status of `pending`, `in_progress` or `completed` when updating an assignment.

The optional `description`, `module` and `priority` fields accept strings or NULL values.

Additional restrictions, including maximum description length, module length and predefined priority values, are not currently enforced by the backend.

### 3.3 Parameterised SQL Queries

All CRUD operations use parameterised SQL statements with `?` placeholders.

For example:

```sql
SELECT * FROM assignments WHERE id = ?
```

This prevents user-supplied values from being directly concatenated into SQL statements and reduces the risk of SQL injection.

### 3.4 Database Transactions

INSERT, UPDATE and DELETE operations use `connection.commit()` to save changes.

Database connections are closed using `try/finally` blocks to ensure resources are released.

---

## 4. Entity Relationship Diagram

EduTrack uses a single database entity: `assignments`.

The table contains seven attributes, with `id` serving as the primary key.

No foreign-key relationships are required because the agreed application does not contain additional database tables.

![EduTrack Database ERD](database-erd.png)

The diagram represents the database structure used by the implemented assignment tracker.

---

## 5. Database CRUD Operations

The database layer provides the following functions in `backend/database.py`:

| Function | Description | SQL Operation |
|---|---|---|
| `get_connection()` | Establishes a database connection | — |
| `create_assignments_table()` | Creates the assignments table if necessary | CREATE TABLE |
| `create_assignment()` | Inserts a new assignment | INSERT |
| `get_assignments()` | Retrieves all assignments | SELECT |
| `get_assignment()` | Retrieves an assignment by ID | SELECT |
| `update_assignment()` | Updates an existing assignment | UPDATE |
| `delete_assignment()` | Deletes an assignment | DELETE |

### 5.1 Create

The `create_assignment()` function inserts an assignment into the database.

SQLite generates the assignment ID and applies the default status `pending`.

The function returns the generated ID.

### 5.2 Read

The `get_assignments()` function retrieves all assignments.

The `get_assignment()` function retrieves one assignment using its unique ID.

SQLite rows are converted into Python dictionaries for use by the FastAPI application.

### 5.3 Update

The `update_assignment()` function modifies an existing assignment identified by its ID.

The implemented UPDATE operation supports six editable fields:

- `title`
- `due_date`
- `status`
- `description`
- `module`
- `priority`

The UPDATE query preserves the original assignment ID.

The function returns a Boolean value indicating whether a matching record was updated.

### 5.4 Delete

The `delete_assignment()` function removes an assignment using its ID.

The function returns a Boolean value indicating whether a record was deleted.

---

## 6. Design Rationale

SQLite was selected because it is lightweight, requires no separate database server and is appropriate for a local student project prototype.

A single-table design keeps the application simple while supporting the required assignment-management functionality.

The database structure avoids unnecessary complexity and remains suitable for the agreed project scope.

The application does not currently require separate tables for user accounts, courses, enrolments, grading, attendance or file submissions.

The design can be extended in future versions if additional requirements are introduced.

---

## 7. Database Testing

The SQLite database implementation was tested using pytest.

The automated database test suite contains nine tests covering database functionality.

### 7.1 Automated Test Coverage

The SQLite tests cover:

- Database connection.
- Assignment table creation.
- Required table columns.
- Default assignment status.
- Creating an assignment.
- Retrieving assignments.
- Retrieving an assignment by ID.
- Updating an assignment.
- Deleting an assignment.

### 7.2 Testing Environment

Tests use temporary SQLite database files to avoid modifying the application's working database.

This allows database operations to be tested independently and repeatedly.

### 7.3 Test Results

**SQLite Database Tests:** 9 passed  
**Failed Tests:** 0

The complete backend test suite, including FastAPI API tests, returned:

**17 passed, 0 failed.**

An additional API test verified that all six editable assignment fields could be updated and retrieved successfully.

### 7.4 Database Persistence Verification

Data persistence was verified through assignment creation, updating and retrieval.

Manual FastAPI Swagger UI testing also confirmed that updated assignment information could be retrieved through GET requests after being modified through PUT.

---

## 8. Implementation Summary

The EduTrack SQLite database has been implemented using Python's built-in `sqlite3` library.

The database uses a single `assignments` table containing seven fields and supports the required CRUD operations.

Database connections, parameterised SQL queries and transaction commits are managed within `backend/database.py`.

The implemented database has passed all nine dedicated SQLite tests and supports the FastAPI REST endpoints.

**Implementation Status:** Database Implemented and Tested.

---

*End of Document — EduTrack Database Design, Version 1.1*
