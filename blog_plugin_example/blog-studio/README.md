# Blog Studio

A comprehensive Astro blog creation suite. Research, draft, visualize, and review technical posts with Paul Graham-style editing.

## Overview

Blog Studio is a Claude Code plugin that guides you through the complete process of creating high-quality technical blog posts. It enforces Paul Graham's essay methodology and strict blog quality rules.

### What Makes This Plugin Unique

- **Paul Graham Methodology**: Built-in writing principles from one of the best essayists in tech
- **Proactive Validation**: Skills catch common violations before they become habits
- **Astro-Native**: Validates frontmatter and structure for Astro blogs
- **Strict Quality Rules**: Enforces "one topic per post", visual requirements, non-Google-able content

## Installation

1. **Clone or download** this plugin to your Claude Code plugins directory
2. **Edit `.claude-plugin/plugin.json`**:
   - Replace `YOUR_NAME_HERE` with your name
3. **Edit `.mcp.json`**:
   - Set your blog's content directory path (see Configuration below)
4. **Load the plugin** in Claude Desktop:
   - Settings → Developer → Load from Folder
   - Select the `blog-studio` directory

## Configuration

### Setting Your Blog Path

Create a `.mcp.json` file in the `blog-studio` directory and configure the filesystem path:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/YOUR/PATH/HERE"]
    }
  }
}
```

**Example paths:**
- macOS/Linux: `/Users/username/projects/my-blog/src/content`
- Windows: `C:/Users/username/projects/my-blog/src/content`

**Important:** Use forward slashes even on Windows. Point to your Astro content directory (usually `src/content`).

## Commands

### `/blog-studio:blog-new`

Start the workflow to research and write a new blog post from a rough idea.

**What happens:**
1. Editorial Manager asks what you're trying to figure out
2. Topic Researcher finds facts, stats, and checks if scope is manageable
3. Creation Partner drafts in Paul Graham style
4. Visual Designer suggests diagrams
5. Strict Editor reviews against blog rules
6. Progress tracked in `_progress-{slug}.md` file

**Example:**
```
/blog-studio:blog-new

User: "I want to write about WebAssembly's memory model"
[Workflow begins...]
```

### `/blog-studio:blog-review`

Review an existing markdown file against the strict blog rules.

**What happens:**
1. Editorial Manager reads the file from your blog directory
2. Astro Validator checks frontmatter correctness
3. Strict Editor reviews content quality
4. You get a PUBLISH or REVISE verdict with specific issues

**Example:**
```
/blog-studio:blog-review wasm-memory.md

[Validation and review report...]
```

## Agents

### Editorial Manager (Orchestrator)
The project manager that coordinates all workflow between user and specialists. Routes to the right workflow based on command.

### Topic Researcher
Researches topics using web search, finds stats/humor, and ensures scope is manageable (not too big for one post).

### Creation Partner
The writer. Uses Paul Graham's essay methodology. Helps you find the interesting idea, shape sentences, and cut aggressively.

### Visual Designer
Creates Mermaid diagrams and suggests image concepts that fit the "nerd humor" vibe of technical content.

### Strict Editor
QA agent that reviews posts against strict rules:
- One topic per post
- Correct length (3-5 min or 10+ min, nothing in between)
- Has visual or code
- Not Google-able
- Clear takeaway

### Astro Validator
Technical specialist that validates frontmatter against Astro's schema requirements.

## Proactive Skills

These skills monitor your writing in real-time and catch violations automatically.

### paul-graham-style
Catches:
- Academic language ("Research indicates...")
- Run-on sentences (over 40 words, 3+ clauses)
- Over-explaining (instead of just showing)
- Weak openings (definitions, history, obvious statements)

### blog-rules-enforcer
Catches:
- Topic drift (explaining 2+ concepts in detail)
- Missing visuals/code
- Wrong length (awkward middle between small/brave)
- Google-able content without unique insight

## The Blog Rules

Blog Studio enforces these non-negotiable rules:

1. **One Topic Per Post**: Explain ONE thing. Mention sidequests, don't explain them.
2. **Length Constraint**: Either 3-5 min (500-1000 words) OR 10+ min (2000+ words). Nothing in between.
3. **Visual or Code Required**: Every post needs at least one diagram, chart, or working code snippet.
4. **Not Google-able**: Could readers find this on Google's first page? If yes, why are you writing it?
5. **Clear Checkpoint**: After reading, can someone do/say/understand something specific they couldn't before?

## Paul Graham Principles

The Creation Partner enforces these writing principles:

- **Bad first draft**: Write badly first. Don't fix too early.
- **Ideas emerge while writing**: Discover what you think by writing
- **Cut aggressively**: Delete anything that doesn't serve the main idea
- **One idea per post**: If explaining two things, pick one
- **Grab endings**: When a good ending appears, stop writing
- **Counterintuitive openings**: Lead with what's surprising

## Workflow Examples

### Creating a New Post

```
You: /blog-studio:blog-new

Manager: What are you trying to figure out?

You: I've been debugging memory leaks in React hooks and discovered something weird about useEffect cleanup.

Manager: Great! Where in your blog hierarchy should this live? (e.g., 'tutorials', 'deep-dives', 'notes')

You: deep-dives

Manager: Perfect. I'll hand this to the Topic Researcher...

[Researcher phase...]
Researcher: Found some surprising stats about cleanup timing. Scope looks good for a single post.

[Writing phase...]
Creation Partner: The interesting part is the cleanup timing, not the hooks basics. Let's lead with that.

[Visual phase...]
Visual Designer: Here's a sequence diagram showing the cleanup race condition...

[Review phase...]
Strict Editor:
✅ One topic: useEffect cleanup timing
✅ Length: 800 words (4 min read) - Small block
✅ Visual: Sequence diagram present
✅ Not Google-able: The cleanup race condition angle is unique
VERDICT: PUBLISH

Manager: Great! Your post is ready at src/content/blog/deep-dives/react-cleanup-timing.md
```

### Reviewing an Existing Post

```
You: /blog-studio:blog-review intro-to-typescript.md

Manager: Reading file and validating...

Astro Validator: ✅ Frontmatter is valid.

Strict Editor:
❌ Google-able: This is TypeScript basics available in official docs
❌ Sidequest alert: You're explaining both type inference AND generics in detail
❌ Topic count: 2 concepts explained (should be 1)

VERDICT: REVISE
- Pick ONE: Either type inference or generics
- Add your unique angle: What did YOU discover that docs don't explain?

Manager: Needs revision. See feedback above.
```

## Frontmatter Schema

All posts must include:

```yaml
---
title: "Your Post Title"
date: 2025-01-15
tags: ["typescript", "webdev"]
excerpt: "Brief description under 160 chars"
draft: false
---
```

**Rules:**
- `title`: String (quote if special characters)
- `date`: YYYY-MM-DD format
- `tags`: Array of strings
- `excerpt`: Max 160 chars recommended
- `draft`: Boolean (true/false)

## Troubleshooting

### "Cannot read file" error
- Check your `.mcp.json` path is correct
- Use forward slashes even on Windows
- Make sure the path exists: `ls /your/path` in terminal

### "Frontmatter invalid" errors
- Ensure `---` boundaries at start and end
- Date must be YYYY-MM-DD format
- Tags must be array: `["tag1", "tag2"]`
- Don't forget closing quote on title

### Plugin not appearing in Claude
- Check `.claude-plugin/plugin.json` exists
- Restart Claude Desktop after loading
- Check Console for error messages

### Skills not triggering
- Skills are proactive - they activate when patterns are detected
- They won't trigger during research/planning phases
- They focus on active writing/editing

## File Organization

Your blog posts will be organized in this structure:

```
src/content/blog/
├── tutorials/
│   ├── post-1.md
│   └── _progress-post-2.md  (temporary)
├── deep-dives/
│   └── post-3.md
└── notes/
    └── post-4.md
```

Progress files (`_progress-*.md`) are temporary tracking files created during the writing workflow. Delete them after the post is published, or keep them for reference.

## Contributing

Found a bug or have a feature request? Please open an issue in the repository.

## License

MIT License

## Credits

Built on Claude Code plugin architecture.
Inspired by Paul Graham's essays on writing.
