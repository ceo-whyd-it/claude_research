---
title: "Getting Started: Installation, Setup, and Your First Agent"
series: "Mastering Claude Agent SDK"
part: 2
date: 2026-02-19
tags: [claude, agent-sdk, ai, python]
prev: "01-overview-and-motivation.md"
next: "03-architecture-and-core-concepts.md"
---

# Getting Started: Installation, Setup, and Your First Agent

This post gets you from zero to a running agent. By the end, you will have the SDK installed, your API key configured, a recommended project structure in place, and two working agent scripts — one in Python, one in TypeScript.

## Prerequisites

Before installing, confirm you have what you need:

| Requirement | Minimum | Check |
|-------------|---------|-------|
| Python | 3.10+ | `python --version` |
| API Key | — | [console.anthropic.com](https://console.anthropic.com/) |

For TypeScript development: Node.js 18+ (`node --version`).

## Installation

```bash
# Python
pip install claude-agent-sdk

# TypeScript/JavaScript
npm install @anthropic-ai/claude-agent-sdk
```

That is all that is needed. The SDK installs the Claude Code CLI as a dependency, so there is nothing else to set up separately.

## Configuring Your API Key

The SDK reads your API key from the environment variable `ANTHROPIC_API_KEY`.

```bash
# Linux/macOS — add to your shell profile for persistence
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

For project-level configuration, use a `.env` file (install `python-dotenv` first):

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

```python
# Load it at the top of your script
from dotenv import load_dotenv
load_dotenv()
```

Never commit your `.env` file. Add it to `.gitignore` immediately.

## Enterprise Authentication

If your organization uses cloud providers instead of direct Anthropic access:

```bash
# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
# (plus standard AWS credentials: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id

# Microsoft Azure (via Azure AI Foundry)
export CLAUDE_CODE_USE_FOUNDRY=1
```

## Your First Agent in Python

Create a file called `hello_agent.py`:

```python
import asyncio
from claude_agent_sdk import query, AssistantMessage, TextBlock, ResultMessage

async def main():
    print("Asking Claude what files are in the current directory...\n")

    # query() is the simplest way to run an agent
    # It returns an async generator that streams messages as they arrive
    async for message in query(
        prompt="List the files in the current directory and describe what each one might be for."
    ):
        # AssistantMessage contains Claude's text responses
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)

        # ResultMessage is always the last message — contains cost and session info
        elif isinstance(message, ResultMessage):
            print(f"\n\nDone! Cost: ${message.total_cost_usd:.4f}, Turns: {message.num_turns}")

asyncio.run(main())
```

Run it:

```bash
python hello_agent.py
```

What happens under the hood: Claude automatically uses the `Glob` or `Bash` tool to list your directory contents, reads what comes back, and then writes its description. You will see the response stream in as Claude generates it.

## Your First Agent in TypeScript

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

    if (message.type === "result") {
      console.log(`\n\nDone! Cost: $${message.total_cost_usd?.toFixed(4)}`);
    }
  }
}

main().catch(console.error);
```

Run it:

```bash
npx tsx hello_agent.ts
```

## Recommended Project Structure

A minimal but well-organized agent project looks like this:

```
my-agent/
├── .env                    # ANTHROPIC_API_KEY (never commit!)
├── .gitignore              # .env, __pycache__, node_modules, etc.
├── requirements.txt        # claude-agent-sdk and dependencies
├── CLAUDE.md               # Agent instructions (read automatically by SDK)
├── agent.py                # Main entry point
├── prompts/                # System prompts as markdown files
│   ├── main_agent.md
│   └── researcher.md
└── output/                 # Where agents write their results
```

## What Is CLAUDE.md?

`CLAUDE.md` is a special file that the SDK automatically reads from your working directory and includes in the agent's context at startup. It is how you give the agent project-specific knowledge without repeating it in every prompt.

Use it to tell the agent about your project:

```markdown
# CLAUDE.md

## Project Commands
- Run tests: `pytest tests/`
- Format code: `black . && isort .`
- Build docs: `mkdocs build`

## Architecture Notes
- Database: PostgreSQL 15 via SQLAlchemy 2.0
- API: FastAPI with Pydantic v2 models
- Auth: JWT tokens, 24h expiry

## Code Style
- Type hints required for all public functions
- Docstrings: Google style
- Max line length: 100 characters

## Important Paths
- Config: `src/config.py`
- Models: `src/models/`
- API routes: `src/api/`
```

The agent uses this to write code that actually fits your project conventions, run the right commands, and avoid stepping on your architecture decisions.

## A Note on the 12-Second Startup Cost

The SDK spawns the Claude Code CLI as a subprocess. This adds roughly 12 seconds of startup overhead on the first call. For interactive tools or long-running batch processes this is acceptable. For high-frequency, low-latency applications (sub-second response requirements), consider a different approach.

When using `ClaudeSDKClient` (covered in Part 3), the subprocess persists across calls within a session, so you only pay the startup cost once per session.

## Quick Reference: 60-Second Setup

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=sk-ant-api03-your-key
python hello_agent.py
```

That is the complete path from zero to running agent. The SDK is now installed, authenticated, and proven to work on your machine.

## What's Next

With your environment set up and a working agent in hand, Part 3 goes deep on the core concepts: the two interaction modes (`query()` vs `ClaudeSDKClient`), how to read the streaming message types, the full built-in tool inventory with permission modes, the hook system for intercepting agent behavior, how subagents work, and custom tools via MCP. This is the mental model that makes everything else click.

Read on: [Part 3 — Architecture and Core Concepts](03-architecture-and-core-concepts.md)
