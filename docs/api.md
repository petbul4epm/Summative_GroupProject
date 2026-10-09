# Assignment API contract

| Method | Endpoint | Result |
| --- | --- | --- |
| GET | /assignments | 200 array, ordered by due_date then id |
| GET | /assignments/{id} | 200 record or 404 |
| POST | /assignments | 201 created record |
| PUT | /assignments/{id} | 200 updated record or 404 |
| DELETE | /assignments/{id} | 200 deleted:true or 404 |

POST and PUT accept title (required, 1–120 trimmed characters), description (optional, up to 2000), due_date (required ISO date), module (optional, up to 100), priority (low/medium/high, default medium) and status (pending/completed, default pending). PUT replaces the record using the same input schema. Return includes integer id. Invalid payloads return 422 with FastAPI detail. Missing records return 404 with detail. Use Content-Type: application/json. Swagger /docs provides interactive examples.

Example:
```json
{"title":"Database Coursework","description":"Draft report","due_date":"2026-11-01","module":"Databases","priority":"high","status":"pending"}
```
