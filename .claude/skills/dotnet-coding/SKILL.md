---
name: dotnet-coding
description: .NET implementation workflow. Delegates frontend work to dotnet-frontend-developer and backend work to dotnet-backend-developer. Both agents receive the plan as input and work in parallel when their tasks are independent. Applies dotnet format and git-commit after implementation.
---

## When to Use

- Implementing a planned .NET feature (after dotnet-plan has been run)
- Writing new ASP.NET Core endpoints, EF entities, Blazor components, or services
- Adding tests for existing code

---

## Pre-flight: Determine Scope

If `<SCOPE>` was passed as input (e.g. from `dotnet-development-workflow`), use it directly — do not ask again.

Otherwise ask once:

```
Does this feature require:
  [F] Frontend only (Blazor / Razor / MVC views)
  [B] Backend only  (API / EF Core / services)
  [A] Both frontend and backend
```

Store as `<SCOPE>`.

---

## Workflow

### If `<SCOPE>` = B or A — Launch dotnet-backend-developer

Launch **dotnet-backend-developer** agent with:
- Task: `$ARGUMENTS`
- Plan file: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- The agent implements: Domain entities, Application commands/queries/handlers,
  Infrastructure repositories + EF configuration + migration, API controllers or Minimal API endpoints, Unit tests

### If `<SCOPE>` = F or A — Launch dotnet-frontend-developer

Launch **dotnet-frontend-developer** agent with:
- Task: `$ARGUMENTS`
- Plan file: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- The agent implements: Blazor components, Razor Pages, MVC views, JS interop, validation

### Parallelism Rule

| Condition | Execution |
|-----------|-----------|
| Backend and frontend are independent (no shared new types) | Launch **both agents in parallel** |
| Frontend depends on backend types/DTOs not yet written | Backend first → then frontend |

---

## Steps Each Agent Follows

| Step | Backend Agent | Frontend Agent |
|------|--------------|----------------|
| 0 | Confirm target repo + read plan | Confirm target repo + read plan |
| 1 | Explore solution structure | Explore existing components |
| 2 | Implement Domain layer | Design component hierarchy |
| 3 | Implement Application layer (CQRS) | Implement Blazor components |
| 4 | Implement Infrastructure + migration | Add forms + validation |
| 5 | Implement API layer | Add JS interop (if needed) |
| 6 | Write unit tests | Self-review checklist |
| 7 | Self-review | Run build + tests |
| 8 | Skills gate → commit | Skills gate → commit |

---

## Mandatory Skills Gate (Pre-Commit)

After each agent completes, invoke in order:

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Verify XML doc comments on all public APIs and components
3. **Invoke `Skill: git-commit`** — branch rules, commit message format

---

## Commit Format

```
feat: <description>
subagent: dotnet-backend-developer   ← or dotnet-frontend-developer

<optional body>
```

---

## Key Principles

1. **Agent-first** — never implement inline; always delegate to the appropriate agent
2. **Parallel when safe** — launch backend and frontend agents together when independent
3. **Plan-driven** — both agents read the plan file; never implement from the prompt alone
4. **Migration required** — backend agent must create and verify EF migration before committing
5. **Tests required** — both agents add tests before committing
