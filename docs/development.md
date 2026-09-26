# Tria Home — Development Guide

This document describes how to set up, test, run, and contribute to the Tria Home codebase.

Tria Home is currently in early V0.1 development. The development process prioritises small, testable changes and a consistently working codebase.


## Prerequisites

The current Tria Home backend requires:

- Python 3.11
- `pip`
- a Python virtual environment
- Git

The project should be developed and run from within its virtual environment rather than using the system Python installation.

Postman is optional but useful for manual API testing.


## Initial Setup

Clone the repository and move into the project directory:

```bash
git clone https://github.com/smosgr/triahome.git
cd Triahome
```

Create the virtual environment using Python 3.11:

```bash
python3.11 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Verify that the correct Python environment is active:

```bash
python3 --version
which python3
```

The Python version should be 3.11 and the path should point inside the project:

```text
.../Triahome/.venv/bin/python3
```


## Virtual Environment

Activate the environment whenever starting a Tria Home development session:

```bash
source .venv/bin/activate
```

When activated, the terminal prompt should normally show:

```text
(.venv)
```

To leave the virtual environment:

```bash
deactivate
```

Do not install Tria Home dependencies into the system Python environment.

If `pip` reports that the Python environment is externally managed, first check that `.venv` is activated.

Do not use `sudo pip`, `--user`, or `--break-system-packages` as a workaround for normal project development.


## Testing

Automated tests are part of the normal Tria Home development workflow.

**Tests must be run before running/building the application and before committing significant changes.**

Run the complete test suite with:

```bash
python3 -m pytest
```

Use `python3 -m pytest` rather than calling `pytest` directly.

This ensures pytest runs using the Python interpreter from the active virtual environment rather than a globally installed version.

A successful test run should end with all tests passing:

```text
===================== all tests passed =====================
```

If any test fails, investigate and fix the failure before proceeding.

To run a specific test file:

```bash
python3 -m pytest tests/unit/test_main.py
```

For more detailed test output:

```bash
python3 -m pytest -v
```


## Test Organisation

The test suite is organised into three categories:

```text
tests/
├── unit/
├── functional/
└── integration/
```

### Unit Tests

Unit tests verify isolated application behaviour and logic.

Current unit tests include application logic and API behaviour while the test structure continues to evolve.

Examples include:

- property issue scope checking;
- deterministic diagnostic behaviour;
- request validation;
- Repair Case API behaviour;
- evidence API behaviour.

As the application grows, API-level tests can be moved into the functional test layer where appropriate.


### Functional Tests

Functional tests are intended to verify behaviour across application boundaries from the perspective of the API or user workflow.

The functional test structure has been created and will expand as V0.1 workflows become more complete.

Examples of future functional tests include:

```text
Create Repair Case
      ↓
Add evidence
      ↓
Investigate
      ↓
Receive structured result
```


### Integration Tests

Integration tests verify interaction with infrastructure or other implementation boundaries.

Current integration tests verify SQLAlchemy and SQLite persistence, including:

- Repair Case persistence;
- Evidence persistence;
- the Repair Case → Evidence relationship.

Database integration tests must use isolated temporary databases rather than the normal development database.

This prevents automated integration tests from modifying:

```text
data/tria.db
```

Temporary test databases are created through pytest's temporary filesystem support and discarded after the tests complete.


## Testing Philosophy

New behaviour should normally be accompanied by automated tests.

The preferred development cycle is:

```text
Define expected behaviour
       ↓
Write or update tests
       ↓
Implement the change
       ↓
Run the complete test suite
       ↓
Tests pass?
  ├── No → Fix and test again
  └── Yes
       ↓
Run and manually verify where appropriate
       ↓
Commit
```

Tests should verify behaviour rather than unnecessarily depending on implementation details.

This is particularly important for components such as the property issue gate, persistence layer, evidence handling and diagnostic engine, where the underlying implementation may change as Tria develops while the expected behaviour remains stable.

When a feature introduces a new persistence or infrastructure boundary, integration tests should be added where appropriate.


## Build

There is currently no separate compilation or packaging step for the V0.1 Python backend.

At this stage, the effective development validation step is:

```bash
python3 -m pytest
```

As the project grows, build, linting, type-checking, security checks and dependency-management commands can be added and automated through CI.


## Local Database

Tria Home currently uses SQLite for local relational persistence.

The development database is stored at:

```text
data/tria.db
```

No separate database server needs to be installed or started.

The current persistence path is:

```text
FastAPI
   ↓
Repository Layer
   ↓
SQLAlchemy
   ↓
SQLite
```

Database engine and session configuration are defined in:

```text
app/database.py
```

SQLAlchemy persistence models are defined in:

```text
app/models.py
```

Repair Case repository operations are defined in:

```text
app/cases.py
```

Pydantic API models remain defined separately in:

```text
app/schemas.py
```

This separation prevents API contracts from being directly tied to the database implementation.


### Current Database Model

The current database contains two related entities:

```text
repair_cases
├── id
├── description
├── status
└── created_at
      │
      │ one-to-many
      ▼
evidence
├── id
├── case_id
├── type
└── content
```

`evidence.case_id` references the Repair Case that owns the evidence.

Repair Cases and their associated evidence persist across application restarts.


### Database Creation

During the current early development stage, SQLAlchemy creates missing tables using:

```python
Base.metadata.create_all(bind=engine)
```

This is sufficient for establishing the initial local database.

However, `create_all()` is not a full migration system.

Changing an existing SQLAlchemy model does not mean an existing database table will automatically be migrated to the new structure.

As the data model becomes more mature, explicit schema migrations are expected to be introduced, likely using Alembic.


### Local Data

The `data/` directory is local application data and is ignored by Git.

To inspect it:

```bash
ls -lh data
```

The directory currently contains the SQLite development database and may later contain local binary evidence storage during development.

Do not commit the contents of `data/`.

Deleting:

```text
data/tria.db
```

deletes the local development data.

During the current development stage, the database can be recreated when the application starts, but local data should not be deleted if it needs to be retained.


## Run Locally

First activate the virtual environment if it is not already active:

```bash
source .venv/bin/activate
```

Run the tests:

```bash
python3 -m pytest
```

**Only after the tests pass**, start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Stop the development server with:

```text
Ctrl+C
```

Application data stored in SQLite remains available after the server is stopped and restarted.


## Manual API Testing

Postman can be used for manual API testing in addition to the automated test suite.

Postman is useful for:

- inspecting real request and response bodies;
- checking HTTP status codes;
- following a Repair Case through multiple requests;
- verifying persistence manually;
- exploring API behaviour while developing a feature.

Automated tests remain the primary source of truth. Postman complements them rather than replacing them.


### Local Postman Requests

When using Postman against:

```text
http://127.0.0.1:8000
```

the request must be sent through the local Postman Desktop Agent or desktop application.

A cloud-based agent cannot directly access the local development server.


### Example Repair Case Flow

Create a Repair Case:

```text
POST /cases
```

Example body:

```json
{
  "description": "The pipe under my kitchen sink is leaking."
}
```

The response contains the Repair Case ID.

Add text evidence:

```text
POST /cases/{case_id}/evidence
```

Example body:

```json
{
  "type": "text",
  "content": "The leak happens when the washing machine drains."
}
```

Retrieve the Repair Case:

```text
GET /cases/{case_id}
```

The response should contain the Repair Case and its associated evidence.


### Manual Persistence Check

A useful manual persistence check is:

```text
Create Repair Case
       ↓
Add Evidence
       ↓
Retrieve Case
       ↓
Stop Uvicorn
       ↓
Restart Uvicorn
       ↓
Retrieve same Case
```

The Repair Case and evidence should still exist after the application process restarts.

This verifies the behaviour of the real local application in addition to the automated database tests.


## Development Workflow

The normal local workflow is:

```text
Activate environment
       ↓
Pull latest changes
       ↓
Run existing tests
       ↓
Make changes
       ↓
Add/update tests
       ↓
python3 -m pytest
       ↓
Tests pass?
  ├── No → Fix and test again
  └── Yes
       ↓
Run application
       ↓
Manual verification where appropriate
       ↓
Check Git changes
       ↓
Stage intended files
       ↓
Commit
       ↓
Push
```

A typical development session therefore begins with:

```bash
source .venv/bin/activate
git pull
python3 -m pytest
```

Before committing:

```bash
python3 -m pytest
git status
```

Review the changes and stage only the files that should be included in the commit:

```bash
git add <files-you-want-to-commit>
git status
```

For example:

```bash
git add README.md docs/
git status
```

Then commit and push:

```bash
git commit -m "Describe the change"
git push
```

Using `git add .` is acceptable when intentionally staging all current changes, but reviewing and staging the intended files explicitly reduces the risk of accidentally committing local files or unrelated changes.


## Files That Must Not Be Committed

Do not commit:

- `.venv/`
- `.env`
- secrets or API keys
- `__pycache__/`
- `*.pyc`
- `.DS_Store`
- `data/`
- local databases;
- locally uploaded evidence;
- other machine-specific or generated files.

These should be covered by `.gitignore`.

The current local application data rule is:

```text
data/
```

which prevents the SQLite database and future local evidence storage from being tracked by Git.

Always check:

```bash
git status
```

before committing.

Environment configuration that needs to be shared with other developers should eventually be represented by a safe template such as `.env.example`, containing variable names and example values but no real secrets.


## Project Structure

The current project is organised approximately as follows:

```text
Triahome/
├── app/
│   ├── ai.py
│   ├── cases.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   ├── safety.py
│   └── schemas.py
│
├── data/
│   └── tria.db
│
├── tests/
│   ├── unit/
│   │   ├── test_ai.py
│   │   └── test_main.py
│   │
│   ├── functional/
│   │
│   └── integration/
│       └── test_database.py
│
├── static/
│   ├── app.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   └── product.md
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

The structure will evolve as the application grows.

The current separation is intentional:

```text
schemas.py      API/application data contracts
models.py       database persistence models
database.py     database configuration
cases.py        Repair Case persistence/repository operations
ai.py           scope and diagnostic logic
main.py         FastAPI endpoints
```

Avoid introducing additional architectural layers until they solve a concrete problem in the developing application.


## Evidence Storage Direction

Text evidence is currently persisted in SQLite.

Binary evidence such as images should not be stored directly as SQLite database blobs.

The planned development direction is:

```text
Repair Case
      ↓
Evidence Metadata
      ↓
storage_key
      ↓
Storage Implementation
```

During local development, binary evidence can be stored on the local filesystem, for example under:

```text
data/uploads/
```

The persistence model should use a storage key rather than tightly coupling evidence to an absolute local path.

This is intended to allow the storage implementation to evolve approximately as follows:

```text
Development                  Production

SQLite                       PostgreSQL
   │                             │
metadata                      metadata
   │                             │
storage_key                   storage_key
   │                             │
   ▼                             ▼
Local filesystem             Object storage
                             such as S3
```

The exact image evidence contract and storage implementation should be defined and tested when image evidence is introduced.


## Dependency Management

The project currently uses:

```text
requirements.txt
```

This is sufficient for the early V0.1 development phase.

Dependencies must be installed inside the active virtual environment.

When intentionally adding a dependency during the current phase, the environment can be updated and the dependency list regenerated:

```bash
python3 -m pip install <package>
python3 -m pip freeze > requirements.txt
```

Changes to `requirements.txt` should be reviewed before committing.


### Planned Dependency Management

The planned next step is to move towards explicit dependency and version management using:

```text
pyproject.toml
```

together with a lock file.

A tool such as `uv` may be used when this transition is made.

This will allow:

- direct dependencies to be distinguished from transitive dependencies;
- dependency versions to be managed deliberately;
- automated dependency updates;
- reproducible development and deployment environments;
- development dependencies to be separated from runtime dependencies.

Dependency-management automation can be introduced once the initial backend architecture has stabilised.


## Development Principles

During V0.1 development:

1. Keep changes small and testable.
2. Add or update tests alongside behavioural changes.
3. Run the complete test suite before running or committing.
4. Keep API contracts explicit using schemas.
5. Separate API contracts from persistence models.
6. Keep API behaviour separate from diagnostic logic.
7. Access persistent Repair Case data through a defined persistence/repository boundary.
8. Keep automated database tests isolated from development data.
9. Avoid introducing AI calls where deterministic logic is sufficient.
10. Keep binary evidence separate from relational data where practical.
11. Design local storage so it can evolve towards production infrastructure without unnecessary rewrites.
12. Avoid premature architectural complexity.
13. Never commit secrets, local databases, uploaded evidence or local environment files.
14. Prefer reproducible development environments.
15. Keep the codebase in a working state at each commit.

The goal is not simply to add features quickly. Each development step should leave Tria Home with a clearer, testable foundation for the next step.