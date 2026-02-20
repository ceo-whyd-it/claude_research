"""
Example 2: Agent Definitions with Claude Agent SDK

This example shows how to programmatically define agents
using the Python SDK.
"""

import asyncio
from claude_agent_sdk import (
    query,
    AgentDefinition,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
)


async def main():
    """Create a code review team with specialized agents."""

    # Define specialized agents
    agents = {
        "security-reviewer": AgentDefinition(
            description="Reviews code for security vulnerabilities",
            prompt="""You are a security expert. Review code for:
            - SQL injection vulnerabilities
            - XSS vulnerabilities
            - Authentication/authorization issues
            - Sensitive data exposure
            - Input validation problems

            Provide specific line numbers and fix suggestions.""",
            tools=["Read", "Grep"],
            model="sonnet",
        ),

        "performance-reviewer": AgentDefinition(
            description="Reviews code for performance issues",
            prompt="""You are a performance optimization expert. Review code for:
            - Inefficient algorithms
            - Resource leaks
            - Unnecessary database queries
            - Missing indexes
            - Caching opportunities

            Provide specific optimization suggestions.""",
            tools=["Read", "Grep"],
            model="sonnet",
        ),

        "test-coverage-reviewer": AgentDefinition(
            description="Reviews code for testing gaps",
            prompt="""You are a testing expert. Review code for:
            - Missing test coverage
            - Untested edge cases
            - Missing error handling tests
            - Integration test gaps
            - Test quality issues

            Suggest specific tests to add.""",
            tools=["Read", "Grep", "Bash"],
            model="sonnet",
        ),
    }

    options = ClaudeAgentOptions(
        agents=agents,
        max_turns=10,
    )

    # Create the team
    prompt = """Create a code review team with our three specialized reviewers.

    Have them review the file 'app.py' in parallel, each focusing on their specialty.
    After all reviews complete, synthesize their findings into a prioritized action list.
    """

    print("🎯 Starting code review team...\n")

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"{block.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
