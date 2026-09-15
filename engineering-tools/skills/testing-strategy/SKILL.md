---
name: testing-strategy
description: Design test strategies and test plans. TRIGGER with "how should we test", "test strategy for", "test plan", "what tests do we need", or when user needs help with testing approaches, coverage, or test architecture.
---

# Testing Strategy

Design effective testing strategies balancing coverage, speed, and maintenance.

## Testing Pyramid

```
        /  E2E  \         Few, slow, high confidence
       / Integration \     Some, medium speed
      /    Unit Tests  \   Many, fast, focused
```

## Strategy by Component

- **API endpoints**: Unit tests for logic, integration for HTTP, contract tests for consumers
- **Data pipelines**: Input validation, transformation correctness, idempotency
- **Frontend**: Component tests, interaction tests, visual regression, accessibility
- **Infrastructure**: Smoke tests, chaos engineering, load tests

## Coverage Focus

**Cover**: Business-critical paths, error handling, edge cases, security boundaries, data integrity
**Skip**: Trivial getters/setters, framework code, one-off scripts

## Output

Test plan with: what to test, test type per area, coverage targets, example test cases. Identify gaps in existing coverage.
