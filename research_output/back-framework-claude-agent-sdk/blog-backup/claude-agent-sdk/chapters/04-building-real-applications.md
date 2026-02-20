---
title: "Building Real Applications: A Production Multi-Agent Research System"
series: "Mastering Claude Agent SDK"
part: 4
date: 2026-02-19
tags: [claude, agent-sdk, ai, python]
prev: "03-architecture-and-core-concepts.md"
next: "05-next-steps-and-ecosystem.md"
---

# Building Real Applications: A Production Multi-Agent Research System

This is where theory becomes practice. We are going to build a research agent from scratch — not a toy example, but a system with real structure, safety guardrails, parallel subagents, and custom business tools. We will do it in four steps, each building on the last.

The final system will:
1. Accept a research question
2. Decompose it into subtopics
3. Spawn specialized researcher subagents in parallel
4. Check an internal knowledge base via a custom MCP tool
5. Synthesize all findings into a structured markdown report
6. Save the report to disk — with safety hooks preventing writes outside a designated directory

## Step 1: Basic Research Agent

Start as simple as possible — one agent, web search, write a report:

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

asyncio.run(research("Claude Agent SDK best practices 2026"))
```

This works but has no guardrails. The agent can write files anywhere, costs are unbounded, and you have no visibility into what it is doing. Step 2 fixes that.

## Step 2: Add Safety Hooks

Production systems need audit trails and restrictions. Before deploying, wrap the agent with hooks:

```python
# research_agent_v2.py
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, ResultMessage

writes_log = []

async def log_writes(input_data, tool_use_id, context):
    """Audit every Write call."""
    if input_data.get("tool_name") == "Write":
        file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
        writes_log.append(file_path)
        print(f"  [Audit] Writing to: {file_path}")
    return {}

async def restrict_write_location(input_data, tool_use_id, context):
    """Only allow writes to the output/ directory."""
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
        system_prompt="You are a research assistant. Write all output files to the output/ directory.",
        allowed_tools=["WebSearch", "WebFetch", "Write"],
        permission_mode="acceptEdits",
        max_turns=20,           # Prevent runaway sessions
        max_budget_usd=0.50,    # Hard cost cap
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

asyncio.run(research("Claude Agent SDK best practices 2026"))
```

Notice the two key additions: `max_turns=20` and `max_budget_usd=0.50`. These are your circuit breakers for production. Without them, a confused agent can run for many turns and rack up significant costs.

## Step 3: Add Parallel Subagents

A single-agent system searches the web serially. A multi-agent system can investigate different angles simultaneously, completing in a fraction of the time:

```python
# research_agent_v3.py
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
        print(f"  [Orchestrator] Spawning: {agent}")
    return {}

async def research(question: str):
    Path("output").mkdir(exist_ok=True)

    options = ClaudeAgentOptions(
        system_prompt="""You are a research orchestrator. For each research question:
1. Identify 2-3 distinct research angles
2. Delegate each angle to the appropriate specialist subagent using Task
3. Wait for all subagents to complete
4. Synthesize their reports into one comprehensive markdown document
5. Save the final report to output/research_report.md""",

        allowed_tools=["Task", "Read", "Write"],
        permission_mode="acceptEdits",
        max_turns=30,
        max_budget_usd=2.00,

        agents={
            "technical-researcher": AgentDefinition(
                description="Researches technical implementation details, APIs, and architecture.",
                prompt="""You research technical details. Find:
- API documentation and code examples
- Architecture decisions and design patterns
- Performance characteristics and limitations
Return your findings as structured markdown with source URLs.""",
                tools=["WebSearch", "WebFetch"],
            ),
            "usecase-researcher": AgentDefinition(
                description="Researches real-world use cases and adoption stories.",
                prompt="""You research real-world adoption. Find:
- Production use cases and case studies
- Companies and teams using this technology
- Success metrics and ROI data
Return your findings as structured markdown with source URLs.""",
                tools=["WebSearch", "WebFetch"],
            ),
            "comparison-researcher": AgentDefinition(
                description="Researches alternatives and ecosystem positioning.",
                prompt="""You are a technology analyst. Find:
- Key alternatives and how they compare
- Community sentiment and common criticisms
- When to use this vs. alternatives
Return your findings as structured markdown with source URLs.""",
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
    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\nResearch complete!")
            print(f"Subagents used: {TOPICS_LOG}")
            print(f"Total cost: ${message.total_cost_usd:.4f}")
            print(f"Turns: {message.num_turns}")

if __name__ == "__main__":
    asyncio.run(research(
        "Research the Claude Agent SDK: technical architecture, real-world use cases, and how it compares to LangChain"
    ))
```

## Step 4: Add Custom Business Tools

The final piece is connecting the agent to your own data. An internal knowledge base, a CRM, a database — these are all reachable via in-process MCP tools:

```python
# Add to research_agent_v3.py
from claude_agent_sdk import tool, create_sdk_mcp_server

# Simulate a company knowledge base
KNOWLEDGE_BASE = {
    "claude-agent-sdk": "Internal adoption: 3 teams, 12 projects since Q4 2025. Avg 40% productivity gain in CI/CD workflows.",
    "langchain": "Used by data team for RAG pipelines since 2023. Not used for agentic workflows.",
    "openai": "Legacy integrations only. New projects standardized on Claude.",
}

@tool("search_knowledge_base", "Search internal company knowledge base", {"query": str})
async def search_knowledge_base(args):
    query_term = args["query"].lower()
    results = [
        f"- {key}: {value}"
        for key, value in KNOWLEDGE_BASE.items()
        if query_term in key or query_term in value.lower()
    ]
    if results:
        return {"content": [{"type": "text", "text": "\n".join(results)}]}
    return {"content": [{"type": "text", "text": f"No internal data found for '{args['query']}'."}]}

internal_tools = create_sdk_mcp_server(
    name="internal",
    version="1.0.0",
    tools=[search_knowledge_base]
)

# Then in ClaudeAgentOptions:
# mcp_servers={"internal": internal_tools},
# allowed_tools=[..., "mcp__internal__search_knowledge_base"]
```

The orchestrator's system prompt now includes: "Also check the internal knowledge base using `mcp__internal__search_knowledge_base` to add any proprietary context not available on the web."

## Production Deployment Checklist

Before putting any agent in production, work through this list:

**1. Containerize it**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install claude-agent-sdk
COPY agent.py prompts/ ./
CMD ["python", "agent.py"]
```

Isolated containers prevent agents from touching host systems they should not.

**2. Set hard limits**

```python
options = ClaudeAgentOptions(
    max_budget_usd=1.00,   # Hard limit: $1 per session
    max_turns=50,           # Hard limit: 50 turns max
)
```

Never skip these in production. A prompt injection or confused agent can run indefinitely without them.

**3. Log ResultMessage data**

Every `ResultMessage` gives you `session_id`, `total_cost_usd`, and `num_turns`. Store these in your database. They are essential for debugging, cost attribution, and audit compliance.

**4. Use `permission_mode="default"` for user-facing apps**

The default mode asks for confirmation before each tool use. For internal automation where you trust the agent, `"acceptEdits"` is appropriate. For customer-facing products, always confirm.

**5. Restrict write paths with hooks**

Always use the write-location restriction hook from Step 2. An agent that can write anywhere is an agent that can overwrite configuration files, secrets, and code.

## The External MCP Ecosystem

Beyond custom tools, the MCP ecosystem gives you ready-made integrations:

| Integration | What the Agent Can Do |
|-------------|----------------------|
| GitHub MCP | Read/write PRs, issues, code; create commits |
| Slack MCP | Post messages, read channels, manage threads |
| PostgreSQL MCP | Execute SQL queries, explore schema |
| Figma MCP | Read design specs, extract component specs |
| Playwright MCP | Browser automation, web scraping, screenshots |
| Google Drive MCP | Read/write documents and spreadsheets |

Configuration follows the same pattern:

```python
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

## What's Next

You now have a complete, production-ready multi-agent pattern. Part 5 covers the bigger picture: advanced topics like extended thinking, session resumption, context compaction, and the CI/CD integrations. It also distills community wisdom on what works, what to avoid, and where the SDK is heading in 2026.

Read on: [Part 5 — Next Steps and the Ecosystem](05-next-steps-and-ecosystem.md)
