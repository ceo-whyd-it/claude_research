"""
03-real-app/research_agent.py
--------------------------------
A complete multi-agent research system.

This is a production-grade example demonstrating:
  - Multi-agent orchestration (3 specialist subagents)
  - Safety hooks (restrict write locations, log all actions)
  - Budget and turn limits
  - Custom in-process MCP tools (knowledge base lookup)
  - Proper error handling
  - Cost and session tracking

Usage:
  python research_agent.py "What are the key features of the Claude Agent SDK?"
  python research_agent.py  (uses default question)

Output:
  Prints to stdout + saves report to output/research_report.md

Prerequisites:
  pip install claude-agent-sdk
  export ANTHROPIC_API_KEY=sk-ant-api...
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
    tool,
    create_sdk_mcp_server,
)


# ═══════════════════════════════════════════
# Custom MCP Tools (Internal Knowledge Base)
# ═══════════════════════════════════════════

# Simulated internal knowledge base
INTERNAL_KB = {
    "claude agent sdk": "Internal adoption: 3 teams using it in production since Q4 2025. Primary use cases: CI/CD automation, code review pipelines.",
    "langchain": "Used by data team for RAG pipelines. Not used for agentic workflows.",
    "openai": "Legacy integrations only. New projects use Claude exclusively.",
}


@tool(
    "search_knowledge_base",
    "Search the internal company knowledge base for proprietary information",
    {"query": str},
)
async def search_knowledge_base(args: dict[str, Any]) -> dict:
    query_lower = args["query"].lower()
    results = []

    for key, value in INTERNAL_KB.items():
        if any(word in key for word in query_lower.split()):
            results.append(f"**{key}**: {value}")

    if results:
        return {"content": [{"type": "text", "text": "\n".join(results)}]}
    return {
        "content": [
            {
                "type": "text",
                "text": f"No internal knowledge base entries found for '{args['query']}'.",
            }
        ]
    }


# Bundle into MCP server
internal_tools_server = create_sdk_mcp_server(
    name="internal",
    version="1.0.0",
    tools=[search_knowledge_base],
)


# ═══════════════════════════════════════════
# Safety Hooks
# ═══════════════════════════════════════════

audit_log: list[dict] = []


async def audit_all_tools(input_data: dict, tool_use_id: str, context) -> dict:
    """Logs every tool call for audit purposes."""
    entry = {
        "timestamp": time.time(),
        "tool": input_data.get("tool_name", "unknown"),
        "input_preview": str(input_data.get("tool_input", {}))[:80],
    }
    audit_log.append(entry)
    return {}


async def restrict_write_to_output(input_data: dict, tool_use_id: str, context) -> dict:
    """Only allow writing to the output/ directory."""
    tool_name = input_data.get("tool_name", "")
    if tool_name == "Write":
        file_path = input_data.get("tool_input", {}).get("file_path", "")
        if file_path and not file_path.startswith("output/"):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Security policy: files must be written to output/ only. "
                        f"Attempted path: {file_path}"
                    ),
                }
            }
    return {}


async def log_subagent_calls(input_data: dict, tool_use_id: str, context) -> dict:
    """Logs when the orchestrator spawns subagents."""
    if input_data.get("tool_name") == "Task":
        agent = input_data.get("tool_input", {}).get("subagent_type", "unknown")
        print(f"  [Orchestrator → {agent}]", flush=True)
    return {}


# ═══════════════════════════════════════════
# Subagent Definitions
# ═══════════════════════════════════════════

SUBAGENTS = {
    "technical-researcher": AgentDefinition(
        description=(
            "Expert technical researcher. Finds implementation details, "
            "API documentation, architecture information, and code examples."
        ),
        prompt="""You are a senior technical researcher.
For the given research question, find:
1. Official documentation and API references
2. Architecture and implementation details
3. Code examples and best practices
4. Known limitations and gotchas

Use WebSearch to find authoritative sources.
Use WebFetch to extract detailed technical information.

Return your findings as structured markdown with:
- Key technical facts
- Code examples (if relevant)
- Source URLs
- Confidence level for each finding""",
        tools=["WebSearch", "WebFetch"],
    ),

    "usecase-researcher": AgentDefinition(
        description=(
            "Use case and adoption researcher. Finds real-world applications, "
            "success stories, and industry adoption patterns."
        ),
        prompt="""You are a technology adoption researcher.
For the given topic, find:
1. Real-world use cases and production deployments
2. Companies and teams using this technology
3. Success metrics and testimonials
4. Common industry patterns

Use WebSearch and WebFetch to find community content, blog posts, and case studies.

Return your findings as structured markdown with:
- Notable use cases and examples
- Adoption patterns
- Source URLs""",
        tools=["WebSearch", "WebFetch"],
    ),

    "comparison-researcher": AgentDefinition(
        description=(
            "Competitive analysis researcher. Compares alternatives, "
            "identifies tradeoffs, and maps the ecosystem."
        ),
        prompt="""You are a technology analyst.
For the given topic, find:
1. Key alternatives and competitors
2. Comparison articles and benchmarks
3. When to use this vs. alternatives
4. Community sentiment and critiques

Use WebSearch and WebFetch to find comparison articles and reviews.

Return your findings as structured markdown with:
- Alternatives overview table
- Key differentiators
- When to use each option
- Source URLs""",
        tools=["WebSearch", "WebFetch"],
    ),
}


# ═══════════════════════════════════════════
# Main Research Agent
# ═══════════════════════════════════════════

async def run_research(question: str) -> None:
    """
    Runs the multi-agent research pipeline.

    Args:
        question: The research question to investigate
    """
    print(f"\nResearch Question: {question}")
    print("=" * 70)
    print("Starting multi-agent research pipeline...\n")

    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)

    # Build options
    options = ClaudeAgentOptions(
        system_prompt="""You are a research orchestrator. Your job is to:
1. Decompose the research question into 2-3 focused subtopics
2. Delegate each subtopic to the appropriate specialist subagent using Task
3. Also check the internal knowledge base using mcp__internal__search_knowledge_base
4. Wait for all subagents to complete
5. Synthesize all findings into a comprehensive markdown report
6. Save the final report to output/research_report.md

Structure the final report with:
- Executive Summary (2-3 sentences)
- Technical Overview
- Real-World Use Cases
- Alternatives & Ecosystem
- Internal Notes (from knowledge base)
- Key Takeaways
- Sources""",

        # Tools available to the orchestrator
        allowed_tools=[
            "Task",                              # Spawn subagents
            "Write",                             # Save the final report
            "mcp__internal__search_knowledge_base",  # Internal KB lookup
        ],

        permission_mode="acceptEdits",

        # Custom MCP tools (internal knowledge base)
        mcp_servers={"internal": internal_tools_server},

        # Specialist subagents
        agents=SUBAGENTS,

        # Safety limits
        max_turns=30,           # Stop after 30 turns
        max_budget_usd=2.00,    # Hard limit: $2 per session

        # Safety hooks
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="*", hooks=[audit_all_tools]),
                HookMatcher(matcher="Write", hooks=[restrict_write_to_output]),
                HookMatcher(matcher="Task", hooks=[log_subagent_calls]),
            ],
        },
    )

    # Track metrics
    start_time = time.time()
    subagents_used: list[str] = []

    # Run the agent
    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    if block.name == "Task":
                        agent = block.input.get("subagent_type", "?")
                        if agent not in subagents_used:
                            subagents_used.append(agent)

        elif isinstance(message, ResultMessage):
            elapsed = time.time() - start_time

            print(f"\n\n{'=' * 70}")
            print(f"Research Pipeline Complete!")
            print(f"  Time elapsed:      {elapsed:.1f}s")
            print(f"  Total cost:        ${message.total_cost_usd:.4f}")
            print(f"  Turns taken:       {message.num_turns}")
            print(f"  Subagents used:    {subagents_used}")
            print(f"  Tool calls logged: {len(audit_log)}")
            print(f"  Session ID:        {message.session_id}")
            print(f"\n  Report saved to: output/research_report.md")

            # Print audit summary
            if audit_log:
                print(f"\n  Audit log summary:")
                tool_counts: dict[str, int] = {}
                for entry in audit_log:
                    tool_counts[entry["tool"]] = tool_counts.get(entry["tool"], 0) + 1
                for t, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
                    print(f"    {t}: {count} call(s)")


# ═══════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════

def main():
    # Get question from command line or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = (
            "What is the Claude Agent SDK? Cover: technical architecture, "
            "real-world use cases, and how it compares to LangChain."
        )

    asyncio.run(run_research(question))


if __name__ == "__main__":
    main()
