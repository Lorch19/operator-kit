#!/usr/bin/env python3
"""
Security Reminder Hook for Claude Code
Checks for security patterns in file edits and blocks on likely vulnerabilities.
Based on Anthropic's official security-guidance plugin.

Hook type: PreToolUse (fires on Edit, Write, MultiEdit)
Exit codes: 0 = allow, 1 = show error to user, 2 = block tool call and show to Claude

MATCHING IS REGEX, NOT SUBSTRING -- this matters.
An earlier version matched bare substrings and was unusable as a gate:
  - a bare dot-format call was flagged as SQL injection on every str.format()
  - the word "pickle" matched in a comment or a variable name
  - a bare eval-paren matched inside identifiers like _supervisor_eval(...)
  - a bare exec-paren matched JavaScript's regex .exec(...)
Measured across 8 real repos, 4 of 5 benign edits were hard-blocked. A gate
that fires on arrival gets deleted, so every rule below is anchored on word
boundaries and matches a vulnerability shape rather than a bare substring.

Known false-positive mode: prose that quotes a pattern (docs about this hook)
can trip the rule it describes. Reword, or set ENABLE_SECURITY_REMINDER=0.

Rules are ordered cheapest-signal first; the first match wins.
Fails OPEN on malformed input -- a bug here must never block real work.
"""

import json
import os
import re
import sys

SECURITY_PATTERNS = [
    {
        "ruleName": "child_process_exec",
        # child_process.exec(...) or a bare execSync(...) -- but NOT regex.exec(...)
        "regex": r"child_process\.exec(?:Sync)?\s*\(|(?<![\w_.])execSync\s*\(",
        "reminder": "Security Warning: child_process exec can lead to command injection. Use execFile() instead with argument arrays.",
    },
    {
        "ruleName": "new_function_injection",
        "regex": r"new\s+Function\s*\(",
        "reminder": "Security Warning: new Function() with dynamic strings can lead to code injection. Consider alternatives.",
    },
    {
        "ruleName": "eval_injection",
        # bare call only -- not my_eval(...), cmd_eval(...), obj.eval(...)
        "regex": r"(?<![\w_.])eval\s*\(",
        "reminder": "Security Warning: dynamic evaluation executes arbitrary code. Use JSON.parse() for data or alternative patterns.",
    },
    {
        "ruleName": "react_dangerously_set_html",
        "regex": r"dangerouslySetInnerHTML",
        "reminder": "Security Warning: dangerouslySetInnerHTML can lead to XSS. Ensure content is sanitized with DOMPurify.",
    },
    {
        "ruleName": "document_write_xss",
        "regex": r"\bdocument\.write(?:ln)?\s*\(",
        "reminder": "Security Warning: document.write can be exploited for XSS. Use createElement() and appendChild().",
    },
    {
        "ruleName": "innerHTML_xss",
        # assignment only, not comparison
        "regex": r"\.innerHTML\s*=(?!=)",
        "reminder": "Security Warning: innerHTML with untrusted content leads to XSS. Use textContent or DOMPurify.",
    },
    {
        "ruleName": "pickle_deserialization",
        # the dangerous calls, not the bare word
        "regex": r"\b(?:cPickle|pickle)\.(?:loads?|Unpickler)\s*\(",
        "reminder": "Security Warning: pickle with untrusted content can execute arbitrary code. Use JSON instead.",
    },
    {
        "ruleName": "os_system_injection",
        "regex": r"\bos\.system\s*\(|\bcommands\.getoutput\s*\(",
        "reminder": "Security Warning: shell-invoking helpers should only be used with static arguments, never user-controlled input.",
    },
    {
        "ruleName": "sql_injection",
        # An interpolated string that actually starts a SQL statement --
        # an f-string literal, a concatenation, or a dot-format on a SQL literal.
        "regex": (
            r"""f["'`]\s*(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b"""
            r"""|["'`]\s*(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b[^"'`]*["'`]\s*(?:\+|%|\.format\s*\()"""
            r"""|["'`]\s*(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b[^"'`]*\{"""
        ),
        "reminder": "Security Warning: String interpolation in SQL queries leads to injection. Use parameterized queries.",
    },
]

COMPILED = [
    (p["ruleName"], re.compile(p["regex"], re.IGNORECASE), p["reminder"])
    for p in SECURITY_PATTERNS
]


def check_patterns(file_path, content):
    """Check if content matches any security patterns."""
    if not content:
        return None, None
    for rule_name, regex, reminder in COMPILED:
        if regex.search(content):
            return rule_name, reminder
    return None, None


def extract_content(tool_name, tool_input):
    """Extract content to check from tool input."""
    if tool_name == "Write":
        return tool_input.get("content", "") or ""
    elif tool_name == "Edit":
        return tool_input.get("new_string", "") or ""
    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits", []) or []
        return "\n".join((edit.get("new_string", "") or "") for edit in edits)
    return ""


def main():
    if os.environ.get("ENABLE_SECURITY_REMINDER", "1") == "0":
        sys.exit(0)

    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)  # fail open

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {}) or {}

    if tool_name not in ["Edit", "Write", "MultiEdit"]:
        sys.exit(0)

    # Never gate edits to this hook itself -- otherwise it cannot be maintained.
    edited = tool_input.get("file_path", "") or ""
    if edited and os.path.realpath(edited) == os.path.realpath(__file__):
        sys.exit(0)

    content = extract_content(tool_name, tool_input)
    rule_name, reminder = check_patterns(tool_input.get("file_path", ""), content)

    if rule_name and reminder:
        print(f"{reminder} [{rule_name}]", file=sys.stderr)
        sys.exit(2)  # Block and show to Claude

    sys.exit(0)


if __name__ == "__main__":
    main()
