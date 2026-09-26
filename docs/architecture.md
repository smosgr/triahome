# Tria Home — Architecture

This document describes the high-level architecture of Tria Home.

It is intentionally concise and will evolve alongside the product.

The core architectural goal is:

> **Understand the property problem, gather the right evidence, protect the user, and determine the right next action.**


## High-Level Architecture

Tria is designed around a **Repair Case** rather than a single AI conversation.

A problem may require several pieces of evidence before it can be diagnosed safely.

```text
User / Client
      ↓
Property Issue Gate
      ↓
Repair Case
      ↓
Evidence Collection ←────────────┐
      ↓                          │
Investigation                    │
      ↓                          │
Enough evidence? ─── No ─────────┘
      ↓ Yes
Likely Diagnosis
      ↓
Safety Gate
      ↓
 ┌──────────────────┐
 ↓                  ↓
Safe DIY       Professional
 ↓                  ↓
Parts / Tools   Correct Trade
 ↓                  ↓
Repair Guide    Repair Report
 └─────────┬────────┘
           ↓
       Resolution
```

Safety checks may interrupt the normal flow earlier if the description or evidence indicates an immediate hazard.


## V0.1 Request Flow

Tria is being built around a persistent Repair Case.

The current backend flow is:

```text
User / Client
      │
      ▼
Problem Description
      │
      ▼
FastAPI Backend
      │
      ├── validate request
      └── check property-repair scope
      │
      ▼
Repair Case
      │
      ├── unique ID
      ├── status
      ├── creation timestamp
      └── evidence
      │
      ▼
Repository Layer
      │
      ▼
SQLAlchemy
      │
      ▼
SQLite
```

Evidence can be added to an existing Repair Case and retrieved in later requests.

Repair Cases and their evidence persist across application restarts.

The next stage expands this flow to support image evidence and investigation:

```text
Repair Case
      ↓
Evidence Collection
      ↓
Investigation
      ↓
AI Diagnostic Service
      ↓
Safety Gate
      ↓
Structured Result
```

The frontend should not depend directly on free-form AI output.

Diagnostic services should return structured information that can be validated by the backend before it is presented to the user.


## The Repair Case

The **Repair Case** is the central object in Tria.

A conversation with the AI is not itself the case. Instead, each interaction adds information or evidence to the same Repair Case.

A Repair Case currently contains:

- a unique identifier;
- original problem description;
- status;
- creation timestamp;
- collected text evidence.

As the investigation model develops, a Repair Case may also contain:

- photos, video and audio;
- observations;
- questions and answers;
- requested additional evidence;
- likely causes and confidence;
- uncertainty;
- safety information;
- parts, materials and tools;
- repair guidance or required professional trade;
- final outcome.

This allows Tria to investigate a problem progressively rather than treating every interaction as a completely new request.


## Persistence Architecture

Repair Cases must persist across requests and application restarts.

Tria therefore separates the application and API models from the persistence implementation:

```text
FastAPI
   ↓
Repository Layer
   ↓
SQLAlchemy
   ↓
SQLite
```

### Development Database

The current development database is SQLite.

The local database file is:

```text
data/tria.db
```

SQLite provides persistent relational storage without requiring a separate database server during early development.

The `data/` directory is excluded from Git and must not contain committed application or user data.

SQLite is a development persistence implementation rather than a permanent infrastructure constraint.

SQLAlchemy provides the database abstraction layer so the persistence implementation can later migrate to a production relational database such as PostgreSQL without coupling the API directly to SQLite.


### Current Data Model

The current persisted entities are:

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

`evidence.case_id` is a foreign key referencing `repair_cases.id`.

A Repair Case can therefore accumulate multiple evidence records over time.


### Models and Schemas

Tria deliberately separates API contracts from database models.

```text
app/schemas.py
      ↓
Pydantic API models

app/models.py
      ↓
SQLAlchemy persistence models
```

Pydantic models define the data accepted and returned by the API.

SQLAlchemy models define how application data is persisted.

The repository layer in:

```text
app/cases.py
```

translates between these representations.

Database engine and session configuration are defined in:

```text
app/database.py
```


### Database Sessions

SQLAlchemy sessions provide the application's working connection to the database.

Repository operations open a session, perform the required database operation, commit changes where necessary, and return application-level models to the rest of Tria.

This keeps database-specific behaviour out of the API endpoints as much as practical.


### Schema Creation and Migrations

During the current early development stage, missing database tables are created using:

```python
Base.metadata.create_all(bind=engine)
```

This creates tables that do not yet exist, but it is not a full database migration system.

As the schema becomes more mature and existing tables need controlled changes, Tria is expected to introduce explicit database migrations, likely using Alembic.


### Time Handling

Repair Case creation timestamps are generated in UTC.

The API exposes timezone-aware timestamps even where the local SQLite implementation does not preserve timezone metadata in the same way as a production database may.

UTC is the application-level timestamp convention.


## Core Components

### Property Issue Gate

The first application-level check determines whether the request belongs within Tria's property maintenance and repair scope.

Out-of-scope requests stop here rather than being passed to a general-purpose AI.

The current implementation uses deterministic scope checking.

This is intentionally simple and can later be replaced by a more capable classification mechanism without changing the overall Repair Case workflow.


### Evidence & Investigation

Tria should **investigate before guessing**.

A description or single image may not provide enough evidence for a reliable diagnosis.

When more information is required, Tria should request the most useful next piece of evidence.

```text
Analyse current evidence
       ↓
Enough evidence?
  ├── Yes → Continue
  │
  └── No → Request targeted evidence
                ↓
         Add to Repair Case
                ↓
            Analyse again
```

Additional evidence could include another photo, a different angle, video, audio, a measurement, or an answer to a targeted question.

Text evidence can already be attached to and persisted against a Repair Case.

The investigation loop itself has not yet been implemented.


### Diagnostic Engine

The diagnostic engine analyses the available evidence and produces structured information such as:

- observed problem;
- likely causes;
- confidence;
- uncertainty;
- additional evidence required.

The rest of the application should consume structured diagnostic data rather than depend directly on free-form AI output.

The current diagnostic implementation is deterministic mock logic.

Real AI integration will be introduced after the Repair Case and evidence contracts are sufficiently established.


### Safety

Safety is a separate system concern rather than simply part of the AI diagnosis.

Potential electrical, gas, structural, fire, flooding or other serious hazards must be capable of stopping the normal investigation or DIY path.

The diagnostic model should therefore not have sole authority to decide whether repair instructions are safe to provide.

The full safety decision layer has not yet been implemented.


### Resolution

Once sufficient evidence exists and safety checks have been applied, Tria determines the appropriate next action.

There are two main paths:

```text
Safe + suitable for DIY
       ↓
Parts / Tools
       ↓
Repair Guidance

OR

Professional intervention required
       ↓
Correct Trade
       ↓
Tria Repair Report
```


## Evidence Storage

Text evidence is currently stored as structured data in the relational database.

Binary evidence such as images, video and audio should not be stored directly in the relational database.

The intended architecture is:

```text
Repair Case
     │
     ▼
Evidence Metadata
     │
     ├── evidence ID
     ├── case ID
     ├── evidence type
     ├── media metadata
     └── storage key
              │
              ▼
        Object Storage
```

During development, binary evidence can use local filesystem storage.

The intended production evolution is object storage such as Amazon S3 or an equivalent service.

The database should store a **storage key** rather than depend on a local filesystem path or permanent public URL.

Conceptually:

```text
Development                     Production

SQLite                          PostgreSQL
   │                                │
evidence metadata               evidence metadata
   │                                │
storage_key                      storage_key
   │                                │
   ▼                                ▼
Local Storage                   Object Storage
data/uploads/...                S3 / equivalent
```

This separation allows the storage implementation to change without changing the fundamental Repair Case or Evidence contracts.

It also allows storage, retention and retrieval costs to be considered independently from the relational data model.


## Structured Data

Communication between the diagnostic system, backend and frontend should use structured data.

Conceptually, a diagnosis may contain:

```text
Diagnosis
│
├── Problem
│   ├── category
│   ├── summary
│   └── confidence
│
├── Safety
│   ├── risk level
│   ├── hazards
│   └── immediate action
│
├── Likely Causes
│
├── Additional Evidence Needed
│
├── Resolution
│   ├── safe to DIY
│   ├── professional required
│   └── recommended action
│
├── Parts / Tools
│
└── Repair Steps
```

Using structured contracts allows the diagnostic engine to evolve without tightly coupling the frontend to a particular AI model.


## Current Implementation

The current backend establishes the first persistent Repair Case workflow.

```text
Client
   ↓
FastAPI
   │
   ├─────────────────┐
   ↓                 ↓
Diagnosis API     Repair Case API
   │                 │
   ↓                 ├── create case
Property Gate        ├── retrieve case
   │                 └── add text evidence
   ↓                         │
Mock Diagnosis               ↓
                       Repository Layer
                              ↓
                          SQLAlchemy
                              ↓
                            SQLite
```

The current implementation provides:

- request validation;
- property-repair scope checking;
- structured diagnostic response models;
- deterministic mock diagnostic behaviour;
- persistent Repair Case creation;
- persistent Repair Case retrieval;
- UTC creation timestamps;
- persistent text evidence collection;
- one-to-many Repair Case → Evidence persistence;
- repository-based database access;
- SQLite local development storage;
- isolated database integration testing.

Repair Cases and their evidence persist across application restarts.

The diagnostic engine remains deterministic at this stage.

This allows the Repair Case, evidence and persistence architecture to be established and tested before introducing AI model cost, variability and external dependencies.

The following major capabilities are not yet implemented:

- image evidence upload and storage;
- investigation/evidence-sufficiency loop;
- AI-based diagnosis;
- full safety decision layer;
- visual annotations;
- parts and tool recommendations;
- complete DIY guidance;
- professional escalation workflow.


## Testing Architecture

Testing is part of the application architecture rather than an afterthought.

The test suite currently covers application logic, API behaviour and database persistence.

The intended separation is:

```text
tests/
├── unit/
├── functional/
└── integration/
```

Unit tests cover isolated application logic.

Functional/API tests validate behaviour across API requests.

Integration tests validate boundaries such as database persistence.

Database integration tests use isolated temporary SQLite databases rather than the development database at:

```text
data/tria.db
```

This prevents automated tests from modifying development data.

The full automated test suite should remain green before development changes are considered complete.


## AI & Cost Considerations

Tria's investigation process may require several rounds of evidence.

Each AI model call can introduce:

- token usage;
- latency;
- infrastructure cost.

The architecture should therefore avoid unnecessarily treating every follow-up answer, photo or video as a completely new diagnosis.

The intended principle is:

```text
Existing Repair Case
       +
New Evidence
       ↓
Targeted Analysis
```

The exact approach to model selection, context management, caching and incremental analysis has **not yet been decided**.

These decisions should be made when the AI layer is implemented and measured rather than fixed prematurely.

Binary evidence also introduces infrastructure costs beyond AI inference, including:

- object storage;
- storage requests;
- retrieval;
- data transfer;
- image or video processing;
- retention.

These costs should eventually be evaluated at the Repair Case level rather than considering individual infrastructure prices in isolation.


## Architectural Principles

As Tria develops:

1. **The Repair Case is the source of investigation state.**
2. **Investigate before diagnosing.**
3. **Keep uncertainty visible.**
4. **Safety is independent of model confidence.**
5. **Use structured contracts between components.**
6. **Keep Tria within its property-repair scope.**
7. **Avoid unnecessary model calls and token usage.**
8. **Keep components replaceable where practical.**
9. **Separate structured data from binary evidence storage.**
10. **Keep development infrastructure portable toward production where practical.**
11. **Do not add architectural complexity until it solves a real problem.**


## Planned Evolution

The initial backend foundation is now established:

```text
Request / Response Contracts       ✓
        ↓
Property Scope Gate                ✓
        ↓
Repair Case                        ✓
        ↓
Persistent Relational Storage      ✓
        ↓
Text Evidence                      ✓
```

Development can now continue from that foundation:

```text
Image Evidence
      ↓
Local Evidence Storage
      ↓
Storage Abstraction
      ↓
Investigation Loop
      ↓
AI Integration
      ↓
Safety Layer
      ↓
Visual Annotations
      ↓
Parts / Tools
      ↓
DIY Guidance
      OR
Professional Escalation
```

The local evidence-storage implementation should preserve a storage contract that can later move to production object storage such as S3 or an equivalent service.

Likewise, SQLite is a development persistence implementation rather than a permanent infrastructure constraint.

The repository and SQLAlchemy layers are intended to make migration to a production relational database such as PostgreSQL manageable.

As the database schema evolves, explicit database migrations will eventually replace automatic table creation.

This remains a development direction rather than a fixed implementation specification.

Architecture decisions should continue to be revisited as the real Tria workflow is built, tested and measured.