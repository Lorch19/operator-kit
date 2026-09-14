---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

## Workflow at a Glance

```
1. CAPTURE INTENT → Understand what the skill should do and when it triggers
2. DRAFT          → Write SKILL.md with frontmatter + instructions
3. TEST           → Run 2-3 realistic prompts (with-skill vs baseline)
4. EVALUATE       → User reviews outputs in eval-viewer; run quantitative benchmarks
5. IMPROVE        → Rewrite skill based on feedback, generalize from examples
   ↻ Repeat 3-5 until satisfied
6. OPTIMIZE       → Run description optimizer for better triggering accuracy
7. PACKAGE        → Bundle as .skill file for distribution
```

**Jump in where the user is.** New idea → start at step 1. Existing draft → start at step 3. Just vibing → skip the formal eval loop entirely.

After the skill is done, run the description optimizer (`scripts/run_loop.py`) to improve triggering accuracy.

### Reference Files
| When you need... | Read |
|---|---|
| Full eval workflow (spawning runs, grading, viewer) | `references/eval-workflow.md` |
| Description optimization for trigger accuracy | `references/description-optimization.md` |
| Claude.ai or Cowork environment adaptations | `references/environment-guides.md` |

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This is one continuous sequence — don't stop partway through. The full workflow covers: spawning with-skill and baseline runs in parallel, drafting assertions while runs are in progress, capturing timing data, grading, aggregating benchmarks, and launching the eval viewer for human review.

**Read `references/eval-workflow.md` for the complete step-by-step eval workflow.** It covers workspace layout, subagent prompts, grading format, benchmark aggregation, the viewer UI, and how to read feedback.

Key points to remember:
- Put results in `<skill-name>-workspace/` as a sibling to the skill directory, organized by iteration
- Spawn with-skill AND baseline runs in the same turn (don't do them sequentially)
- Always use `eval-viewer/generate_review.py` to create the viewer — don't write custom HTML
- GENERATE THE EVAL VIEWER *BEFORE* evaluating outputs yourself — get results in front of the human ASAP

---

## Improving the skill

After the user reviews outputs in the viewer, improve the skill based on their feedback. The full improvement philosophy and iteration loop are in `references/eval-workflow.md` (section "Improving the skill").

Core principles:
1. **Generalize from feedback** — don't overfit to the test examples. The skill will be used across many different prompts.
2. **Keep the prompt lean** — remove instructions that aren't pulling their weight. Read transcripts, not just outputs.
3. **Explain the why** — help the model understand reasoning instead of rigid ALWAYS/NEVER rules.
4. **Look for repeated work** — if all test runs wrote similar helper scripts, bundle that script in `scripts/`.

Iterate until the user is happy, feedback is all empty, or you're not making meaningful progress.

---

## Description Optimization

The description field in SKILL.md frontmatter determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

**Read `references/description-optimization.md` for the full optimization workflow** — generating trigger eval queries, reviewing with the user via HTML template, running the `scripts/run_loop.py` optimization, and applying results.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Environment-Specific Instructions

For **Claude.ai** or **Cowork** environments, read `references/environment-guides.md`. It covers adaptations for environments without subagents, without a browser/display, and Cowork-specific quirks.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.
- `references/eval-workflow.md` — Full eval workflow: spawning runs, grading, viewer, feedback, and improvement loop
- `references/description-optimization.md` — Description optimization: trigger eval queries, HTML review, run_loop.py
- `references/environment-guides.md` — Claude.ai and Cowork adaptations

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!
