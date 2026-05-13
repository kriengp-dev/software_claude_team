---
name: dotnet-plan
description: Feature planning workflow for .NET projects. Enforces codebase exploration and research before implementation, then delegates to dotnet-planner to produce structured planning documents covering API design, EF Core schema, DI registration, and implementation steps.
---

## When to Use

- Before implementing any new .NET feature that touches more than one layer
- Before adding a new entity, API endpoint, or Blazor component set
- When the architecture impact is unclear
- Before any database schema change (EF migration)

---

## Workflow

### Step 0 — Research & Reuse (Mandatory)

**Do not plan until this step is complete.**

Run Steps 0a and 0b in parallel, then 0c after both finish.

#### 0a — Existing Codebase Analysis

Launch **dotnet-analyzer** agent on the target repo:
- Map existing layers, naming conventions, and patterns in use
- Identify reusable services, repositories, or base classes
- Find existing entities related to the feature

#### 0b — NuGet / External Package Search

Search for proven .NET libraries before writing from scratch:

```bash
# Check NuGet for existing packages
dotnet search <keyword>
# or search https://www.nuget.org
```

Look for:
- MediatR, FluentValidation, AutoMapper, Mapster (application layer)
- Polly, Refit, RestSharp (HTTP clients)
- Hangfire, Quartz.NET (background jobs)
- SignalR, gRPC (real-time / RPC)

#### 0c — Reuse Decision

After 0a + 0b, decide explicitly:

| Decision | Condition |
|----------|-----------|
| **Use existing library** | A NuGet package covers ≥ 80% of requirements |
| **Extend existing code** | Similar feature already exists in the repo |
| **Write from scratch** | No suitable option after search |

---

### Step 1 — Plan

Launch **dotnet-planner** agent with:
- Feature description from `$ARGUMENTS`
- Analysis findings from Step 0a (existing patterns, reusable code)
- NuGet candidates from Step 0b

The plan must include all 5 sections:
1. PRD (requirements, user story, success criteria)
2. Architecture (layers affected, files to create/modify)
3. System Design (API contract, DB schema, EF config, sequence diagrams)
4. DI Registrations (all `builder.Services.Add*` calls)
5. Task List (phased, ordered, with risk levels)

**Output:** `<TARGET_REPO>/doc/plan_<feature-name>.md`

---

## Mandatory Skills Gate (Pre-Commit)

After the plan file is written:

1. **Invoke `Skill: git-commit`** — branch rules, commit message format

---

## Commit Format

```
docs: add implementation plan for <feature-name>
subagent: dotnet-planner
```

---

## Key Principles

1. **Research before plan** — Step 0 is mandatory; no plan without codebase analysis
2. **Reuse over rewrite** — check existing code and NuGet packages first
3. **Migration-aware** — every schema change must include EF migration in the task list
4. **Layer-correct** — plan must respect existing Clean Architecture boundaries
