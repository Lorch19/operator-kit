---
name: security-guidance
description: Security reminder hook that warns about potential security issues when editing files, including command injection, XSS, eval, pickle, SQL injection, and unsafe code patterns. Install as a PreToolUse hook to get automatic security warnings during development.
---

# Security Guidance Hook

A PreToolUse hook that monitors file edits for 9 common security anti-patterns and blocks with warnings.

## Patterns Detected

| Pattern | Risk | Safe Alternative |
|---------|------|-----------------|
| `child_process.exec()` | Command injection | Use `execFile()` with argument arrays |
| `new Function()` | Code injection | Alternative design patterns |
| `eval()` | Arbitrary code execution | `JSON.parse()` or alternatives |
| `dangerouslySetInnerHTML` | XSS | Sanitize with DOMPurify |
| `document.write()` | XSS | `createElement()` + `appendChild()` |
| `.innerHTML =` | XSS | `textContent` or DOMPurify |
| `pickle` | Arbitrary code execution | JSON serialization |
| `os.system` | Command injection | Static arguments only |
| SQL string interpolation | SQL injection | Parameterized queries |

## Installation

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/operator-kit/meta-tools/security-guidance/hooks/security_reminder_hook.py"
          }
        ]
      }
    ]
  }
}
```

## How It Works

- Fires on every Edit, Write, or MultiEdit tool call
- Checks the *new* content against 9 security patterns
- Exit code 0 = allow (no pattern found)
- Exit code 2 = block and warn Claude (pattern found)
- Disable with `ENABLE_SECURITY_REMINDER=0` environment variable
- Fails open on malformed input, and never gates edits to itself

## Matching Is Regex, Not Substring

Every rule is anchored on word boundaries and matches a vulnerability *shape*.
This is deliberate: an earlier version compared bare substrings and was
unusable as a gate. Measured across 8 real repos, 4 of 5 benign edits were
hard-blocked — a bare dot-format call flagged every `str.format` as SQL
injection, the word "pickle" matched inside a comment, and a bare eval-paren
matched inside identifiers such as `_supervisor_eval`.

A gate that fires on arrival gets deleted, and a deleted gate protects
nothing. So the rules distinguish:

| Blocked | Allowed |
|---------|---------|
| a `pickle.loads` call | the word pickle in a comment |
| a bare eval-paren | `cmd_eval`, `_supervisor_eval` |
| a bare `execSync` call | JavaScript's `regex.exec` |
| SQL built by f-string, concat, or dot-format | any other `str.format` call |
| an `.innerHTML` assignment | an `.innerHTML` comparison |

**Known false-positive mode:** prose that *quotes* a pattern — including docs
about this hook — can trip the rule it describes. Reword, or set
`ENABLE_SECURITY_REMINDER=0` for that edit.
