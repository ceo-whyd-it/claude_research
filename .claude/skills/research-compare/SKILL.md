---
name: research-compare
description: Side-by-side comparison of 2-4 alternatives. Use when user says "compare", "vs", "which should I use", "X or Y", "alternatives to", or wants to choose between options.
---

# Research Compare

Create a structured side-by-side comparison of 2-4 alternatives to help the user make a decision.

## Workflow

### Phase 0: Clarify Alternatives

If the user has not specified which alternatives to compare, ask them before proceeding. For example:

- "Compare React vs Vue" — alternatives are clear, proceed.
- "Compare web frameworks" — ask: "Which frameworks would you like to compare? (e.g., Django vs FastAPI vs Flask)"
- "What database should I use?" — ask: "Which databases are you considering? (e.g., PostgreSQL vs MongoDB vs SQLite)"

### Phase 1: Research

Gather information from all three sources. Research each source independently, then aggregate findings.

**Note:** All three subagents are used — `docs_researcher` gets official specs, `repo_analyzer` checks repositories, and `web_researcher` finds community opinions and benchmarks.

#### From Official Documentation (docs_researcher)

For EACH alternative being compared:

- Official docs URL and current version
- Primary use cases and target audience
- Key features and capabilities
- Installation and setup complexity
- Performance claims or benchmarks from official sources
- Pricing model (if applicable)
- Known limitations acknowledged by maintainers

#### From the Repository (repo_analyzer)

For EACH alternative being compared (if it has a public repo):

- Repository URL and metadata (stars, forks, last commit, license)
- Commit frequency and contributor count (project health)
- Issue count and response time (maintenance quality)
- Code size and dependency count
- Quality of examples and documentation in repo
- Release frequency and versioning

#### From Community Content (web_researcher)

- Head-to-head comparison articles
- Benchmark results from independent sources
- Migration stories (people who switched from one to another)
- Community size indicators (Stack Overflow questions, Reddit activity, Discord members)
- Common complaints and praise for each
- "I chose X because..." posts and discussions
- Industry adoption trends

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: What & Why
2. Level 2: Feature Matrix
3. Level 3: Tradeoff Analysis
4. Level 4: Real-World Fit
5. Level 5: Decision Framework

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the comparison folder.

## Output Format

Create the folder in the current working directory (`./research_output/compare-{alternatives}/`) containing:

```
research_output/compare-{alternatives}/
├── README.md           # Overview and how to use this comparison
├── comparison.md       # Detailed comparison with feature matrix and analysis
├── resources.md        # All links organized by alternative and source
└── learning-path.md    # Main content following the five levels
```

For the folder name, join alternative names with `-vs-` (e.g., `compare-fastapi-vs-django-vs-flask`).
