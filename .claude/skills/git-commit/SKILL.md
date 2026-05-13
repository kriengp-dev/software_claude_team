---
name: git-commit
description: Git branching, commit message format, and PR workflow rules for this project. Reference whenever making commits or opening pull requests.
origin: ECC
---

## When to Use

- Before making any `git commit`
- When creating a pull request
- When unsure which branch to commit on or how to format a commit message

---

## Branch Rules

**Never commit directly to `main` or `master`.** This is enforced by a `PreToolUse` hook that blocks all `git commit` commands when the current branch is `main` or `master`.

### If the current branch IS `main` or `master`

Create a feature branch first:

```bash
git checkout -b <type>/<short-description>
```

Branch prefix must match the commit type:

| Prefix | Use for |
|--------|---------|
| `feat/` | New feature |
| `fix/` | Bug fix |
| `refactor/` | Code restructuring without behavior change |
| `docs/` | Documentation only |
| `test/` | Tests only |
| `chore/` | Build, tooling, config |
| `perf/` | Performance improvement |

### If the current branch is NOT `main` or `master`

Commit directly on the current branch — no need to create a new branch.

```bash
# Already on feat/modbus-server — just commit
git add <files>
git commit -m "feat: add holding register read handler
subagent: c-developer"
```

---

## Commit Message Format

```
<type>: <description>
subagent: <agent>

<optional body>
```

> **CRITICAL:** `subagent:` must be on its **own line** immediately after the subject line.
>
> Wrong:  `feat: add uart driver subagent: c-developer`
> Correct: `feat: add uart driver` then newline then `subagent: c-developer`

- **`<type>`**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
- **`subagent`**: the agent that made the change — use one of the agent names below

| Agent | Value |
|-------|-------|
| c-developer | `c-developer` |
| c-reviewer | `c-reviewer` |
| c-build-resolver | `c-build-resolver` |
| c-analyser | `c-analyser` |
| c-planner | `c-planner` |
| dotnet-backend-developer | `dotnet-backend-developer` |
| dotnet-frontend-developer | `dotnet-frontend-developer` |
| dotnet-reviewer | `dotnet-reviewer` |
| dotnet-planner | `dotnet-planner` |
| dotnet-analyzer | `dotnet-analyzer` |
| dotnet-build-resolver | `dotnet-build-resolver` |
| deep-research-specialist | `research` |
| document-writer | `document-writer` |
| Human / user | ask user for name → `author: <name>` (omit line if declined) |

**Examples:**

```bash
# c-developer implemented a feature
feat: add holding register read handler
subagent: c-developer

# c-reviewer cleaned up dead code
refactor: remove unused uart_flush stub
subagent: c-reviewer

# c-build-resolver fixed a linker error
fix: resolve undefined reference to crc16_init
subagent: c-build-resolver

# test written by c-developer (TDD)
test: add unit tests for holding register read
subagent: c-developer

# human commits (no subagent line)
chore: update .gitignore for CCS build artifacts
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

### Separate Commits by Change Type

**Always split docs, code, and test changes into separate commits.** Do not mix them in one commit.

| What changed | Commit type | Example message |
|---|---|---|
| Documentation only (`.md`, design docs, comments) | `docs` | `docs: update Modbus register map design` |
| Implementation code (`.c`, `.h`) | `feat` / `fix` / `refactor` / `perf` | `feat: implement holding register read` |
| Tests only (TDD, unit tests, stubs) | `test` | `test: add unit tests for holding register read` |
| Build / config / tooling | `chore` | `chore: add Unity test runner to CMakeLists` |

**Order within a feature branch:**

```
test: write failing tests for holding register read   ← RED
feat: implement holding register read                 ← GREEN
refactor: extract register validation to helper       ← REFACTOR
docs: add Doxygen comments to holding register module
```

**Wrong — mixed commit:**
```
# BAD: mixes code, test, and docs in one commit
feat: add holding register read, tests, and docs
```

---

## Pull Request Workflow

1. Analyze full commit history — not just the latest commit (`git diff [base-branch]...HEAD`)
2. Draft a PR title (≤ 70 characters) and body summary
3. Include a test plan checklist
4. Push with `-u` flag if the branch has no upstream yet:
   ```bash
   git push -u origin <branch-name>
   ```
5. Open PR targeting `main`

---

## Commit Checklist

- [ ] Current branch is NOT `main` or `master`
- [ ] Commit contains only one type of change (docs, code, or test — not mixed)
- [ ] Commit message follows `<type>: <description>` format
- [ ] All tests pass before committing implementation code
- [ ] `/c-coding-standard` and `/c-doxygen-standard` applied before committing C files
