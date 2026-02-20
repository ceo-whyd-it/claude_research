---
name: learning-a-concept
description: Create learning paths for concepts, methodologies, and mental models. Use when user asks to learn about non-code topics like GTD, Zettelkasten, second brain, TDD methodology, design thinking, or any structured approach/framework of thought.
---

# Learning a Concept

Create comprehensive learning paths for concepts, methodologies, and mental models.

## Workflow

### Phase 1: Research

Gather information from two sources. Research each source independently, then aggregate findings.

**Note:** Concepts do not have repositories — only `docs_researcher` and `web_researcher` are used.

#### From Official Documentation

- Canonical source URL (book, website, original author)
- The motivation behind the concept
- What problem does it solve / what does it help with
- Who is it for and when should it be applied
- Core principles (3-5 fundamental ideas)
- The methodology or process steps
- Official examples or case studies
- Known limitations or common misapplications

#### From Community Content

- Top tutorials and guides (title, author, URL, why it's valuable)
- Video resources (title, channel, duration)
- Comparison articles (vs alternatives, key tradeoffs)
- Common gotchas and mistakes people mention
- Community channels (Reddit, forums, dedicated communities)
- Real-world use cases and testimonials
- Tools and apps that implement or support the concept

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Overview & Motivation
2. Level 2: Core Principles
3. Level 3: The Methodology
4. Level 4: Practical Application
5. Level 5: Next Steps

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the learning path folder.

## Output Format

Create the folder in the current working directory (`./research_output/concept-{concept-name}/`) containing:

```
research_output/concept-{concept-name}/
├── README.md           # Overview, essential references, and how to use this learning path
├── resources.md        # All links organized by source (official, community)
├── learning-path.md    # Main content following the five levels
└── templates/          # Printable templates, checklists, worksheets
    ├── 01-quick-start/
    ├── 02-core-workflow/
    └── 03-advanced/
```

### README.md Must Include an "Essential References" Section

After the overview and before the learning path description, include a curated **Essential References** section with the 4-6 most important links a learner should bookmark:

- **Official docs** — main documentation or canonical source URL
- **Best tutorial** — single best written tutorial with author name
- **Best video** — single best video resource with channel and duration
- **Community** — primary community channel (Reddit, forums, or dedicated communities)

Note: Concepts do not have repositories or changelogs — skip "Repository" and "Changelog/Releases" rows.

Format as a markdown table:

| Resource | Link | Why |
|----------|------|-----|
| Official Docs | [docs.example.com](https://docs.example.com) | Comprehensive reference, always up-to-date |
| ... | ... | ... |
