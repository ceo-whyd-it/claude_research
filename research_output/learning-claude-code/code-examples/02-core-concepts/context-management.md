# Context Management Examples

Practical examples of managing Claude's context window.

## Example 1: Monitoring Context

```bash
claude

# Check current context usage
You: /context

# Expected output:
# Token usage: 12,450 / 200,000 (6%)
#
# Breakdown:
# - System prompt: 8,200 tokens
# - Conversation: 3,100 tokens
# - Tool outputs: 1,150 tokens
```

## Example 2: When to Clear Context

**❌ Bad: Polluted Context**
```bash
# Session 1: Debug authentication (30k tokens)
You: fix the login bug
[...long debugging session...]

# Session continues: Add unrelated feature (context now 65k tokens)
You: add a dark mode toggle
[...Claude struggles, slower responses...]

# Session continues: Refactor (context 95k tokens)
You: refactor the API layer
[...Claude makes mistakes, forgets earlier decisions...]
```

**✅ Good: Fresh Context**
```bash
# Session 1: Debug authentication
You: fix the login bug
[...debugging complete...]
You: /context
# Result: 30k tokens used

You: /clear

# Session 2: New feature with clean context
You: add a dark mode toggle
[...fast, accurate responses...]
```

## Example 3: Document & Clear Pattern

**For multi-hour features:**

```bash
# Hour 1: Start feature
You: build a user profile page with avatar upload

[...work happens...]

# Hour 1 end: Document progress
You: "Document your implementation to PROFILE_PROGRESS.md with:
- What's complete
- What's pending
- Architecture decisions
- Files changed"

[Claude creates detailed progress doc]

You: /context
# Result: 58k tokens (29%)

You: /clear

# Hour 2: Resume fresh
You: read PROFILE_PROGRESS.md and continue with the pending items

[...continues with fresh context...]
```

## Example 4: Using CLAUDE.md for Persistent Rules

**Instead of this (repeated each session):**
```bash
claude
You: use TypeScript strict mode, prefer async/await, put tests in __tests__/

# Next session:
claude
You: remember to use TypeScript strict mode, prefer async/await...
[Wasteful, pollutes context]
```

**Do this (one-time setup):**
```bash
# Create CLAUDE.md in project root
cat > CLAUDE.md << 'EOF'
# Project: My App

## Code Style
- TypeScript strict mode
- Prefer async/await over callbacks
- Tests in __tests__/ directories

## Commands
- Test: npm test
- Build: npm run build
- Dev: npm run dev
EOF

# Now every session has these rules automatically
claude
You: add a new API endpoint
# Claude automatically follows CLAUDE.md rules
```

## Example 5: Subagents for Research

**Keep main context clean by delegating research:**

```bash
claude

# Main task: Implement feature
You: add OAuth authentication

# Need to research but don't want to pollute context:
You: use a subagent to research which OAuth library to use for Next.js.
Compare next-auth vs auth0 vs clerk. Don't pollute our current context.

[Subagent spawns, researches in separate context, returns findings]
[Your main context stays focused on implementation]

You: based on the research, use next-auth and implement Google OAuth
```

## Token Budgets by Activity

| Activity | Typical Token Usage | Recommendation |
|----------|---------------------|----------------|
| Simple bug fix | 5k - 15k | No need to clear |
| Feature implementation | 30k - 60k | Clear when done |
| Large refactor | 60k - 100k | Document & clear midway |
| Long debugging | 40k - 80k | Clear after solving |
| Research/exploration | 20k - 40k | Use subagent or clear after |

## Best Practices Summary

1. **Check context regularly**: `/context` every 30-60 minutes
2. **Clear at 60-70%**: Don't wait until 100%
3. **Document before clearing**: Create progress markdown files
4. **Use CLAUDE.md**: For rules that apply to all sessions
5. **Use subagents**: For research that would pollute context
6. **Start fresh for new tasks**: New feature = new session
