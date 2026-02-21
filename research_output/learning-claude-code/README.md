# Learning Claude Code

A comprehensive, progressive learning path for mastering Claude Code — Anthropic's AI-powered pair programming tool.

## What is Claude Code?

Claude Code is an **agentic coding assistant** that reads your codebase, edits files, runs commands, and integrates with your development tools. It enables developers to pair-program with Claude through natural language, shifting from traditional request-response interactions to real-time collaborative development.

Think of it as "a very fast intern with perfect memory" that can:
- Navigate and understand entire codebases
- Implement features across multiple files
- Write and run tests autonomously
- Debug from error messages and stack traces
- Automate Git workflows (commits, branches, PRs)
- Integrate with CI/CD pipelines

## Essential References

| Resource | Link | Why |
|----------|------|-----|
| **Official Docs** | [code.claude.com/docs](https://code.claude.com/docs/en/overview) | Comprehensive reference, always up-to-date |
| **Repository** | [GitHub (68.1k⭐)](https://github.com/anthropics/claude-code) | Source code, examples, official plugins |
| **Engineering Deep Dive** | [Building a C Compiler](https://www.anthropic.com/engineering/building-c-compiler) | Real-world case study demonstrating capabilities |
| **Best Tutorial** | [Builder.io Guide](https://www.builder.io/blog/claude-code) | Practical tips from experienced users |
| **Best Video** | [Official Video Tutorials](https://support.claude.com/en/collections/10548294-video-tutorials) | 26+ videos covering all features |
| **Community** | [Discord (61k+ members)](https://discord.com/invite/6PPFFzqPDZ) | Active support and discussions |
| **Tips Repository** | [claude-code-tips (GitHub)](https://github.com/ykdojo/claude-code-tips) | 45 tips from basics to advanced |
| **Best Practices** | [ClaudeLog Hub](https://claudelog.com/) | Central documentation and guides hub |

## How to Use This Learning Path

This guide follows a progressive 5-level structure:

1. **Level 1: Overview & Motivation** — Understand what Claude Code is and why it matters
2. **Level 2: Installation & Hello World** — Get up and running in minutes
3. **Level 3: Core Concepts** — Master the fundamental mental models
4. **Level 4: Practical Patterns** — Build real workflows and solve actual problems
5. **Level 5: Next Steps** — Advanced topics and where to go deeper

### Recommended Approach

- **Complete Beginners**: Start at Level 1, work through sequentially
- **Experienced Developers**: Skim Level 1, start at Level 2
- **Current Users**: Jump to Level 4 for patterns, Level 5 for advanced topics
- **Long Session Users**: Focus on context management in Levels 3-4

### Code Examples

All code examples are in `code-examples/` with subdirectories for each level. Each example includes:
- Complete, runnable code
- Expected output
- Common mistakes and fixes
- Progressive complexity

## Repository Structure

```
learning-claude-code/
├── README.md              # This file - overview and getting started
├── resources.md           # All links organized by source
├── learning-path.md       # Main content - the 5 levels
└── code-examples/         # Runnable examples
    ├── 01-hello-world/
    ├── 02-core-concepts/
    └── 03-patterns/
```

## Who This Is For

- **New Users**: Never used Claude Code before
- **Current Users**: Want to use it more effectively
- **Long Session Users**: Struggling with context management
- **Team Leads**: Evaluating Claude Code for teams
- **Production Users**: Need security and best practices

## Key Insight from Community

> "The single highest-leverage thing you can do: Give Claude something to verify against (tests, screenshots, expected outputs). Claude performs dramatically better with clear success criteria."

Start your learning journey in **learning-path.md** →

---

**Last Updated**: February 2026
**Claude Code Version**: 2.1.50+
**Sources**: Official docs, GitHub repository, community experiences from 30+ articles and 100+ real-world use cases
