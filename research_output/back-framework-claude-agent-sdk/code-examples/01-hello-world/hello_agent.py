"""
01-hello-world/hello_agent.py
------------------------------
Your first Claude Agent SDK program.

This demonstrates the minimal working agent:
- Import the SDK
- Call query() with a prompt
- Iterate the streaming response
- Print Claude's text responses

Prerequisites:
  pip install claude-agent-sdk
  export ANTHROPIC_API_KEY=sk-ant-api...

Run:
  python hello_agent.py
"""

import asyncio
from claude_agent_sdk import (
    query,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)


async def main():
    print("Hello Agent SDK!")
    print("=" * 50)
    print("Prompt: What is the Claude Agent SDK and what can it do?\n")

    # query() returns an async generator of messages
    # It streams results as they arrive
    async for message in query(
        prompt="What is the Claude Agent SDK and what can it do? Give a 3-sentence summary."
    ):
        # AssistantMessage = Claude's text response
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    # Print each text block as it arrives (streaming)
                    print(block.text, end="", flush=True)

        # ResultMessage = final summary (always arrives last)
        elif isinstance(message, ResultMessage):
            print(f"\n\n{'=' * 50}")
            print(f"Session complete!")
            print(f"  Cost:   ${message.total_cost_usd:.4f}")
            print(f"  Turns:  {message.num_turns}")
            print(f"  Model:  {message.usage}")


# Run the async main function
asyncio.run(main())


"""
Expected output:
================
Hello Agent SDK!
==================================================
Prompt: What is the Claude Agent SDK and what can it do?

The Claude Agent SDK is Anthropic's framework for building autonomous AI agents
that can take actions in the real world...

==================================================
Session complete!
  Cost:   $0.0023
  Turns:  1
  Model:  ...
"""
