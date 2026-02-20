"""
02-core-concepts/subagents_demo.py
------------------------------------
Demonstrates the subagent (multi-agent) system.

Shows:
  - Defining specialized subagents with AgentDefinition
  - Giving subagents their own system prompts and tool restrictions
  - Orchestrator delegating to subagents via the Task tool
  - How to structure a multi-agent pipeline

Run:
  python subagents_demo.py
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)


# ─────────────────────────────────────────────
# Demo: Code Review Multi-Agent System
# ─────────────────────────────────────────────
async def demo_code_review_agents():
    print("=== Multi-Agent Code Review System ===")
    print("Orchestrator → security-reviewer + performance-reviewer\n")

    options = ClaudeAgentOptions(
        system_prompt="""You are a code review orchestrator.
When asked to review code:
1. Call the security-reviewer agent to analyze for security issues
2. Call the performance-reviewer agent to analyze for performance issues
3. Combine their findings into a unified review report""",

        # Orchestrator tools: Task (to call subagents) + file reading
        allowed_tools=["Task", "Read", "Glob", "Grep"],
        permission_mode="acceptEdits",

        # Define the specialist subagents
        agents={
            "security-reviewer": AgentDefinition(
                description=(
                    "Expert security auditor. Reviews code for vulnerabilities, "
                    "authentication issues, injection risks, and exposed secrets."
                ),
                prompt="""You are a senior application security engineer.
Analyze code for:
- SQL/command injection vulnerabilities
- Authentication and authorization flaws
- Hardcoded secrets, API keys, or passwords
- Input validation and sanitization gaps
- Insecure dependencies or configurations

For each finding:
- Severity: Critical / High / Medium / Low
- Location: file and line if known
- Description: what the issue is
- Remediation: how to fix it

Return findings as a structured markdown report.""",
                tools=["Read", "Glob", "Grep"],  # Read-only: safe!
            ),

            "performance-reviewer": AgentDefinition(
                description=(
                    "Performance optimization expert. Reviews code for bottlenecks, "
                    "inefficient patterns, and scaling issues."
                ),
                prompt="""You are a senior performance engineer.
Analyze code for:
- N+1 database queries
- Missing indexes or inefficient queries
- Unnecessary loops, redundant computations
- Memory leaks and excessive allocations
- Missing caching opportunities
- Blocking I/O in async contexts

For each finding:
- Impact: High / Medium / Low
- Location: file and line if known
- Description: the performance issue
- Optimization: specific improvement to make

Return findings as a structured markdown report.""",
                tools=["Read", "Glob", "Grep"],
            ),
        },
    )

    # Track which subagents were called
    subagent_calls = []

    # Stream the response, watching for Task tool calls
    print("Starting review pipeline...\n")
    async for message in query(
        prompt="Review the Python files in this directory for security and performance issues.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    if block.name == "Task":
                        agent_name = block.input.get("subagent_type", "unknown")
                        subagent_calls.append(agent_name)
                        print(f"\n  [Orchestrator spawning subagent: {agent_name}]")

        elif isinstance(message, ResultMessage):
            print(f"\n\n{'=' * 60}")
            print(f"Code review complete!")
            print(f"  Subagents called: {subagent_calls}")
            print(f"  Total cost: ${message.total_cost_usd:.4f}")
            print(f"  Turns taken: {message.num_turns}")


# ─────────────────────────────────────────────
# Demo 2: Research decomposition agents
# ─────────────────────────────────────────────
async def demo_research_agents():
    print("\n\n=== Multi-Agent Research System ===")
    print("Orchestrator → web-researcher + docs-researcher\n")

    options = ClaudeAgentOptions(
        system_prompt="""You are a research orchestrator.
For research questions:
1. Use web-researcher to find community content and articles
2. Use docs-researcher to find official documentation
3. Synthesize both into a comprehensive answer""",

        allowed_tools=["Task", "Write"],
        permission_mode="acceptEdits",

        agents={
            "web-researcher": AgentDefinition(
                description="Searches the web for articles, tutorials, and community discussions.",
                prompt="""Search the web for relevant articles, tutorials, and community content.
Use WebSearch to find recent, high-quality sources.
Use WebFetch to extract detailed information from the best results.
Return a summary with key insights and source URLs.""",
                tools=["WebSearch", "WebFetch"],
            ),

            "docs-researcher": AgentDefinition(
                description="Finds and extracts information from official documentation.",
                prompt="""Search for official documentation on the topic.
Focus on: official docs, API references, and authoritative guides.
Use WebSearch to find official sources, WebFetch to extract details.
Return precise technical information with source URLs.""",
                tools=["WebSearch", "WebFetch"],
            ),
        },
    )

    async for message in query(
        prompt="Research: What are the best practices for error handling in async Python code?",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\nCost: ${message.total_cost_usd:.4f}")


async def main():
    await demo_code_review_agents()
    # Uncomment to run the research demo too:
    # await demo_research_agents()


asyncio.run(main())
