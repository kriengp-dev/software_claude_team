---
name: dotnet-review
description: .NET code review workflow. Delegates to dotnet-reviewer agent to review for async correctness, EF Core anti-patterns, SOLID violations, security vulnerabilities, and Blazor-specific issues. MUST BE USED after any .NET code change.
---

## When to Use

- After dotnet-backend-developer or dotnet-frontend-developer writes or modifies code
- Before merging any branch into main
- After receiving .NET code from an external source

---

## Workflow

### Mandatory: Delegate to dotnet-reviewer Agent

**Always launch the dotnet-reviewer agent. Never review inline.**

Launch **dotnet-reviewer** agent with:
- Project path and scope from `$ARGUMENTS`
- Focus: **Section 1 — Code Review** (not refactor/cleanup — use `/dotnet-refactor` for that)
- The agent runs `dotnet build`, `dotnet format --verify-no-changes`, and `git diff` before reviewing

---

## Re-review Rule (CRITICAL)

If the dotnet-reviewer agent finds and fixes CRITICAL or HIGH issues:
- **Launch a NEW dotnet-reviewer agent** to confirm the fixes — the agent that applied the fixes must not verify its own work
- The new agent must run `dotnet build` and re-read every fixed file
- Only when the new agent reports no CRITICAL or HIGH issues may the workflow proceed

---

## What the Agent Reviews

### Review Priorities

| Priority | Category | Key Checks |
|----------|----------|-----------|
| CRITICAL | Async / Concurrency | `.Result`/`.Wait()`, `async void`, missing `CancellationToken` |
| CRITICAL | Security | SQL injection, missing `[Authorize]`, IDOR, mass assignment, hardcoded secrets |
| CRITICAL | EF Core | N+1 queries, missing `AsNoTracking()`, `SaveChanges` in loop |
| HIGH | Code Quality | Fat controllers, magic strings, missing null checks, broad `catch (Exception)` |
| HIGH | Architecture | Domain referencing Infrastructure, skipping abstractions, circular dependencies |
| MEDIUM | Performance | Missing pagination, unnecessary `.ToList()`, sync I/O |
| MEDIUM | Blazor | Missing `@key`, unsubscribed events, business logic in `.razor` |

### Approval Criteria

- **Approve**: No CRITICAL or HIGH issues
- **Warning**: MEDIUM issues only — noted, not blocking
- **Block**: Any CRITICAL or HIGH — must be resolved before merge

---

## Mandatory Skills Gate (Pre-Commit)

After review and any fixes:

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Verify XML doc comments on modified public APIs
3. **Invoke `Skill: git-commit`** — branch rules, commit message format

---

## Commit Format

```
fix: <description>
subagent: dotnet-reviewer
```

---

## Key Principles

1. **Agent-first** — never review inline; always delegate to dotnet-reviewer
2. **CRITICAL and HIGH block merge** — no exceptions
3. **Section 1 only** — this skill is for review; use `/dotnet-refactor` for cleanup
