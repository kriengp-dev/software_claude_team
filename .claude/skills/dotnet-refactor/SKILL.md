---
name: dotnet-refactor
description: .NET dead code cleanup and refactor workflow. Delegates to dotnet-reviewer agent (Section 2) to remove unused code, eliminate duplicate logic, fix SOLID violations, and apply performance optimizations on a stable codebase.
---

## When to Use

- After `dotnet build` passes and all tests are green
- Removing dead code, unused NuGet references, or duplicate logic
- Fixing architecture violations found during review
- Before a major feature addition to reduce technical debt

**Never run during active feature development on the same files.**

---

## Prerequisites

Before launching the agent, confirm:
- [ ] `dotnet build` passes with no errors
- [ ] All tests pass (`dotnet test`)
- [ ] No active feature development on the same files

---

## Workflow

### Mandatory: Delegate to dotnet-reviewer Agent (Section 2)

Launch **dotnet-reviewer** agent with:
- Project path / scope from `$ARGUMENTS`
- Focus: **Section 2 — Refactor & Dead Code Cleanup**

### What the Agent Does

**1. Detect unused code:**
```bash
dotnet format <TARGET_REPO> --diagnostics IDE0005  # unused usings
grep -rn "TODO\|FIXME\|HACK" <TARGET_REPO> --include="*.cs"
```

**2. Categorize candidates:**

| Risk | Category | Examples |
|------|----------|---------|
| SAFE | Clearly unused | Private methods with zero callers, unused `using` directives |
| CAREFUL | Indirect usage | Registered via DI by name, reflection, `[FromServices]` |
| RISKY | Public API surface | Public methods in libraries, controller actions |

**3. Remove one category at a time** — rebuild and retest after each batch

**4. Eliminate duplicates** — merge duplicate services, DTOs, or utility methods

**5. Apply optimizations:**
| Category | Action |
|----------|--------|
| `async`/`await` | Remove unnecessary `async Task` wrappers (`return Task.FromResult`) |
| LINQ | Replace multiple enumerations with single pass |
| Allocations | Replace `string` concatenation in loops with `StringBuilder` |
| EF queries | Add `.AsNoTracking()`, projections, `AnyAsync` vs `CountAsync` |
| DI lifetime | Verify Scoped/Singleton/Transient is correct for each service |

---

## Mandatory Skills Gate (Pre-Commit after each batch)

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Run `dotnet build` + `dotnet test` — verify nothing broke
3. **Invoke `Skill: git-commit`** — one commit per passing batch

---

## Commit Format

```
refactor: <description>
subagent: dotnet-reviewer
```

---

## Key Principles

1. **Agent-first** — never refactor inline; always delegate to dotnet-reviewer
2. **Verify before delete** — never remove code based on grep alone; check DI registrations and reflection
3. **One batch at a time** — build and test after each removal category
4. **Conservative on RISKY** — public APIs may have external consumers; leave if in doubt
