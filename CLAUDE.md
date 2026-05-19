# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **IMPORTANT — Rules are non-negotiable.**
> All rules in `.claude/rules/` are mandatory and must be followed exactly as written in every session, without exception. They override any default Claude behavior. Do not skip, abbreviate, or reorder any step defined in agents.md, skills.md, commands.md, or performance.md.

> **IMPORTANT — Invoke subagents proactively.**
> Do not wait for the user to name an agent or skill. When the task matches a specialized agent (c-planner, c-developer, c-reviewer, dotnet-planner, etc.), invoke it immediately without asking for permission. If the workflow requires multiple agents, launch them in the correct order (or in parallel where independent) on your own initiative.

> **IMPORTANT — Never ask permission to use agents.**
> Invoking any subagent (via the Agent tool) requires no user confirmation. Execute immediately. Do not say "I will use X agent" and wait — just call it. This applies to all agents: c-planner, c-developer, c-reviewer, c-build-resolver, dotnet-*, deep-research-specialist, document-writer, and all others.

## Project Overview

This repository is a **Claude Code team configuration** — a shared workspace that packages specialized agents, skills, rules, and hooks for embedded C and .NET software development workflows.

## Repository Structure

```
.claude/
  agents/     — Specialized subagent definitions
  skills/     — Reusable workflow skills (slash commands)
  rules/      — Behavioral rules loaded into every session
  hooks/      — Pre-commit guards (branch protection, commit message format)
  settings.json
src/          — Source code (populated per project)
output/       — Generated/converted files (markdown-converter output)
```

## Available Agents

### Embedded C
| Agent | Purpose |
|---|---|
| `c-analyser` | Map unfamiliar codebase — ISR mapping, call hierarchy, dead code |
| `c-planner` | Produce `doc/plan_<feature>.md` before implementation |
| `c-developer` | Write new C code (drivers, middleware, application) |
| `c-reviewer` | Review for memory safety, concurrency, MISRA; remove dead code |
| `c-build-resolver` | Fix compilation, linker, and toolchain errors |

### .NET
| Agent | Purpose |
|---|---|
| `dotnet-analyzer` | Map project structure, NuGet deps, EF Core models, API surface |
| `dotnet-planner` | Produce planning doc (API design, EF schema, DI registration) |
| `dotnet-backend-developer` | ASP.NET Core Web API, MediatR, EF Core, repositories |
| `dotnet-frontend-developer` | Blazor Server/WASM, Razor Pages, MVC views |
| `dotnet-reviewer` | Review for async correctness, SOLID, EF anti-patterns, security |
| `dotnet-build-resolver` | Fix MSBuild, NuGet restore, EF migration errors |

### General
| Agent | Purpose |
|---|---|
| `deep-research-specialist` | External research — datasheets, standards, RTOS docs |
| `document-writer` | Technical docs, architecture diagrams (Mermaid), SDD, ICD |

## Available Skills (Slash Commands)

### Embedded C Workflows
- `/c-development-workflow` — Full flow: plan → code → review
- `/c-plan` — Research & plan before implementation
- `/c-coding` — Implement without forced TDD
- `/c-tdd` — TDD: RED → GREEN → REFACTOR
- `/c-review` — Code review + dead code cleanup
- `/c-refactor` — Refactor stable codebase
- `/c-build-resolve` — Fix build errors
- `/c-analyze` — Analyse unfamiliar codebase
- `/c-coding-standard` — Enforce C coding standards
- `/c-doxygen-standard` — Add/verify Doxygen comments

### .NET Workflows
- `/dotnet-development-workflow` — Full flow: plan → code → review
- `/dotnet-plan` — Plan before implementation
- `/dotnet-coding` — Implement (frontend + backend in parallel)
- `/dotnet-review` — Code review
- `/dotnet-refactor` — Dead code and SOLID cleanup
- `/dotnet-build-resolve` — Fix build errors
- `/dotnet-analyze` — Analyse unfamiliar solution

### General
- `/git-commit` — Branch-safe commit with enforced message format
- `/markdown-converter` — Convert PDF/DOCX/URL ↔ Markdown ↔ HTML/DOCX
- `/embedded-research-workflow` — Structured external research

## Mandatory Order Before Committing C Code

```
/c-coding-standard → /c-doxygen-standard → /git-commit
```

## Git Hooks (Auto-enforced)

Two hooks run on every `Bash` and `PowerShell` tool call:

- **`guard_main_branch.py`** — Blocks direct commits to `main`/`master`; requires a feature branch
- **`validate_commit_msg.py`** — Enforces `<type>: <description>` + `subagent: <agent>` format

## Model Selection

| Model | Use for |
|---|---|
| Haiku 4.5 | Lightweight agents, formatting, worker pipelines |
| **Sonnet 4.6** (default) | Main development, orchestration, C/NET implementation |
| Opus 4.7 | Complex architecture, concurrency analysis, deep reasoning |

## Rules Reference

> **These files are mandatory. Read and apply all of them at the start of every session.**

Detailed behavioral rules are in `.claude/rules/`:

- [agents.md](.claude/rules/agents.md) — When and how to use each agent, parallelism rules
- [skills.md](.claude/rules/skills.md) — When to invoke each skill
- [commands.md](.claude/rules/commands.md) — Slash command reference
- [performance.md](.claude/rules/performance.md) — Model selection and context management

### Non-negotiable rules summary

| Rule | Requirement |
|---|---|
| Agent-first | Always delegate to a specialized agent — never handle multi-step tasks inline |
| Proactive agents | Invoke the correct agent immediately when the task matches — do not ask the user first |
| Parallel agents | Launch independent agents simultaneously; only serialize when output feeds input |
| C commit gate | `c-coding-standard` → `c-doxygen-standard` → `git-commit` — no exceptions |
| No main commits | Never commit directly to `main`/`master` — always use a feature branch |
| Reviewer always | `c-reviewer` or `dotnet-reviewer` must run after every code change — no exceptions |
| Planner first | Use `c-planner` or `dotnet-planner` before implementing any multi-file change |
| Reference repos — ask first | Paths marked "อ้างอิง" (reference) must not be edited without explicit user permission. Ask before touching them; if approved, delegate to the relevant subagent. |
