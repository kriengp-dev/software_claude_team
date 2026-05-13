"""
Pre-commit hook: validates git commit message format.

Rules enforced:
  1. Subject must start with a valid type (feat, fix, refactor, docs, test,
     chore, perf, ci, revert, merge) optionally followed by a scope: (scope).
  2. 'subagent:' must NOT appear on the subject line — it belongs on its own
     line in the body, separated from the subject by a newline.

Reads Claude Code PreToolUse JSON from stdin; writes allow/block JSON to stdout.
"""

import sys
import json
import re

VALID_TYPES = [
    'feat', 'fix', 'refactor', 'docs', 'test',
    'chore', 'perf', 'ci', 'revert', 'merge',
]


def extract_message(cmd: str) -> str:
    """Try to extract commit message text from a git commit command string."""

    # PowerShell @'...'@ heredoc
    m = re.search(r"-m\s+@'(.*?)'@", cmd, re.DOTALL)
    if m:
        return m.group(1).strip()

    # Bash heredoc: -m "$(cat <<'EOF'\n...\nEOF\n)"
    m = re.search(
        r'''-m\s+["\$\(]*cat\s+<<['"]{0,1}(\w+)['"]{0,1}\s*\n(.*?)\n\1''',
        cmd, re.DOTALL,
    )
    if m:
        return m.group(2).strip()

    # Multi-line -m "..."
    m = re.search(r'-m\s+"((?:[^"\\]|\\.|\n)+)"', cmd, re.DOTALL)
    if m:
        return m.group(1).strip()

    # Multi-line -m '...'
    m = re.search(r"-m\s+'((?:[^'\\]|\\.|\n)+)'", cmd, re.DOTALL)
    if m:
        return m.group(1).strip()

    return ''


def validate(msg: str) -> list:
    """Return a list of error strings, empty if the message is valid."""
    errors = []

    lines = msg.replace('\\n', '\n').split('\n')
    subject = lines[0].strip()

    # Rule 1: valid type prefix
    type_match = re.match(r'^(\w+)(\([^)]+\))?:\s*\S', subject)
    if type_match:
        commit_type = type_match.group(1)
        if commit_type not in VALID_TYPES:
            errors.append(
                f'Invalid type "{commit_type}". '
                f'Allowed: {", ".join(VALID_TYPES)}'
            )
    elif subject:
        errors.append('Subject must start with <type>: (e.g. feat:, fix:, docs:)')

    # Rule 2: subagent: must NOT be on the subject line
    if re.search(r'subagent\s*:', subject, re.IGNORECASE):
        errors.append(
            '"subagent:" must be on its own line after the subject — '
            'NOT appended to the subject line.\n'
            '  Wrong : feat: add driver subagent: c-developer\n'
            '  Correct: feat: add driver\\nsubagent: c-developer'
        )

    return errors


def main():
    d = json.load(sys.stdin)

    if d.get('tool_name') not in ('Bash', 'PowerShell'):
        print(json.dumps({'decision': 'allow'}))
        return

    cmd = d.get('tool_input', {}).get('command', '')

    if 'git commit' not in cmd:
        print(json.dumps({'decision': 'allow'}))
        return

    msg = extract_message(cmd)
    if not msg:
        print(json.dumps({'decision': 'allow'}))
        return

    errors = validate(msg)
    if errors:
        reason = (
            'COMMIT FORMAT BLOCKED:\n' +
            '\n'.join(f'  - {e}' for e in errors) +
            '\n\nRequired format:\n'
            '  <type>: <description>\n'
            '  subagent: <agent-name>\n\n'
            '  <optional body>\n\n'
            'Valid types: ' + ', '.join(VALID_TYPES)
        )
        print(json.dumps({'decision': 'block', 'reason': reason}))
    else:
        print(json.dumps({'decision': 'allow'}))


if __name__ == '__main__':
    main()
