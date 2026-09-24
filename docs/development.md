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
python3 -m pytest tests/test_main.py
```

For more detailed test output:

```bash
python3 -m pytest -v
```


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
   ├── No → fix and test again
   └── Yes
        ↓
Run and manually verify where appropriate
        ↓
Commit
```

Tests should verify behaviour rather than unnecessarily depending on implementation details.

This is particularly important for components such as the property issue gate and diagnostic engine, where the underlying implementation may change as Tria develops while the expected behaviour remains stable.


## Build

There is currently no separate compilation or packaging step for the V0.1 Python backend.

At this stage, the effective development validation step is:

```bash
python3 -m pytest
```

As the project grows, build, linting, type-checking, security checks and dependency-management commands can be added and automated through CI.


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
   ├── No → fix and test again
   └── Yes
        ↓
Run application
        ↓
Manual verification where appropriate
        ↓
Check Git changes
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

Review the files being committed before staging them:

```bash
git add .
git status
```

Then commit and push:

```bash
git commit -m "Describe the change"
git push
```


## Files That Must Not Be Committed

Do not commit:

- `.venv/`
- `.env`
- secrets or API keys
- `__pycache__/`
- `*.pyc`
- `.DS_Store`
- other machine-specific or generated files

These should be covered by `.gitignore`.

Always check:

```bash
git status
```

before committing.


## Project Structure

The current project is organised approximately as follows:

```text
Triahome/
├── app/
│   ├── ai.py
│   ├── main.py
│   ├── prompts.py
│   ├── safety.py
│   └── schemas.py
│
├── tests/
│   ├── test_main.py
│   └── test_ai.py
│
├── static/
├── templates/
├── docs/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

The structure will evolve as the application grows. Avoid introducing additional architectural layers until they solve a concrete problem in the developing application.


## Dependency Management

The project currently uses:

```text
requirements.txt
```

This is sufficient for the early V0.1 development phase.

As the dependency set grows, Tria Home should move towards explicit dependency and version management using:

```text
pyproject.toml
```

together with a lock file.

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
5. Separate API behaviour from diagnostic logic.
6. Avoid introducing AI calls where deterministic logic is sufficient.
7. Avoid premature architectural complexity.
8. Never commit secrets or local environment files.
9. Prefer reproducible development environments.
10. Keep the codebase in a working state at each commit.

The goal is not simply to add features quickly. Each development step should leave Tria Home with a clearer, testable foundation for the next step.