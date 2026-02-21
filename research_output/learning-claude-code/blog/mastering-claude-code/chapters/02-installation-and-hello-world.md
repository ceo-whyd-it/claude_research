---
title: "Installation & Hello World: Get Started in Minutes"
description: "Install Claude Code and run your first session. Learn the basics of how it works through hands-on examples."
date: 2026-02-21
part: 2
series: "Mastering Claude Code"
series_order: 2
prev: "01-overview-and-motivation.md"
next: "03-core-concepts.md"
tags: ["claude-code", "installation", "tutorial", "hello-world"]
---

# Part 2: Installation & Hello World

### Prerequisites

**System Requirements**:
- **OS**: macOS 13+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+
- **RAM**: 4 GB minimum
- **Network**: Internet connection required
- **Shell**: Bash or Zsh recommended

**Account Requirements** (one of):
- Claude Pro/Max subscription (recommended - unified access)
- Anthropic Console account with billing
- Claude for Teams/Enterprise
- Cloud provider access (Bedrock, Vertex AI, Azure)

### Installation Steps

**macOS/Linux/WSL**:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Alternative: Package Managers**

macOS (Homebrew):
```bash
brew install --cask claude-code
```

Windows (WinGet):
```powershell
winget install Anthropic.ClaudeCode
```

### Verification

Check installation:
```bash
claude --version
# Expected: claude-code version 2.1.50 (or newer)

claude doctor
# Expected: ✓ All checks passed
```

### Hello World: Your First Session

**Step 1**: Create a test project
```bash
mkdir claude-test
cd claude-test
```

**Step 2**: Start Claude Code
```bash
claude
```

You'll see:
```
Welcome to Claude Code!
Logging you in...
✓ Logged in as your-email@example.com

Type your message or press Ctrl+C to exit.
```

**Step 3**: Ask your first question
```
You: what files are in this directory?
```

Claude will:
1. Run `ls` command
2. Report findings
3. Wait for next instruction

**Step 4**: Create your first file
```
You: create a hello.py file that prints "Hello from Claude Code!"
```

Claude will:
1. Ask permission to create file (if in default mode)
2. Write the file
3. Show you what it created

**Step 5**: Run and verify
```
You: run the python file and show me the output
```

Claude will:
1. Execute `python hello.py`
2. Display output: `Hello from Claude Code!`
3. Confirm success

**Step 6**: Exit
Press `Ctrl+C` or type `exit`

### Understanding What Just Happened

1. **Context Gathering**: Claude used `ls` to understand your directory
2. **File Creation**: Claude wrote `hello.py` using the Write tool
3. **Execution**: Claude ran bash commands to execute your script
4. **Verification**: Claude showed you the results

This is the **agentic loop** in action: Gather context → Take action → Verify results.

### Common First-Session Issues

| Problem | Solution |
|---------|----------|
| `claude: command not found` | Restart terminal or add to PATH manually |
| "Not logged in" error | Run `claude login` and authenticate |
| Permission denied on file creation | Check directory write permissions |
| Slow startup | First run downloads models; subsequent runs are faster |
| Can't exit | Press `Ctrl+C` twice, or type `exit` |

---

---

**Next**: [Part 3: Core Concepts →](03-core-concepts.md)

**Series Navigation**:
- [← Part 1: Overview & Motivation](01-overview-and-motivation.md)
- **Part 2: Installation & Hello World** (You are here)
- [Part 3: Core Concepts →](03-core-concepts.md)

---

*Part of the "Mastering Claude Code" series*
