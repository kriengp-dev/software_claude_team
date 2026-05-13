---
name: c-plan
description: Feature planning workflow for embedded C/C++ projects. Enforces Research & Reuse before implementation, then delegates to c-planner to produce structured planning documents.
---

## When to Use

- Before implementing any new peripheral driver, middleware, or application feature
- Before refactoring that touches more than 3 files
- When it is unclear which files need to change
- When hardware-specific knowledge (datasheet, SDK, HAL) is needed before coding

---

## Workflow

### Step 0 — Research & Reuse (Mandatory)

**Do not start planning until this step is complete.**

Run Steps 0a and 0b in parallel, then 0c after both are done.

#### 0a — Vendor Documentation

Use **deep-research-specialist** agent to find:
- MCU datasheet and reference manual (register map, peripheral description, timing)
- Vendor SDK / HAL API documentation
- Application notes and errata relevant to the feature

Trigger: any peripheral driver or hardware-facing code.

#### 0b — GitHub Code Search

Search for existing embedded C implementations before writing anything new:

```bash
gh search repos "<peripheral> embedded C driver" --language C --sort stars
gh search code "<function_or_pattern>" --language C
```

Look for:
- Vendor BSP examples (STMicroelectronics, espressif, raspberrypi GitHub orgs)
- Proven open-source drivers that solve 80%+ of the problem

#### 0c — Existing Codebase Analysis

Use **c-analyser** agent to inspect the target repo:
- Find any existing driver, middleware, or utility that can be reused or extended
- Map the module structure to understand where the new feature fits
- Identify patterns (ring buffers, state machines, ISR handlers) already in use
- Check for shared variables or peripherals already claimed by another module

After 0a + 0b + 0c, decide explicitly:

| Decision | Condition |
|----------|-----------|
| **Port / wrap existing open-source** | A proven implementation exists and meets ≥ 80% of requirements |
| **Extend existing code in repo** | Similar driver already exists in the target repo (found by c-analyser) |
| **Write from scratch** | No suitable implementation found after exhaustive search |

Document the decision and its rationale in the plan.

---

### Step 1 — Plan First

Use **c-planner** agent with the research and analysis findings from Step 0.

The plan must include all of the following documents (sections within the single plan file):

#### 1a — PRD (Product Requirements Document)
- Feature name and one-line description
- User story: "As a [role], I need [capability] so that [outcome]"
- Functional requirements (what it must do)
- Non-functional requirements (timing, memory budget, ISR constraints, thread safety)
- Out of scope (what it explicitly does NOT do)
- Success criteria (measurable, testable)

#### 1b — Architecture
- Layer diagram: which layer this feature lives in (HAL / driver / middleware / application)
- New files to create (`.c` + `.h` pairs with paths)
- Existing files to modify (with reason)
- Dependencies: other modules, RTOS primitives, HAL functions this feature relies on
- Data flow: how data moves from hardware → driver → middleware → application

#### 1c — System Design
- Internal state machine (if applicable) — states, transitions, guards
- Interrupt / DMA design — ISR responsibilities, shared variables, critical sections
- Error handling strategy — return codes, fault states, recovery
- Resource usage — RAM estimate, stack depth, peripheral lock requirements

#### 1d — Tech Doc (API Contract)
Public API that will be exposed in the `.h` file:

```c
/**
 * @brief <function purpose>
 * @param[in]  <name> <description>
 * @param[out] <name> <description>
 * @return <return values and their meaning>
 */
<return_type> <module>_<verb>_<noun>(<params>);
```

For each public function: name, parameters, return type, error codes, thread-safety guarantee.

#### 1e — Task List (Implementation Order)

Ordered steps following TDD or implement-first, depending on team preference:

```
Phase 1 — Foundation
  [ ] Step 1: <action> (File: src/...) — Risk: Low/Med/High
  [ ] Step 2: <action> (File: src/...) — Depends on: Step 1

Phase 2 — Core Implementation
  [ ] Step 3: ...

Phase 3 — Integration & Test
  [ ] Step N: write unit tests for host
  [ ] Step N+1: hardware-in-the-loop verification
```

Each step must have: specific action, file path, dependency, risk level.

---

## Plan Output

Save all documents as sections within a single file:

```
<target-repo>/doc/plan_<feature-name>.md
```

---

## Plan File Format

```markdown
# Implementation Plan: [Feature Name]

**Date:** YYYY-MM-DD
**Target repo:** <path>
**Research summary:** <1-sentence finding from Step 0 — reuse decision included>

---

## PRD
...

## Architecture
...

## System Design
...

## Tech Doc (API Contract)
...

## Task List
...

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| ...  | ...        | ...    | ...        |
```

---

## Mandatory Skills Gate (Pre-Commit)

After the plan file is written, invoke before committing:

1. **Invoke `Skill: git-commit`** — branch rules, commit message format, PR process

---

## Commit Format

```
docs: add implementation plan for <feature>
subagent: c-planner
```

---

## Key Principles

1. **Research before plan** — Step 0 is mandatory; no plan without it
2. **Reuse over rewrite** — port a proven implementation when one exists
3. **Hardware-aware** — every plan accounts for ISR safety, stack limits, and timing
4. **Testable steps** — each task step must be independently compilable and testable
5. **Single file** — all 5 documents live in one plan file, not scattered across files
