# Tria Home

> **AI-powered property repair triage — from “something is wrong” to knowing what to do next.**

Tria Home is a focused AI assistant for diagnosing and resolving **home and property maintenance problems**.

When something breaks, leaks, comes loose, makes an unusual noise, or stops working, the user should not need to know the technical name of the fault or which trade to call.

Show Tria the problem using a description, photo, video, or audio. Tria investigates the issue, gathers additional evidence when needed, identifies likely causes, applies safety controls, and helps determine what to do next.

The goal is:

> **Problem discovered → problem understood → appropriate resolution**

## See. Snap. Sort.

**See** — notice a problem in the property.

**Snap** — show Tria what is happening.

**Sort** — understand the problem and move towards the appropriate resolution.

---

## How Tria Works

```text
Something is wrong
        ↓
Describe and show the problem
        ↓
Tria investigates
        ↓
Enough evidence?
   ├── No → Request targeted evidence
   │              ↓
   │         Continue investigation
   │
   └── Yes
        ↓
Likely diagnosis
        ↓
Safety check
        ↓
   ┌───────────────┐
   ↓               ↓
Safe DIY      Professional
   ↓               ↓
Parts/tools     Correct trade
   ↓               ↓
Repair guide    Repair report
   └───────┬───────┘
           ↓
       Resolution
```

Tria is designed to **investigate before guessing**. If the available evidence is not sufficient, it asks for the next useful photo, video, audio, measurement, or answer rather than forcing a diagnosis.

Safety can interrupt this process at any point.

---

## Product Scope

Tria is specifically designed for **property maintenance and repair**.

This includes areas such as:

- plumbing and drainage;
- heating and hot water;
- doors, windows, locks and fittings;
- damp, mould and water ingress;
- walls, ceilings and flooring;
- selected household appliance faults;
- electrical warning signs, subject to strict safety controls;
- other property maintenance problems.

Tria is **not a general-purpose AI assistant**. Requests outside the property-maintenance domain are rejected rather than passed through to an unrestricted AI.

---

## V0.1

The first version focuses on proving one complete repair journey rather than building the entire future platform.

The first end-to-end test case is:

> **A leaking or loose under-sink waste connection.**

This allows Tria to develop and test the core experience:

**evidence → investigation → diagnosis → safety → resolution**

Once this works reliably, the same approach can expand to other property-maintenance problems.

---

## Documentation

More detailed project information is kept separately:

- **[Product](docs/product.md)** — product vision, users, scope, principles and V0.1.
- **[Architecture](docs/architecture.md)** — Repair Cases, evidence, investigation, diagnosis, safety and system structure.
- **[Development](docs/development.md)** — local setup, testing, running the application and development workflow.

---

## Status

🚧 **Tria Home is currently in early development.**

The current focus is building and testing the core property-repair investigation and diagnostic workflow.

---

## Contact

Questions, feedback, or interested in Tria Home?

📧 **triahome@gmail.com**