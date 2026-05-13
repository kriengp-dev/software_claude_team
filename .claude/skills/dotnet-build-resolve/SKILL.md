---
name: dotnet-build-resolve
description: .NET build error resolution workflow. Delegates to dotnet-build-resolver agent to fix MSBuild errors, NuGet restore failures, project reference issues, EF Core migration errors, and SDK version conflicts with minimal surgical changes.
---

## When to Use

- `dotnet build` or `dotnet restore` fails with compilation or package errors
- EF Core migration commands fail
- NuGet version conflicts prevent build
- SDK version mismatch (`global.json` issues)

**Do not use for logic bugs — use dotnet-coding instead.**

---

## Workflow

### Mandatory: Delegate to dotnet-build-resolver Agent

**Always launch the dotnet-build-resolver agent. Never fix build errors inline.**

Launch **dotnet-build-resolver** agent with:
- Target repo path: from `$ARGUMENTS`
- Error output: paste the full error or instruct the agent to run `dotnet build` itself
- The agent detects the build system and project layout automatically

---

## Resolution Workflow the Agent Follows

```
1. dotnet restore   → identify NuGet failures
2. dotnet build     → capture all compiler errors
3. Read affected file → understand context
4. Apply minimal fix  → only what's needed
5. dotnet build     → verify fix
6. Check new errors → ensure nothing broke
```

---

## Common Error Patterns

| Error Code | Cause | Typical Fix |
|-----------|-------|------------|
| `CS0246` | Type/namespace not found | Add `using` or `<PackageReference>` |
| `CS0103` | Name doesn't exist | Fix name or add `using` |
| `CS8600–CS8603` | Nullable warning as error | Add `?`, `!`, or null check |
| `NU1107` | NuGet version conflict | Pin version in `.csproj` |
| `NU1202` | Incompatible framework | Downgrade package or upgrade `<TargetFramework>` |
| `MSB4019` | Project reference not found | Fix relative path in `<ProjectReference>` |
| `NETSDK1045` | SDK version required | Update `global.json` or install required SDK |
| EF migration fail | Missing design-time factory | Add `IDesignTimeDbContextFactory<T>` |

---

## Stop Conditions

Stop and report if:
- Same error persists after 3 fix attempts
- Fix introduces more errors than it resolves
- Error requires project restructure or major version upgrade

---

## Mandatory Skills Gate (Pre-Commit)

After `dotnet build` succeeds:

1. Run `dotnet format <TARGET_REPO>` — apply any formatting fixes
2. **Invoke `Skill: git-commit`** — branch rules, commit message format

---

## Commit Format

```
fix: <description>
subagent: dotnet-build-resolver
```

---

## Key Principles

1. **Agent-first** — never fix build errors inline; always delegate
2. **Surgical fixes only** — do not refactor, rename, or reorganize while fixing a build error
3. **One fix at a time** — verify after each change before applying the next
4. **Never suppress warnings** with `#pragma warning disable` without user approval
