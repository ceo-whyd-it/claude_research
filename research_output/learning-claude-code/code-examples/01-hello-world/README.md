# Hello World Examples

First interactions with Claude Code.

## Example 1: Your First Claude Code Session

```bash
# Start Claude Code
claude

# Ask about the current directory
You: what files are in this directory?

# Create a simple file
You: create a hello.py file that prints "Hello from Claude Code!"

# Run the file
You: run the python file

# Expected output:
# Hello from Claude Code!
```

## Example 2: Simple Bug Fix

```bash
# Start with broken code
echo 'def greet(name):
    print("Hello, " + name + "!")

greet()  # Missing argument!' > buggy.py

# Start Claude
claude

# Ask Claude to fix it
You: fix the bug in buggy.py - it's missing an argument

# Claude will:
# 1. Read buggy.py
# 2. Identify the issue (missing name parameter)
# 3. Ask how you want it fixed
# 4. Update the code
```

## Example 3: Understanding Existing Code

```bash
claude

# Paste this code and ask Claude to explain it
You: Explain what this Python code does:

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Claude will:
# - Identify it as a recursive Fibonacci implementation
# - Explain how it works
# - Point out performance issues (exponential time)
# - Suggest optimizations (memoization)
```

## Common Commands for Beginners

| Command | What It Does |
|---------|-------------|
| `claude` | Start new session |
| `claude -c` | Continue last session |
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `Ctrl+C` | Exit Claude Code |
| `Esc` | Stop current action |
| `Shift+Tab` | Change permission mode |

## Tips

- Start simple: Ask Claude to explain files before changing them
- Be specific: "create a Python script that..." vs "make a script"
- Let Claude run commands: Say "run the tests" not just "write tests"
- Press Esc to stop: You can interrupt Claude anytime
