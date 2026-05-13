---
description: Implement a .NET feature — delegates to dotnet-backend-developer and/or dotnet-frontend-developer based on scope. Both agents read the plan file. Frontend and backend launch in parallel when independent.
---

Follow the workflow defined in `.claude/skills/dotnet-coding/SKILL.md` exactly.

Feature / task: $ARGUMENTS

---

## Step 0 — Ask Scope (once, before starting)

Ask:
```
Scope for: $ARGUMENTS
  [F] Frontend only (Blazor / Razor / MVC views)
  [B] Backend only  (API / EF / services)
  [A] Both frontend and backend
```

---

## Step 1 — Launch Agent(s)

### Backend (scope B or A)

Launch **dotnet-backend-developer** agent:
- Task: $ARGUMENTS
- Plan: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Implements: Domain → Application (CQRS) → Infrastructure (EF + migration) → API layer → tests

### Frontend (scope F or A)

Launch **dotnet-frontend-developer** agent:
- Task: $ARGUMENTS
- Plan: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Implements: Blazor components → forms + validation → JS interop (if needed) → tests

**Parallelism:** Launch both agents simultaneously when frontend does not depend on new backend types.

---

## Step 2 — Skills Gate (after each agent completes)

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Verify XML doc comments on public APIs and components
3. **Skill: git-commit** — (`feat: <description>` / `subagent: dotnet-backend-developer` or `dotnet-frontend-developer`)

$ARGUMENTS
