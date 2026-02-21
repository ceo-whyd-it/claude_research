---
name: research-from-notes
description: Enhance local draft files with internet research. Use when user says "enhance my notes", "research from my drafts", "expand my local files", or has draft content in research_input/ that needs verification and expansion.
---

# Research From Notes

Read the user's local draft files, identify what needs verification and expansion, delegate internet research to subagents with that context, and produce enhanced output that integrates draft content with research findings.

## Workflow

### Phase 0: Read & Analyze Local Drafts

1. Use Glob to discover all text files in `research_input/{topic}/` (`.md`, `.txt`, and other text formats)
2. Read each file using Read
3. Extract from the drafts:
   - **Topics mentioned** — subjects, technologies, concepts referenced
   - **Claims to verify** — factual statements, version numbers, dates, attributions
   - **Questions raised** — explicit questions or implied gaps ("I'm not sure if...", "TODO", "?")
   - **Gaps to fill** — areas that are mentioned but underdeveloped
4. Create a synthesis organized by which subagent should handle what:
   - `docs_researcher`: claims needing official source verification, technical details to confirm
   - `web_researcher`: topics needing broader context, questions to answer, gaps to fill with community knowledge
   - `repo_analyzer`: only if drafts mention specific repositories, tools, or code patterns to verify

**If no `research_input/{topic}/` folder exists:** Stop and guide the user:

> To use this skill, create a folder with your draft files:
>
> ```
> mkdir research_input/{topic}
> ```
>
> Then add your draft files (`.md`, `.txt`, etc.) to that folder and try again.

### Phase 1: Research (Guided by Drafts)

Delegate to subagents in parallel. Each delegation prompt MUST include relevant excerpts from the drafts so subagents know what to verify and expand.

#### From Official Documentation (docs_researcher)

- Verify factual claims found in drafts against official sources
- Confirm version numbers, release dates, and attributions
- Find official documentation for topics mentioned in drafts
- Look up best practices and recommendations for technologies referenced
- Include draft excerpts as context: "The draft states: '{claim}'. Verify this against official sources."

#### From Community Content (web_researcher)

- Find articles and discussions that expand on draft topics
- Answer explicit questions raised in the drafts
- Fill knowledge gaps identified in the analysis
- Find real-world examples and case studies for concepts in drafts
- Discover perspectives the drafts may have missed
- Include draft excerpts as context: "The draft asks: '{question}'. Find authoritative answers."

#### From Repository Analysis (repo_analyzer)

- **Only if drafts mention specific repos or tools**
- Verify code patterns or examples mentioned in drafts
- Find working examples for techniques discussed
- Check if referenced APIs or interfaces are current
- Include draft excerpts as context: "The draft references this pattern: '{code}'. Verify it works."

### Phase 2: Merge & Structure

For each topic area from the drafts:

1. Start with the original draft content as the foundation
2. Layer in verification results (confirmed, corrected, or flagged)
3. Add expansion from research (new context, answers, examples)
4. Fill identified gaps with researched content

Organize into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Problem Space (Validated)
2. Level 2: Key Players & Solutions (Verified)
3. Level 3: Landscape Map (Contextualized)
4. Level 4: Tradeoffs & Considerations (Claims Verified, Gaps Filled)
5. Level 5: Next Steps (Answered & Directed)

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

**Content attribution:** Clearly distinguish what came from drafts vs. what was researched:
- `[Draft]` — content from original draft files
- `[Verified]` — draft content confirmed by research
- `[Corrected]` — draft content that was inaccurate, with correction
- `[Expanded]` — new content added by research
- `[Gap Filled]` — content addressing a gap or question from drafts

### Phase 3: Output

Generate the research folder.

## Output Format

Create the folder in the current working directory (`./research_output/enhanced-{topic}/`) containing:

```
research_output/enhanced-{topic}/
├── README.md              # Overview + draft analysis summary + what changed
├── original-drafts/       # Copy of input files for reference
├── enhanced-content.md    # Main 5-level content integrating drafts + research
├── verification.md        # Claims table: claim | status | source | notes
└── resources.md           # All links organized by relevance to draft topics
```

### File Details

**README.md** — Overview including:
- What draft files were processed
- Summary of analysis (topics found, claims checked, questions answered, gaps filled)
- High-level summary of what changed between drafts and enhanced output

**original-drafts/** — Copy of all input files from `research_input/{topic}/` for reference

**enhanced-content.md** — The main deliverable:
- 5-level progressive learning structure
- Integrates original draft content with research findings
- Uses attribution tags (`[Draft]`, `[Verified]`, `[Corrected]`, `[Expanded]`, `[Gap Filled]`)
- Each section builds on the previous, from validated problem space to directed next steps

**verification.md** — Systematic claim verification:

| Claim | Status | Source | Notes |
|-------|--------|--------|-------|
| "Python 3.10 introduced pattern matching" | Verified | docs.python.org | PEP 634, released Oct 2021 |
| "React is faster than Vue" | Corrected | benchmarks.dev | Depends on use case; Vue is comparable |

**resources.md** — All links from research, organized by:
- Relevance to specific draft topics
- Source type (official docs, articles, discussions, repos)
- Priority (directly answers draft questions vs. supplementary)
