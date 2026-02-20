---
name: research-arxiv
description: Find and summarize recent arxiv papers on a research topic. Use when user mentions "arxiv", "recent papers", "what's new in research on", "latest research", or asks about academic papers on a topic.
---

# Research Arxiv

Find recent arxiv papers on a topic, summarize findings, and identify trends.

## Workflow

### Phase 1: Research

Gather information from two sources. Research each source independently, then aggregate findings.

**Note:** Arxiv research does not require repository analysis — only `web_researcher` and `docs_researcher` are used.

#### From Community Content (web_researcher)

- Search arxiv.org for recent papers on the topic (last 1-2 years)
- Find blog posts, Twitter threads, and discussions about key papers
- Identify influential authors and research groups in the area
- Find survey papers or literature reviews if they exist
- Community opinions on which papers are most impactful
- Conference presentations or talks related to the topic

#### From Official Documentation (docs_researcher)

- Fetch paper abstracts and metadata from arxiv.org
- Get citation counts and related papers where available
- Find the papers' key claims and contributions from abstracts
- Identify the datasets, benchmarks, or methods referenced
- Check for companion project pages or official blog posts

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Field Overview
2. Level 2: Key Papers
3. Level 3: Methods & Approaches
4. Level 4: Trends & Open Problems
5. Level 5: Getting Involved

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the research folder.

## Output Format

Create the folder in the current working directory (`./research_output/arxiv-{topic}/`) containing:

```
research_output/arxiv-{topic}/
├── README.md           # Overview and how to use this research summary
├── papers.md           # Detailed paper summaries with links and key findings
├── synthesis.md        # Cross-paper analysis, themes, and connections
└── learning-path.md    # Main content following the five levels
```
