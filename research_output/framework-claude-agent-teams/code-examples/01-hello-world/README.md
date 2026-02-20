# Example 1: Hello World - Your First Agent Team

This example demonstrates the simplest possible agent team setup.

## What This Example Shows

- How to enable agent teams
- Creating a basic team with natural language
- Understanding team output
- Basic team cleanup

## Files

- `setup_instructions.md` — Step-by-step setup
- `example_prompt.txt` — The prompt to create your first team
- `expected_output.txt` — What you should see

## Run This Example

```bash
# 1. Enable agent teams
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. Start Claude Code
claude

# 3. Paste the content from example_prompt.txt
```

## What Happens

1. Claude Code spawns 2 teammates
2. Each teammate performs their assigned task
3. Teammates report results back to lead
4. Lead synthesizes and presents findings
5. Team cleans up automatically

## Expected Duration

~ 2-3 minutes
