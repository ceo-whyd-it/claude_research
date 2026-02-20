---
name: create-blog-series
description: Transform completed research output into a multi-part linked blog series. Use when user says "create blog series", "turn this into blog posts", "blog this research", "make blog posts from", or wants to generate publishable content from research.
---

# Create Blog Series

Transform completed research output into a hierarchical, multi-part blog series with linked navigation.

## Prerequisite

This skill requires completed research with at least `README.md` and `learning-path.md` in a `research_output/` subfolder. If none exists, prompt the user to run a learning or research skill first.

## Workflow

### Phase 1: Identify Source

Use **Bash** to discover available research folders (the orchestrator does not have Glob or Read):

1. Run `ls research_output/` to list available folders
2. Present the list to the user and ask which research to convert
3. Run `ls research_output/{folder}/` to verify these required files exist:
   - `README.md` (required)
   - `learning-path.md` (required)
4. From the same listing, note whether these optional sources are present:
   - `practical-takeaways.md` — if present, Part 6 will be generated
   - `code-examples/` folder — if present, Part 7 will be generated

Do NOT attempt to read file contents — the `blog_writer` subagent handles all parsing.

### Phase 2: Generate

Spawn the `blog_writer` subagent using the **Task tool** with only:
- **Folder path**: Full path to the research output folder (e.g., `research_output/framework-claude-agent-sdk/`)
- **Today's date**: For frontmatter date fields (today is {{date}})

The blog_writer will independently:
1. Read and parse all source files (README.md, learning-path.md, etc.)
2. Discover optional content (practical-takeaways.md, code-examples/)
3. Create the directory structure under `blog/{series-slug}/`
4. Generate all blog posts with proper frontmatter
5. Wire prev/next navigation links across subfolders

### Phase 3: Verify

After the blog_writer completes, use **Bash** to verify the output:

1. Run `ls -R research_output/{folder}/blog/` to confirm the file structure
2. Report to the user showing:
   - Total parts generated
   - File paths for each part
   - Which optional parts were included/skipped

## Output Structure

```
research_output/{topic}/blog/{series-slug}/
├── 00-introduction.md
├── chapters/
│   ├── 01-{level-1-slug}.md
│   ├── 02-{level-2-slug}.md
│   ├── 03-{level-3-slug}.md
│   ├── 04-{level-4-slug}.md
│   ├── 05-{level-5-slug}.md
│   └── 06-practical-takeaways.md         ← if practical-takeaways.md exists
└── code-examples/
    └── 07-hands-on-code.md               ← if code-examples/ exists
```
