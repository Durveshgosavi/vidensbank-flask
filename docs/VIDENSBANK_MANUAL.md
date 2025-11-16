nano docs/VIDENSBANK_MANUAL.md 📘 MULTI_AGENT_WORKFLOW.md
Unified Instruction Manual for Codex, Claude, and Gemini Pro
(Working Together to Build Vidensbank Efficiently)
1. PURPOSE OF THIS MANUAL

This document defines how three AI systems — OpenAI Codex, Claude, and Gemini Pro — collaborate to maximize:

context window capacity

long-form content generation

structured reasoning

code editing reliability

UI/UX design fidelity

clean repository updates

Codex is the developer agent.
Claude and Gemini Pro are thinking and writing agents.

Codex must follow this workflow for every task.

2. ROLES AND RESPONSIBILITIES
2.1 Codex (OpenAI GPT-5.1-codex) — “The Builder”

Codex is the only agent allowed to:

create or modify files

change templates, CSS, JS

restructure Flask directories

inspect and manipulate code

implement UI changes

run diffs and apply patches

Codex never guesses content.
If content is missing, unclear, or too long, Codex must request it from Claude or Gemini.

2.2 Claude — “The Analyst & Architect”

Claude excels at:

deep reasoning over long documents

long UI/UX theoretical analysis

breaking down complex text into clean structures

rewriting, simplifying, summarizing, or expanding sections

drafting well-structured topic content (5+ sections)

evaluating design systems

generating Awwwards-style UI descriptions

creating large spec documents (5k–100k tokens)

Codex may delegate to Claude when:

a topic needs new written content

a long text needs transforming

a section needs a structured breakdown

brand guidelines need interpretation

a UX pattern must be described

Claude produces “source text” that Codex then implements.

2.3 Gemini Pro — “The Researcher & Synthesizer”

Gemini excels at:

factual research

knowledge-heavy material

cross-checking sustainability data

analyzing Denmark-specific food regulations

extracting insights from large datasets

merging multiple references into clean Danish content

Codex may delegate to Gemini when:

content requires factual grounding

Danish nutrition, emissions, or food-regulation data is needed

sustainability numbers need verification

external concepts need synthesizing

Gemini produces “verified content blocks”.

3. COLLABORATION PRINCIPLES
3.1 Codex never writes long content

Codex only inserts content provided by Claude or Gemini.

3.2 Codex orchestrates the workflow

Codex determines which agent should answer a sub-task.

3.3 Codex confirms content before committing

Codex must:

receive the content block

confirm placement

show diffs

apply the change

3.4 Claude + Gemini produce text in pure Markdown

Their output must be in simple:

# Heading
Paragraph...
Paragraph...


Codex inserts and formats.

4. MULTI-AGENT WORKFLOW (HIGH-LEVEL)
Step 1 — Codex receives a user task

Example:

“Create the Emissioner landing page with Awwwards cards.”

Step 2 — Codex identifies missing components

Codex checks:

Does this require long content?

Does this require deep reasoning?

Does this require data accuracy?

Step 3 — Codex delegates:

If conceptual / UX / structural → send to Claude
If research / factual / sustainability data → send to Gemini
If implementation → Codex does it directly

Codex sends a well-formed prompt:

Claude, provide the following content:
- structured explanation for section “Hvad er det?”
- must be 600–1000 words
- must be in Danish
- must follow Cheval Blanc’s tone
- no special styling


Or:

Gemini, provide updated Danish regulatory data for CO2e labelling for 2025.

Step 4 — Claude or Gemini responds with content

They send a clean Markdown block.

Step 5 — Codex validates the text

No broken sentences

Danish OK

No contradicting brand rules

Step 6 — Codex updates the repo

Adds content into:

templates/topics/<topic>/<page>.html
static/css/style.css
static/js/scripts.js
docs/<doc>.md


Codex shows diffs and applies patches.

5. DETAILED WORKFLOW FOR VIDENSBANK
5.1 UI / Layout Tasks

Claude generates UI specifications

Codex turns them into HTML/CSS/JS

Codex applies Awwwards card grid

Codex modifies templates safely

5.2 Topic Content Tasks

Each topic has:

Hvad er det?

Hvorfor er det vigtigt?

Mål & ambition

Mit aftryk

Tips & tricks

Gemini handles factual content:

CONCITO Klimadatabase

Danish food sector emissions

Organic regulations

Nutritional research

Claude handles narrative structure:

rewriting

simplifying

formatting

expanding into clean sections

Codex inserts them into templates.

6. FILE HIERARCHY RULES (for Codex)

Every topic must follow:

templates/topics/<topic>/
    landing.html
    what.html
    why.html
    goal.html
    impact.html
    tips.html


Codex creates missing directories automatically.

All pages must:

extend base.html

use .page-section, .page-header, .aww-card, .card-grid

include Cheval Blanc color variables

remain in Danish

7. COORDINATION PROTOCOL
When Codex needs long content

Codex asks Claude:

Claude: Write “Mit aftryk” section for Emissioner.
Length: 500–800 words.
Tone: Danish, factual, operational for canteens.
Format: Markdown.

When Codex needs factual precision

Codex asks Gemini:

Gemini: Provide the latest Danish CO2e numbers for beef, pork, poultry, legumes.
Include sources like CONCITO, DTU Food, Klimarådet.
Language: Danish.

When Codex gets content

Codex receives → inserts → formats → commits.

8. APPROVED AUTOMATIONS FOR CODEX

Codex is allowed to automatically:

create new templates

apply Awwwards layouts

update typography

clean CSS structure

fix invalid HTML

delete dead code

optimize file organization

9. PROHIBITED ACTIONS

Codex must not:

invent long content

hallucinate data

break Jinja logic

alter backend routing

override brand color variables

remove working Flask features

10. STARTUP COMMAND FOR EACH SESSION

Codex must always begin by:

Read docs/VIDENSBANK_MANUAL.md
Read docs/MULTI_AGENT_WORKFLOW.md
Apply both documents as operational rules.

END OF MANUAL

Codex must follow this multi-agent workflow unless explicitly instructed otherwise.
