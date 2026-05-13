---
description: Plan a .NET feature — runs codebase analysis and NuGet research, then delegates to dotnet-planner to produce a structured plan with API design, EF schema, DI registrations, and task list.
---

Follow the workflow defined in `.claude/skills/dotnet-plan/SKILL.md` exactly.

Feature / task: $ARGUMENTS

---

## Execution Order

### Step 0 — Research & Reuse (run 0a + 0b in parallel, then 0c)

**0a — Existing codebase analysis** (parallel with 0b)
Launch **dotnet-analyzer** agent:
- Map existing layers, naming conventions, reusable services and base classes
- Identify existing entities related to the feature

**0b — NuGet package search** (parallel with 0a)
Run directly:
```bash
dotnet search <feature-keyword>
```
Return: candidate NuGet packages with versions and purpose

**0c — Reuse decision** (after 0a + 0b complete)
Decide: use existing NuGet / extend existing code / write from scratch.

---

### Step 1 — Plan (after Step 0 is complete)

Launch **dotnet-planner** agent with:
- Feature: $ARGUMENTS
- Analysis findings from Step 0a
- NuGet candidates from Step 0b
- Reuse decision

Produce plan at `<TARGET_REPO>/doc/plan_<feature-name>.md` with all 5 sections:
1. PRD, 2. Architecture, 3. System Design, 4. DI Registrations, 5. Task List

---

### Step 2 — Skills Gate

1. **Skill: git-commit** — (`docs: add implementation plan for <feature>` / `subagent: dotnet-planner`)

$ARGUMENTS
