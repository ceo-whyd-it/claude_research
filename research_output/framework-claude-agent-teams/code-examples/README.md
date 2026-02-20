# Code Examples for Claude Agent Teams

Hands-on examples demonstrating agent teams concepts from basic to advanced.

## Examples Overview

| Example | Difficulty | Time | Key Concepts |
|---------|-----------|------|--------------|
| **01-hello-world** | Beginner | 5 min | Team creation, basic coordination |
| **02-core-concepts** | Intermediate | 15 min | Agent definitions, specialized agents, SDK usage |
| **03-real-app** | Advanced | 30 min | Cross-layer development, dependencies, plan approval |

## Prerequisites

- Claude Code installed and configured
- Agent teams enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- Python 3.10+ (for SDK examples)
- Basic understanding of async programming (for SDK examples)

## Quick Start

### Example 1: Hello World

Perfect for first-time users. No code required - just natural language prompts.

```bash
cd 01-hello-world
# Follow README.md instructions
```

**What you'll learn:**
- How to create your first agent team
- Understanding team output
- Basic team coordination

### Example 2: Core Concepts

Learn to programmatically define agents using the Claude Agent SDK.

```bash
cd 02-core-concepts
pip install -r requirements.txt
python agent_definitions.py
```

**What you'll learn:**
- Defining agents with specialized expertise
- Assigning tools to agents
- Creating custom system prompts
- Parallel code review patterns

### Example 3: Real Application

Build a complete feature across multiple layers with agent teams.

```bash
cd 03-real-app
# Follow README.md for full setup
```

**What you'll learn:**
- Task decomposition for parallel work
- Managing dependencies between teammates
- Plan approval workflow
- Cross-layer feature development

## Learning Path

**Suggested order:**

1. Start with **01-hello-world** to understand the basics
2. Move to **02-core-concepts** to learn SDK usage
3. Build a real feature with **03-real-app**

## Example Patterns

Each example demonstrates specific patterns:

### Pattern 1: Parallel Specialization (Example 2)
Multiple experts reviewing the same code from different angles.

**Use when:**
- Code review
- Security audit
- Multi-perspective analysis

### Pattern 2: Sequential Dependencies (Example 3)
Teammates working on different layers with clear dependencies.

**Use when:**
- Full-stack feature development
- Pipeline workflows
- Multi-stage processing

### Pattern 3: Debate Structure (Conceptual)
Agents challenge each other's theories.

**Use when:**
- Debugging with competing hypotheses
- Architectural decisions
- Design exploration

## Common Modifications

### Change Model Mix

```python
agents = {
    "architect": AgentDefinition(
        model="opus",  # Higher capability for complex design
        # ...
    ),
    "implementer": AgentDefinition(
        model="sonnet",  # Cost-effective for implementation
        # ...
    ),
}
```

### Add More Agents

```python
agents = {
    # Existing agents...
    "documentation-writer": AgentDefinition(
        description="Writes comprehensive documentation",
        prompt="You are a technical writer...",
        tools=["Read", "Write"],
    ),
}
```

### Customize Tools

```python
AgentDefinition(
    # Read-only reviewer
    tools=["Read", "Grep"],

    # Can run tests
    tools=["Read", "Grep", "Bash"],

    # Can modify code
    tools=["Read", "Write", "Edit", "Bash"],
)
```

## Troubleshooting

### "Agent teams not enabled"
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### "Permission denied" errors
Pre-approve common operations before spawning team.

### Teammates don't coordinate
Use explicit task dependencies in spawn prompt.

### File conflicts
Assign distinct file ownership to each teammate.

## Next Steps

After completing these examples:

1. Review the main [learning-path.md](../learning-path.md) for deeper concepts
2. Check [resources.md](../resources.md) for community projects
3. Join the [Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ)
4. Build your own agent team for your specific use case!

## Feedback

These examples are designed to teach progressively. If you get stuck or have suggestions for improvement, please share in the Discord community.

---

**Happy team building!** 🎯
