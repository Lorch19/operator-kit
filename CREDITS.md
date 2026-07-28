# Credits

Third-party skills vendored into Operator Kit, with their upstream source and license.

## mattpocock/skills

Source: https://github.com/mattpocock/skills — © 2026 Matt Pocock, MIT License.

Vendored (lightly adapted: `/setup-matt-pocock-skills` references renamed to
`/agent-context-setup`, Codex `agents/openai.yaml` manifests dropped, router
references removed):

| Skill | Landed at | Upstream path |
|---|---|---|
| `grilling` | `thinking-tools/grilling` | `skills/productivity/grilling` |
| `grill-me` | `thinking-tools/grill-me` | `skills/productivity/grill-me` |
| `handoff` | `thinking-tools/handoff` | `skills/productivity/handoff` |
| `teach` | `thinking-tools/teach` | `skills/productivity/teach` |
| `research` | `thinking-tools/research` | `skills/engineering/research` |
| `wayfinder` | `thinking-tools/wayfinder` | `skills/engineering/wayfinder` |
| `writing-great-skills` | `meta-tools/writing-great-skills` | `skills/productivity/writing-great-skills` |
| `tdd` | `engineering-tools/skills/tdd` | `skills/engineering/tdd` |
| `diagnosing-bugs` | `engineering-tools/skills/diagnosing-bugs` | `skills/engineering/diagnosing-bugs` |
| `codebase-design` | `engineering-tools/skills/codebase-design` | `skills/engineering/codebase-design` |
| `domain-modeling` | `engineering-tools/skills/domain-modeling` | `skills/engineering/domain-modeling` |
| `prototype` | `engineering-tools/skills/prototype` | `skills/engineering/prototype` |
| `to-spec` | `engineering-tools/skills/to-spec` | `skills/engineering/to-spec` |
| `to-tickets` | `engineering-tools/skills/to-tickets` | `skills/engineering/to-tickets` |
| `triage` | `engineering-tools/skills/triage` | `skills/engineering/triage` |
| `implement` | `engineering-tools/skills/implement` | `skills/engineering/implement` |
| `improve-codebase-architecture` | `engineering-tools/skills/improve-codebase-architecture` | `skills/engineering/improve-codebase-architecture` |
| `agent-context-setup` | `engineering-tools/skills/agent-context-setup` | `skills/engineering/setup-matt-pocock-skills` |

Deliberately **not** taken: `ask-matt` (his router — Operator Kit uses `NAVIGATOR.md`
files instead), `code-review` (Operator Kit already ships one), and everything under
`skills/personal/`, `skills/misc/`, `skills/in-progress/`, `skills/deprecated/`.

### MIT License

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Anthropic knowledge-work-plugins / official skills

`operations-tools/`, `engineering-tools/` (original 10), `sales-tools/`, `design-tools/`,
`document-tools/`, `doc-coauthoring/`, `meta-tools/skill-creator`,
`meta-tools/webapp-testing` — from Anthropic's published skill collections.

## Pawel Huryn — PM Skills

`analytics-tools/`, `gtm-tools/`.
