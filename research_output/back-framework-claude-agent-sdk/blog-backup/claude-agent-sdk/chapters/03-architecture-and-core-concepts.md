---
title: "Architecture and Core Concepts: The Mental Model That Makes Everything Click"
series: "Mastering Claude Agent SDK"
part: 3
date: 2026-02-19
tags: [claude, agent-sdk, ai, python]
prev: "02-setup-and-first-project.md"
next: "04-building-real-applications.md"
---

# Architecture and Core Concepts: The Mental Model That Makes Everything Click

This is the longest post in the series, and for good reason: the concepts covered here are the foundation for everything else. Master these six concepts and the rest of the SDK falls into place naturally.

## Concept 1: The Two Interaction Modes

The SDK gives you two ways to run an agent, and choosing the wrong one is the most common beginner mistake.

### `query()` — Stateless, One-Shot

Use `query()` when each task is independent and you do not need Claude to remember anything between calls:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Glob"],
        permission_mode="acceptEdits"
    )

    async for message in query(
        prompt="Count the total lines of Python code in this project.",
        options=options
    ):
        if isinstance(message, ResultMessage):
            print(f"Cost: ${message.total_cost_usd:.4f}, Turns: {message.num_turns}")

asyncio.run(main())
```

Each call to `query()` starts a fresh session. Claude has no memory of previous calls.

### `ClaudeSDKClient` — Stateful, Multi-Turn

Use `ClaudeSDKClient` when you need a conversation where Claude remembers context across exchanges:

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

        # Second exchange — Claude remembers the project context
        await client.query("What database migration tool should I use?")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

The `ClaudeSDKClient` also reuses the subprocess across calls, so you only pay the startup overhead once per session.

**Rule of thumb:** Tasks = `query()`. Conversations = `ClaudeSDKClient`.

---

## Concept 2: Message Types and Streaming

Every response from the SDK is an async stream of typed messages. You must iterate the full stream — Claude's response is not a single object, it is a sequence of events arriving as the agent thinks and acts.

The four message types:

```python
from claude_agent_sdk import (
    AssistantMessage,  # Claude's text responses and tool use requests
    UserMessage,       # Your prompts (echoed back in the stream)
    SystemMessage,     # System prompt (echoed back at start)
    ResultMessage,     # Final summary: cost, turns, session ID
)
from claude_agent_sdk import TextBlock, ToolUseBlock, ThinkingBlock

async for message in query(prompt="Analyze this codebase"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(f"[Text] {block.text}")
            elif isinstance(block, ToolUseBlock):
                print(f"[Tool] Claude is using: {block.name}")
            elif isinstance(block, ThinkingBlock):
                print(f"[Thinking] {block.thinking[:80]}...")

    elif isinstance(message, ResultMessage):
        print(f"Total cost: ${message.total_cost_usd:.4f}")
        print(f"Turns: {message.num_turns}")
        print(f"Session ID: {message.session_id}")
```

`ResultMessage` always arrives last. Store its `session_id` if you want to resume a conversation later, and its `total_cost_usd` if you are tracking spend.

**Common mistake:** Assuming a single `AssistantMessage` contains the full response. Text arrives in multiple messages as Claude takes intermediate steps. Always consume the full stream.

---

## Concept 3: Tools and Permissions

The built-in tools give Claude its real-world capabilities. You control which tools Claude can access with an explicit allowlist.

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Claude can ONLY use these tools — everything else is blocked
    allowed_tools=["Read", "Glob", "Grep"],

    # Permission mode controls how tool use is approved:
    # "default"           → Ask user to confirm before each tool (interactive)
    # "acceptEdits"       → Auto-approve file edits; ask for bash
    # "plan"              → Show what Claude would do, but don't execute
    # "bypassPermissions" → Full autonomy — use carefully
    permission_mode="acceptEdits",

    cwd="/path/to/your/project",
)

async for msg in query(prompt="Find all TODO comments", options=options):
    ...
```

The full built-in tool inventory:

| Tool | What It Does | Risk Level |
|------|-------------|-----------|
| `Read` | Read files (text, images, PDFs) | Safe |
| `Glob` | Find files by pattern | Safe |
| `Grep` | Search file contents by regex | Safe |
| `WebSearch` | Search the web | Safe |
| `WebFetch` | Fetch and parse web pages | Safe |
| `Write` | Create new files | Medium |
| `Edit` | Modify existing files | Medium |
| `Bash` | Execute terminal commands | High |
| `Task` | Spawn specialized subagents | Depends |
| `AskUserQuestion` | Prompt the user interactively | Safe |

For production systems, write a custom permission callback instead of relying on modes:

```python
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

async def my_permission_check(tool_name, tool_input, context):
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if "rm -rf" in command:
            return PermissionResultDeny(message="Refusing destructive rm -rf")
    return PermissionResultAllow()

options = ClaudeAgentOptions(
    can_use_tool=my_permission_check,
    allowed_tools=["Read", "Write", "Bash"]
)
```

---

## Concept 4: Hooks — Intercepting the Agent Lifecycle

Hooks let you run your own Python functions at key points in the agent's lifecycle — before a tool executes, after it completes, or when the session ends. This is where you add logging, auditing, safety guardrails, and observability.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_all_tools(input_data, tool_use_id, context):
    tool_name = input_data.get("tool_name", "unknown")
    print(f"[Audit] Tool called: {tool_name}")
    return {}  # Always return a dict — None will cause errors

async def block_dangerous_bash(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "Bash":
        command = input_data.get("tool_input", {}).get("command", "")
        if "rm -rf /" in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Blocked: rm -rf / detected",
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[log_all_tools]),      # all tools
            HookMatcher(matcher="Bash", hooks=[block_dangerous_bash]),  # bash only
        ],
        "PostToolUse": [
            HookMatcher(matcher="Write", hooks=[log_all_tools]),  # after writes
        ],
    }
)
```

Available hook events:

| Event | When It Fires |
|-------|--------------|
| `PreToolUse` | Before any tool executes |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `UserPromptSubmit` | When a new prompt is submitted |
| `Stop` | When the conversation ends |
| `SubagentStop` | When a subagent finishes |
| `PreCompact` | Before message compaction for long sessions |

**Critical rule:** Hook functions must always return a dict. An empty dict `{}` means "allow, no modification." Never return `None`.

---

## Concept 5: Subagents — Multi-Agent Systems

The `Task` tool lets the orchestrator agent spawn specialized subagents and delegate work to them. Each subagent has its own system prompt, tool restrictions, and model (so you can use a cheaper model for workers).

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Task"],

    agents={
        "security-reviewer": AgentDefinition(
            description="Expert security auditor. Finds vulnerabilities and auth issues.",
            prompt="""You are a senior security engineer. Review code for:
- SQL injection, command injection vulnerabilities
- Authentication and authorization flaws
- Hardcoded secrets or API keys
- Input validation gaps
Report findings with severity (Critical/High/Medium/Low) and remediation steps.""",
            tools=["Read", "Glob", "Grep"],  # Read-only — safe by design
        ),
        "performance-reviewer": AgentDefinition(
            description="Performance optimizer. Identifies bottlenecks and scaling issues.",
            prompt="""You are a performance engineer. Find:
- N+1 database queries, missing indexes
- Inefficient loops, redundant computations
- Blocking I/O in async contexts
Suggest specific optimizations with expected impact.""",
            tools=["Read", "Glob", "Grep"],
        ),
    }
)
```

The data flow:

```
Main Orchestrator (Sonnet/Opus — smarter, pricier)
├── Calls Task → security-reviewer (Haiku — cheaper, focused)
│   └── Returns: security findings as markdown
├── Calls Task → performance-reviewer (Haiku — cheaper, focused)
│   └── Returns: performance findings as markdown
└── Synthesizes both → Final report to you
```

**Cost optimization:** Set `model="claude-haiku-4-5"` in `AgentDefinition` to use cheaper models for subagents while keeping the orchestrator on Sonnet or Opus.

---

## Concept 6: Custom Tools via In-Process MCP Servers

The Model Context Protocol (MCP) is the standard for extending Claude's capabilities with custom tools. The easiest form is an **in-process MCP server** — a Python function that Claude can call.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

@tool("get_weather", "Get current weather for a city", {"city": str})
async def get_weather(args):
    city = args["city"]
    # In real code, call your weather API here
    return {"content": [{"type": "text", "text": f"Weather in {city}: 72F, Sunny"}]}

@tool("lookup_customer", "Look up a customer by email", {"email": str})
async def lookup_customer(args):
    email = args["email"]
    # In real code, query your database here
    return {"content": [{"type": "text", "text": "Customer: Jane Smith, Plan: Pro"}]}

# Bundle tools into a named server
business_tools = create_sdk_mcp_server(
    name="business-tools",
    version="1.0.0",
    tools=[get_weather, lookup_customer]
)

options = ClaudeAgentOptions(
    mcp_servers={"biz": business_tools},
    # Naming pattern: mcp__{server-alias}__{tool-name}
    allowed_tools=["mcp__biz__get_weather", "mcp__biz__lookup_customer"]
)
```

You can also connect to **external MCP servers** — separate processes providing tools like GitHub integration, Slack messaging, or database access:

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_your_token"}
        }
    },
    allowed_tools=["mcp__github__list_pull_requests", "mcp__github__create_issue"]
)
```

---

## The Full Mental Model

With all six concepts in hand, here is how they compose:

```
Your Prompt
    |
ClaudeAgentOptions
  ├── allowed_tools        (what Claude can use)
  ├── permission_mode      (how approvals work)
  ├── hooks                (your code runs at lifecycle events)
  ├── agents               (specialist subagents for delegation)
  └── mcp_servers          (custom tools from your codebase or external services)
    |
query() or ClaudeSDKClient
    |
Streaming message types:
  SystemMessage → UserMessage → AssistantMessage(s) → ResultMessage
```

## What's Next

Part 4 puts this mental model to work. We build a complete, production-grade multi-agent research system in four progressive steps: a simple research agent, safety hooks, parallel subagents, and custom business tools. By the end, you will have code you can actually deploy.

Read on: [Part 4 — Building Real Applications](04-building-real-applications.md)
