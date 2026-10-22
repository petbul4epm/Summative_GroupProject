# EduTrack — REST API Specification

**Project:** EduTrack — Student Assignment & Progress Tracker  
**Module:** CPU4106 — Group Project  
**Document Version:** 1.1  
**Author Role:** Backend Developer  
**Technology:** Python, FastAPI, Pydantic, SQLite  
**Implementation Status:** Backend Implemented and Tested

---

## 1. Introduction

### 1.1 Purpose

This document defines the REST API specification for EduTrack, a student assignment management application.

The API provides communication between the web-based frontend and the SQLite database. It allows students to create, retrieve, update and delete assignment records using standard HTTP methods.

This specification describes the implemented API endpoints, data structures, request and response formats, validation rules, HTTP status codes and backend testing results.

### 1.2 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend framework | Python / FastAPI | Process HTTP requests and return responses |
| Data validation | Pydantic | Validate request data and define response models |
| Database | SQLite3 | Store assignment records |
| Application server | Uvicorn | Run the FastAPI application |
| API documentation | Swagger UI / OpenAPI | Interactive endpoint documentation |
| Automated testing | pytest / FastAPI TestClient | Verify database and API functionality |

### 1.3 API Configuration

**Default Base URL:** `http://127.0.0.1:8000`  
**Local Testing URL:** `http://127.0.0.1:8001`  
**Swagger UI:** `/docs`  
**OpenAPI Schema:** `/openapi.json`  
**Data Format:** JSON  
**Request Content-Type:** `application/json`

The API is designed for a local, single-user application prototype. Authentication and user account management are not implemented.

---

## 2. API Architecture

EduTrack follows a three-layer architecture:

**Frontend → FastAPI Backend → SQLite Database**

The frontend sends HTTP requests to the FastAPI application. FastAPI validates request data using Pydantic models and executes the appropriate database function.

The database layer performs SQL operations and returns the requested information.

FastAPI then generates an HTTP response containing a status code and, where applicable, JSON data.

### 2.1 Backend Components

| File | Responsibility |
|---|---|
| `backend/main.py` | FastAPI application and REST endpoints |
| `backend/models.py` | Pydantic request and response models |
| `backend/database.py` | SQLite connection, table creation and CRUD functions |
| `backend/edutrack.db` | Local SQLite database, created automatically |
| `backend/tests/test_database.py` | Database tests |
| `backend/tests/test_api.py` | REST API tests |

### 2.2 Database Initialisation

The FastAPI application uses a lifespan function to initialise the SQLite assignments table when the application starts.

The database is accessed through functions in `backend/database.py`.

SQL queries use parameterised statements to separate SQL instructions from supplied values.

---

## 3. Assignment Data Model

The API manages records stored in the SQLite `assignments` table.

### 3.1 Assignment Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | Integer | Generated | Unique assignment identifier |
| `title` | String | Yes | Assignment title |
| `description` | String or null | No | Additional assignment information |
| `due_date` | Date | Yes | Assignment deadline |
| `status` | String | Required on update | Assignment progress status |
| `module` | String or null | No | Associated academic module |
| `priority` | String or null | No | Assignment priority |

The assignment ID is generated automatically by SQLite.

On creation, the database assigns the default status `pending`.

The API supports the following assignment statuses:

- `pending`
- `in_progress`
- `completed`

The API currently accepts `priority` as an optional string without restricting it to specific values.

### 3.2 Pydantic Models

**AssignmentCreate**

Used to validate POST request bodies.

Required fields:
- `title`
- `due_date`

Optional fields:
- `description`
- `module`
- `priority`

**AssignmentUpdate**

Used to validate PUT request bodies.

Required fields:
- `title`
- `due_date`
- `status`

Optional fields:
- `description`
- `module`
- `priority`

**AssignmentResponse**

Defines the JSON structure returned by FastAPI, including the generated `id`, assignment details and current `status`.

---

## 4. REST API Endpoints

The following endpoints are implemented.

| HTTP Method | Endpoint | Operation | Success Code |
|---|---|---|---|
| GET | `/assignments` | Retrieve all assignments | 200 |
| GET | `/assignments/{assignment_id}` | Retrieve an assignment by ID | 200 |
| POST | `/assignments` | Create an assignment | 201 |
| PUT | `/assignments/{assignment_id}` | Update an assignment | 200 |
| DELETE | `/assignments/{assignment_id}` | Delete an assignment | 204 |

### 4.1 GET /assignments

**Description:** Retrieves all assignment records from SQLite.

**Method:** GET  
**Endpoint:** `/assignments`  
**Request Body:** None  
**Success:** 200 OK

**Example Request**

`GET /assignments`

**Example Response**

```json
[
  {
    "id": 1,
    "title": "Database Coursework",
    "due_date": "2026-11-20",
    "description": "Create an ERD diagram",
    "module": "Databases",
    "priority": "high",
    "status": "pending"
  }
]
```

If no records exist, the endpoint returns:

```json
[]
```

**Database Function:** `get_assignments()`

---

### 4.2 GET /assignments/{assignment_id}

**Description:** Retrieves a single assignment using its unique ID.

**Method:** GET  
**Endpoint:** `/assignments/{assignment_id}`  
**Path Parameter:** `assignment_id` — Integer  
**Success:** 200 OK

**Example Request**

`GET /assignments/1`

**Example Response**

```json
{
  "id": 1,
  "title": "Database Coursework",
  "due_date": "2026-11-20",
  "description": "Create an ERD diagram",
  "module": "Databases",
  "priority": "high",
  "status": "pending"
}
```

**Error Responses**

- `404 Not Found` — Assignment does not exist.
- `422 Unprocessable Entity` — Invalid assignment ID format.

**Database Function:** `get_assignment()`

---

### 4.3 POST /assignments

**Description:** Creates and saves a new assignment.

**Method:** POST  
**Endpoint:** `/assignments`  
**Content-Type:** `application/json`  
**Success:** 201 Created

**Example Request Body**

```json
{
  "title": "Database Coursework",
  "due_date": "2026-11-20",
  "description": "Create an ERD diagram",
  "module": "Databases",
  "priority": "high"
}
```

**Example Response — 201 Created**

```json
{
  "id": 1,
  "title": "Database Coursework",
  "due_date": "2026-11-20",
  "description": "Create an ERD diagram",
  "module": "Databases",
  "priority": "high",
  "status": "pending"
}
```

**Processing Rules**

1. FastAPI receives the JSON request.
2. Pydantic validates the required and optional fields.
3. The `create_assignment()` function inserts the record into SQLite.
4. SQLite generates the unique assignment ID and assigns the default status `pending`.
5. FastAPI retrieves and returns the created assignment.

**Error Responses**

- `422 Unprocessable Entity` — Missing or invalid required fields.
- `500 Internal Server Error` — Assignment cannot be retrieved after insertion.

**Database Function:** `create_assignment()`

---

### 4.4 PUT /assignments/{assignment_id}

**Description:** Updates an existing assignment.

**Method:** PUT  
**Endpoint:** `/assignments/{assignment_id}`  
**Path Parameter:** `assignment_id` — Integer  
**Content-Type:** `application/json`  
**Success:** 200 OK

**Example Request**

`PUT /assignments/5`

**Example Request Body**

```json
{
  "title": "Database Design - Final Version",
  "due_date": "2026-11-30",
  "status": "completed",
  "description": "Completed database design and SQLite testing",
  "module": "CPU4106 Group Project",
  "priority": "high"
}
```

**Example Response — 200 OK**

```json
{
  "id": 5,
  "title": "Database Design - Final Version",
  "due_date": "2026-11-30",
  "description": "Completed database design and SQLite testing",
  "module": "CPU4106 Group Project",
  "priority": "high",
  "status": "completed"
}
```

**Processing Rules**

1. FastAPI receives the assignment ID and updated JSON data.
2. Pydantic validates the request using `AssignmentUpdate`.
3. The API passes the validated data to `update_assignment()`.
4. SQLite updates the matching record using its ID.
5. FastAPI retrieves and returns the updated assignment.

The operation supports all six editable fields:

- `title`
- `due_date`
- `status`
- `description`
- `module`
- `priority`

The `title`, `due_date` and `status` fields are required.

The `description`, `module` and `priority` fields are optional. Under the current implementation, omitted optional fields are saved as null during PUT requests.

The assignment ID remains unchanged.

**Error Responses**

- `404 Not Found` — Assignment does not exist.
- `422 Unprocessable Entity` — Invalid ID or request data.

**Database Function:** `update_assignment()`

---

### 4.5 DELETE /assignments/{assignment_id}

**Description:** Permanently deletes an existing assignment.

**Method:** DELETE  
**Endpoint:** `/assignments/{assignment_id}`  
**Path Parameter:** `assignment_id` — Integer  
**Request Body:** None  
**Success:** 204 No Content

**Example Request**

`DELETE /assignments/5`

**Successful Response**

`HTTP 204 No Content`

The response contains no JSON body.

**Processing Rules**

1. FastAPI receives the assignment ID.
2. The `delete_assignment()` function executes a parameterised SQLite DELETE query.
3. If the assignment is deleted, FastAPI returns HTTP 204.
4. If the assignment does not exist, FastAPI returns HTTP 404.

**Error Responses**

- `404 Not Found` — Assignment does not exist.
- `422 Unprocessable Entity` — Invalid assignment ID.

**Database Function:** `delete_assignment()`

The frontend must handle HTTP 204 without attempting to parse an empty response as JSON.

---

## 5. Request Validation

Pydantic performs automatic validation for POST and PUT request bodies.

### 5.1 Implemented Validation Rules

| Field | Implemented Rule |
|---|---|
| `title` | Required; 1–200 characters |
| `due_date` | Required; must be a valid date |
| `status` | Required for PUT; permitted values are `pending`, `in_progress`, `completed` |
| `description` | Optional string or null |
| `module` | Optional string or null |
| `priority` | Optional string or null |
| `assignment_id` | Must be an integer path parameter |

The current Pydantic implementation does not explicitly reject whitespace-only titles, enforce maximum lengths for description or module, or limit priority to a predefined set of values.

### 5.2 Validation Error Example

**Invalid POST Request**

```json
{
  "title": "",
  "due_date": "2026-11-15"
}
```

**Expected Status:** 422 Unprocessable Entity

FastAPI returns JSON validation details identifying the invalid field.

---

## 6. HTTP Status Codes

| Status Code | Description | Applicable Endpoints |
|---|---|---|
| 200 OK | Request processed successfully | GET, PUT |
| 201 Created | Assignment created successfully | POST |
| 204 No Content | Assignment deleted successfully | DELETE |
| 404 Not Found | Assignment ID does not exist | GET by ID, PUT, DELETE |
| 422 Unprocessable Entity | Invalid request body or path parameter | POST, PUT and ID-based endpoints |
| 500 Internal Server Error | Server-side failure | POST retrieval failure or other unexpected backend errors |

### Example 404 Response

```json
{
  "detail": "Assignment not found"
}
```

FastAPI automatically generates validation errors for requests that fail Pydantic checks.

---

## 7. Backend and Database Interaction

The database layer is implemented in `backend/database.py`.

### 7.1 Database Functions

| Function | Purpose |
|---|---|
| `get_connection()` | Establish an SQLite connection |
| `create_assignments_table()` | Create the assignments table if it does not exist |
| `create_assignment()` | Insert an assignment |
| `get_assignments()` | Retrieve all assignments |
| `get_assignment()` | Retrieve one assignment by ID |
| `update_assignment()` | Update assignment information |
| `delete_assignment()` | Delete an assignment |

### 7.2 SQL Operations

The database layer uses the following SQL operations:

- **INSERT** — create a new assignment.
- **SELECT** — retrieve one or multiple assignments.
- **UPDATE** — modify an existing assignment.
- **DELETE** — remove an assignment.

SQL statements use parameter placeholders (`?`) with separately supplied values.

Database connections are closed after operations using `try/finally` blocks.

Changes made through INSERT, UPDATE and DELETE are committed to SQLite.

### 7.3 Data Persistence

Assignment data is stored in the SQLite database and remains available after the API processes a request.

Data persistence was verified through POST, PUT and subsequent GET operations.

---

## 8. API Testing and Verification

Backend functionality was tested using pytest, FastAPI TestClient and the interactive Swagger UI documentation.

### 8.1 Automated Test Results

| Test Category | Tests Passed |
|---|---:|
| SQLite Database Tests | 9 |
| FastAPI Endpoint Tests | 8 |
| **Total** | **17** |

**Result:** 17 passed, 0 failed.

One Starlette/httpx deprecation warning was reported and did not prevent successful test execution.

The FastAPI test suite uses temporary SQLite databases to isolate test data.

### 8.2 FastAPI Test Coverage

The automated API tests cover:

| Test | Functionality |
|---|---|
| Test 10 | POST — Create Assignment |
| Test 11 | GET — Retrieve All Assignments |
| Test 12 | GET — Retrieve Assignment by ID |
| Test 13 | GET — Assignment Not Found |
| Test 14 | PUT — Update Assignment |
| Test 15 | DELETE — Remove Assignment |
| Test 16 | POST — Invalid Title |
| Test 17 | PUT — Update All Assignment Fields |

### 8.3 Complete Assignment Update Verification

Test 17, `test_update_all_assignment_fields_api`, verifies the complete update functionality required by User Story US4.

The test performs the following operations:

1. Creates an assignment using POST.
2. Updates all six editable fields using PUT.
3. Retrieves the updated record using GET.
4. Compares the retrieved field values with the expected updated values.

**Result:** Passed.

### 8.4 Manual Swagger UI Verification

The API was tested locally through Swagger UI using Uvicorn on port 8001.

| Endpoint | Verified HTTP Status |
|---|---|
| POST `/assignments` | 201 Created |
| GET `/assignments` | 200 OK |
| GET `/assignments/{assignment_id}` | 200 OK |
| PUT `/assignments/{assignment_id}` | 200 OK |
| DELETE `/assignments/{assignment_id}` | 204 No Content |

The complete PUT operation was manually verified using assignment ID 5.

A subsequent GET request confirmed that the updated title, due date, description, module, priority and status were stored successfully.

### 8.5 Testing Limitations

Automated testing verifies the implemented backend functions and selected HTTP behaviours.

Not every possible invalid input, missing-resource operation or browser interaction has a dedicated automated test.

Full frontend–backend integration and end-to-end testing are not included in the verified backend results.

---

## 9. API Documentation and Usage

FastAPI automatically generates interactive API documentation using OpenAPI.

The Swagger UI is available at:

`http://127.0.0.1:8000/docs`

For the local test server running on port 8001:

`http://127.0.0.1:8001/docs`

Swagger UI enables developers to inspect available endpoints, view request and response schemas, execute API requests and examine returned HTTP status codes.

### Starting the API

From the project's root directory:

```bash
python -m uvicorn backend.main:app --reload --port 8001
```

Once the server is running, the API endpoints can be accessed from the browser or an HTTP client.

---

## 10. Implementation Summary

The EduTrack REST API has been implemented using Python, FastAPI, Pydantic and SQLite.

The API provides five core assignment-management endpoints supporting creation, retrieval, updating and deletion of records.

The implementation includes server-side validation, database persistence, HTTP error handling and automated tests.

The complete assignment update functionality supports all six editable fields and has been verified using both automated and manual testing.

**Backend Test Results:** 17 passed, 0 failed.

The backend is implemented and independently tested. Frontend–backend integration remains pending.

---

*End of Document — EduTrack REST API Specification, Version 1.1*
