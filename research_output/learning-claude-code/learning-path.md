# Claude Code Learning Path

A progressive, 5-level guide to mastering Claude Code from first principles to production workflows.

---

## Level 1: Overview & Motivation

### What Problem Does Claude Code Solve?

**Traditional AI coding assistants** operate in request-response mode:
1. You describe what you want
2. AI generates code
3. You copy-paste it
4. You manually test and debug
5. Repeat

**Claude Code** transforms this into **collaborative pair programming**:
- Claude reads your entire codebase autonomously
- Edits multiple files across your project
- Runs commands and verifies results
- Iterates until tests pass
- Creates commits and pull requests
- Works continuously without constant prompting

### What Existed Before? Why Is This Better?

| Traditional Tools | Claude Code |
|-------------------|-------------|
| **GitHub Copilot**: Line-by-line autocomplete in your editor | **Full codebase awareness**: Understands project architecture |
| **ChatGPT**: Copy-paste code snippets manually | **Direct file editing**: Changes files automatically |
| **Cursor**: IDE-integrated chat with context | **Autonomous execution**: Runs tests, fixes errors, iterates |
| **Manual workflows**: You run tests, read errors, fix | **Agentic loop**: Claude runs, reads, fixes autonomously |

**Key Difference**: Claude Code is **agentic** — it doesn't just suggest, it *does*.

### Who Uses It? For What?

**Individual Developers**:
- Building features faster (plan → code → test → commit)
- Debugging from error messages
- Writing tests for existing code
- Refactoring across multiple files
- Learning unfamiliar codebases quickly

**Teams & Enterprises**:
- Automating code reviews in CI/CD
- Onboarding new developers faster
- Maintaining consistency across large codebases
- Batch operations (dependency updates, migrations)
- Security scanning and vulnerability detection

**Non-Engineers** (Yes, really!):
- Growth teams: Generate hundreds of ad variations
- Legal teams: Build prototype tools without developers
- Product managers: Create quick prototypes from Figma designs
- Data analysts: Automate file organization and processing

### Real-World Impact

From Anthropic's case study: **Building a production-grade C compiler**
- **100,000+ lines of Rust code**
- **Compiles Linux** across multiple architectures (x86-64, ARM)
- Built primarily through Claude Code sessions
- Demonstrates: complex multi-file coordination, testing, optimization

From community experiences:
- **Jeremy D. Miller**: Reduced open issues from 50+ to 16 in 2 weeks across multiple projects
- **Anthropic Security Team**: "3x faster" problem resolution
- **General developers**: 40-60% development time reduction reported

### When Should You NOT Use It?

**Avoid Claude Code when**:
1. **Learning fundamentals**: If you're learning to code, write code yourself first
2. **Trivial changes**: Single-line typo fixes don't need AI
3. **High-security secrets**: Don't commit sensitive credentials (use `.gitignore` properly)
4. **No verification possible**: Without tests/specs, Claude can't self-check quality
5. **Offline work required**: Claude Code requires internet connection
6. **100% certainty needed**: AI-generated code needs human review for critical systems

**The Golden Rule**: Treat Claude as a **thought partner, not an oracle**. Always review output.

---

## Level 2: Installation & Hello World

### Prerequisites

**System Requirements**:
- **OS**: macOS 13+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+
- **RAM**: 4 GB minimum
- **Network**: Internet connection required
- **Shell**: Bash or Zsh recommended

**Account Requirements** (one of):
- Claude Pro/Max subscription (recommended - unified access)
- Anthropic Console account with billing
- Claude for Teams/Enterprise
- Cloud provider access (Bedrock, Vertex AI, Azure)

### Installation Steps

**macOS/Linux/WSL**:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Alternative: Package Managers**

macOS (Homebrew):
```bash
brew install --cask claude-code
```

Windows (WinGet):
```powershell
winget install Anthropic.ClaudeCode
```

### Verification

Check installation:
```bash
claude --version
# Expected: claude-code version 2.1.50 (or newer)

claude doctor
# Expected: ✓ All checks passed
```

### Hello World: Your First Session

**Step 1**: Create a test project
```bash
mkdir claude-test
cd claude-test
```

**Step 2**: Start Claude Code
```bash
claude
```

You'll see:
```
Welcome to Claude Code!
Logging you in...
✓ Logged in as your-email@example.com

Type your message or press Ctrl+C to exit.
```

**Step 3**: Ask your first question
```
You: what files are in this directory?
```

Claude will:
1. Run `ls` command
2. Report findings
3. Wait for next instruction

**Step 4**: Create your first file
```
You: create a hello.py file that prints "Hello from Claude Code!"
```

Claude will:
1. Ask permission to create file (if in default mode)
2. Write the file
3. Show you what it created

**Step 5**: Run and verify
```
You: run the python file and show me the output
```

Claude will:
1. Execute `python hello.py`
2. Display output: `Hello from Claude Code!`
3. Confirm success

**Step 6**: Exit
Press `Ctrl+C` or type `exit`

### Understanding What Just Happened

1. **Context Gathering**: Claude used `ls` to understand your directory
2. **File Creation**: Claude wrote `hello.py` using the Write tool
3. **Execution**: Claude ran bash commands to execute your script
4. **Verification**: Claude showed you the results

This is the **agentic loop** in action: Gather context → Take action → Verify results.

### Common First-Session Issues

| Problem | Solution |
|---------|----------|
| `claude: command not found` | Restart terminal or add to PATH manually |
| "Not logged in" error | Run `claude login` and authenticate |
| Permission denied on file creation | Check directory write permissions |
| Slow startup | First run downloads models; subsequent runs are faster |
| Can't exit | Press `Ctrl+C` twice, or type `exit` |

---

## Level 3: Core Concepts

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

## Level 4: Practical Patterns

Build real workflows and solve actual problems.

### Pattern 1: Fix a Bug (Beginner)

**Scenario**: You have a failing test or error message.

**Workflow**:
```bash
# Start with error information
claude

You: "I'm seeing this error when I run npm test:
     TypeError: Cannot read property 'id' of undefined
     at UserService.getUser (src/services/user.ts:42)"

# Claude's process:
# 1. Reads the error stack trace
# 2. Opens src/services/user.ts:42
# 3. Analyzes context around line 42
# 4. Identifies null/undefined issue
# 5. Searches for how getUser is called
# 6. Proposes fix with null check
# 7. Updates code
# 8. Runs npm test to verify
# 9. Reports: "✓ All tests pass"
```

**Key success factors**:
- ✅ Paste full error message (stack trace helps)
- ✅ Mention how to reproduce (what command)
- ✅ Let Claude run tests to verify fix

**What not to do**:
- ❌ "Fix the bug" (too vague - which bug?)
- ❌ Only paste error snippet (need full context)
- ❌ Skip test verification (how do you know it worked?)

---

### Pattern 2: Implement a Feature (Intermediate)

**Scenario**: Add new functionality across multiple files.

**Recommended workflow**: **Plan → Review → Execute**

**Step 1: Start in Plan Mode**
```bash
claude --permission-mode plan

You: "I want to add a 'forgot password' flow. Users should be able to:
1. Request a password reset link via email
2. Click the link to get a reset form
3. Set a new password

We're using Next.js 14 with Prisma and NextAuth. What files need to change?"
```

**Claude in Plan Mode**:
- ✅ Reads existing auth code
- ✅ Identifies relevant files
- ✅ Creates detailed plan
- ❌ Doesn't make any changes yet

**Step 2: Review the Plan**
```
Claude's plan:
1. Database: Add passwordResetToken and passwordResetExpires to User model
2. API Route: Create /api/auth/reset-password (request reset)
3. API Route: Create /api/auth/reset-password/[token] (verify and reset)
4. Email Service: Add sendPasswordResetEmail function
5. UI Component: Create ResetPasswordForm component
6. Page: Add app/reset-password/[token]/page.tsx
7. Tests: Add tests for new API routes

Would you like me to proceed with this plan?
```

**You**: "Yes, but use Resend instead of our current email service. Let's also add rate limiting to prevent abuse."

**Step 3: Execute with Modifications**
```bash
Shift+Tab  # Switch to Normal or Auto-Accept mode

You: "Implement the plan with the changes I mentioned. After each major step, run tests."
```

**Claude's execution**:
```
[Step 1] Updating Prisma schema...
[Step 1] Running: npm run db:push
[Step 1] ✓ Database updated

[Step 2] Creating /api/auth/reset-password route...
[Step 2] Adding rate limiting with upstash/ratelimit...
[Step 2] Running: npm test api/auth/reset-password.test.ts
[Step 2] ✓ 8/8 tests pass

[Step 3] Integrating Resend for emails...
[... continues through all steps ...]

[Complete] All 7 steps done. 24/24 tests pass.
```

**Step 4: Manual Verification**
```bash
You: "Start the dev server and open the reset password page"
Claude: [Runs npm run dev, provides URL]

# You test manually in browser

You: "Works! Create a commit and PR"
Claude: [Creates descriptive commit, pushes, opens PR with summary]
```

**Key success factors**:
- ✅ **Clear requirements up front** (user stories, acceptance criteria)
- ✅ **Plan first** for multi-file changes
- ✅ **Test after each major step** (not just at the end)
- ✅ **Manual verification** for UI/UX changes

---

### Pattern 3: Write Tests for Existing Code (Intermediate)

**Scenario**: You have untested code that needs coverage.

**Workflow**:
```bash
claude

You: "The functions in src/utils/validation.ts have no tests. Write comprehensive tests covering:
- Happy path cases
- Edge cases (empty strings, null, undefined)
- Invalid inputs
- Boundary conditions

Use Vitest (our testing framework). Put tests in src/utils/validation.test.ts.
Run the tests when done and make sure they all pass."
```

**Claude's process**:
```
[Read] src/utils/validation.ts
[Analyze] Found 5 functions: validateEmail, validatePhone, validateZipCode, validateUrl, validateUsername

[Write] src/utils/validation.test.ts
  ├── describe('validateEmail')
  │   ├── it('accepts valid email addresses')
  │   ├── it('rejects invalid formats')
  │   ├── it('handles edge cases')
  │   └── it('handles null/undefined')
  ├── describe('validatePhone')
  │   ├── ... (similar structure)
  └── ... (for each function)

[Run] npm test src/utils/validation.test.ts
[Result] ✓ 43/43 tests pass
[Coverage] 100% line coverage on validation.ts
```

**Pro workflow: Test-Driven Development (TDD)**

**Write tests FIRST, then implementation**:
```bash
You: "I need a function calculateShippingCost(weight, distance, expedited).
Write tests first covering:
- Standard shipping: $5 base + $0.50/lb + $0.10/mile
- Expedited adds 50% surcharge
- Free shipping over $50
- Weight and distance must be positive

The tests should fail initially. Then implement the function to make them pass."
```

**Claude follows Red-Green-Refactor**:
```
[Red] Write tests -> Run -> ✗ 8/8 tests fail (function doesn't exist)
[Green] Implement calculateShippingCost -> Run -> ✓ 8/8 pass
[Refactor] Extract constants, simplify logic -> Run -> ✓ 8/8 pass
```

**Key success factors**:
- ✅ Specify test framework (Vitest, Jest, pytest, etc.)
- ✅ Define what to test (happy path + edge cases)
- ✅ Ask Claude to run tests and verify
- ✅ For TDD: Explicitly say "write tests first"

---

### Pattern 4: Refactor Across Multiple Files (Advanced)

**Scenario**: Update a pattern throughout your codebase.

**Example**: Migrate from CommonJS to ES Modules

**Workflow**:
```bash
claude --permission-mode plan  # Start safe

You: "Search for all files using CommonJS (require/module.exports).
List them and show me how many files are affected. Don't change anything yet."
```

**Claude's reconnaissance**:
```
[Search] grep -r "require\(.*\)" --include="*.js"
[Search] grep -r "module\.exports" --include="*.js"

Found 23 files using CommonJS:
- src/utils/*.js (8 files)
- src/services/*.js (12 files)
- src/config/*.js (3 files)

Total: 23 files, ~400 import/export statements to update
```

**You (review scope)**: "That's more than I expected. Let's start with just src/utils/ first. Convert those 8 files to ESM. After each file, run tests."

**Switch to Auto-Accept for batch operations**:
```bash
Shift+Tab  # to Auto-Accept mode

You: "Convert the 8 utils files. After each file conversion, run: npm test -- src/utils/"
```

**Claude's execution** (auto-accept = no prompts per file):
```
[1/8] src/utils/string.js
  ├── Changed: const foo = require('./bar') -> import foo from './bar'
  ├── Changed: module.exports = {...} -> export default {...}
  ├── Renamed: string.js -> string.mjs
  ├── Run: npm test -- src/utils/string.test.js
  └── ✓ 12/12 tests pass

[2/8] src/utils/array.js
  ├── ...
  └── ✓ 8/8 tests pass

... [continues through all 8 files] ...

[Complete] All 8 files converted. 67/67 tests passing.
```

**Verify and commit**:
```bash
You: "Show me a summary git diff"
Claude: [Runs git diff --stat, shows changes]

You: "Looks good. Create a commit with a clear message"
Claude: [Commits with: "refactor(utils): migrate from CommonJS to ESM"]
```

**Key success factors**:
- ✅ **Scope discovery first** (understand impact before changing)
- ✅ **Incremental changes** (8 files, not 23 at once)
- ✅ **Test after each unit** (catches breaks immediately)
- ✅ **Use Auto-Accept for batch work** (reduces friction)

**What could go wrong**:
- ❌ Changing all 23 files at once (too much to verify)
- ❌ Skipping tests (silent breakage)
- ❌ Losing track of changes (hard to review)

---

### Pattern 5: Debug from Logs/Errors (Advanced)

**Scenario**: Production error or complex debugging.

**Workflow**:
```bash
claude

You: "We're seeing intermittent 500 errors in production. Here's the log:

2026-02-20 14:32:18 ERROR [api] POST /api/orders 500 Internal Server Error
   at OrderService.create (src/services/order.ts:156)
   at async POST /api/orders +142ms
   Error: Cannot read property 'total' of undefined

This happens about 5% of the time. Can you investigate?"
```

**Claude's debugging strategy**:
```
[Read] src/services/order.ts:156
[Analyze] Line 156: const tax = order.cart.total * 0.08
[Hypothesis] order.cart might be null/undefined sometimes

[Search] How is order.cart populated?
[Read] src/services/cart.ts
[Find] cart might be null if session expired

[Search] Error logs for pattern
[Find] Errors correlate with old session IDs

[Diagnosis] Race condition: User's cart session expires between
            adding items and checking out

[Propose Fix]
1. Add null check for order.cart
2. Return 400 Bad Request with clear error if cart expired
3. Add logging to track session expiry events
4. Add test case for expired cart scenario
```

**You**: "Good analysis. Implement the fix with all four improvements."

**Claude implements**:
```
[Edit] src/services/order.ts
  ├── Added: if (!order.cart) throw new BadRequestError('Cart expired')
  ├── Added: logger.warn('Cart expiry during checkout', { userId, sessionId })

[Edit] src/services/order.test.ts
  ├── Added: test('returns 400 when cart expired')

[Run] npm test src/services/order.test.ts
[Result] ✓ 24/24 tests pass (including new test)

[Create] Error message improvement:
  └── "Your shopping cart has expired. Please add items again."
```

**Key success factors**:
- ✅ Provide **full error messages** (stack traces are gold)
- ✅ Provide **context** (when does it happen? how often?)
- ✅ Let Claude **search** and **read** code to understand root cause
- ✅ Ask for **tests** that reproduce the bug

**Pro tip**: For hard-to-reproduce bugs, ask Claude to add logging first, then fix.

---

### Pattern 6: Context Management for Long Sessions (Advanced)

**Scenario**: Multi-hour session building a complex feature.

**Anti-pattern (what NOT to do)**:
```bash
# Hour 1: Implement authentication
# Hour 2: Add API endpoints
# Hour 3: Build UI components
# Hour 4: Debug integration
# [Context at 95%]
# Hour 5: Claude starts making mistakes, forgetting earlier decisions
# Hour 6: You're correcting Claude's corrections
```

**Recommended pattern: "Document & Clear"**

**Hour 1**:
```bash
You: "Build authentication system for our app. Use NextAuth with Prisma."
[...work happens...]
Claude: "Authentication complete. Tests passing."

You: "Document your implementation to AUTH_PROGRESS.md including:
- What you built
- Architecture decisions
- What still needs to be done
- Any issues or TODOs

Then check context usage with /context"
```

**Claude creates**:
```markdown
# AUTH_PROGRESS.md

## ✅ Completed (2024-02-20, 2:30 PM)

### Implementation
- Installed NextAuth.js v5
- Configured providers: GitHub, Google, Email
- Prisma schema: User, Account, Session, VerificationToken tables
- API route: /api/auth/[...nextauth]

### Architecture Decisions
- Using JWT strategy (not database sessions) for better performance
- Email verification required for email/password signups
- Session expires after 30 days

### Files Created/Modified
- app/api/auth/[...nextauth]/route.ts
- lib/auth/config.ts
- prisma/schema.prisma (updated)
- .env (added AUTH_SECRET, GITHUB_ID, GOOGLE_ID)

## 🔄 TODO Next
- Add protected route middleware
- Create login/signup UI components
- Add role-based permissions
- Test OAuth flows manually

## ⚠️ Issues
- None currently
```

**Context check**:
```bash
Claude: /context
[Result] Token usage: 67,234 / 200,000 (34%)
```

**Hour 2** (fresh start):
```bash
You: /clear
[Context reset]

You: "Read AUTH_PROGRESS.md and continue with the TODO items. Start with protected route middleware."
```

**Benefits**:
- ✅ Fresh context (fast, accurate responses)
- ✅ Documented decisions (searchable, reviewable)
- ✅ Clear handoff between sessions
- ✅ Can resume days later

**Alternative: Use subagents for investigation**:
```bash
You: "Use a subagent to investigate how to implement rate limiting for our API.
Don't pollute our current context. Report back with findings."

[Subagent spawns with separate context]
[Subagent researches, returns summary]
[Main context remains clean]
```

**Key success factors**:
- ✅ **Monitor context**: Run `/context` every hour
- ✅ **Clear at 60-70%**: Don't wait until 100%
- ✅ **Document before clearing**: Create progress files
- ✅ **Use subagents for research**: Keep main context focused

---

## Level 5: Next Steps

You've mastered the fundamentals. Here's where to go deeper.

### Advanced Topics to Explore

#### 1. **Multi-Agent Orchestration**

**What it is**: Coordinate multiple Claude sessions to work in parallel.

**When to use**:
- Large features with independent modules
- Research tasks (parallel investigation)
- Debugging (test multiple hypotheses simultaneously)

**Getting started**:
- Read: [Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)
- Read: [Multi-Agent Orchestration Guide](https://sjramblings.io/multi-agent-orchestration-claude-code-when-ai-teams-beat-solo-acts/)
- Try: Official `agent-sdk-dev` plugin for custom orchestration

**Example use case**:
```
Project: Build e-commerce platform

Agent Team:
├── Frontend Agent: React components + Tailwind
├── Backend Agent: API routes + database
├── Testing Agent: Write tests for both
└── Lead (you): Coordinate, review, integrate

Each agent has separate context, works independently.
Lead merges work via git.
```

---

#### 2. **Custom Skills Development**

**What it is**: Create reusable workflows as markdown files.

**When to use**:
- Repeating patterns (e.g., "add CRUD endpoints for new model")
- Team standardization (everyone uses same workflows)
- Complex multi-step processes

**Getting started**:
- Read: Official plugins in the GitHub repo
- Study: `.claude/skills/` examples
- Create: Start with a simple `/commit` skill

**Skill template**:
```markdown
# /add-crud

Add CRUD endpoints for a new database model.

## Arguments
- model_name: Name of the model (e.g., "Product")

## Steps
1. Create Prisma schema for {model_name}
2. Run: npx prisma migrate dev
3. Create src/api/{model_name}/route.ts with:
   - GET /api/{model_name} (list all)
   - GET /api/{model_name}/[id] (get one)
   - POST /api/{model_name} (create)
   - PUT /api/{model_name}/[id] (update)
   - DELETE /api/{model_name}/[id] (delete)
4. Create tests in src/api/{model_name}/route.test.ts
5. Run tests: npm test -- src/api/{model_name}/
6. Return summary of created files
```

**Resources**:
- Best: [Official Plugin Development Guide](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)

---

#### 3. **Hooks for Enterprise Security**

**What it is**: Intercept and validate Claude's actions before execution.

**When to use**:
- Production systems (prevent dangerous operations)
- Compliance requirements (audit all changes)
- Team safety (block unapproved patterns)

**Getting started**:
- Read: [Hooks examples in repo](https://github.com/anthropics/claude-code/tree/main/examples/hooks)
- Study: `security-guidance` plugin
- Implement: Start with a PreToolUse validator

**Example: Block production database access**:
```python
# .claude/hooks/pre_tool_use.py

def pre_tool_use(tool_name, tool_input):
    """Prevent accidental production database operations"""

    if tool_name == "bash":
        command = tool_input.get("command", "")

        # Block production database connections
        if "PROD_DATABASE_URL" in command:
            return {
                "block": True,
                "reason": "❌ Production database access blocked. Use staging instead."
            }

        # Block destructive migrations without confirmation
        if "prisma migrate reset" in command:
            return {
                "block": True,
                "reason": "⚠️ migrate reset requires manual confirmation"
            }

    return {"block": False}
```

**Resources**:
- Best: [Hardening Claude Code: Security Framework](https://medium.com/@emergentcap/hardening-claude-code-a-security-review-framework-and-the-prompt-that-does-it-for-you-c546831f2cec)

---

#### 4. **MCP (Model Context Protocol) Integrations**

**What it is**: Connect external tools and data sources to Claude.

**Available MCP servers**:
- Database connectors (PostgreSQL, MySQL, MongoDB)
- APIs (Jira, Linear, Notion, GitHub)
- Cloud services (AWS, GCP, Azure)
- Development tools (Docker, Kubernetes)

**When to use**:
- Need to query databases directly
- Integrate with project management (Jira tickets)
- Deploy infrastructure (Terraform, cloud APIs)
- Monitor production (logs, metrics)

**Getting started**:
```bash
# Interactive MCP setup
claude mcp add

# Choose from available servers:
# - @modelcontextprotocol/server-postgres
# - @modelcontextprotocol/server-github
# - @modelcontextprotocol/server-slack
# ... and many more
```

**Example use case**:
```bash
# With PostgreSQL MCP installed:
You: "Query the production database to find all users who signed up in the last 7 days"

Claude: [Uses MCP to execute SQL query safely]
Claude: "Found 1,247 new users. Top 5 countries: US (412), UK (203), CA (156), AU (98), DE (87)"
```

**Resources**:
- Official: [MCP Documentation](https://code.claude.com/docs/en/mcp)
- Catalog: [Available MCP Servers](https://github.com/modelcontextprotocol/servers)

---

#### 5. **CI/CD Integration**

**What it is**: Run Claude Code in GitHub Actions, GitLab CI/CD, or other automation.

**Use cases**:
- Automated PR reviews
- Test generation for untested code
- Security scanning
- Dependency update PRs
- Release note generation

**Getting started**:
```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: curl -fsSL https://claude.ai/install.sh | bash

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review this PR for:
          - Security vulnerabilities
          - Code quality issues
          - Missing tests
          - Performance problems

          Output as markdown. Be concise." \
          --output-format json > review.json

      - name: Post Comment
        uses: actions/github-script@v7
        with:
          script: |
            const review = require('./review.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review.output
            });
```

**Resources**:
- Official: [GitHub Actions Guide](https://code.claude.com/docs/en/github-actions)
- Official: [GitLab CI/CD Guide](https://code.claude.com/docs/en/gitlab-ci-cd)

---

### Hands-On Project: Build a Complete Feature

**Mini-Project**: Build a "Newsletter Subscription" feature using all learned patterns.

**Requirements**:
1. Database: Add `Newsletter` model with email, subscribedAt, unsubscribedAt
2. API: `/api/newsletter/subscribe` and `/api/newsletter/unsubscribe`
3. UI: Newsletter signup form component
4. Validation: Email format, prevent duplicates
5. Email: Send welcome email (using Resend)
6. Tests: Full test coverage
7. Security: Rate limiting, input sanitization

**Step-by-step workflow**:

**Phase 1: Planning (Plan Mode)**
```bash
claude --permission-mode plan

You: [Paste requirements above]
"Create a detailed implementation plan. List all files to create/modify."
```

**Phase 2: Implementation (Auto-Accept Mode)**
```bash
Shift+Tab  # to Auto-Accept

You: "Implement the plan. After each major component (DB, API, UI, Tests),
run tests and verify."
```

**Phase 3: Manual Testing**
```bash
You: "Start dev server. I'll test the form manually."
[Test in browser]

You: "Works! Add logging for subscription events. Then commit and create PR."
```

**Expected time**: 30-45 minutes (mostly watching Claude work)

**What you'll practice**:
- ✅ Planning before coding
- ✅ Incremental testing
- ✅ Context management
- ✅ Permission mode switching
- ✅ Integration with external service (email)
- ✅ Security considerations (rate limiting)
- ✅ Git workflow automation

---

### Community Resources for Continued Learning

**Join the Community**:
- [Discord (61k+ members)](https://discord.com/invite/6PPFFzqPDZ) - Daily discussions, help, tips
- r/ClaudeCode - Reddit community
- Twitter/X: Follow @AnthropicAI for updates

**Weekly Learning**:
- [Anthropic Blog](https://claude.com/blog) - Official announcements and case studies
- [Claude Code Release Notes](https://github.com/anthropics/claude-code/releases) - New features

**Deep Dives**:
- [32 Claude Code Tips](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to) - Basics to advanced
- [How I Use Every Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature) - Comprehensive guide

**Comparison Research**:
- [30-Day Tool Comparison](https://javascript.plainenglish.io/github-copilot-vs-cursor-vs-claude-i-tested-all-ai-coding-tools-for-30-days-the-results-will-c66a9f56db05) - vs Copilot, Cursor

---

### How to Get Help

**When stuck**:

1. **Documentation First**: [code.claude.com/docs](https://code.claude.com/docs/en/overview)
2. **Troubleshooting Guide**: [Official troubleshooting](https://code.claude.com/docs/en/troubleshooting)
3. **Community Search**: Search Discord/Reddit for similar issues
4. **Ask Claude**: `claude "explain how [feature] works"`
5. **GitHub Issues**: [Report bugs](https://github.com/anthropics/claude-code/issues)

**Best practices for asking for help**:
- Include Claude Code version (`claude --version`)
- Describe what you're trying to do
- Show exact error messages
- Mention what you've already tried

---

### Final Wisdom from the Community

**Top 3 insights from experienced users**:

1. **"Give Claude something to verify against"** (DoltHub)
   - Tests, screenshots, expected outputs
   - Single highest-leverage improvement

2. **"Context is currency"** (Builder.io)
   - Use `/clear` liberally
   - Document before clearing
   - Fresh context > long polluted context

3. **"Plan first, code second"** (Multiple sources)
   - Planning mode prevents wasted work
   - Human review before execution
   - Saves time overall despite upfront cost

**Remember**: Claude Code is a **thought partner**, not a replacement for thinking. Your job shifts from writing code to:
- Defining requirements clearly
- Reviewing output critically
- Making architectural decisions
- Verifying correctness

---

**Congratulations!** You've completed the Claude Code learning path. You now have the knowledge to:
- Use Claude Code effectively for daily development
- Manage long coding sessions without context issues
- Apply proven patterns from production users
- Extend Claude Code for your specific needs

**Next**: Build something! The best way to solidify learning is practice.

---

**Feedback**: Found this helpful? Have suggestions? Share them in the [Discord community](https://discord.com/invite/6PPFFzqPDZ) or open an issue on the [learning materials repo](https://github.com/anthropics/claude-code).

**Last Updated**: February 2026
**Claude Code Version**: 2.1.50+
