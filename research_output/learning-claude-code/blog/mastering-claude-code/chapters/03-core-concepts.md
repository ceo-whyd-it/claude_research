---
title: "Core Concepts: Master the Fundamentals"
description: "Learn the 5 fundamental mental models that separate casual users from power users of Claude Code."
date: 2026-02-21
part: 3
series: "Mastering Claude Code"
series_order: 3
prev: "02-installation-and-hello-world.md"
next: "04-practical-patterns.md"
tags: ["claude-code", "concepts", "agentic-loop", "context-management"]
---

# Part 3: Core Concepts

Master these 5 fundamental mental models to use Claude Code effectively.

### Concept 1: The Agentic Loop

**What it is**: Claude Code operates in a continuous gather → act → verify cycle.

**How it works**:
```
1. GATHER CONTEXT
   ├── Read files (@mentions, searches)
   ├── Run commands (ls, git status)
   └── Understand your request

2. TAKE ACTION
   ├── Edit files (Write, Edit tools)
   ├── Run commands (tests, builds, git)
   └── Create artifacts (commits, PRs)

3. VERIFY RESULTS
   ├── Check test output
   ├── Review command results
   └── Ask for confirmation

4. REPEAT until task complete or interrupted
```

**Example in practice**:
```
You: "Fix the authentication bug - users can't log in with email addresses containing +"

Claude's loop:
[GATHER] Read auth.py, user.py, tests/
[GATHER] Search for email validation patterns
[ACT] Identify regex bug in validate_email()
[ACT] Update regex to allow + character
[ACT] Run: pytest tests/test_auth.py
[VERIFY] ✓ All 15 tests pass
[ACT] Create git commit with fix
[VERIFY] Report completion
```

**Common mistake**: Interrupting too early. Let Claude complete the verification phase before redirecting.

**Pro tip**: You can press `Esc` at any time to stop current action without losing context.

---

### Concept 2: Context Window Management

**What it is**: Claude's "working memory" that holds your conversation, file contents, and command outputs.

**Why it matters**:
- Context fills up during long sessions
- Performance degrades as context approaches limit
- **Most critical skill for long sessions**

**Visual mental model**:
```
Context Window (200k tokens max)
├── System prompt (20k tokens)
├── CLAUDE.md file (if exists)
├── Your conversation history
├── Files Claude has read
├── Command outputs
└── Tool call history

When full:
├── Auto-compaction (summarizes older content)
└── Performance degradation ("Claude gets dumber")
```

**Managing context effectively**:

**Strategy 1: Use `/clear` between unrelated tasks**
```bash
You: "Refactor the authentication module"
[...long conversation...]
Claude: "Done! Tests pass."

You: /clear

You: "Now help me set up Docker for this project"
# Fresh start - auth work doesn't pollute Docker task
```

**Strategy 2: Document & Clear for multi-day work**
```bash
You: "Document your progress and next steps to progress.md, then clear context"
Claude: [Writes detailed progress file]
You: /clear
You: "Read progress.md and continue from where you left off"
```

**Strategy 3: Use CLAUDE.md for persistent rules**
```markdown
# CLAUDE.md
# This file is loaded every session automatically

## Code Style
- Use TypeScript strict mode
- Prefer async/await over callbacks

## Testing
- Run single test files, not full suite
- Use: npm test -- path/to/test.ts
```

**Monitoring context**:
```bash
/context          # Shows current token usage
/compact          # Manually trigger compaction
```

**Common mistake**: Letting context fill to 100%, then wondering why Claude makes mistakes.

**Pro tip**: **Reset at ~60-70% capacity** for best performance in long sessions.

---

### Concept 3: Permission Modes & Safety

**What it is**: Three modes controlling what Claude can do without asking.

**The three modes**:

**1. Default Mode** (Balanced)
- ✅ Reads files freely
- ❓ Asks before editing files
- ❓ Asks before running bash commands
- Best for: Most users, general work

**2. Auto-Accept Mode** (Fast)
- ✅ Reads files freely
- ✅ Edits files without asking
- ❓ Still asks for bash commands
- Best for: Trusted tasks, refactoring, test writing

**3. Plan Mode** (Safe)
- ✅ Reads files freely
- ❌ Cannot edit files
- ❌ Cannot run commands
- Best for: Exploration, planning, understanding unfamiliar code

**Switching modes**:
```bash
# Keyboard shortcut
Shift + Tab         # Cycles through modes

# Command
/plan               # Enter plan mode
/normal             # Return to normal mode

# CLI flag
claude --permission-mode plan
claude --permission-mode auto-accept
```

**Safety net: Checkpoints**
- Automatic checkpoint before each file edit
- Press `Esc + Esc` to open rewind menu
- Select checkpoint to restore
- Works like git for your Claude session

**Example workflow**:
```bash
# Start in Plan Mode to understand code
claude --permission-mode plan
You: "How does the authentication system work? What files would need changing to add OAuth?"

[Claude explores, creates plan - no changes made]

# Switch to Normal Mode to implement
Shift+Tab (to Normal Mode)
You: "Implement the OAuth flow from your plan"

[Claude edits files, asks permission for each]

# If something goes wrong
Esc + Esc           # Rewind to before changes
```

**Common mistake**: Working in default mode for large refactorings (too many permission prompts).

**Pro tip**: **Plan → Review → Auto-Accept** workflow for complex features.

---

### Concept 4: Session Continuity & Workflows

**What it is**: Claude Code sessions are persistent conversations stored locally.

**Session management**:

**Starting sessions**:
```bash
claude                    # New session
claude --continue         # Resume most recent session (alias: -c)
claude --resume           # Choose from recent sessions (alias: -r)
```

**Session philosophy**:
- Each session = one conversation thread
- Sessions preserve full context
- Can resume days/weeks later
- Sessions stored in `~/.claude/sessions/`

**When to start fresh vs continue**:

**Start FRESH when**:
- Beginning unrelated task
- Context is polluted
- Previous session had errors
- Better prompt available

**CONTINUE when**:
- Iterating on same feature
- Building on previous work
- Mid-task interruption
- Following up on questions

**Forking workflows**: Create alternative approaches
```bash
# In session A, working on feature
You: "Add user authentication"
[...work in progress...]

# Fork to try different approach
# In new terminal:
claude                    # New session (automatic fork)
You: "Try OAuth instead of JWT for authentication"
```

**Practical pattern: Git worktrees for parallel work**:
```bash
# Main session on main branch
git worktree add ../my-feature feature-branch
cd ../my-feature
claude                    # Separate session, separate branch

# Both sessions can run simultaneously
# No file conflicts, clean separation
```

**Common mistake**: Continuing sessions with 90%+ context usage.

**Pro tip**: Use `claude -c` for quick follow-ups, but **start fresh** for significant new work.

---

### Concept 5: Extensibility Through Configuration

**What it is**: Claude Code is deeply customizable through files, not UI settings.

**The configuration hierarchy**:

```
1. CLAUDE.md (Project-specific, highest priority)
   └── Lives in project root
   └── Loaded automatically every session
   └── Defines project patterns, conventions, workflows

2. Skills (.claude/skills/*.md)
   └── Reusable workflows
   └── Can be invoked by name
   └── Template-based automation

3. Custom Commands (.claude/commands/*.md)
   └── Slash commands (e.g., /commit, /review)
   └── Project-specific shortcuts

4. Hooks (.claude/hooks/*.py or *.js)
   └── PreToolUse: Intercept commands before execution
   └── PostToolUse: Process results after execution
   └── Example: Block dangerous commands, format outputs

5. MCP Servers (Model Context Protocol)
   └── Connect external tools (databases, APIs, Jira, Slack)
   └── Configured in settings.json

6. Plugins (from marketplace or custom)
   └── Bundled functionality (skills + hooks + commands)
   └── Example: commit-commands, code-review, security-guidance
```

**Minimal CLAUDE.md example**:
```markdown
# Project Context

This is a Next.js 14 app using TypeScript, Tailwind, and Prisma.

## Code Style
- Use "use client" for interactive components
- Prefer Server Components by default
- Use Zod for validation

## Commands
- Tests: `npm test -- path/to/file`
- Dev: `npm run dev`
- Build: `npm run build && npm run typecheck`

## Architecture
- API routes in app/api/
- Components in components/ (shadcn/ui)
- Database logic in lib/db/
```

**Custom slash command example** (`.claude/commands/pr.md`):
```markdown
# /pr

Create a pull request for the current branch.

## Steps
1. Run git status to check staged changes
2. If nothing staged, stage all changes
3. Create commit with descriptive message
4. Push to remote with -u flag
5. Create PR using gh pr create with:
   - Title from commit message
   - Body with summary and test plan
6. Return PR URL
```

**Hook example** (`.claude/hooks/pre_tool_use.py`):
```python
# Block dangerous commands
def pre_tool_use(tool_name, tool_input):
    if tool_name == "bash":
        dangerous = ["rm -rf", "sudo", "chmod 777"]
        command = tool_input.get("command", "")

        for pattern in dangerous:
            if pattern in command:
                return {
                    "block": True,
                    "reason": f"Blocked dangerous pattern: {pattern}"
                }

    return {"block": False}
```

**Common mistake**: Putting too much in CLAUDE.md (keep it under 200 lines).

**Pro tip**: **Start with CLAUDE.md only**. Add skills/hooks/MCP as needs arise, not prematurely.

---

---

**Next**: [Part 4: Practical Patterns →](04-practical-patterns.md)

**Series Navigation**:
- [← Part 2: Installation & Hello World](02-installation-and-hello-world.md)
- **Part 3: Core Concepts** (You are here)
- [Part 4: Practical Patterns →](04-practical-patterns.md)

---

*Part of the "Mastering Claude Code" series*
