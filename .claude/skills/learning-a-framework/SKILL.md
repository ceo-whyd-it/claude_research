---
name: learning-a-framework
description: Create learning paths for software frameworks and SDKs. Use when user asks to learn about frameworks like Django, Next.js, Claude Agent SDK, LangChain, DSPy, Rails, FastAPI, or any full-featured development framework.
---

# Learning a Framework

Create comprehensive learning paths for software frameworks and SDKs.

## Workflow

### Phase 1: Research

Gather information from three sources. Research each source independently, then aggregate findings.

#### From Official Documentation

- Official docs URL and current version
- The motivation behind the framework
- What problem does it solve / what does it help with
- What types of applications can be built with it
- Use cases
- Installation steps and prerequisites
- Project scaffolding / quick start commands
- Core architecture (request lifecycle, component model, data flow)
- Core concepts (3-5 fundamental ideas)
- Official code examples and starter templates
- Plugin/extension ecosystem overview
- API reference highlights
- Known limitations or caveats

#### From the Repository

- Repository URL and metadata (stars, last commit, license)
- Core system architecture (directory structure, entry points, configuration)
- README quick start section
- Examples folder contents (what each example demonstrates)
- Starter templates or project generators
- Extension points and plugin architecture
- Concise summary of the project's main function and the technologies used

#### From Community Content

- Top tutorials (title, author, URL, why it's valuable)
- Video resources (title, channel, duration)
- Comparison articles (vs alternatives, key tradeoffs)
- Common gotchas and mistakes people mention
- Community channels (Discord, Reddit, forums)
- Real-world use cases and testimonials
- Popular plugins, extensions, or middleware

### Phase 2: Structure

Organize content into progressive levels. `references/progressive-learning.md` is the source of truth.

You MUST create exactly 5 levels in this order:

1. Level 1: Overview & Motivation
2. Level 2: Setup & First Project
3. Level 3: Architecture & Core Concepts
4. Level 4: Building Real Applications
5. Level 5: Next Steps

Do NOT merge, skip, or rename levels. Each level's content requirements are defined in the reference file.

### Phase 3: Output

Generate the learning path folder.

## Output Format

Create the folder in the current working directory (`./research_output/framework-{framework-name}/`) containing:

```
research_output/framework-{framework-name}/
├── README.md           # Overview, essential references, and how to use this learning path
├── resources.md        # All links organized by source (official, community)
├── learning-path.md    # Main content following the five levels
└── code-examples/      # Runnable code for each section
    ├── 01-hello-world/
    ├── 02-core-concepts/
    └── 03-real-app/
```

### README.md Must Include an "Essential References" Section

After the overview and before the learning path description, include a curated **Essential References** section with the 5-8 most important links a learner should bookmark:

- **Official docs** — main documentation URL
- **Repository** — GitHub URL with star count
- **Best tutorial** — single best written tutorial with author name
- **Best video** — single best video resource with channel and duration
- **Community** — primary community channel (Slack, Discord, or Reddit)
- **Changelog/Releases** — where to track updates

Format as a markdown table:

| Resource | Link | Why |
|----------|------|-----|
| Official Docs | [docs.example.com](https://docs.example.com) | Comprehensive reference, always up-to-date |
| ... | ... | ... |
