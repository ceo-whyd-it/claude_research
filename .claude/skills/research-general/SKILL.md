---
name: research-general
description: Perform a broad landscape scan on any topic. Use when user asks for an "overview of", "landscape", "what's out there on", "broad research on", "survey of", or wants a wide but shallow scan before diving deeper.
---

# Research General

Perform a wide landscape scan on a topic — identify key players, solutions, tradeoffs, and where to dig deeper.

## Workflow

### Phase 1: Research

Gather information from two sources. Research each source independently, then aggregate findings.

**Note:** General research is wide, not deep — only `docs_researcher` and `web_researcher` are used. Skip `repo_analyzer`.

#### From Official Documentation (docs_researcher)

- Identify the primary sources and authorities on the topic
- Official definitions, standards, or specifications
- Key organizations or companies involved
- Canonical resources and reference material
- Current state of the art or best practices
- Industry reports or white papers if available

#### From Community Content (web_researcher)

- Blog posts, articles, and opinion pieces on the topic
- Video resources (talks, tutorials, conference presentations)
- Community discussions (Reddit, HN, forums)
- Comparison and "state of" articles
- Different perspectives and schools of thought
- Emerging trends and recent developments
- Real-world case studies and experience reports

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Problem Space
2. Level 2: Key Players & Solutions
3. Level 3: Landscape Map
4. Level 4: Tradeoffs & Considerations
5. Level 5: Recommended Deep Dives

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the research folder.

## Output Format

Create the folder in the current working directory (`./research_output/research-{topic}/`) containing:

```
research_output/research-{topic}/
├── README.md           # Overview and how to use this research summary
├── landscape.md        # The full landscape map with categories and players
├── resources.md        # All links organized by source and category
└── learning-path.md    # Main content following the five levels
```
