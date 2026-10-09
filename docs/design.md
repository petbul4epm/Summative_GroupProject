# Design and wireframe specification

Architecture: browser (HTML/CSS/JavaScript) → FastAPI REST API → SQLite. FastAPI serves the frontend from the same origin.

Assignment schema: id primary key; title required; description optional; due_date ISO date; status pending/completed; module optional; priority low/medium/high. One table, no learner accounts.

Student 2 screens are combined in a responsive single page: dashboard counters and completion progress at the top; add/edit form at left; filtered assignment list with expandable descriptions at right. At small widths the form and list stack. Editing fills the same form; cancel restores creation mode.

Use cases: create assignment; view details; edit assignment; toggle status; delete after confirmation. Overdue means pending with due_date earlier than the browser’s local calendar date. A due date of today is not overdue.

Flow: form → browser validation → JSON fetch POST/PUT → Pydantic validation → parameterised SQL → response → list refresh. User text uses textContent; no HTML injection from titles/descriptions.

Keyboard focus, labels, live status messages and mobile rules are implemented; manual accessibility validation remains required. No WCAG conformance claim.
