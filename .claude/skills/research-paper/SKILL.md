---
name: research-paper
description: Deep dive into a specific academic paper. Use when user says "explain this paper", "paper deep dive", "summarize paper", provides a specific paper title, or shares an arxiv URL.
---

# Research Paper

Create a comprehensive deep dive into a specific academic paper — summarize it, explain the method, and extract practical takeaways.

## Workflow

### Phase 1: Research

Gather information from two sources. Research each source independently, then aggregate findings.

**Note:** Paper research primarily uses `web_researcher` and `docs_researcher`. Skip `repo_analyzer` unless the paper has a known companion repository — in that case, use `repo_analyzer` to examine the reference implementation.

#### From Community Content (web_researcher)

- Find the paper on arxiv or other sources
- Blog posts explaining or summarizing the paper
- Twitter/X threads discussing the paper
- Conference talks or video presentations by the authors
- Follow-up papers that cite or build on this work
- Community discussions (Reddit, HN, forums)
- Critiques or rebuttals of the paper
- Simplified explanations or "ELI5" versions

#### From Official Documentation (docs_researcher)

- Fetch the paper abstract and full text (from arxiv, project page, or PDF link)
- Author affiliations and other notable work by same authors
- Official project page or companion website if it exists
- Datasets or benchmarks used in the paper
- Any errata or updated versions of the paper

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Background & Motivation
2. Level 2: Core Method
3. Level 3: Key Results
4. Level 4: Practical Implications
5. Level 5: Related Work & Next Steps

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the paper research folder.

## Output Format

Create the folder in the current working directory (`./research_output/paper-{paper-name}/`) containing:

```
research_output/paper-{paper-name}/
├── README.md                # Overview and how to use this paper summary
├── summary.md               # Structured summary of the paper
├── practical-takeaways.md   # What practitioners can use from this paper
├── resources.md             # All links (paper, discussions, related work)
└── learning-path.md         # Main content following the five levels
```

For the folder name, use a short slug of the paper title (e.g., `paper-attention-is-all-you-need`).
