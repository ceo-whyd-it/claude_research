# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

L7 Agent — a multi-agent research orchestration system built on the Claude Agent SDK (`claude-agent-sdk`). A main orchestrator agent (Sonnet) delegates research tasks to three specialized subagents (Haiku): `docs_researcher`, `repo_analyzer`, and `web_researcher`. All file-based output is written to the `research_output/` directory.

## Commands

```bash
# Install dependencies
uv sync

# Run the agent
uv run python agent.py
```

There are no test or lint commands configured.

## Architecture

**Entry point:** `agent.py` — sets up the `ClaudeSDKClient` with agent definitions and an interactive input loop. Streams `AssistantMessage` responses and formats them via `utils.py`.

**Agent hierarchy:**
- **Main orchestrator** (`agent.py`, prompt: `prompts/main_agent.md`) — Sonnet model. Receives user input, matches skills, delegates to subagents in parallel, synthesizes results.
- **docs_researcher** (prompt: `prompts/docs_researcher.md`) — Haiku. Tools: `WebSearch`, `WebFetch`. Extracts info from official docs.
- **repo_analyzer** (prompt: `prompts/repo_analyzer.md`) — Haiku. Tools: `WebSearch`, `Bash`. Clones and analyzes repositories.
- **web_researcher** (prompt: `prompts/web_researcher.md`) — Haiku. Tools: `WebSearch`, `WebFetch`. Finds articles, videos, community content.

**Prompt system:** All agent system prompts live in `prompts/` as markdown files, loaded at startup by `load_prompt()`. Edit these to change agent behavior.

**Skill system:** Skills in `.claude/skills/` define structured workflows (e.g., `learning-a-tool`, `learning-a-concept`, `learning-a-framework`, `research-arxiv`, `research-general`, `research-compare`, `research-paper`). The orchestrator follows skill instructions when a skill matches the user's request.

**Display:** `utils.py` tracks subagent identities via `parent_tool_use_id` and color-codes output — blue for main agent, magenta for subagents.

## Environment Variables

Set in `.env` at project root:
- `ANTHROPIC_API_KEY` — required

## Requirements

- Python >= 3.13
- UV package manager
