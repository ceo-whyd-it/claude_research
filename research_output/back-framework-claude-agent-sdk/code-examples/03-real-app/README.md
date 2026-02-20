# Real App: Multi-Agent Research System

A production-grade research agent demonstrating advanced Claude Agent SDK patterns.

## What It Does

1. Takes a research question as input
2. Spawns 3 specialist subagents in sequence:
   - `technical-researcher` — official docs, APIs, architecture
   - `usecase-researcher` — real-world adoption, case studies
   - `comparison-researcher` — alternatives, tradeoffs, ecosystem
3. Queries an internal knowledge base (custom MCP tool)
4. Synthesizes all findings into `output/research_report.md`

## Features Demonstrated

| Feature | Implementation |
|---------|---------------|
| Multi-agent orchestration | 3 `AgentDefinition` specialists |
| Safety hooks | Write restriction to `output/` only |
| Audit logging | All tool calls logged |
| Custom MCP tools | In-process knowledge base |
| Budget limits | `max_budget_usd=2.00` |
| Turn limits | `max_turns=30` |
| Cost tracking | `ResultMessage.total_cost_usd` |

## Setup & Run

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=sk-ant-api...

# Default question
python research_agent.py

# Custom question
python research_agent.py "What are the best practices for async Python error handling?"
```

## Expected Output

```
Research Question: What is the Claude Agent SDK?...
======================================================================
Starting multi-agent research pipeline...

  [Orchestrator → technical-researcher]
  [Orchestrator → usecase-researcher]
  [Orchestrator → comparison-researcher]

# Research Report: Claude Agent SDK
...synthesized report...

======================================================================
Research Pipeline Complete!
  Time elapsed:      45.2s
  Total cost:        $0.0834
  Turns taken:       12
  Subagents used:    ['technical-researcher', 'usecase-researcher', 'comparison-researcher']
  Tool calls logged: 23
  Report saved to: output/research_report.md
```

## Extending This Example

**Add more subagents:**
```python
SUBAGENTS["code-examples-researcher"] = AgentDefinition(
    description="Finds working code examples and starter templates.",
    prompt="...",
    tools=["WebSearch", "WebFetch"],
)
```

**Add real database lookup:**
```python
import psycopg2

@tool("query_database", "Query the production database", {"sql": str})
async def query_database(args):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(args["sql"])
    rows = cursor.fetchall()
    return {"content": [{"type": "text", "text": str(rows)}]}
```

**Add Slack notification:**
```python
options = ClaudeAgentOptions(
    mcp_servers={
        "internal": internal_tools_server,
        "slack": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-slack"],
            "env": {"SLACK_BOT_TOKEN": os.environ["SLACK_BOT_TOKEN"]}
        }
    },
    allowed_tools=[..., "mcp__slack__post_message"]
)
```
