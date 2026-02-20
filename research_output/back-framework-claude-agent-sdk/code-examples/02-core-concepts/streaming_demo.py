"""
02-core-concepts/streaming_demo.py
------------------------------------
Demonstrates all message types in the streaming response.

Shows:
  - All four message types: UserMessage, SystemMessage, AssistantMessage, ResultMessage
  - Content block types: TextBlock, ToolUseBlock, ThinkingBlock
  - How to distinguish messages
  - The difference between query() (stateless) and ClaudeSDKClient (stateful)

Run:
  python streaming_demo.py
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    # Message types
    AssistantMessage,
    UserMessage,
    SystemMessage,
    ResultMessage,
    # Content block types
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)


# ─────────────────────────────────────────────
# Demo 1: Inspect every message type
# ─────────────────────────────────────────────
async def demo_all_message_types():
    print("\n=== Demo 1: All Message Types ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant. Keep answers brief.",
        allowed_tools=["Bash"],  # Give Claude a tool to use so we see ToolUseBlock
    )

    async for message in query(
        prompt="Run `echo 'hello from bash'` and tell me what it printed.",
        options=options,
    ):
        # Each message type appears in order:
        # SystemMessage → UserMessage → AssistantMessage (possibly multiple) → ResultMessage

        if isinstance(message, SystemMessage):
            print(f"[SystemMessage] content: {message.content[:50]}...")

        elif isinstance(message, UserMessage):
            print(f"[UserMessage] content preview: {str(message.content)[:80]}...")

        elif isinstance(message, AssistantMessage):
            print(f"[AssistantMessage] {len(message.content)} content block(s):")
            for i, block in enumerate(message.content):
                if isinstance(block, TextBlock):
                    print(f"  [{i}] TextBlock: {block.text[:100]}")
                elif isinstance(block, ToolUseBlock):
                    print(f"  [{i}] ToolUseBlock: tool={block.name}, input={block.input}")
                elif isinstance(block, ToolResultBlock):
                    print(f"  [{i}] ToolResultBlock: tool_use_id={block.tool_use_id}")

        elif isinstance(message, ResultMessage):
            print(f"\n[ResultMessage]")
            print(f"  session_id:    {message.session_id}")
            print(f"  total_cost:    ${message.total_cost_usd:.5f}")
            print(f"  num_turns:     {message.num_turns}")
            print(f"  duration_ms:   {message.duration_ms}")


# ─────────────────────────────────────────────
# Demo 2: query() is stateless
# ─────────────────────────────────────────────
async def demo_stateless_query():
    print("\n=== Demo 2: Stateless query() ===\n")

    # First call
    print("Call 1: 'My name is Alice'")
    async for message in query(prompt="My name is Alice."):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"  → {block.text[:100]}")

    # Second call — Claude does NOT remember the name from the first call!
    print("\nCall 2: 'What is my name?'")
    async for message in query(prompt="What is my name?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"  → {block.text}")  # "I don't know your name"


# ─────────────────────────────────────────────
# Demo 3: ClaudeSDKClient is stateful
# ─────────────────────────────────────────────
async def demo_stateful_client():
    print("\n=== Demo 3: Stateful ClaudeSDKClient ===\n")

    async with ClaudeSDKClient() as client:
        # First exchange
        print("Exchange 1: 'My name is Alice'")
        await client.query("My name is Alice.")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"  → {block.text[:100]}")

        # Second exchange — Claude DOES remember!
        print("\nExchange 2: 'What is my name?'")
        await client.query("What is my name?")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"  → {block.text}")  # "Your name is Alice!"


async def main():
    await demo_all_message_types()
    await demo_stateless_query()
    await demo_stateful_client()


asyncio.run(main())
