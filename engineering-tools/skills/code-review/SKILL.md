---
name: code-review
disable-model-invocation: true
description: Review code changes for security, performance, and correctness. TRIGGER with a PR URL or diff, "review this before I merge", "is this code safe?", or when checking for injection risks, N+1 queries, missing edge cases, or error handling gaps.
argument-hint: "<PR URL, diff, or file path>"
---

# /code-review

Review code changes with a structured lens on security, performance, correctness, and maintainability.

## Review Dimensions

### Security
- SQL injection, XSS, CSRF, secrets in code, SSRF, path traversal

### Performance
- N+1 queries, memory allocations, O(n²) in hot paths, missing indexes, resource leaks

### Correctness
- Edge cases (empty, null, overflow), race conditions, error handling, off-by-one

### Maintainability
- Naming clarity, single responsibility, duplication, test coverage

## Output

```markdown
## Code Review: [PR title or file]

### Summary
[1-2 sentence overview]

### Critical Issues
| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|

### Suggestions
| # | File | Line | Suggestion | Category |
|---|------|------|------------|----------|

### What Looks Good
- [Positive observations]

### Verdict
[Approve / Request Changes / Needs Discussion]
```

## Tips

1. **Provide context** — "This is a hot path" or "This handles PII"
2. **Specify concerns** — "Focus on security" narrows the review
3. **Include tests** — I'll check test coverage too
