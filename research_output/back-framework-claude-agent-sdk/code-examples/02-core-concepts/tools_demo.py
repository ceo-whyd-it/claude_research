"""
02-core-concepts/tools_demo.py
--------------------------------
Demonstrates built-in tools and permission modes.

Shows:
  - Allowlisting specific tools
  - Different permission modes
  - Custom per-tool permission callback
  - Reading tool use from the message stream

Run:
  python tools_demo.py
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
    PermissionResultAllow,
    PermissionResultDeny,
)


# ─────────────────────────────────────────────
# Demo 1: Read-only agent (safe for untrusted environments)
# ─────────────────────────────────────────────
async def demo_read_only_agent():
    print("=== Demo 1: Read-Only Agent ===")
    print("Claude can only read files and search — no writes, no bash\n")

    options = ClaudeAgentOptions(
        # Whitelist: Claude ONLY gets these tools
        allowed_tools=["Read", "Glob", "Grep", "WebSearch"],
        # Auto-accept all allowed tools (no confirmation prompts)
        permission_mode="acceptEdits",
    )

    async for message in query(
        prompt="List all Python files in this directory and count the total lines of code.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    # You can see exactly which tool Claude chose to use
                    print(f"\n  [Using tool: {block.name}]")

        elif isinstance(message, ResultMessage):
            print(f"\n\nCost: ${message.total_cost_usd:.4f}")


# ─────────────────────────────────────────────
# Demo 2: Permission modes
# ─────────────────────────────────────────────
async def demo_permission_modes():
    print("\n=== Demo 2: Permission Modes ===\n")

    # "plan" mode — Claude describes what it WOULD do but doesn't execute
    print('Mode: "plan" — Claude explains its plan without executing')
    print("-" * 50)

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="plan",  # Show plan only, don't execute
    )

    async for message in query(
        prompt="Create a hello.py file that prints 'Hello World'",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)


# ─────────────────────────────────────────────
# Demo 3: Custom permission callback
# ─────────────────────────────────────────────
async def demo_custom_permissions():
    print("\n\n=== Demo 3: Custom Permission Callback ===\n")

    # Track what the agent tried to do
    denied_actions = []
    allowed_actions = []

    async def my_permission_check(tool_name: str, tool_input: dict, context):
        """
        Custom logic to decide if Claude can use a tool.
        Return PermissionResultAllow() or PermissionResultDeny(message).
        """
        if tool_name == "Bash":
            command = tool_input.get("command", "")

            # Block any destructive commands
            dangerous_patterns = ["rm -rf", "sudo rm", "dd if=", "mkfs", "> /dev/"]
            for pattern in dangerous_patterns:
                if pattern in command:
                    denied_actions.append(f"Bash: {command[:50]}")
                    return PermissionResultDeny(
                        message=f"Blocked dangerous command containing '{pattern}'",
                        interrupt=False,  # Don't stop the session, just deny this action
                    )

            # Allow safe bash commands
            safe_prefixes = ["echo", "ls", "cat", "pwd", "python", "npm test"]
            is_safe = any(command.strip().startswith(p) for p in safe_prefixes)
            if is_safe:
                allowed_actions.append(f"Bash: {command[:50]}")
                return PermissionResultAllow()
            else:
                # Ask for confirmation for unknown commands
                # (In a real app, you'd prompt the user here)
                denied_actions.append(f"Bash (unknown): {command[:50]}")
                return PermissionResultDeny(
                    message=f"Unknown bash command '{command[:30]}' blocked. Allowed: echo, ls, cat, pwd, python, npm test"
                )

        # Allow all other tools
        allowed_actions.append(f"{tool_name}")
        return PermissionResultAllow()

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Write"],
        can_use_tool=my_permission_check,
    )

    async for message in query(
        prompt="Run `echo hello`, then try `rm -rf /tmp/test`, then list files with `ls -la`.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)

    print(f"\n\nAllowed actions: {allowed_actions}")
    print(f"Denied actions:  {denied_actions}")


async def main():
    await demo_read_only_agent()
    await demo_permission_modes()
    await demo_custom_permissions()


asyncio.run(main())
