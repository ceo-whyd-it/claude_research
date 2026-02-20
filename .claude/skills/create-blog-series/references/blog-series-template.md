# Blog Series Template Reference

This document defines the frontmatter schema, post body templates, and navigation rules for the blog series generator.

## Frontmatter Schema

Every post in the series uses this exact frontmatter format:

```yaml
---
title: "{Series Title} — Part {N}: {Part Title}"
date: YYYY-MM-DD
series_name: "{series-slug}"
part_number: 0
total_parts: 6
prev: null
next: "./chapters/01-getting-started.md"
tags: ["topic-name", "series"]
excerpt: "Under 160 characters describing this post"
draft: true
---
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Format: `{Series Title} — Part {N}: {Part Title}`. Part 0 uses "Introduction" as part title. |
| `date` | date | YYYY-MM-DD format, same date for all posts in the series |
| `series_name` | string | Slug matching the research folder name (e.g., `framework-claude-agent-sdk`) |
| `part_number` | integer | 0-based index of this post in the series |
| `total_parts` | integer | 6, 7, or 8 depending on available source material |
| `prev` | string or null | Relative path to previous post, null for Part 0 |
| `next` | string or null | Relative path to next post, null for the final part |
| `tags` | array | Always includes the topic name and "series" |
| `excerpt` | string | Under 160 characters, descriptive and enticing |
| `draft` | boolean | Always `true` — user publishes manually |

### Relative Path Examples for prev/next

Paths are relative to the file's own location.

**From `00-introduction.md` (root level):**
- prev: `null`
- next: `"./chapters/01-overview-and-motivation.md"`

**From `chapters/01-overview-and-motivation.md`:**
- prev: `"../00-introduction.md"`
- next: `"./02-installation-and-hello-world.md"`

**From `chapters/02-installation-and-hello-world.md`:**
- prev: `"./01-overview-and-motivation.md"`
- next: `"./03-core-concepts.md"`

**From `chapters/05-next-steps.md` (when Part 6 exists):**
- prev: `"./04-practical-patterns.md"`
- next: `"./06-practical-takeaways.md"`

**From `chapters/06-practical-takeaways.md` (when Part 7 exists):**
- prev: `"./05-next-steps.md"`
- next: `"../code-examples/07-hands-on-code.md"`

**From `code-examples/07-hands-on-code.md`:**
- prev: `"../chapters/06-practical-takeaways.md"` (or `"../chapters/05-next-steps.md"` if no Part 6)
- next: `null`

## Post Body Templates

### Part 0 — Introduction

```markdown
{Hook — counterintuitive angle on the topic, 2-3 sentences}

## Series Structure

| Part | Title | Location |
|------|-------|----------|
| 0 | Introduction | [This post](./00-introduction.md) |
| 1 | {Level 1 Title} | [Chapter 1](./chapters/01-{slug}.md) |
| 2 | {Level 2 Title} | [Chapter 2](./chapters/02-{slug}.md) |
| 3 | {Level 3 Title} | [Chapter 3](./chapters/03-{slug}.md) |
| 4 | {Level 4 Title} | [Chapter 4](./chapters/04-{slug}.md) |
| 5 | {Level 5 Title} | [Chapter 5](./chapters/05-{slug}.md) |
| 6 | Practical Takeaways | [Chapter 6](./chapters/06-practical-takeaways.md) |
| 7 | Hands-On Code | [Code Examples](./code-examples/07-hands-on-code.md) |

{Only include rows 6 and 7 if those source materials exist.}

## Who This Is For

{Target audience — who benefits from this series, what level of experience is assumed}

## How to Read This Series

{Reading order suggestions — sequential for beginners, jump-to for experienced readers}

## Essential References

| Resource | Link |
|----------|------|
| Official Docs | [{title}]({url}) |
| Repository | [{title}]({url}) |
| Best Tutorial | [{title}]({url}) |

{Top 3 links — the same ones from README.md's Essential References section.}
```

Target length: 400-600 words.

### Parts 1-5 — Chapters

```markdown
{Hook — counterintuitive opening, NOT a definition or history. 2-3 sentences.}

## {Main Section Heading}

{Adapted content from this level of learning-path.md. NOT copy-paste.
 Restructure for narrative flow. Add transitions. Create a story arc.
 Break into subsections as needed.}

### {Subsection if needed}

{Code block or mermaid diagram — at least one per post is required.}

```language
// Working example that demonstrates the concept
```

## Takeaway

{What the reader can now do or understand. Specific and actionable. 2-3 sentences.}

## Further Reading

- [{Link Title}]({URL}) — {one-line description}
- [{Link Title}]({URL}) — {one-line description}

{2-4 links from resources.md most relevant to this chapter's topic. Every link must have a working URL.}
```

Target length: 800-1500 words.

### Part 6 — Practical Takeaways

```markdown
{Hook — why practical application differs from theory. 2-3 sentences.}

## Key Takeaways

{Condensed, actionable insights from practical-takeaways.md.
 Bullet points or numbered list with brief explanations.
 Each takeaway should be something the reader can act on immediately.}

## When to Use What

{Decision guide — help readers choose the right approach for their situation.
 Could be a table, flowchart (mermaid), or structured comparison.}

## Further Reading

- [{Link Title}]({URL}) — {one-line description}
- [{Link Title}]({URL}) — {one-line description}

{2-4 links to decision guides and comparison articles from resources.md.}
```

Target length: 600-1200 words.

### Part 7 — Hands-On Code

```markdown
{Hook — why running code teaches more than reading about it. 2-3 sentences.}

## Examples Overview

{Brief table or list of what each code example subfolder contains.}

## {Example Subfolder Name} (e.g., "Hello World")

{Walkthrough of the example — what it demonstrates, key files, expected output.
 Include relevant code snippets inline.}

```language
// Key code from the example
```

{Repeat for each subfolder in code-examples/.}

## Running the Examples

{Prerequisites and instructions for running the code examples.}

## Further Reading

- [{Link Title}]({URL}) — {one-line description}
- [{Link Title}]({URL}) — {one-line description}

{2-4 links to example repos and getting-started guides from resources.md.}
```

Target length: 600-1200 words.

## Navigation Footer Rules

The navigation footer appears at the bottom of every post, after a horizontal rule.

### Format by Position

**Part 0 (first post):**
```markdown
---

**Next: [Part 1: {Title}](./chapters/01-{slug}.md) ->**
```

**Part 1 (prev is introduction, in different folder):**
```markdown
---

**<- Previous: [Introduction](../00-introduction.md)** | **[Series Home](../00-introduction.md)** | **Next: [Part 2: {Title}](./02-{slug}.md) ->**
```

**Parts 2-4 (middle chapters, same folder):**
```markdown
---

**<- Previous: [Part {N-1}: {Title}](./{prev-file})** | **[Series Home](../00-introduction.md)** | **Next: [Part {N+1}: {Title}](./{next-file}) ->**
```

**Last part in series (whichever part is final):**
```markdown
---

**<- Previous: [Part {N-1}: {Title}]({prev-path})** | **[Series Home](../00-introduction.md)**

*This is the final part of the series. Return to the [Introduction](../00-introduction.md) for the full series map.*
```

**Cross-subfolder navigation (chapters → code-examples):**
- From any chapter to Part 7: `../code-examples/07-hands-on-code.md`
- From Part 7 to any chapter: `../chapters/{filename}.md`
- From Part 7 to introduction: `../00-introduction.md`
