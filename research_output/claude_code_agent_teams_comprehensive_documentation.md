# Claude Code Agent Teams - Comprehensive Documentation Research

## Official Documentation URL

**Primary Source:** https://code.claude.com/docs/en/agent-teams

**Current Version:** Claude Code (latest as of February 2026)

**Status:** Experimental feature - Disabled by default

---

## Executive Summary

Agent Teams is an experimental feature in Claude Code that enables coordinating multiple Claude Code instances working together as a unified team. Unlike subagents, agent teams allow each teammate to have its own context window, run independently, and communicate directly with each other through a shared task list.

The team consists of a team lead (main orchestrator session) that coordinates work and spawns teammates (separate Claude instances) that work on assigned tasks in parallel.

---

## Motivation & Problem Solved

Agent teams solve the problem of coordinating complex, parallel work that benefits from real-time inter-agent communication and collaboration.

**Problems Addressed:**
- Sequential bottlenecks when work requires sustained parallelism
- Collaboration overhead (subagents cannot discuss findings with each other)
- Context window limits on large exploratory tasks
- Coordination complexity for teams with interdependent features

**What It Helps With:**
- Research and code review with multiple perspectives
- Debugging with competing hypotheses and debate
- Cross-layer feature development (frontend, backend, tests)
- Parallel exploration with self-coordination
- Complex feature development with independent work streams

---

## Agent Teams vs. Subagents Comparison

| Dimension | Subagents | Agent Teams |
|-----------|-----------|------------|
| Context | Own window; results return to caller | Own window; fully independent |
| Communication | Report to main agent only | Direct inter-teammate messaging |
| Coordination | Main agent manages work | Shared task list with self-coordination |
| Token Cost | Lower | ~7x higher (each teammate is separate instance) |
| Best For | Focused tasks, quick research | Complex work requiring discussion |
| Nesting | Can nest subagents | No nested teams allowed |

---

## Installation & Prerequisites

### System Requirements
- macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+
- 4 GB+ RAM, Internet connection required
- Bash or Zsh shell recommended

### Installation

Native (Recommended):
\
Homebrew:
\
---

## Quick Start

### Enable Agent Teams

Agent teams are disabled by default. Enable via:

\
Or in settings.json:
\
### Create a Team

\
---

## Core Architecture

### Team Structure
- Team Lead Session (orchestrator, spawns teammates, manages tasks)
- Teammate Sessions (independent Claude Code instances)
- Shared Task List (coordination with dependencies)
- Mailbox/Messaging (direct agent communication)
- Team Config (~/.claude/teams/{team-name}/config.json)

### Key Features
- Automatic message delivery between teammates
- Task dependencies auto-resolve
- File locking prevents race conditions
- Lead stays in control (approves team creation)

---

## Core Concepts

### 1. Shared Task List with Self-Coordination
Teammates see shared task list, claim pending work, auto-resolve dependencies. Prevents lead from bottleneck.

### 2. Independent Context Windows
Each teammate has separate Claude instance. Communicate directly, not through lead.

### 3. Debate & Collaboration Structure
Work requires discussion. Debate prevents cognitive anchoring - investigators disprove each other.

### 4. Automatic Dependency Management
Dependencies resolve automatically when tasks complete without manual intervention.

### 5. Plan Approval & Risk Mitigation
For risky work, require plan approval. Teammates work read-only, create plans, lead approves/rejects.

---

## Official Examples

### Code Review
\
### Debugging
\
### Feature Development
\
---

## Known Limitations

1. No session resumption with in-process teammates
2. Task status can lag
3. Shutdown can be slow
4. One team per session
5. No nested teams
6. Lead is fixed (cannot be promoted)
7. Permissions set at spawn
8. Split panes require tmux/iTerm2
9. Orphaned tmux sessions possible

### Token Usage
Agent teams use ~7x more tokens than single sessions. Each teammate = separate Claude instance.

---

## Best Practices

1. Give teammates adequate context with task-specific spawn prompts
2. Right-size tasks (5-6 per teammate)
3. Prevent file conflicts (each teammate owns different files)
4. Monitor and steer teams
5. Start simple (review, research, debugging)
6. Wait for teammates (don't let lead implement instead)
7. Use plan approval for risky work
8. Keep spawn prompts focused

---

## Summary

**Agent Teams Enable:**
- Multiple Claude Code instances working together
- Direct communication between teammates
- Shared task lists with dependency resolution
- Parallel work on complex problems

**Best For:**
- Research with multiple perspectives
- Competing hypothesis investigations
- Cross-layer feature development
- Complex reviews requiring diverse expertise

**To Start:**
1. Enable: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
2. Create: Create a team to [task description]
3. Claude handles rest with natural language

---

**Research Date:** February 20, 2026
**Source:** https://code.claude.com/docs/en/agent-teams
**Status:** Complete extraction of official documentation
