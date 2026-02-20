# Claude Agent SDK — Learning Path

> A comprehensive, progressive learning guide for Anthropic's **Claude Agent SDK** (`claude-agent-sdk`).
> Built from official documentation, repository analysis, and community research.

---

## What Is This?

This learning path takes you from zero to production with the Claude Agent SDK — Anthropic's framework for building autonomous AI agents that can read files, run commands, search the web, and delegate work to specialized subagents.

## How to Use This Learning Path

Work through the five levels in order. Each level builds on the previous.

| Level | Focus | Time Estimate |
|-------|-------|--------------|
| Level 1: Overview & Motivation | Understand what the SDK is and why it exists | 20 min |
| Level 2: Setup & First Project | Install and run your first agent | 30 min |
| Level 3: Architecture & Core Concepts | Master the mental model | 45 min |
| Level 4: Building Real Applications | Build production-grade agents | 2-4 hrs |
| Level 5: Next Steps | Ecosystem, community, and advanced topics | Ongoing |

## Files in This Package

```
framework-claude-agent-sdk/
├── README.md              ← You are here
├── learning-path.md       ← Main content (all 5 levels)
├── resources.md           ← All links organized by source
└── code-examples/
    ├── 01-hello-world/    ← Minimal agent, streaming messages
    ├── 02-core-concepts/  ← Tools, subagents, hooks, sessions, MCP
    └── 03-real-app/       ← Multi-agent research orchestrator
```

## Prerequisites

- Python 3.10+ or Node.js 18+
- An Anthropic API key from platform.claude.com
- Basic async Python knowledge (helpful but not required)

## Quick Start (60 seconds)

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=your-key-here
python code-examples/01-hello-world/hello_agent.py
```

---

*Research gathered February 2026 · SDK version v0.1.38 (Python) / v0.2.47 (TypeScript)*
