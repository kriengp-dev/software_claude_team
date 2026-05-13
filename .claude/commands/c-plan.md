---
description: Run the full feature planning workflow for an embedded C/C++ project. Enforces Research & Reuse (Step 0) before delegating to c-planner. Never skips research.
---

**Always follow this exact sequence. Do not start planning without completing Step 0.**

Follow the workflow defined in `.claude/skills/c-plan/SKILL.md` exactly.

Feature / task: $ARGUMENTS

---

## Execution Order

### Step 0 — Research & Reuse (run 0a + 0b in parallel, then 0c)

**0a — Vendor documentation** (parallel with 0b)
Launch **deep-research-specialist** agent:
- Find MCU datasheet, reference manual, application notes, and errata for any hardware-facing part of the feature
- Return: key register names, API functions, timing constraints, known errata

**0b — GitHub code search** (parallel with 0a)
Run directly:
```bash
gh search repos "<feature keyword> embedded C" --language C --sort stars
gh search code "<relevant function or pattern>" --language C
```
Return: list of candidate libraries or BSP examples with URLs and star counts

**0c — Existing codebase analysis** (after 0a + 0b complete)
Launch **c-analyser** agent on the target repo:
- Find any existing module, driver, or utility that overlaps with the feature
- Map where the new feature fits in the current layer structure
- Identify reusable patterns already in the codebase

After all three: make the reuse decision (port / extend / write from scratch) and document it.

---

### Step 1 — Plan (after Step 0 is complete)

Launch **c-planner** agent with:
- Feature description: $ARGUMENTS
- Research findings from Step 0a (vendor docs, errata)
- Candidate libraries from Step 0b (if any)
- Codebase analysis from Step 0c (existing patterns, layer structure)
- Reuse decision from Step 0

Produce a single plan file at `<target-repo>/doc/plan_<feature-name>.md` containing all 5 sections:
1. PRD
2. Architecture
3. System Design
4. Tech Doc (API Contract)
5. Task List

---

### Step 2 — Skills Gate (after plan file is written)

1. **Skill: git-commit** — branch rules, commit message format (`docs: add implementation plan for <feature>` + `subagent: c-planner`)

$ARGUMENTS
