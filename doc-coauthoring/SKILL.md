---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

**Initial offer:**
Offer a structured workflow with three stages:

1. **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
2. **Refinement & Structure**: Iteratively build each section through brainstorming and editing
3. **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots

This ensures the doc works when others read it (including when they paste it into Claude). Ask if they want this workflow or prefer freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows, enabling smart guidance later.

### Initial Questions

Start by asking for meta-context about the document:

1. What type of document is this? (e.g., technical spec, decision doc, proposal)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

Inform them they can answer in shorthand or dump information however works best.

**If user provides a template or mentions a doc type:**
- Ask if they have a template document to share
- If they provide a link or file, fetch/read it via the appropriate integration

**If user mentions editing an existing shared document:**
- Read the current state via integration
- Check for images without alt-text -- when others use Claude to understand the doc, Claude won't see images. Ask if they want alt-text generated; if so, request they paste each image into chat.

### Info Dumping

Once initial questions are answered, encourage the user to dump all the context they have:
- Background on the project/problem
- Related team discussions or shared documents
- Why alternative solutions aren't being used
- Organizational context (team dynamics, past incidents, politics)
- Timeline pressures or constraints
- Technical architecture or dependencies
- Stakeholder concerns

Advise them not to worry about organizing it -- just get it all out. Offer multiple ways to provide context:
- Info dump stream-of-consciousness
- Point to team channels or threads to read
- Link to shared documents

**If integrations are available** (Slack, Teams, Google Drive, SharePoint, or other MCP servers), mention these can pull context directly.

**If no integrations are detected:** Suggest enabling connectors in Claude settings, or pasting relevant content directly.

**During context gathering:**
- If user mentions channels/docs: read via integration if available, otherwise ask them to paste
- If unknown entities/projects are mentioned: ask before searching connected tools
- Track what's learned vs. still unclear

**Clarifying questions:**
When user signals they've done their initial dump, generate 5-10 numbered questions based on gaps. Tell them shorthand answers are fine (e.g., "1: yes, 2: see #channel, 3: no because backwards compat"), or they can link more docs or keep info-dumping.

**Exit condition:** Sufficient context has been gathered when you can ask about edge cases and trade-offs without needing basics explained.

**Transition:** Ask if there's more context or if it's time to move on to drafting. Proceed to Stage 2 when ready.

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming, curation, and iterative refinement.

**Instructions to user:**
Explain that the document will be built section by section. For each section: clarifying questions, brainstorming options, curation, drafting, and iterative refinement.

**Section ordering:**

If the document structure is clear: ask which section they'd like to start with. Suggest starting with whichever section has the most unknowns. For decision docs, that's usually the core proposal. For specs, it's typically the technical approach. Summary sections are best left for last.

If user doesn't know what sections they need: based on the document type and template, suggest 3-5 sections appropriate for the doc type. Ask if this structure works or if they want to adjust.

**Create the scaffold:**
Once structure is agreed, create the document with all section headers and "[To be written]" placeholders.
- **With artifacts:** Use `create_file` to create an artifact. Provide the scaffold link.
- **Without artifacts:** Create a markdown file in the working directory (e.g., `decision-doc.md`). Confirm the filename.

### Per-Section Loop

For each section, run this cycle:

### Step 1: Clarifying Questions

Announce work on the section. Ask 5-10 clarifying questions about what should be included based on context gathered and the section's purpose. Shorthand answers are fine.

### Step 2: Brainstorming

Generate 5-20 numbered options (scaled to section complexity). Look for context shared earlier that might have been forgotten and angles not yet mentioned. Offer to brainstorm more if they want additional options.

### Step 3: Curation

Ask which points to keep, remove, or combine. Request brief justifications to learn priorities for the next sections. Examples: "Keep 1,4,7,9", "Remove 3 (duplicates 1)", "Combine 11 and 12". If user gives freeform feedback instead of numbered selections, parse their preferences and proceed.

### Step 4: Gap Check

Ask if anything important is missing for this section.

### Step 5: Drafting

Use `str_replace` to replace the placeholder with actual content. With artifacts, provide a link after drafting. Without artifacts, confirm the file edit is complete and name the file. Ask them to read through and indicate what to change -- being specific helps learning for future sections.

On the first section, include this note: "Instead of editing the doc directly, tell me what to change. This helps me learn your style for later sections."

### Step 6: Iterative Refinement

Apply feedback via `str_replace` (never reprint the whole doc). With artifacts, provide link after each edit. Without artifacts, confirm edits are complete. If user edits doc directly and asks you to read it, note the changes as style preferences for future sections.

Keep iterating until satisfied. After 3 consecutive iterations with no substantial changes, ask if anything can be removed without losing important information.

When section is done, confirm it's complete and ask if ready to move to the next section.

**Repeat for all sections.**

### Near Completion

As approaching completion (80%+ of sections done), re-read the entire document and check for:
- Flow and consistency across sections
- Redundancy or contradictions
- Anything that feels like "slop" or generic filler
- Whether every sentence carries weight

Read the entire document and provide feedback.

**When all sections are drafted and refined:**
Announce all sections are complete. Do one final review for overall coherence, flow, and completeness. Provide any final suggestions.

Ask if they're ready to move to Reader Testing, or if they want to refine anything else.

## Stage 3: Reader Testing

**Goal:** Test the document with a fresh Claude (no context bleed) to verify it works for readers. This catches blind spots -- things that make sense to the authors but might confuse others.

### Step 1: Predict Reader Questions

Generate 5-10 questions that readers would realistically ask when encountering this document. Think about:
- What would they type into Claude or search for?
- What context might they lack?
- What decisions or trade-offs might they question?

### Step 2: Test the Questions

**With sub-agents (Claude Code, Cowork):**
For each question, invoke a sub-agent with just the document content and the question -- no context from this conversation. Also run a sub-agent to check for:
- Ambiguity in key terms or decisions
- False assumptions the doc makes
- Internal contradictions

Summarize what Reader Claude got right and wrong.

**Without sub-agents (claude.ai):**
Guide the user to test manually:
1. Open a fresh Claude conversation
2. Paste or share the document content
3. Ask the generated questions
4. Also ask: "What might be ambiguous?", "What context does this doc assume?", "Any internal contradictions?"

Have them report back what Reader Claude struggled with.

### Step 3: Fix Gaps

If Reader Claude struggled with any questions or surfaced issues:
1. List the specific problems found
2. Loop back to Stage 2 refinement for the problematic sections
3. Re-test after fixes to confirm the gaps are closed

### Exit Condition

Reader Claude consistently answers questions correctly and doesn't surface new gaps or ambiguities. The doc is ready for its audience.

## Final Review

When Reader Testing passes:

1. Recommend they do a final read-through themselves -- they own this document and are responsible for its quality
2. Suggest double-checking any facts, links, or technical details
3. Ask them to verify it achieves the impact they wanted

Ask if they want one more review, or if the work is done.

**If done**, provide final tips:
- Consider linking this conversation in an appendix so readers can see how the doc was developed
- Use appendices to provide depth without bloating the main doc
- Update the doc as feedback is received from real readers

## What NOT to Do

- **Don't skip context gathering** -- jumping straight to drafting produces generic docs that miss organizational nuance.
- **Don't reprint the whole doc after small edits** -- use `str_replace` for surgical changes. Keep brainstorming lists in conversation, not artifacts.
- **Don't skip Reader Testing** -- authors always think the doc makes sense. Fresh-eyes testing catches the gaps that matter most.
- **Don't force the workflow** -- if the user wants to skip stages or work freeform, let them. The workflow serves the user.

## Tips

- **Tone:** Direct and procedural. Explain rationale briefly when it affects behavior. Don't sell the approach -- just execute it.
- **Deviations:** If user wants to skip a stage, let them. If frustrated, acknowledge and suggest ways to move faster. Always give user agency to adjust the process.
- **Context gaps:** Address missing context immediately as it comes up -- don't let gaps accumulate. If context is missing on something mentioned, proactively ask.
- **Artifacts:** Use `create_file` for drafting full sections, `str_replace` for all edits, provide link after every change. Brainstorming lists stay in conversation, not in artifacts.
- **Quality:** Don't rush through stages. Each iteration should make meaningful improvements. The goal is a document that actually works for readers.
