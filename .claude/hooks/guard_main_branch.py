"""
PreToolUse hook: block git commit and git merge operations on main/master.

Covers both Bash and PowerShell tool calls. Handles:
  - `git commit ...`
  - `git merge ...`
  - `git checkout main` / `git checkout master`
  - `git switch main` / `git switch master`
  - `git -C <path> commit ...` / `git -C <path> merge ...`

Project root is resolved from this script's own location (__file__), so the
hook remains portable when the project is moved to a different directory.

Reads Claude Code PreToolUse JSON from stdin; writes allow/block JSON to stdout.
"""

import sys
import json
import subprocess
import re
import os

PROTECTED_BRANCHES = {'main', 'master'}

# Resolve project root relative to this script: hooks/ -> .claude/ -> project/
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, '..', '..'))


def get_current_branch(work_dir=None):
    """Return current branch name, or empty string on failure."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True, text=True,
            cwd=work_dir, timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return ''


def extract_git_dash_c_path(cmd):
    """Extract the path from `git -C <path> ...` pattern, or None."""
    m = re.search(r'git\s+-C\s+["\']?([^"\'\s]+)["\']?', cmd)
    return m.group(1) if m else None


def is_dangerous_git_op(cmd):
    """Return True if the command performs a write operation on a protected branch."""
    flat = ' '.join(cmd.split())
    dangerous_patterns = [
        r'\bgit\b.*\bcommit\b',
        r'\bgit\b.*\bmerge\b',
        r'\bgit\b.*\bcheckout\b\s+(main|master)\b',
        r'\bgit\b.*\bswitch\b\s+(main|master)\b',
    ]
    return any(re.search(p, flat) for p in dangerous_patterns)


def get_repo_root(path=None):
    """Return git root for the given path (or CWD if None)."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True,
            cwd=path, timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return ''


def is_project_root(root):
    """Return True if root is the Claude config repo itself."""
    try:
        return os.path.normcase(os.path.normpath(root)) == os.path.normcase(PROJECT_ROOT)
    except Exception:
        return False


def main():
    d = json.load(sys.stdin)
    tool_name = d.get('tool_name', '')

    if tool_name not in ('Bash', 'PowerShell'):
        print(json.dumps({'decision': 'allow'}))
        return

    cmd = d.get('tool_input', {}).get('command', '')

    if not is_dangerous_git_op(cmd):
        print(json.dumps({'decision': 'allow'}))
        return

    # Use the -C <path> if present so branch and root resolve to the TARGET repo,
    # not the Claude project CWD.
    dash_c_path = extract_git_dash_c_path(cmd)
    branch = get_current_branch(work_dir=dash_c_path)
    root = get_repo_root(path=dash_c_path)

    # Allow all git ops inside the Claude config repo itself.
    # Committing here requires an explicit user instruction — enforced by workflow,
    # not by this hook.
    if is_project_root(root):
        print(json.dumps({'decision': 'allow'}))
        return

    if branch in PROTECTED_BRANCHES:
        reason = (
            f'BLOCKED: Cannot commit/merge directly to branch "{branch}".\n'
            'Create or switch to a feature branch first:\n'
            '  git checkout -b feat/<short-description>\n\n'
            'Agents must NEVER merge to main/master. '
            'Merging is done via Pull Request by the human only.\n'
            'See .claude/skills/git-commit/SKILL.md for the correct workflow.'
        )
        print(json.dumps({'decision': 'block', 'reason': reason}))
        return

    print(json.dumps({'decision': 'allow'}))


if __name__ == '__main__':
    main()
