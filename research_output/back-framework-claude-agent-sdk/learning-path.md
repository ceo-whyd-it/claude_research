# Claude Agent SDK — Learning Path

> **Rebranding Note:** In September 2025, Anthropic renamed the *Claude Code SDK* to the **Claude Agent SDK**, reflecting its use far beyond coding (research, email, data analysis, business automation).
> - Python: `pip install claude-agent-sdk`
> - TypeScript: `npm install @anthropic-ai/claude-agent-sdk`

---

## Level 1: Overview & Motivation

### What Problem Does It Solve?

Before the Claude Agent SDK, building autonomous AI agents required you to manually implement the **tool loop** — the cycle of:

1. Call the Claude API
2. Parse the response for tool use requests
3. Execute each tool yourself
4. Package the results and call the API again
5. Repeat until Claude stops requesting tools

This was complex, error-prone boilerplate. The Claude Agent SDK **automates this entire loop**, giving you the same autonomous execution engine that powers Claude Code — but as a programmable Python or TypeScript library.

```
Before SDK (manual loop):
  You write → API call → parse tools → execute → send results → API call → ...

With SDK (automated loop):
  You write prompt → SDK handles everything → results stream back to you
```

### What Is the Claude Agent SDK?

The Claude Agent SDK is a framework for building **autonomous AI agents** that can:

- **Read, write, and edit files** on your filesystem
- **Execute terminal commands** (bash, git, npm, etc.)
- **Search the web** and fetch web pages
- **Delegate subtasks** to specialized subagents
- **Connect to external services** via the Model Context Protocol (MCP)

It wraps the Claude API with an autonomous agent loop and a rich permission system that makes agents safe to run in production.

### What Existed Before? Why Is This Better?

| Approach | Limitation |
|----------|-----------|
| Raw Claude API | You must implement the tool loop yourself |
| LangChain | General orchestration, weak on real system access (files, terminal) |
| OpenAI Assistants API | Sandboxed execution; limited real system access |
| Devin / similar products | $500/month, not programmable |
| **Claude Agent SDK** | Programmable, real system access, fine-grained permissions, MIT licensed |

### Who Uses It? For What Applications?

**Who uses it:**
- Engineers building CI/CD automation and code review pipelines
- Teams building internal tools for non-technical users
- Researchers building multi-agent workflows
- Companies building customer support and business automation

**What gets built:**
- **Code review agents** — scan PRs for bugs, security issues, style violations
- **Research agents** — decompose a question into subtasks, search web, synthesize findings
- **Email assistants** — classify, draft responses, manage IMAP mailboxes
- **CI/CD agents** — run tests, analyze failures, create fix PRs automatically
- **Customer support agents** — look up orders, process returns, escalate to humans
- **Data analysis agents** — query databases, generate charts, write reports
- **Personal coding assistants** — build features, refactor code, write tests

### When Should You NOT Use It?

- **You only need a simple API call** — use the Anthropic Python SDK directly
- **You need a RAG/retrieval pipeline** — use LangChain or LlamaIndex instead
- **You need a visual workflow builder** — use LangGraph or n8n
- **High-frequency, low-latency tasks** — the SDK spawns a subprocess per call (~12s overhead)
- **You need a specific LLM other than Claude** — the SDK only works with Claude

### Architecture at a Glance

```
Your Code (Python or TypeScript)
        ↓
  query() or ClaudeSDKClient
        ↓
  SubprocessCLITransport
  (spawns Claude Code CLI as subprocess)
        ↓
  Claude Code CLI
  (manages the agent loop + tool execution)
        ↓
  Anthropic API
  (Claude Sonnet / Opus / Haiku model)
```

The SDK spawns the Claude Code CLI as a subprocess and communicates with it via stdin/stdout using a JSON protocol. The CLI handles:
- Sending your prompt to the Claude API
- Detecting tool use requests in Claude's response
- Executing tools (file reads, bash commands, web searches, etc.)
- Returning tool results to Claude
- Streaming the final response back to your code

---

## Level 2: Setup & First Project

### Prerequisites

| Requirement | Minimum Version | Check Command |
|------------|----------------|---------------|
| Python | 3.10+ | `python --version` |
| API Key | — | Get at https://console.anthropic.com/ |

For TypeScript: Node.js 18+ (`node --version`)

### Installation

```bash
# Python
pip install claude-agent-sdk

# TypeScript/JavaScript
npm install @anthropic-ai/claude-agent-sdk
```

Set your API key as an environment variable:

```bash
# Linux/macOS
export ANTHROPIC_API_KEY=sk-ant-api...

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-api..."

# Or create a .env file (install python-dotenv first)
echo "ANTHROPIC_API_KEY=sk-ant-api..." > .env
```

### Alternative Authentication (Enterprise)

```bash
# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
# + standard AWS credentials

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Microsoft Azure
export CLAUDE_CODE_USE_FOUNDRY=1
```

### Your First Agent (Python)

Create a file called `hello_agent.py`:

```python
import asyncio
from claude_agent_sdk import query, AssistantMessage, TextBlock

async def main():
    print("Asking Claude what files are in the current directory...\n")

    async for message in query(
        prompt="List the files in the current directory and describe what each one might be for."
    ):
        # AssistantMessage contains Claude's text responses
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

asyncio.run(main())
```

Run it:

```bash
python hello_agent.py
```

**Expected output:** Claude will automatically use the `Bash` or `Glob` tool to list your files, then describe them. You'll see its response streaming in.

### Your First Agent (TypeScript)

```typescript
// hello_agent.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  console.log("Asking Claude what files are in the current directory...\n");

  for await (const message of query({
    prompt: "List the files in the current directory and describe each one.",
  })) {
    if (message.type === "assistant") {
      const textBlocks = message.message?.content?.filter(
        (b: any) => b.type === "text"
      );
      for (const block of textBlocks ?? []) {
        process.stdout.write(block.text);
      }
    }
  }
}

main();
```

Run it:

```bash
npx tsx hello_agent.ts
```

### Project Structure for Agents

A typical agent project looks like this:

```
my-agent/
├── .env                    # ANTHROPIC_API_KEY (never commit this!)
├── .gitignore              # Include .env, __pycache__, etc.
├── requirements.txt        # claude-agent-sdk and other deps
├── CLAUDE.md               # Agent instructions (read by the SDK automatically)
├── agent.py                # Main entry point
├── prompts/                # System prompts for different agents
│   ├── main_agent.md
│   └── subagents/
│       └── researcher.md
└── output/                 # Where agents write their results
```

**What is `CLAUDE.md`?**
The SDK automatically reads `CLAUDE.md` from your working directory and includes it in the agent's context. Use it to give the agent project-specific knowledge:

```markdown
# CLAUDE.md

## Project Commands
- Run tests: `pytest tests/`
- Build: `python -m build`

## Code Style
- Use type hints for all function signatures
- Docstrings required for public functions

## Architecture Notes
- Database: PostgreSQL via SQLAlchemy
- API: FastAPI with Pydantic models
```

---

## Level 3: Architecture & Core Concepts

### Concept 1: The Two Interaction Modes

The SDK offers two ways to interact with Claude:

#### `query()` — Stateless, One-Shot

Use `query()` for standalone tasks where each call is independent:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Glob"],
        permission_mode="acceptEdits"  # Don't ask for confirmation
    )

    async for message in query(
        prompt="Count the total lines of Python code in this project.",
        options=options
    ):
        if isinstance(message, ResultMessage):
            print(f"Cost: ${message.total_cost_usd:.4f}")
            print(f"Turns taken: {message.num_turns}")

asyncio.run(main())
```

#### `ClaudeSDKClient` — Stateful, Multi-Turn

Use `ClaudeSDKClient` for conversations where Claude needs to remember context across exchanges:

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def main():
    async with ClaudeSDKClient() as client:
        # First exchange
        await client.query("My project uses FastAPI and PostgreSQL.")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up — Claude remembers the project context!
        await client.query("What database migration tool should I use?")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

**Common mistake:** Using `query()` for multi-turn conversations — each `query()` call starts fresh. Use `ClaudeSDKClient` instead.

---

### Concept 2: Message Types and Streaming

Every response from the SDK is an **async stream of messages**. There are four message types:

```python
from claude_agent_sdk import (
    AssistantMessage,  # Claude's text responses and tool use
    UserMessage,       # Your prompts (echoed back)
    SystemMessage,     # System prompt (echoed back)
    ResultMessage,     # Final summary: cost, turns, session ID
)
from claude_agent_sdk import TextBlock, ToolUseBlock, ThinkingBlock

async for message in query(prompt="Analyze this codebase"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(f"[Text] {block.text}")
            elif isinstance(block, ToolUseBlock):
                print(f"[Tool] {block.name}({block.input})")
            elif isinstance(block, ThinkingBlock):
                print(f"[Thinking] {block.thinking[:100]}...")

    elif isinstance(message, ResultMessage):
        print(f"\n--- Session Complete ---")
        print(f"Total cost: ${message.total_cost_usd:.4f}")
        print(f"Turns: {message.num_turns}")
        print(f"Session ID: {message.session_id}")
```

**Key insight:** `ResultMessage` always arrives last. Use it to get cost, turn count, and session ID for resuming conversations.

**Common mistake:** Assuming Claude's entire response is in one `AssistantMessage`. Text arrives in multiple messages as Claude thinks and acts. Always iterate the full stream.

---

### Concept 3: Tools and Permissions

The SDK gives Claude a rich set of **built-in tools**. You control which tools Claude can use:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Allowlist: Claude can ONLY use these tools
    allowed_tools=["Read", "Glob", "Grep"],  # Read-only: safe!

    # Permission mode controls confirmation prompts:
    # "default"           → Ask user before every tool use (interactive)
    # "acceptEdits"       → Auto-accept file edits, ask for bash
    # "plan"              → Show plan without executing
    # "bypassPermissions" → Full autonomy (use carefully in prod)
    permission_mode="acceptEdits",

    # Where the agent works from
    cwd="/home/user/my-project",
)

async for msg in query(prompt="Find all TODO comments", options=options):
    ...
```

**Available built-in tools:**

| Tool | What It Does | Risk Level |
|------|-------------|-----------|
| `Read` | Read files (text, images, PDFs) | Safe |
| `Glob` | Find files by pattern | Safe |
| `Grep` | Search file contents | Safe |
| `WebSearch` | Search the web | Safe |
| `WebFetch` | Fetch web pages | Safe |
| `Write` | Create new files | Medium |
| `Edit` | Modify existing files | Medium |
| `Bash` | Execute terminal commands | High |
| `Task` | Spawn subagents | Depends |
| `AskUserQuestion` | Ask the user questions | Safe |

**Custom permission callback:**

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

async def my_permission_check(tool_name, tool_input, context):
    # Block any rm -rf commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if "rm -rf" in command:
            return PermissionResultDeny(
                message="Refusing to run destructive rm -rf command"
            )
    # Allow everything else
    return PermissionResultAllow()

options = ClaudeAgentOptions(
    can_use_tool=my_permission_check,
    allowed_tools=["Read", "Write", "Bash"]
)
```

---

### Concept 4: Hooks — Intercepting the Agent Lifecycle

Hooks let you intercept and control what the agent does at key lifecycle points:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

# Hook function signature: (input_data, tool_use_id, context) -> dict
async def log_all_tool_use(input_data, tool_use_id, context):
    tool_name = input_data.get("tool_name", "unknown")
    print(f"[Hook] Tool called: {tool_name}")
    return {}  # Empty dict = don't block, don't modify

async def block_dangerous_bash(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "Bash":
        command = input_data.get("tool_input", {}).get("command", "")
        dangerous = ["rm -rf /", "sudo rm", "format", "dd if="]
        for danger in dangerous:
            if danger in command:
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Blocked dangerous command: {danger}",
                    }
                }
    return {}

options = ClaudeAgentOptions(
    hooks={
        # PreToolUse: runs BEFORE any tool is executed
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[log_all_tool_use]),     # Log all tools
            HookMatcher(matcher="Bash", hooks=[block_dangerous_bash]),  # Safety check
        ],
        # PostToolUse: runs AFTER a tool completes
        "PostToolUse": [
            HookMatcher(matcher="Write", hooks=[log_all_tool_use]),  # Log writes
        ],
    }
)
```

**Available hook events (Python SDK):**

| Event | When It Fires |
|-------|--------------|
| `PreToolUse` | Before any tool executes |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `UserPromptSubmit` | When a new prompt is submitted |
| `Stop` | When the conversation ends |
| `SubagentStop` | When a subagent finishes |
| `PreCompact` | Before message compaction |

**Common mistake:** Forgetting to return an empty dict `{}` from hooks. If your hook returns `None`, it may cause errors. Always return a dict.

---

### Concept 5: Subagents — Delegating to Specialists

Subagents let you create a **multi-agent system** where a main orchestrator delegates to specialized workers:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    # The main agent can call these subagents via the "Task" tool
    allowed_tools=["Read", "Glob", "Grep", "Task"],

    # Define specialized subagents
    agents={
        "security-reviewer": AgentDefinition(
            description="Expert security auditor. Finds vulnerabilities, auth issues, and injection risks.",
            prompt="""You are a senior security engineer. Review code for:
- SQL injection vulnerabilities
- Authentication and authorization flaws
- Hardcoded secrets or API keys
- Input validation issues
Report findings with severity (Critical/High/Medium/Low) and remediation steps.""",
            tools=["Read", "Glob", "Grep"],  # Read-only for safety
        ),
        "performance-reviewer": AgentDefinition(
            description="Performance optimizer. Identifies bottlenecks and suggests improvements.",
            prompt="""You are a performance engineer. Review code for:
- N+1 database queries
- Missing indexes
- Unnecessary loops or redundant computations
- Memory leaks and inefficient data structures
Suggest specific optimizations with expected impact.""",
            tools=["Read", "Glob", "Grep"],
        ),
    }
)

async for message in query(
    prompt="""Review the codebase:
1. Use the security-reviewer agent to find security issues
2. Use the performance-reviewer agent to find performance issues
3. Synthesize both reports into a prioritized action plan""",
    options=options
):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

**Data flow in multi-agent systems:**

```
Main Orchestrator (Sonnet/Opus)
├── Reads broad prompt
├── Decomposes into subtasks
├── Calls Task tool → security-reviewer subagent (Haiku, cheaper)
│   └── Returns: security findings report
├── Calls Task tool → performance-reviewer subagent (Haiku, cheaper)
│   └── Returns: performance findings report
└── Synthesizes both reports → Final response to you
```

**Cost optimization tip:** Use an expensive model (Sonnet/Opus) for the orchestrator and a cheaper model (Haiku) for subagents by setting `model` in `AgentDefinition`.

---

### Concept 6: Custom Tools via In-Process MCP Servers

The Model Context Protocol (MCP) lets you create custom tools that Claude can call:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

# Define custom tools with the @tool decorator
@tool("get_weather", "Get current weather for a city", {"city": str})
async def get_weather(args):
    city = args["city"]
    # In real code, you'd call a weather API here
    return {
        "content": [{"type": "text", "text": f"Weather in {city}: 72°F, Sunny"}]
    }

@tool("lookup_customer", "Look up a customer by email", {"email": str})
async def lookup_customer(args):
    email = args["email"]
    # In real code, you'd query your database
    return {
        "content": [{
            "type": "text",
            "text": f"Customer: Jane Smith, Plan: Pro, Status: Active"
        }]
    }

# Bundle tools into an in-process MCP server
business_tools = create_sdk_mcp_server(
    name="business-tools",
    version="1.0.0",
    tools=[get_weather, lookup_customer]
)

options = ClaudeAgentOptions(
    mcp_servers={"biz": business_tools},
    # Tool naming: mcp__{server-name}__{tool-name}
    allowed_tools=["mcp__biz__get_weather", "mcp__biz__lookup_customer"]
)

async for message in query(
    prompt="What's the weather in Seattle? Also look up customer john@example.com",
    options=options
):
    ...
```

**MCP vs. Built-in Tools:**
- **Built-in tools** — File I/O, Bash, WebSearch — are always available
- **In-process MCP tools** — Custom Python functions, run in the same process (fast)
- **External MCP servers** — Remote processes (Slack, GitHub, databases) connected via subprocess

---

## Level 4: Building Real Applications

### The Project: Multi-Agent Research System

We'll build a research agent that:
1. Takes a research question
2. Decomposes it into subtopics
3. Spawns specialized researcher subagents (in parallel)
4. Synthesizes findings into a structured report
5. Saves the report to disk

This mirrors real production use cases.

### Step 1: Basic Research Agent

Start simple — one agent, web search, write a report:

```python
# research_agent_v1.py
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage

async def research(topic: str, output_file: str = "report.md"):
    print(f"Researching: {topic}\n")

    options = ClaudeAgentOptions(
        system_prompt="""You are a research assistant. When asked to research a topic:
1. Search for recent information using WebSearch
2. Fetch key pages with WebFetch to get details
3. Synthesize findings into a well-structured markdown report
4. Save the report using the Write tool""",
        allowed_tools=["WebSearch", "WebFetch", "Write"],
        permission_mode="acceptEdits",
    )

    async for message in query(
        prompt=f"Research '{topic}' and save a comprehensive report to {output_file}",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\nDone! Cost: ${message.total_cost_usd:.4f}")

asyncio.run(research("Claude Agent SDK best practices 2025"))
```

### Step 2: Add Safety Hooks

Before deploying, add hooks to log and control what the agent does:

```python
# research_agent_v2.py
import asyncio
import json
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, AssistantMessage, TextBlock, ResultMessage

# Track what the agent writes
writes_log = []

async def log_writes(input_data, tool_use_id, context):
    """Log all Write tool calls."""
    if input_data.get("tool_name") == "Write":
        file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
        writes_log.append(file_path)
        print(f"  [Hook] Writing to: {file_path}")
    return {}

async def restrict_write_location(input_data, tool_use_id, context):
    """Only allow writing to the output/ directory."""
    if input_data.get("tool_name") == "Write":
        file_path = input_data.get("tool_input", {}).get("file_path", "")
        if not file_path.startswith("output/"):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Files must be written to output/ directory only",
                }
            }
    return {}

async def research(topic: str):
    Path("output").mkdir(exist_ok=True)

    options = ClaudeAgentOptions(
        system_prompt="""You are a research assistant. Write all output files to the output/ directory.""",
        allowed_tools=["WebSearch", "WebFetch", "Write"],
        permission_mode="acceptEdits",
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Write", hooks=[restrict_write_location, log_writes]),
            ]
        }
    )

    async for message in query(
        prompt=f"Research '{topic}' and save a report to output/report.md",
        options=options
    ):
        if isinstance(message, ResultMessage):
            print(f"\nFiles written: {writes_log}")
            print(f"Cost: ${message.total_cost_usd:.4f}")

asyncio.run(research("Claude Agent SDK best practices 2025"))
```

### Step 3: Add Subagents for Parallel Research

Scale up with specialized subagents that research different angles simultaneously:

```python
# research_agent_v3.py — Full multi-agent system
import asyncio
from pathlib import Path
from claude_agent_sdk import (
    query, ClaudeAgentOptions, AgentDefinition,
    AssistantMessage, TextBlock, ResultMessage, HookMatcher
)

TOPICS_LOG = []

async def log_task_calls(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "Task":
        agent = input_data.get("tool_input", {}).get("subagent_type", "unknown")
        TOPICS_LOG.append(agent)
        print(f"  [Orchestrator] Spawning subagent: {agent}")
    return {}

async def research(question: str):
    Path("output").mkdir(exist_ok=True)

    options = ClaudeAgentOptions(
        system_prompt="""You are a research orchestrator. For each research question:
1. Identify 2-3 distinct research angles (technical details, use cases, community reception)
2. Delegate each angle to the appropriate specialized subagent using the Task tool
3. Wait for all subagents to complete
4. Synthesize their reports into one comprehensive markdown document
5. Save the final report to output/research_report.md""",

        allowed_tools=["Task", "Read", "Write"],
        permission_mode="acceptEdits",

        agents={
            "technical-researcher": AgentDefinition(
                description="Researches technical implementation details, APIs, and architecture.",
                prompt="""You research technical details. Use WebSearch and WebFetch to find:
- API documentation and code examples
- Architecture decisions and design patterns
- Performance benchmarks and limitations
Write a technical summary with code examples. Return your findings as markdown.""",
                tools=["WebSearch", "WebFetch"],
            ),
            "use-case-researcher": AgentDefinition(
                description="Researches real-world use cases and adoption stories.",
                prompt="""You research real-world adoption. Use WebSearch and WebFetch to find:
- Production use cases and testimonials
- Companies and teams using this technology
- Success stories and ROI metrics
Write a use-cases summary. Return your findings as markdown.""",
                tools=["WebSearch", "WebFetch"],
            ),
            "community-researcher": AgentDefinition(
                description="Researches community sentiment, tutorials, and common issues.",
                prompt="""You research community content. Use WebSearch and WebFetch to find:
- Top tutorials and learning resources
- Common pain points and gotchas
- Community discussions (Reddit, HN, Discord)
- Comparison with alternatives
Return your findings as markdown.""",
                tools=["WebSearch", "WebFetch"],
            ),
        },

        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Task", hooks=[log_task_calls]),
            ]
        }
    )

    print(f"Starting research: {question}\n")
    print("=" * 60)

    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\n{'=' * 60}")
            print(f"Research complete!")
            print(f"Subagents spawned: {TOPICS_LOG}")
            print(f"Total cost: ${message.total_cost_usd:.4f}")
            print(f"Turns: {message.num_turns}")

if __name__ == "__main__":
    question = "Research the Claude Agent SDK: technical architecture, real-world use cases, and community reception"
    asyncio.run(research(question))
```

### Step 4: Add Custom Business Tools

Connect the agent to your own data sources:

```python
# Add to research_agent_v3.py

from claude_agent_sdk import tool, create_sdk_mcp_server

# Simulate a company knowledge base
KNOWLEDGE_BASE = {
    "claude-agent-sdk": "Internal adoption: 3 teams, 12 projects, avg 40% productivity gain",
    "langchain": "Used by data team for RAG pipelines since 2023",
}

@tool("search_knowledge_base", "Search internal company knowledge base", {"query": str})
async def search_knowledge_base(args):
    query_term = args["query"].lower()
    results = []
    for key, value in KNOWLEDGE_BASE.items():
        if query_term in key or query_term in value.lower():
            results.append(f"- {key}: {value}")

    if results:
        return {"content": [{"type": "text", "text": "\n".join(results)}]}
    return {"content": [{"type": "text", "text": "No internal data found for this query."}]}

# Create MCP server
internal_tools = create_sdk_mcp_server(
    name="internal",
    version="1.0.0",
    tools=[search_knowledge_base]
)

# Add to options:
# mcp_servers={"internal": internal_tools},
# allowed_tools=[..., "mcp__internal__search_knowledge_base"]
```

### Plugin/Extension Ecosystem

Beyond custom tools, connect to external services via standard MCP servers:

| Integration | What It Enables |
|-------------|----------------|
| GitHub MCP | Read/write PRs, issues, code; automated PR creation |
| Slack MCP | Post messages, read channels, manage notifications |
| PostgreSQL MCP | Direct SQL queries, schema exploration |
| Figma MCP | Read design specs, generate code from designs |
| Playwright MCP | Browser automation, web scraping, screenshots |
| Google Drive MCP | Read/write documents and spreadsheets |

Install and configure an MCP server:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_your_token_here"}
        }
    },
    allowed_tools=["mcp__github__list_pull_requests", "mcp__github__create_issue"]
)
```

### Deployment Considerations

**For production deployments:**

1. **Run in Docker containers** — Isolate each agent session:
   ```dockerfile
   FROM python:3.12-slim
   RUN pip install claude-agent-sdk
   COPY agent.py .
   CMD ["python", "agent.py"]
   ```

2. **Use `permission_mode="default"`** for user-facing apps (asks before each action)

3. **Set budget limits** to prevent runaway costs:
   ```python
   options = ClaudeAgentOptions(
       max_budget_usd=1.00,  # Hard limit: $1 per session
       max_turns=50,          # Hard limit: 50 turns max
   )
   ```

4. **Log everything** — Store `ResultMessage` data (session_id, cost, turns) in your database

5. **Never hardcode API keys** — Use environment variables or secrets managers

---

## Level 5: Next Steps

### Advanced Topics to Explore

| Topic | What to Learn | Resource |
|-------|--------------|---------|
| **Extended Thinking** | Give Claude more reasoning time for complex problems | [Anthropic Docs: Extended Thinking](https://platform.claude.com/docs/en/agent-sdk/python) |
| **Context Compaction** | Handle long sessions without losing context | SDK docs: `PreCompact` hook |
| **Session Resumption** | Resume conversations using session IDs | `ResultMessage.session_id` |
| **File Checkpointing** | Rewind file changes made during a session | `enable_file_checkpointing=True` |
| **Dynamic MCP Tool Loading** | Load MCP tools on-demand to save context space | Requires Sonnet 4+ or Opus 4+ |
| **Bedrock/Vertex Deployment** | Deploy to AWS or GCP for enterprise compliance | `CLAUDE_CODE_USE_BEDROCK=1` |
| **Budget Management** | Prometheus metrics, per-team quotas | eesel.ai production guide |
| **CI/CD Integration** | GitHub Actions with `@claude` mentions | [claude-code-action repo](https://github.com/anthropics/claude-code-action) |

### Recommended Learning Projects

1. **PR Review Bot** — GitHub Action that reviews every PR for bugs and style
2. **Codebase Q&A** — Ask questions about a large codebase using Grep/Read
3. **Automated Report Generator** — Research a topic weekly, email a summary
4. **Database Query Agent** — Natural language SQL query generator with safety guardrails
5. **Multi-Agent Test Suite Generator** — Orchestrate test-writer, implementer, and reviewer subagents

### Getting Help

| Channel | Best For |
|---------|---------|
| [Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ) | Quick questions, sharing projects, community support |
| [GitHub Issues (Python SDK)](https://github.com/anthropics/claude-agent-sdk-python/issues) | Bug reports and feature requests |
| [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) | Tips, showcase, discussion |
| [platform.claude.com/docs](https://platform.claude.com/docs/en/agent-sdk/overview) | Official reference |
| [Anthropic Engineering Blog](https://www.anthropic.com/engineering) | Deep dives and best practices |

### The Community Consensus on What Works

After synthesizing community feedback (Reddit, HN, Discord, blog posts):

**Claude Agent SDK excels at:**
- Agents that touch **real systems** — files, terminals, APIs
- **Rapid prototyping** before committing to heavier frameworks
- **CI/CD automation** — runs outside local editors, scriptable
- **Large codebase analysis** — 200k token context handles full repos

**Common pitfalls to avoid:**
- Breaking up complex tasks — "do this entire app" fails; "do this one component" succeeds
- Vigilantly reviewing test files — Claude may modify tests to match wrong implementations
- Letting Claude control Git — humans should own Git operations; Claude owns file changes
- Forgetting context budget — use `/compact` or `max_turns` for long sessions

**The sweet spot combination:**
```
Claude Agent SDK (system access + agent loop)
    +
MCP servers (Slack, GitHub, databases)
    +
LangChain (if you need RAG/retrieval)
```

### Roadmap: Where the SDK Is Heading

Based on Anthropic's engineering blog and recent releases (Feb 2026):
- **Tool Search** — Dynamic loading of relevant MCP tools (Sonnet 4+ only)
- **Structured Outputs** — Enforce JSON schemas on agent responses
- **Extended Thinking** — Control Claude's internal reasoning budget
- **Better IDE Integration** — JetBrains native integration announced Sept 2025
- **Skills System** — Reusable agent capabilities across projects

---

*This learning path was generated in February 2026 from official documentation, source repository analysis, and community content. The Claude Agent SDK is actively developed; always check the [official docs](https://platform.claude.com/docs/en/agent-sdk/overview) for the latest.*
