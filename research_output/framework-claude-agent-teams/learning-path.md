# Claude Agent Teams — Learning Path

A progressive guide to building multi-agent systems with Claude Code and the Claude Agent SDK.

---

## Level 1: Overview & Motivation

### What Problem Does This Framework Solve?

**Claude Agent Teams** solve the critical challenge of **coordinating complex, parallel work** that benefits from real-time inter-agent communication and collaboration.

**Traditional limitations:**
- **Sequential bottlenecks** — Single agents must finish one task before starting another
- **Collaboration overhead** — Subagents can only report back to the main agent; they can't discuss findings with each other
- **Context window limits** — Large exploratory tasks consume excessive context in single sessions
- **Coordination complexity** — Features spanning multiple layers need shared state and task management

**What Agent Teams enable:**
- Multiple Claude Code instances working simultaneously
- Direct inter-agent communication (not just through the lead)
- Shared task lists with automatic dependency resolution
- Parallel exploration with self-coordination
- Debate structures where agents challenge each other's theories

### What Existed Before? Why Is This Better?

**Before Agent Teams:**

1. **Single Agent Approach** — One Claude instance handling all work sequentially
   - Slow for large tasks
   - No parallelization
   - Limited by single context window

2. **Subagent Pattern** — Main agent spawns temporary helpers
   - Subagents work independently but only report back to parent
   - No inter-subagent communication
   - Main agent becomes coordination bottleneck
   - Good for simple delegation, not complex collaboration

**Agent Teams improvement:**
- Teammates communicate directly without going through lead
- Shared task list enables self-coordination
- True parallelism with independent context windows
- Debate and collaboration structures
- Automatic dependency management

### Who Uses It? For What Types of Applications?

**Ideal use cases:**

1. **Parallel Code Review** — Multiple reviewers (security, performance, testing) examining different aspects simultaneously
2. **Competing Hypothesis Debugging** — 5 agents investigating different theories, debating to find root cause
3. **Cross-Layer Feature Development** — Frontend, backend, database, test teams working independently
4. **Architectural Exploration** — Different design approaches evaluated and compared in parallel
5. **Research with Synthesis** — Multiple researchers investigating different aspects, discussing findings

**Production users:**
- **Spotify** — Large-scale code migrations triggered via Slack bots
- **Security/Hai** — Vulnerability analysis (44% faster, 25% more accurate)
- **GitHub Copilot** — Complex codebase-spanning reasoning
- **Cursor IDE** — Multi-step coding problems

### When Should You NOT Use It?

**Avoid agent teams when:**

1. **Simple, sequential tasks** — Single agent is more cost-effective
2. **Quick focused operations** — Subagents are sufficient (lower token cost)
3. **Tasks don't benefit from discussion** — No need for inter-agent communication
4. **Limited budget** — Agent teams use 3-4x tokens vs single session
5. **Tasks are independent** — No coordination needed, just run them separately

**Use subagents instead when:**
- You need quick, focused results
- Agents don't need to communicate with each other
- Main agent can effectively coordinate all work
- Cost is a primary concern

### Architecture Overview at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                      Team Lead Session                       │
│  (Main orchestrator: creates team, spawns teammates, manages) │
└────────────┬────────────────────────────────────┬────────────┘
             │                                     │
    ┌────────▼──────────┐              ┌─────────▼─────────┐
    │  Teammate Session  │              │ Teammate Session  │
    │ (Independent Claude│◄────────────►│(Independent Claude│
    │  Code instance)    │  Direct      │ Code instance)    │
    └────────┬───────────┘ Messaging    └─────────┬─────────┘
             │                                     │
             └──────────┬──────────────────────────┘
                        │
               ┌────────▼────────┐
               │  Shared Task    │
               │      List       │
               │ (~/.claude/     │
               │   tasks/)       │
               └─────────────────┘
```

**Key components:**
- **Team Lead** — Orchestrator that spawns and coordinates teammates
- **Teammates** — Independent Claude Code instances with own context windows
- **Shared Task List** — Self-coordination mechanism for claiming and completing work
- **Direct Messaging** — Teammates communicate without going through lead
- **Team Config** — Metadata stored at `~/.claude/teams/{team-name}/`

---

## Level 2: Setup & First Project

### Prerequisites

**System Requirements:**
- **OS:** macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+
- **Hardware:** 4 GB+ RAM, Internet connection required
- **Shell:** Bash or Zsh recommended

**Knowledge:**
- Basic command line usage
- Understanding of async programming (for SDK usage)
- Familiarity with Claude API (helpful but not required)

### Installation Steps

**Step 1: Install Claude Code**

Choose your platform:

```bash
# macOS/Linux (Native - Recommended)
curl -fsSL https://claude.ai/install.sh | bash

# macOS (Homebrew)
brew install --cask claude-code

# Windows (WinGet)
winget install Anthropic.ClaudeCode
```

**Step 2: Verify Installation**

```bash
claude --version
```

**Step 3: Enable Agent Teams (Required)**

Agent teams are **experimental** and disabled by default. Enable them:

**Option A: Environment Variable**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**Option B: Settings File**

Create or edit `~/.claude/settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**Step 4: Set Up API Key**

```bash
# During first run, you'll be prompted for your API key
claude

# Or set it in settings.json:
{
  "env": {
    "ANTHROPIC_API_KEY": "your-key-here"
  }
}
```

### Minimal Working Project

**Your First Agent Team:**

1. Create a test project:
```bash
mkdir agent-team-test
cd agent-team-test
echo "# Test Project" > README.md
echo "def hello(): return 'world'" > app.py
```

2. Start Claude Code:
```bash
claude
```

3. Create your first team with this prompt:

```
Create a team with 3 reviewers to review the code in this project:
- One reviewer focused on code quality and style
- One reviewer focused on potential bugs
- One reviewer focused on documentation

Have them each review the files and report their findings.
```

4. **Expected output:**

You'll see Claude:
- Spawn 3 teammate sessions
- Each teammate reviews the code from their perspective
- Teammates report findings back to lead
- Lead synthesizes the results

5. **Verify it works:**

Look for output like:
```
🎯 Creating agent team with 3 teammates...
✓ Spawned quality-reviewer
✓ Spawned bug-reviewer
✓ Spawned docs-reviewer

[quality-reviewer]: Reviewing for code quality...
[bug-reviewer]: Checking for potential issues...
[docs-reviewer]: Analyzing documentation...
```

### Directory Structure Walkthrough

After creating a team, Claude Code creates:

```
~/.claude/
├── teams/
│   └── {team-name}/
│       └── config.json          # Team metadata
├── tasks/
│   └── {team-name}/
│       ├── pending/             # Unclaimed tasks
│       ├── in_progress/         # Tasks being worked on
│       └── completed/           # Finished tasks
└── settings.json                # Global settings
```

**Your project:**
```
agent-team-test/
├── README.md
├── app.py
└── .claude/                     # Project-specific settings (optional)
    └── settings.json
```

### Run It, See Output

**Display Modes:**

1. **In-process mode** (default) — All teammates in main terminal
   - Cycle through teammates with `Shift+Down`
   - See one teammate at a time

2. **Split-pane mode** (tmux/iTerm2) — Each teammate gets own pane
   - See all teammates simultaneously
   - Requires tmux or iTerm2

**Toggle task list view:**
```
Ctrl+T    # Show/hide task list
```

### Verify It Works

**Success indicators:**

1. ✅ Teammates spawn successfully
2. ✅ Each teammate completes their assigned task
3. ✅ Lead synthesizes findings
4. ✅ Team cleanup happens at the end

**Common first-time issues:**

| Issue | Solution |
|-------|----------|
| "Agent teams not enabled" | Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| "Permission denied" | Run `chmod +x` on Claude Code binary |
| "API key not found" | Set `ANTHROPIC_API_KEY` in settings |
| Teammates don't spawn | Check rate limits, verify API key |

---

## Level 3: Architecture & Core Concepts

### Core Concept 1: Agent Definitions

**What it is:** Declarative configuration defining an agent's purpose, capabilities, and constraints.

**Key properties:**
```python
@dataclass
class AgentDefinition:
    description: str      # Human-readable purpose
    prompt: str          # System prompt for the agent
    tools: list[str]     # Allowed tools (e.g., ["Read", "Bash"])
    model: str           # "sonnet", "opus", "haiku", or "inherit"
```

**How agents relate:**
- Main orchestrator has access to all agent definitions
- Spawns teammates by referencing their definitions
- Each teammate operates with isolated tools and prompt

**Example:**

```python
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions

agents = {
    "code-reviewer": AgentDefinition(
        description="Reviews code for best practices",
        prompt="You are an expert code reviewer. Focus on readability, maintainability, and potential bugs.",
        tools=["Read", "Grep"],
        model="sonnet",
    ),
    "test-writer": AgentDefinition(
        description="Writes unit tests",
        prompt="You are a testing expert. Write comprehensive tests with good coverage.",
        tools=["Read", "Write", "Bash"],
        model="sonnet",
    ),
}
```

**Common mistakes:**
- ❌ Giving all agents all tools (reduces safety)
- ❌ Using vague descriptions (main agent can't delegate effectively)
- ❌ Omitting model specification (defaults to inherit, may be too expensive)

### Core Concept 2: Shared Task List with Self-Coordination

**What it is:** A file-based task queue that teammates can claim and complete autonomously.

**How it works:**
```
~/.claude/tasks/{team-name}/
├── pending/
│   ├── task-1.json        # Unclaimed tasks
│   └── task-2.json
├── in_progress/
│   └── task-1.json        # Claimed by teammate
└── completed/
    └── task-3.json        # Finished tasks
```

**Lifecycle:**
1. Lead creates tasks and places in `pending/`
2. Teammate claims task (moves to `in_progress/`)
3. Teammate completes work (moves to `completed/`)
4. Dependent tasks auto-unblock

**Task structure:**
```json
{
  "id": "review-auth-module",
  "description": "Review authentication module for security",
  "dependencies": [],
  "assigned_to": null,
  "status": "pending"
}
```

**Configuration pattern:**
```
# In Claude Code, ask lead to:
"Create 5 tasks for the team:
1. Review database schema
2. Review API endpoints (depends on task 1)
3. Review authentication (depends on task 2)
4. Write integration tests (depends on tasks 2 and 3)
5. Update documentation (depends on all tasks)"
```

**Common mistakes:**
- ❌ Creating too many tiny tasks (overhead exceeds benefit)
- ❌ Creating oversized tasks (long waits, reduced feedback)
- ❌ Forgetting dependencies (tasks execute in wrong order)

### Core Concept 3: Independent Context Windows with Direct Communication

**What it is:** Each teammate is a full Claude Code instance with its own conversation history and memory.

**Key characteristics:**
- Teammates don't inherit lead's conversation history
- Each has separate token budget and context window
- Can message each other directly without involving lead

**Communication patterns:**

```
# Lead → Teammate
"Ask the researcher teammate to investigate the database schema"

# Teammate → Lead
Teammate reports findings back automatically

# Teammate → Teammate (Direct)
"Tell the researcher teammate their approach is promising - keep going deeper"
```

**Message delivery:**
- Automatic (lead doesn't need to poll)
- Delivered when teammate next checks messages
- Preserved across teammate's work session

**Example workflow:**
```
You (Lead): Create a team with a researcher and an implementer

Claude (Lead): ✓ Spawned researcher
               ✓ Spawned implementer

You: Ask the researcher to find all database connection code

[researcher]: Found 3 connection points in app/db/...

You: Tell the implementer to refactor based on researcher's findings

[implementer]: Refactoring database connections...
```

**Common mistakes:**
- ❌ Assuming teammates know lead's conversation context
- ❌ Not providing enough detail in spawn prompts
- ❌ Forgetting teammates can talk directly to each other

### Core Concept 4: Debate & Collaboration Structure

**What it is:** Pattern where agents actively challenge each other's assumptions to find better solutions.

**Why it matters:**
- Prevents cognitive anchoring
- Tests hypotheses rigorously
- Surfaces edge cases
- Leads to more robust solutions

**Example structure:**

```
"Create a debugging team with 5 teammates investigating why the app crashes:
- Agent 1: Investigate memory leaks
- Agent 2: Check for race conditions
- Agent 3: Examine network timeouts
- Agent 4: Test database connection handling
- Agent 5: Look for unhandled exceptions

Have them actively try to disprove each other's theories.
Update a findings doc with whatever consensus emerges."
```

**Configuration pattern:**
1. Define competing hypotheses
2. Assign one agent per hypothesis
3. Instruct agents to challenge others
4. Synthesize consensus or identify most likely cause

**Common mistakes:**
- ❌ Not structuring debate (agents agree too easily)
- ❌ Too many competing theories (becomes chaotic)
- ❌ Forgetting to synthesize results

### Core Concept 5: Plan Approval & Risk Mitigation

**What it is:** Safety mechanism where teammates create plans for approval before implementing risky changes.

**When to use:**
- Refactoring critical code
- Database migrations
- Changing public APIs
- Anything with potential for significant breakage

**How it works:**
```
"Create a team to refactor the authentication system.
Require plan approval before implementation.
Each teammate should work in read-only mode, create a plan,
and send approval request to me before making changes."
```

**Workflow:**
1. Teammate analyzes code (read-only)
2. Creates detailed implementation plan
3. Sends plan to lead for approval
4. Waits for approval
5. Implements only after approval

**Plan format:**
```markdown
## Refactoring Plan: Authentication Module

### Current State
- Session storage uses in-memory dict
- No persistence across restarts
- No multi-process support

### Proposed Changes
1. Add Redis session backend
2. Update session middleware
3. Add fallback to in-memory for development

### Risks
- Redis dependency
- Migration path for existing sessions

### Testing Strategy
- Unit tests for session backend
- Integration tests with Redis
- Backward compatibility tests

Awaiting approval to proceed.
```

**Common mistakes:**
- ❌ Not using plan approval for risky changes
- ❌ Approving plans without reviewing them
- ❌ Plans too vague to be useful

---

## Level 4: Building Real Applications

### Application 1: Parallel Code Review System

**Goal:** Build a multi-perspective code review system that analyzes PRs from security, performance, and testing angles simultaneously.

**Step 1: Setup**

```bash
mkdir code-review-team
cd code-review-team

# Create sample code to review
cat > server.py << 'EOF'
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name LIKE '%{request.args.get('search')}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users VALUES ('{data['name']}', '{data['email']}')")
    conn.commit()
    return jsonify({"status": "created"})

if __name__ == '__main__':
    app.run(debug=True)
EOF
```

**Step 2: Create Review Team**

```
Create an agent team to review server.py from three angles:

1. Security Reviewer
   - Check for SQL injection vulnerabilities
   - Verify input validation
   - Check for security best practices
   - Tools: Read, Grep

2. Performance Reviewer
   - Check for inefficient queries
   - Identify resource leaks (unclosed connections)
   - Check for proper indexing
   - Tools: Read, Grep

3. Test Coverage Reviewer
   - Identify untested code paths
   - Check for missing edge case tests
   - Verify error handling is tested
   - Tools: Read, Grep, Bash

Have each reviewer create a report with:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)

After all reviews complete, synthesize into a final report.
```

**Step 3: Expected Output**

```
[security-reviewer]: CRITICAL: SQL injection vulnerability in get_users()
                     CRITICAL: SQL injection in create_user()
                     WARNING: No input sanitization

[performance-reviewer]: CRITICAL: Database connections not closed
                        WARNING: No connection pooling
                        SUGGESTION: Add query result caching

[test-coverage-reviewer]: CRITICAL: No tests exist
                          WARNING: Error paths not handled
                          SUGGESTION: Add integration tests
```

**Step 4: Add Testing Plugin**

Use MCP to add test file analysis:

```python
# In your SDK setup
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("count_tests", "Count test files and assertions", {})
async def count_tests(args):
    # Implementation
    return {"test_files": 0, "assertions": 0}

test_tools = create_sdk_mcp_server(
    name="test-analysis",
    version="1.0.0",
    tools=[count_tests]
)
```

### Application 2: Cross-Layer Feature Development

**Goal:** Build a new API endpoint with frontend, backend, database, and tests developed in parallel.

**Feature:** User profile update system

**Step 1: Decompose Work**

```
Create an agent team to build a user profile update feature.
Break into 4 independent workstreams:

1. Database Teammate
   - Create migration for profile fields
   - Add indexes
   - Write database tests
   Tools: Read, Write, Bash
   Files: migrations/, tests/test_db.py

2. API Teammate
   - Implement PUT /api/users/:id/profile endpoint
   - Add validation
   - Write API tests
   Tools: Read, Write, Bash
   Files: app/routes/users.py, tests/test_api.py
   Depends on: Database teammate completion

3. Frontend Teammate
   - Create ProfileEdit component
   - Add form validation
   - Write component tests
   Tools: Read, Write, Bash
   Files: src/components/ProfileEdit.tsx, src/components/ProfileEdit.test.tsx

4. Integration Teammate
   - Write end-to-end tests
   - Test full user journey
   - Verify all layers work together
   Tools: Read, Write, Bash
   Files: tests/e2e/test_profile_update.py
   Depends on: API and Frontend completion

Use Sonnet for each teammate.
Require plan approval before implementation.
```

**Step 2: Create Starter Files**

```bash
mkdir -p {migrations,app/routes,src/components,tests/{e2e,}}
touch migrations/.gitkeep
touch app/routes/__init__.py
touch src/components/.gitkeep
```

**Step 3: Monitor Progress**

```
# In Claude Code
Ctrl+T    # Toggle task list view

# You'll see:
┌─────────────────────────────────────────┐
│ PENDING                                 │
├─────────────────────────────────────────┤
│ □ Create profile database migration     │
│ □ Implement profile API endpoint        │  (blocked: depends on DB)
│ □ Build ProfileEdit component           │
│ □ Write end-to-end tests                │  (blocked: depends on API + Frontend)
└─────────────────────────────────────────┘

# As work progresses:
┌─────────────────────────────────────────┐
│ IN PROGRESS                             │
├─────────────────────────────────────────┤
│ ⚡ Create profile database migration     │  (database-teammate)
│ ⚡ Build ProfileEdit component           │  (frontend-teammate)
└─────────────────────────────────────────┘
```

**Step 4: Handle Plan Approvals**

When a teammate sends a plan:

```
[database-teammate]:
## Migration Plan

ALTER TABLE users ADD COLUMN (
  bio TEXT,
  avatar_url VARCHAR(500),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_updated_at ON users(updated_at);

Awaiting approval.
```

Your response:
```
Approve the database teammate's plan
```

### Application 3: Competing Hypothesis Debugger

**Goal:** Investigate a production bug using multiple parallel theories.

**Bug:** "Application exits after first user message instead of staying connected"

**Step 1: Define Hypotheses**

```
Create a debugging team with 5 investigators testing different theories:

1. Connection Handler Theory
   - Hypothesis: WebSocket connection closes prematurely
   - Investigate: Connection lifecycle, close handlers
   - Tools: Read, Grep, Bash

2. Event Loop Theory
   - Hypothesis: Event loop exits after first message
   - Investigate: Async/await patterns, loop management
   - Tools: Read, Grep, Bash

3. Exception Handling Theory
   - Hypothesis: Unhandled exception causes exit
   - Investigate: Try/catch blocks, error logging
   - Tools: Read, Grep, Bash

4. Resource Cleanup Theory
   - Hypothesis: Premature cleanup in message handler
   - Investigate: Context managers, cleanup code
   - Tools: Read, Grep, Bash

5. Configuration Theory
   - Hypothesis: Environment setting causes single-message mode
   - Investigate: Config files, environment variables
   - Tools: Read, Grep, Bash

Each agent should:
- Find evidence supporting their theory
- Find evidence contradicting their theory
- Challenge other agents' findings
- Update a shared findings.md document

Final goal: Reach consensus on root cause or identify top 2 likely causes.
```

**Step 2: Create Investigation Workspace**

```bash
mkdir debug-session
cd debug-session
echo "# Investigation Findings" > findings.md
echo "Each agent should add evidence and debate results here." >> findings.md
```

**Step 3: Observe Debate**

```
[connection-handler]: Found WebSocket close() called after first message.
                      Evidence: Line 45 in websocket_handler.py

[event-loop]: But the event loop is configured with run_forever().
              This contradicts connection-handler's theory.

[exception-handler]: Found unhandled ValueError in message parser.
                     Exception gets swallowed but triggers cleanup.

[connection-handler]: exception-handler's finding is compelling.
                      I found cleanup triggered by exception context manager.
                      Revising theory: Exception → cleanup → close.

[configuration]: No environment settings affecting message handling.
                 Configuration theory unlikely.
```

**Step 4: Synthesize Results**

```
What's the consensus on root cause?

[Lead synthesizes]:
Root Cause: Unhandled ValueError in message parser triggers
exception context manager cleanup, which closes WebSocket connection.

Supporting evidence:
- Exception in message parser (exception-handler)
- Context manager cleanup code (connection-handler)
- No proper exception handling (exception-handler)

Fix: Add try/except around message parsing with proper error response.
```

### Plugin/Extension Ecosystem

**Most useful packages for agent teams:**

1. **Model Context Protocol (MCP) Servers**
   - `@modelcontextprotocol/server-slack` — Slack integration
   - `@modelcontextprotocol/server-github` — GitHub operations
   - `@modelcontextprotocol/server-postgres` — Database queries
   - Custom MCP servers for domain-specific tools

2. **Testing Tools**
   - pytest (Python)
   - Jest (TypeScript)
   - Playwright (E2E)

3. **Code Intelligence**
   - Language servers (TypeScript, Python, Go, Rust)
   - Symbol navigation and auto-complete

**Adding an MCP server to your team:**

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
        }
    },
    agents={
        "pr-reviewer": AgentDefinition(
            description="Reviews pull requests",
            prompt="You are a PR reviewer...",
            tools=["Read", "mcp__github__*"],  # Allow all GitHub MCP tools
        )
    }
)
```

### Deployment Considerations

**Key considerations:**

1. **Token Usage** — Agent teams use 3-4x tokens vs single session
   - Use Opus for lead, Sonnet for teammates
   - Clean up teams when done
   - Monitor rate limits

2. **Rate Limits** — Multiple concurrent requests
   - Recommended TPM: 100k-200k for teams of 3-5
   - See [resources.md](./resources.md) for scaling guidance

3. **Permissions** — Pre-approve common operations
   - Set permission mode before spawning
   - Reduces bottlenecks during execution

4. **File Conflicts** — Prevent simultaneous edits
   - Assign distinct file sets to each teammate
   - Use plan approval for overlapping changes

5. **Team Cleanup** — Remove shared resources
   ```
   Clean up the team   # Lead only
   ```

6. **Monitoring** — Track team progress
   - Use Ctrl+T to toggle task view
   - Check `~/.claude/teams/{team-name}/` for status

---

## Level 5: Next Steps

### Advanced Topics to Explore

#### 1. Custom Agent Architectures

**Hollywood Model:**
- Manager (lead)
- Architect (design planner)
- Dev Pair (TDD: test-writer + implementer)
- QA Gatekeeper (final validation)

**Research:** [Hollywood Multi-Agent System](https://medium.com/@LakshmiNarayana_U/i-built-a-hollywood-multi-agent-system-using-ai-a-meta-journey-with-claude-15943361c994)

#### 2. Lifecycle Hooks for Team Control

**Intercept agent events:**

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def on_subagent_start(input_data, tool_use_id, context):
    agent_id = input_data.get("agent_id")
    print(f"Agent {agent_id} starting...")
    # Log to monitoring system
    return {"continue_": True}

options = ClaudeAgentOptions(
    hooks={
        "SubagentStart": [HookMatcher(hooks=[on_subagent_start])],
        "SubagentStop": [HookMatcher(hooks=[on_subagent_stop])],
    }
)
```

**Resources:** [SDK Hooks Documentation](https://platform.claude.com/docs/en/agent-sdk/hooks)

#### 3. Advanced Task Dependency Patterns

**Complex dependency graphs:**
```
Task A → Task B → Task D
      ↘ Task C ↗
```

**Dynamic task creation:**
- Agents create new tasks based on findings
- Automatically added to shared task list
- Dependencies resolved in real-time

#### 4. Performance Optimization

**Reduce token usage:**
- Keep spawn prompts focused
- Use Sonnet instead of Opus for teammates
- Clean up teams promptly
- Avoid redundant context in prompts

**Improve coordination speed:**
- Right-size tasks (5-6 per teammate)
- Use plan approval for risky work only
- Pre-approve common permissions

**Resources:** [Agent Teams Best Practices](https://claudefa.st/blog/guide/agents/agent-teams-best-practices)

#### 5. Production Integration Patterns

**Spotify Pattern: Slack-Triggered Agents**
```
Slack Message → AWS Lambda → Claude Agent Team → Auto-PR
```

**GitHub Bot Pattern:**
```
PR Created → Webhook → Agent Team Review → Comment on PR
```

**Resources:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

### Best Resources for Each Topic

| Topic | Resource | Type |
|-------|----------|------|
| **Agent Teams Fundamentals** | [Official Docs](https://code.claude.com/docs/en/agent-teams) | Docs |
| **SDK Architecture** | [Building with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) | Blog |
| **Practical Examples** | [claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos) | Code |
| **Best Practices** | [ClaudeFast Guide](https://claudefa.st/blog/guide/agents/agent-teams-best-practices) | Guide |
| **Troubleshooting** | [Discord Community](https://discord.com/invite/6PPFFzqPDZ) | Community |
| **Production Use Cases** | [Spotify/Security/Hai Case Studies](https://code.claude.com/docs/en/agent-teams) | Case Studies |

### Community Resources

**Join the Community:**
- **[Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ)** — Active community, quick responses
- **[GitHub Discussions](https://github.com/anthropics/claude-agent-sdk-python/discussions)** — Technical Q&A
- **[r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/)** — General discussion

**Weekly Learning:**
- Discord #question-of-the-week channel
- Featured Projects (Project of the Month voting)

### How to Get Help

**Stuck on something?**

1. **Check official docs first:** [code.claude.com/docs](https://code.claude.com/docs/en/agent-teams)
2. **Search GitHub issues:** [Python SDK Issues](https://github.com/anthropics/claude-agent-sdk-python/issues)
3. **Ask in Discord:** #general-questions or #agent-sdk channels
4. **Review examples:** [claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)

**Include in your question:**
- SDK version (`pip show claude-agent-sdk`)
- Error message (full traceback)
- Minimal reproduction code
- What you expected vs. what happened

### Hands-On Exercises

**Exercise 1: Build a Documentation Generator Team**

Create a team that:
- Reads all code files in a project
- One teammate extracts API signatures
- One teammate writes usage examples
- One teammate generates markdown docs
- Lead synthesizes into comprehensive documentation

**Exercise 2: Multi-Language Code Migrator**

Create a team that:
- Analyzes Python codebase
- One teammate converts to TypeScript
- One teammate writes equivalent tests
- One teammate validates behavior matches
- Outputs working TypeScript project

**Exercise 3: Security Audit Pipeline**

Create a team that:
- Scans codebase for vulnerabilities
- One teammate checks for SQL injection
- One teammate checks for XSS
- One teammate checks for auth issues
- One teammate checks dependencies
- Outputs security report with severity levels

**Challenge Exercise: Self-Improving Team**

Create a team that:
- Reviews its own agent definitions
- Identifies weaknesses in coordination
- Proposes improvements to task decomposition
- Generates updated agent definitions
- Meta-level: agents improving their own architecture

---

**Congratulations!** You now have a comprehensive understanding of Claude Agent Teams. Start building, experiment, and join the community to share what you create.

**Next:** Check out [resources.md](./resources.md) for all the links and references, or dive into the code examples in `code-examples/`.
