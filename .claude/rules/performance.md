# Claude Tool Strategy

> This file describes how to select Claude models and manage context effectively.
> For embedded firmware performance guidelines (cycle budgets, cache, DMA), see the relevant design docs.

## Model Selection Strategy

**Haiku 4.5** (cost-efficient, ~90% of Sonnet capability):
- Lightweight agents with frequent invocation
- Simple code generation and formatting tasks
- Worker agents in multi-agent pipelines

**Sonnet 4.6** (best coding model — default):
- Main development work
- Orchestrating multi-agent workflows
- Complex C driver and middleware implementation

**Opus 4.7** (deepest reasoning):
- Complex architectural decisions for MCU/RTOS design
- Maximum reasoning requirements (e.g., concurrency analysis)
- Research and analysis tasks

## Context Window Management

Avoid the last 20% of context window for:
- Large-scale refactoring spanning multiple C modules
- Feature implementation across many files
- Debugging complex multi-peripheral interactions

Lower context sensitivity tasks (safe in any context):
- Single-file edits
- Independent utility or helper creation
- Documentation updates
- Simple bug fixes

## Extended Thinking + Plan Mode

Extended thinking is enabled by default, reserving up to 31,999 tokens for internal reasoning.

Control extended thinking via:
- **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux)
- **Config**: Set `alwaysThinkingEnabled` in `~/.claude/settings.json`
- **Budget cap**: `export MAX_THINKING_TOKENS=10000`
- **Verbose mode**: Ctrl+O to see thinking output

For complex embedded tasks requiring deep reasoning:
1. Ensure extended thinking is enabled (on by default)
2. Enable **Plan Mode** for structured approach
3. Use multiple critique rounds for thorough analysis
4. Use split role sub-agents for diverse perspectives
