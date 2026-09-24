# Tria Home — Product

This document defines the product direction, users, scope and initial version of Tria Home.

Tria Home is an AI-powered assistant designed specifically for **home and property maintenance problems**.

The goal is simple:

> **Problem discovered → problem understood → appropriate resolution**


## The Problem

Property problems often begin with uncertainty.

Someone may know:

> "There is water leaking under my sink."

but they may not know:

- where the water is coming from;
- what the component is called;
- whether the problem is serious;
- whether they can fix it themselves;
- what part they need;
- or which professional they should contact.

This creates unnecessary uncertainty, delays and potentially unnecessary contractor call-outs.

Tria aims to bridge the gap between **noticing a problem** and **knowing what to do about it**.


## The Tria Experience

The user should not need technical knowledge to use Tria.

They simply:

1. describe what is happening;
2. show Tria the problem using photos, video or audio where useful;
3. answer targeted questions or provide additional evidence when needed;
4. receive a likely explanation of the problem;
5. understand any relevant safety concerns;
6. receive an appropriate route towards resolution.

Depending on the problem, that resolution may be:

**Safe DIY**

→ identify the relevant component  
→ identify parts, materials or tools  
→ provide appropriate repair guidance

or:

**Professional help**

→ identify the appropriate trade  
→ prepare useful information about the problem  
→ generate a Tria Repair Report


## Working Motto

> # **See. Snap. Sort.**

**See** — notice a problem in the property.

**Snap** — show Tria what is happening.

**Sort** — understand the problem and move towards the appropriate resolution.


## Who Tria Is For

### Homeowners

A homeowner discovers a problem but does not know what it is, whether it is dangerous, whether they can repair it, what part they need, or which professional to contact.

Tria helps them understand the problem and determine what to do next.


### Tenants

A tenant can use Tria to investigate and clearly document a maintenance problem.

Where appropriate, the resulting information could eventually be provided directly to their landlord, letting agent or property manager.


### Landlords

A landlord can receive better information about a problem before deciding whether a contractor needs to attend.

This could help reduce unnecessary diagnostic call-outs and improve the information provided to contractors.


### Property Managers & Letting Agents

Tria could eventually provide the first level of maintenance triage before a case reaches a human property manager.

The aim is not simply to automate reporting, but to improve the quality of the information gathered before human intervention is required.


### Contractors

Contractors are primarily downstream users.

Instead of receiving:

> "The sink is broken."

they could eventually receive a structured Tria Repair Report containing useful evidence and information gathered during the investigation.


## Product Principles

### 1. Investigate Before Guessing

Tria should not confidently diagnose a problem simply because a user submitted one image.

If there is not enough evidence, Tria should ask for the **next useful piece of information**.

For example:

> "Take a wider photo showing the pipework under the sink."

> "Take a close-up of this connection."

> "Record a short video while the problem occurs, if it is safe to do so."

The experience should therefore feel like a guided investigation rather than a single AI question and answer.


### 2. Safety Before Repair

Safety is part of the product, not a disclaimer added afterwards.

Potential gas, electrical, structural, fire, flooding or other serious hazards must be capable of stopping the normal DIY journey.

Where appropriate, Tria should provide conservative immediate safety guidance and direct the user towards professional help.


### 3. Show, Don't Just Tell

Where useful, Tria should visually identify the component or area it is discussing.

For example, Tria may highlight:

- a suspected leaking joint;
- damaged seal;
- loose fitting;
- relevant pipe;
- suspicious component.

Visual explanations should help the user understand the diagnosis rather than imply certainty that does not exist.


### 4. Keep Uncertainty Visible

Tria should distinguish between:

- what it can observe;
- what it believes is likely;
- what remains uncertain;
- what additional evidence could help.

A possible cause should not be presented as a confirmed fault unless the available evidence supports that conclusion.


### 5. Focus on Resolution

Tria is not intended to be an open-ended chatbot.

Each interaction should move the Repair Case closer to an outcome.

> **Understand → Decide → Act → Resolve**


## Product Scope

Tria is specifically focused on **property maintenance and repair**.

Examples include:

- plumbing and drainage;
- heating and hot water;
- doors, windows, handles and locks;
- damp, mould and water ingress;
- walls, ceilings and flooring;
- fixtures and fittings;
- selected household appliance faults;
- electrical warning signs, subject to strict safety controls;
- other property maintenance problems.

Tria should reject requests outside this domain rather than becoming a general-purpose AI assistant.


# V0.1

The first version of Tria should prove **one complete repair journey**.

The aim is not to build the entire future property-maintenance platform at once.

The first end-to-end use case is:

> **A leaking or loose under-sink waste connection.**


## Why Start Here?

An under-sink leak provides a useful first test because it can exercise many of the capabilities Tria will eventually require:

- understanding a user's description;
- analysing visual evidence;
- requesting additional evidence;
- identifying components;
- suggesting likely causes;
- representing uncertainty;
- assessing safety;
- identifying parts;
- providing repair guidance;
- reaching a resolution.

It allows us to develop the investigation experience without starting with a high-risk gas or electrical problem.


## V0.1 User Journey

A successful first version should allow a user to:

1. start a property repair case;
2. describe the problem;
3. take or upload a photo;
4. have Tria determine whether the problem is within its scope;
5. have Tria analyse the available evidence;
6. provide additional evidence when specifically requested;
7. receive a likely diagnosis with uncertainty represented appropriately;
8. understand which component or area Tria is referring to;
9. pass through appropriate safety checks;
10. be directed towards DIY or professional help;
11. receive likely parts/tools and repair guidance when DIY is appropriate;
12. receive the appropriate trade and useful repair information when professional help is required.


## Not in V0.1

To keep the first version focused, V0.1 will not attempt to build:

- a proprietary contractor marketplace;
- contractor ratings or vetting;
- contractor scheduling;
- payments;
- automated landlord approval workflows;
- full property-management dashboards;
- property portfolio management;
- native iOS or Android applications;
- AI telephone support;
- deep property-management platform integrations;
- preventive maintenance programmes;
- general-purpose DIY or home-improvement assistance unrelated to a fault.

These may become future layers around the core Tria diagnostic experience.


## Future Direction

Once the core investigation and resolution experience works reliably, Tria could expand into broader property-maintenance workflows.

For example, a tenant could eventually:

```text
Report a problem
      ↓
Receive a secure Tria link
      ↓
Describe and show the problem
      ↓
Complete the AI investigation
      ↓
Problem resolved safely
      OR
Structured case sent to landlord / agent
      ↓
Contractor receives useful repair information
```

Other interfaces could eventually include:

- mobile applications;
- AI voice or telephone reporting;
- landlord and property-manager workflows;
- contractor integrations;
- retailer integrations;
- property-management software integrations.

These are future opportunities rather than requirements for the first product.


## Product Success

The early success of Tria should not be measured by how many features it contains.

The important question is:

> **Can Tria take a real property problem that a non-expert does not understand and safely move it closer to resolution with less unnecessary human intervention?**

If Tria can consistently do that, additional channels, integrations and commercial services can be built around the core experience.