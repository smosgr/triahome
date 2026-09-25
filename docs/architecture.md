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

The first implementation uses a simple web-to-backend diagnostic flow:

```text
User / Web App
      │
      ▼
Upload photo(s) + problem description
      │
      ▼
FastAPI Backend
      │
      ├── validate request
      ├── check property-repair scope
      └── receive / manage evidence
      │
      ▼
AI Diagnostic Service
      │
      ├── identify visible problem
      ├── assess safety risk
      ├── request additional evidence if necessary
      ├── suggest likely causes
      └── determine DIY vs professional
      │
      ▼
Structured JSON Response
      │
      ▼
Frontend
```

The frontend should not depend directly on free-form AI output.

The diagnostic service should return structured information that can be validated by the backend before it is presented to the user.

As Tria develops, this simple request flow will evolve into the fuller Repair Case and investigation architecture.


## The Repair Case

The **Repair Case** is the central object in Tria.

A conversation with the AI is not itself the case. Instead, each interaction adds information or evidence to the same Repair Case.

A Repair Case may eventually contain:

- original problem description;
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


## Core Components

### Property Issue Gate

The first application-level check determines whether the request belongs within Tria's property maintenance and repair scope.

Out-of-scope requests stop here rather than being passed to a general-purpose AI.


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


### Diagnostic Engine

The diagnostic engine analyses the available evidence and produces structured information such as:

- observed problem;
- likely causes;
- confidence;
- uncertainty;
- additional evidence required.

The rest of the application should consume structured diagnostic data rather than depend directly on free-form AI output.


### Safety

Safety is a separate system concern rather than simply part of the AI diagnosis.

Potential electrical, gas, structural, fire, flooding or other serious hazards must be capable of stopping the normal investigation or DIY path.

The diagnostic model should therefore not have sole authority to decide whether repair instructions are safe to provide.


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

The current backend is intentionally simpler than the target architecture:

```text
Client
   ↓
FastAPI
   ↓
DiagnosisRequest
   ↓
Property Issue Gate
   ↓
Mock Diagnostic Logic
   ↓
DiagnosisResponse
```

The current implementation establishes the basic:

- API boundary;
- request validation;
- property scope checking;
- structured response models;
- deterministic diagnostic behaviour.

The mock diagnostic logic allows these foundations to be developed without introducing AI model cost, variability or external dependencies too early.


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
9. **Do not add architectural complexity until it solves a real problem.**


## Planned Evolution

The architecture will expand incrementally as V0.1 develops.

The expected direction is:

```text
Request / Response Contracts
        ↓
Property Scope Gate
        ↓
Repair Case
        ↓
Image / Evidence Handling
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

This is a development direction rather than a fixed implementation specification.

Architecture decisions should be revisited as the real Tria workflow is built, tested and measured.