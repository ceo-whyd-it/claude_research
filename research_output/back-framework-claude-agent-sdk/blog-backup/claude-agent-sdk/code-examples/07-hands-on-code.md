---
title: "Hands-On Code: Every Example Explained Line by Line"
series: "Mastering Claude Agent SDK"
part: 7
date: 2026-02-19
tags: [claude, agent-sdk, ai, python]
prev: "../chapters/05-next-steps-and-ecosystem.md"
---

# Hands-On Code: Every Example Explained Line by Line

This post is a walkthrough of the official Claude Agent SDK code examples. We go through each file in the example collection — from the minimal hello world to the complete production research agent — and explain what every piece does and why it is written that way.

All code in this post is runnable. Copy any example, set `ANTHROPIC_API_KEY`, and run it.

---

## Example Set 1: Hello World (`01-hello-world/`)

### Python: `hello_agent.py`

This is the smallest possible working agent. It demonstrates the three things you do in every agent program: import, call, iterate.

```python
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

    # query() is the primary entry point for one-shot agent tasks.
    # It returns an async generator — you MUST use "async for" to consume it.
    # Never call list() on it; that would block until completion without streaming.
    async for message in query(
        prompt="What is the Claude Agent SDK and what can it do? Give a 3-sentence summary."
    ):
        # AssistantMessage is what Claude says.
        # It arrives in pieces — do not assume one AssistantMessage = full response.
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    # end="" and flush=True give you real streaming output.
                    # Without flush=True, you may see output appear in bursts.
                    print(block.text, end="", flush=True)

        # ResultMessage is ALWAYS the last message in the stream.
        # It is your receipt: cost, turns taken, and session ID.
        elif isinstance(message, ResultMessage):
            print(f"\n\n{'=' * 50}")
            print(f"Session complete!")
            print(f"  Cost:   ${message.total_cost_usd:.4f}")
            print(f"  Turns:  {message.num_turns}")

asyncio.run(main())
```

**Key patterns here:**
- `async for` over `query()` — not `await`, not `list()`, always `async for`
- Type-checking with `isinstance` — the SDK uses typed message classes, not string type fields
- `end="", flush=True` — the two print arguments that make streaming feel real-time

### TypeScript: `hello_agent.ts`

The TypeScript version uses a different type system but the same conceptual pattern:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  console.log("Hello Agent SDK!");
  console.log("=".repeat(50));

  // "for await...of" is the TypeScript equivalent of Python's "async for"
  for await (const message of query({
    prompt: "What is the Claude Agent SDK and what can it do? Give a 3-sentence summary.",
  })) {
    // TypeScript uses string type discriminators instead of isinstance checks
    if (message.type === "assistant") {
      const content = message.message?.content ?? [];
      for (const block of content) {
        if (block.type === "text") {
          // process.stdout.write() gives streaming output without newlines
          process.stdout.write(block.text);
        }
      }
    }

    if (message.type === "result") {
      console.log(`\n\n${"=".repeat(50)}`);
      console.log("Session complete!");
      console.log(`  Cost:  $${message.total_cost_usd?.toFixed(4) ?? "N/A"}`);
      console.log(`  Turns: ${message.num_turns}`);
    }
  }
}

main().catch(console.error);
```

**TypeScript-specific notes:**
- `message.type === "assistant"` instead of `isinstance(message, AssistantMessage)`
- Optional chaining (`?.`) throughout — the TypeScript SDK uses more nullable types
- `process.stdout.write()` instead of `print(end="")` for streaming output

---

## Example Set 2: Core Concepts (`02-core-concepts/`)

### Streaming Demo: `streaming_demo.py`

This file is worth reading carefully — it demonstrates the complete message lifecycle and the difference between stateless `query()` and stateful `ClaudeSDKClient`.

**Demo 1: Every message type in sequence**

```python
from claude_agent_sdk import (
    query, ClaudeSDKClient, ClaudeAgentOptions,
    AssistantMessage, UserMessage, SystemMessage, ResultMessage,
    TextBlock, ToolUseBlock, ToolResultBlock,
)

async def demo_all_message_types():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant. Keep answers brief.",
        allowed_tools=["Bash"],
    )

    async for message in query(
        prompt="Run `echo 'hello from bash'` and tell me what it printed.",
        options=options,
    ):
        # Messages arrive in this order:
        # 1. SystemMessage — your system_prompt echoed back
        # 2. UserMessage — your prompt echoed back
        # 3. AssistantMessage(s) — Claude thinking, using tools, responding
        # 4. ResultMessage — final summary

        if isinstance(message, SystemMessage):
            print(f"[SystemMessage] {message.content[:50]}...")

        elif isinstance(message, UserMessage):
            print(f"[UserMessage] {str(message.content)[:80]}...")

        elif isinstance(message, AssistantMessage):
            print(f"[AssistantMessage] {len(message.content)} block(s):")
            for i, block in enumerate(message.content):
                if isinstance(block, TextBlock):
                    print(f"  [{i}] TextBlock: {block.text[:80]}")
                elif isinstance(block, ToolUseBlock):
                    # ToolUseBlock = Claude requesting a tool to be used
                    print(f"  [{i}] ToolUseBlock: {block.name}({block.input})")
                elif isinstance(block, ToolResultBlock):
                    # ToolResultBlock = the result of a tool call, fed back to Claude
                    print(f"  [{i}] ToolResultBlock: id={block.tool_use_id}")

        elif isinstance(message, ResultMessage):
            print(f"\n[ResultMessage]")
            print(f"  session_id: {message.session_id}")
            print(f"  cost: ${message.total_cost_usd:.5f}")
            print(f"  turns: {message.num_turns}")
            print(f"  duration_ms: {message.duration_ms}")
```

**Why `ToolUseBlock` matters:** When Claude decides to call a tool, you see a `ToolUseBlock` in the `AssistantMessage`. The SDK handles actually executing the tool and returning results, but you can observe (and log) every tool decision by watching for these blocks.

**Demo 2 and 3: Stateless vs. Stateful**

```python
# STATELESS: Each query() call is a fresh session
async def demo_stateless_query():
    async for message in query(prompt="My name is Alice."):
        pass  # Claude knows your name in this call

    # This second call does NOT remember "Alice"
    async for message in query(prompt="What is my name?"):
        if isinstance(message, AssistantMessage):
            # Claude will say "I don't know your name"
            ...

# STATEFUL: ClaudeSDKClient maintains context across calls
async def demo_stateful_client():
    async with ClaudeSDKClient() as client:
        await client.query("My name is Alice.")
        async for msg in client.receive_response():
            pass  # Claude knows your name

        await client.query("What is my name?")
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                # Claude WILL say "Your name is Alice"
                ...
```

The `async with` context manager handles subprocess lifecycle — the subprocess starts on entry and is cleaned up on exit.

---

### Tools Demo: `tools_demo.py`

Three progressively stricter permission patterns.

**Pattern 1: Read-only agent (safest)**

```python
options = ClaudeAgentOptions(
    # Explicit allowlist — Claude cannot use anything not listed here
    allowed_tools=["Read", "Glob", "Grep", "WebSearch"],
    permission_mode="acceptEdits",
)
```

This is the safest configuration for production: Claude can look but cannot touch. No writes, no bash execution.

**Pattern 2: Plan mode (safest with observability)**

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="plan",  # Show what Claude would do — but DO NOT execute
)
```

Plan mode is useful for testing your prompts before enabling execution. Claude explains exactly what it would do without doing it.

**Pattern 3: Custom permission callback (most flexible)**

```python
async def my_permission_check(tool_name: str, tool_input: dict, context):
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        dangerous_patterns = ["rm -rf", "sudo rm", "dd if=", "mkfs", "> /dev/"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return PermissionResultDeny(
                    message=f"Blocked: dangerous command containing '{pattern}'",
                    interrupt=False,  # Don't stop the session; just deny this action
                )

        # Allowlist safe commands
        safe_prefixes = ["echo", "ls", "cat", "pwd", "python", "npm test"]
        if any(command.strip().startswith(p) for p in safe_prefixes):
            return PermissionResultAllow()
        else:
            return PermissionResultDeny(message=f"Unknown command blocked: {command[:30]}")

    return PermissionResultAllow()  # Allow all non-bash tools

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Bash", "Write"],
    can_use_tool=my_permission_check,
)
```

`interrupt=False` in `PermissionResultDeny` is subtle but important: the agent continues running after a denial, rather than stopping. Use `interrupt=True` when a denial means the session should abort.

---

### Hooks Demo: `hooks_demo.py`

This file shows four distinct hook patterns that cover most production use cases.

**Hook pattern 1: Audit logging (observe without blocking)**

```python
execution_log = []

async def log_tool_use(input_data: dict, tool_use_id: str, context) -> dict:
    log_entry = {
        "timestamp": time.time(),
        "tool": input_data.get("tool_name", "unknown"),
        "input_preview": str(input_data.get("tool_input", {}))[:100],
    }
    execution_log.append(log_entry)
    print(f"  [PreToolUse] {log_entry['tool']}: {log_entry['input_preview'][:60]}")
    return {}  # Empty dict = observe only, no blocking
```

**Hook pattern 2: Write location restriction (security guardrail)**

```python
async def block_writes_outside_output(input_data: dict, tool_use_id: str, context) -> dict:
    tool_name = input_data.get("tool_name", "")
    if tool_name in ("Write", "Edit"):
        file_path = input_data.get("tool_input", {}).get("file_path", "")
        if file_path and not file_path.startswith("output/"):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"File writes only allowed in output/. Attempted: {file_path}"
                    ),
                }
            }
    return {}
```

**Hook pattern 3: Input modification (content injection)**

```python
async def add_safety_note_to_writes(input_data: dict, tool_use_id: str, context) -> dict:
    """Prepend a safety header to every Python file written."""
    tool_name = input_data.get("tool_name", "")
    if tool_name == "Write":
        tool_input = input_data.get("tool_input", {})
        if tool_input.get("file_path", "").endswith(".py"):
            original_content = tool_input.get("content", "")
            safety_header = "# Auto-generated by Claude Agent SDK\n# Review before deploying\n\n"

            # Returning "updatedInput" modifies what the tool actually receives
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "updatedInput": {
                        **tool_input,
                        "content": safety_header + original_content,
                    }
                }
            }
    return {}
```

This is powerful: you can modify tool inputs before execution. Use it to normalize file paths, inject headers, sanitize content, or enforce conventions.

**Hook pattern 4: Bash safety audit**

```python
async def audit_bash_commands(input_data: dict, tool_use_id: str, context) -> dict:
    if input_data.get("tool_name") == "Bash":
        command = input_data.get("tool_input", {}).get("command", "")
        dangerous = ["rm -rf /", "sudo rm -rf", "mkfs", "dd if=/dev/zero"]
        for pattern in dangerous:
            if pattern in command:
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Dangerous pattern blocked: '{pattern}'",
                    }
                }
    return {}
```

**Wiring multiple hooks together:**

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[log_tool_use]),           # all tools
            HookMatcher(matcher="Write|Edit", hooks=[block_writes_outside_output]),
            HookMatcher(matcher="Write", hooks=[add_safety_note_to_writes]),
            HookMatcher(matcher="Bash", hooks=[audit_bash_commands]),
        ],
        "PostToolUse": [
            HookMatcher(matcher="*", hooks=[log_tool_result]),
        ],
    },
)
```

The `matcher` field is a pipe-separated list of tool names, or `"*"` for all tools. Hooks run in order within each matcher.

---

### Subagents Demo: `subagents_demo.py`

The multi-agent code review system shows how orchestrators and specialists compose:

```python
options = ClaudeAgentOptions(
    system_prompt="""You are a code review orchestrator.
When asked to review code:
1. Call the security-reviewer agent to analyze for security issues
2. Call the performance-reviewer agent to analyze for performance issues
3. Combine their findings into a unified review report""",

    allowed_tools=["Task", "Read", "Glob", "Grep"],

    agents={
        "security-reviewer": AgentDefinition(
            description="Expert security auditor. Reviews code for vulnerabilities.",
            prompt="""You are a senior application security engineer.
Analyze code for:
- SQL/command injection vulnerabilities
- Authentication and authorization flaws
- Hardcoded secrets, API keys, or passwords
- Input validation and sanitization gaps

For each finding:
- Severity: Critical / High / Medium / Low
- Location: file and line
- Description: the issue
- Remediation: how to fix it

Return findings as a structured markdown report.""",
            tools=["Read", "Glob", "Grep"],  # Read-only subagent
        ),

        "performance-reviewer": AgentDefinition(
            description="Performance optimization expert.",
            prompt="""You are a senior performance engineer.
Find: N+1 queries, missing indexes, unnecessary loops, memory leaks, blocking I/O.
For each: Impact, Location, Description, Optimization.
Return as structured markdown.""",
            tools=["Read", "Glob", "Grep"],
        ),
    },
)

# Watch for Task tool calls to see when subagents spawn
async for message in query(prompt="Review Python files for security and performance issues.", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock) and block.name == "Task":
                agent_name = block.input.get("subagent_type", "unknown")
                print(f"\n  [Spawning subagent: {agent_name}]")
```

**Why `description` matters:** The `description` field in `AgentDefinition` is what the orchestrator uses to decide *which* subagent to call for which task. Write it like a job description — be specific about capabilities.

---

### Custom Tools Demo: `custom_tools_demo.py`

The `@tool` decorator is the fastest way to give Claude access to your own functions:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

# Three required arguments: name, description, input schema
@tool(
    "get_product_info",
    "Look up product information by product ID",
    {"product_id": str},    # Dict of {param_name: python_type}
)
async def get_product_info(args: dict) -> dict:
    # args is always a plain dict — access fields by name
    product_id = args["product_id"].upper()

    # Simulate a database lookup
    products = {
        "P001": {"name": "Widget Pro", "price": 29.99, "stock": 142},
        "P002": {"name": "Gadget Elite", "price": 99.99, "stock": 7},
    }

    if product_id in products:
        p = products[product_id]
        # Return value must have this structure:
        # {"content": [{"type": "text", "text": "..."}]}
        return {
            "content": [{
                "type": "text",
                "text": f"Product: {p['name']}, Price: ${p['price']:.2f}, Stock: {p['stock']}"
            }]
        }
    return {
        "content": [{"type": "text", "text": f"Product '{product_id}' not found."}]
    }

# Bundle into a named server
ecommerce_server = create_sdk_mcp_server(
    name="ecommerce",
    version="1.0.0",
    tools=[get_product_info],
)

# Register in options — naming: mcp__{server-alias}__{tool-name}
options = ClaudeAgentOptions(
    mcp_servers={"store": ecommerce_server},
    allowed_tools=["mcp__store__get_product_info"],
    permission_mode="acceptEdits",
)
```

**Why the return format looks this way:** The MCP protocol defines a specific response format. The `{"content": [{"type": "text", "text": "..."}]}` structure is the standard MCP tool response. Claude knows how to parse it automatically.

---

## Example Set 3: Real Application (`03-real-app/`)

### Production Research Agent: `research_agent.py`

This is the complete system from Part 4, with all production features assembled. Here are the pieces that often get missed in tutorials:

**The audit log pattern:**

```python
audit_log: list[dict] = []

async def audit_all_tools(input_data: dict, tool_use_id: str, context) -> dict:
    entry = {
        "timestamp": time.time(),
        "tool": input_data.get("tool_name", "unknown"),
        "input_preview": str(input_data.get("tool_input", {}))[:80],
    }
    audit_log.append(entry)
    return {}
```

At the end of the session, you have a complete timeline of every tool call. Use it for:
- Debugging why an agent took unexpected actions
- Compliance auditing
- Performance profiling (which tools are called most?)
- Cost attribution (which subagent was most expensive?)

**The session metrics pattern:**

```python
start_time = time.time()
subagents_used: list[str] = []

async for message in query(prompt=question, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock) and block.name == "Task":
                agent = block.input.get("subagent_type", "?")
                if agent not in subagents_used:
                    subagents_used.append(agent)

    elif isinstance(message, ResultMessage):
        elapsed = time.time() - start_time
        print(f"  Time elapsed:      {elapsed:.1f}s")
        print(f"  Total cost:        ${message.total_cost_usd:.4f}")
        print(f"  Turns taken:       {message.num_turns}")
        print(f"  Subagents used:    {subagents_used}")
        print(f"  Tool calls logged: {len(audit_log)}")
        print(f"  Session ID:        {message.session_id}")
```

**The audit summary at the end:**

```python
tool_counts: dict[str, int] = {}
for entry in audit_log:
    tool_counts[entry["tool"]] = tool_counts.get(entry["tool"], 0) + 1
for t, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
    print(f"    {t}: {count} call(s)")
```

This gives you a distribution of tool usage — invaluable for understanding what your agent actually spends time doing.

---

## Common Patterns Summary

Having seen all the examples, here are the patterns that appear in every serious agent:

| Pattern | Code | Why |
|---------|------|-----|
| Always consume the full stream | `async for msg in query(...)` | `ResultMessage` is last; stop early and you miss costs/session ID |
| Type-check every message | `isinstance(msg, AssistantMessage)` | Messages are typed; different types need different handling |
| Return `{}` from hooks | `return {}` | `None` causes errors; empty dict means "allow, no change" |
| Set `max_turns` and `max_budget_usd` | `ClaudeAgentOptions(max_turns=30)` | Circuit breakers for runaway sessions |
| Restrict write paths | Hook blocking non-output/ writes | Safety guardrail for any agent with file write access |
| Log `ResultMessage` data | Store `session_id`, `total_cost_usd` | Required for debugging, cost tracking, session resumption |
| Describe subagents precisely | `AgentDefinition(description=...)` | Orchestrator uses descriptions to decide who to call |

The code in this series is not academic — it reflects patterns that actually work in production. Run it, break it, modify it. That is how the SDK becomes second nature.
