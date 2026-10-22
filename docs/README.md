# EduTrack — Technical Documentation

This directory contains the technical design and implementation documentation for the EduTrack Student Assignment & Progress Tracker (CPU4106 Group Project).

## Documentation

| Document | Description |
|---|---|
| [REST API Specification](api-specification.md) | FastAPI endpoints, JSON requests and responses, Pydantic validation and API testing |
| [Database Design](database-design.md) | SQLite schema, data integrity, CRUD operations and database testing |
| [Entity Relationship Diagram](database-erd.png) | ERD showing the assignments table and its seven fields |
| [System Architecture Diagram](system-architecture.png) | Overview of the frontend, backend and database architecture |

## Implementation Status

The SQLite database and FastAPI REST endpoints have been implemented and independently tested.

**Backend testing:** 17 automated tests passed (9 SQLite and 8 FastAPI).

Frontend–backend integration is pending.

## Technology Stack

Python · FastAPI · Pydantic · SQLite · pytest · HTML · CSS · JavaScript
