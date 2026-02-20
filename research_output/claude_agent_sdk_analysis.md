# Claude Agent SDK — Comprehensive Analysis

**Research Date:** 2026-02-19
**Analyst:** repo_analyzer subagent

---

## 1. Repository URL and Metadata

### Python SDK (Primary)
- **Repository URL:** https://github.com/anthropics/claude-agent-sdk-python
- **Stars:** 4,900
- **License:** MIT
- **Latest Release:** v0.1.38 (February 18, 2026)
- **Contributors:** 47
- **Used by:** 343 projects
- **Language:** Python 99.1%
- **Status:** Alpha (Development Status :: 3)

### TypeScript SDK
- **Repository URL:** https://github.com/anthropics/claude-agent-sdk-typescript
- **Stars:** 813
- **License:** Anthropic Commercial Terms of Service
- **Latest Release:** v0.2.47 (February 18, 2026)
- **Node.js Requirement:** 18+
- **NPM Package:** `@anthropic-ai/claude-agent-sdk`

### Demos Repository
- **Repository URL:** https://github.com/anthropics/claude-agent-sdk-demos
- **Stars:** 1,500
- **Language:** TypeScript (88.4%), Python (9.4%), JavaScript (1.1%)

### PyPI
- **Package Name:** `claude-agent-sdk`
- **PyPI URL:** https://pypi.org/project/claude-agent-sdk/
- **Version:** 0.1.38
- **Python Requirement:** >=3.10

---

## 2. Core System Architecture

### Rebranding Note
The Claude Code SDK was renamed to the **Claude Agent SDK** at version 0.1.0 to reflect its broader applicability beyond coding tasks.

### Architecture Overview

The Claude Agent SDK wraps the Claude Code CLI. The SDK spawns the Claude Code CLI as a subprocess and communicates with it through a bidirectional streaming protocol (stdin/stdout). Custom tools, hooks, and agent definitions are passed via a control protocol to the CLI at initialization.

```
Your Python App
      |
      | (subprocess + stdin/stdout streaming)
      |
Claude Code CLI (bundled in wheel)
      |
      | (Anthropic API)
      |
Claude Model (claude-sonnet-4-5, claude-opus-4-5, claude-haiku-3-5, etc.)
```

### Two Interaction Modes

| Feature             | `query()`                     | `ClaudeSDKClient`                  |
| :------------------ | :---------------------------- | :--------------------------------- |
| **Session**         | Creates new session each time | Reuses same session                |
| **Conversation**    | Single exchange               | Multiple exchanges in same context |
| **Connection**      | Managed automatically         | Manual control                     |
| **Interrupts**      | Not supported                 | Supported                          |
| **Hooks**           | Not supported                 | Supported                          |
| **Custom Tools**    | Not supported                 | Supported                          |
| **Continue Chat**   | New session each time         | Maintains conversation             |
| **Use Case**        | One-off tasks                 | Continuous conversations           |

### Python SDK Directory Structure

```
.
├── .claude/                  # Claude configuration
├── .github/workflows/        # CI/CD workflows (publish.yml)
├── e2e-tests/               # End-to-end tests
├── examples/                # Example scripts
│   ├── quick_start.py        # Basic usage
│   ├── streaming_mode.py     # Comprehensive ClaudeSDKClient examples
│   ├── streaming_mode_ipython.py  # Interactive IPython examples
│   ├── mcp_calculator.py     # In-process MCP server example
│   └── hooks.py              # Hooks examples
├── scripts/                 # Build and utility scripts
│   ├── initial-setup.sh
│   └── build_wheel.py        # Bundles Claude Code CLI into wheel
├── src/claude_agent_sdk/    # Main SDK source
│   ├── __init__.py
│   ├── _version.py
│   ├── _cli_version.py
│   └── types.py             # All type definitions
├── tests/                   # Unit tests
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## 3. README Quick Start Section (Verbatim)

### Installation

```bash
pip install claude-agent-sdk
```

**Prerequisites:**
- Python 3.10+

**Note:** The Claude Code CLI is automatically bundled with the package. If you prefer a system-wide installation:
```bash
curl -fsSL https://claude.ai/install.sh | bash
# Or specify custom path:
ClaudeAgentOptions(cli_path="/path/to/claude")
```

### Quick Start

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for message in query(prompt="What is 2 + 2?"):
        print(message)

anyio.run(main)
```

### With Options

```python
options = ClaudeAgentOptions(
    system_prompt="You are a helpful assistant",
    max_turns=1
)

async for message in query(prompt="Tell me a joke", options=options):
    print(message)
```

### Using Tools

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode='acceptEdits'  # auto-accept file edits
)

async for message in query(
    prompt="Create a hello.py file",
    options=options
):
    pass
```

### Official Documentation Quick Start (Python)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)  # Claude reads the file, finds the bug, edits it


asyncio.run(main())
```

### Run First Agent (List Files)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="What files are in this directory?",
        options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"]),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

---

## 4. Examples Folder Contents

### `examples/quick_start.py` — Basic Usage Patterns

Demonstrates three fundamental patterns:

1. **Basic query** — simple question-answer with message parsing
2. **With options** — custom system prompt and `max_turns`
3. **With tools** — file operations using `Read` and `Write` tools with cost reporting

```python
#!/usr/bin/env python3
"""Quick start example for Claude Code SDK."""

import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)


async def basic_example():
    """Basic example - simple question."""
    print("=== Basic Example ===")

    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def with_options_example():
    """Example with custom options."""
    print("=== With Options Example ===")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant that explains things simply.",
        max_turns=1,
    )

    async for message in query(
        prompt="Explain what Python is in one sentence.", options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def with_tools_example():
    """Example using tools."""
    print("=== With Tools Example ===")

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write"],
        system_prompt="You are a helpful file assistant.",
    )

    async for message in query(
        prompt="Create a file called hello.txt with 'Hello, World!' in it",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage) and message.total_cost_usd > 0:
            print(f"\nCost: ${message.total_cost_usd:.4f}")
    print()
```

### `examples/streaming_mode.py` — ClaudeSDKClient Patterns

Ten comprehensive examples for the `ClaudeSDKClient` streaming interface:

1. **`basic_streaming`** — Simplest pattern: `query()` then `receive_response()`
2. **`multi_turn_conversation`** — Follow-up queries maintaining context
3. **`concurrent_responses`** — Background receive tasks with concurrent sends
4. **`with_interrupt`** — Interrupting long-running operations mid-execution
5. **`manual_message_handling`** — Custom logic iterating messages to extract data
6. **`with_options`** — Configuration via `ClaudeAgentOptions` (tools, system prompt, env)
7. **`async_iterable_prompt`** — Sending multiple messages as an async stream
8. **`bash_command`** — Handling `ToolUseBlock` and `ToolResultBlock` for Bash
9. **`control_protocol`** — Server info retrieval and interrupt demonstration
10. **`error_handling`** — Timeout management, connection errors, cleanup

### `examples/mcp_calculator.py` — In-Process MCP Server

Full demonstration of custom tools via in-process MCP servers:

```python
#!/usr/bin/env python3
"""Example: Calculator MCP Server."""

import asyncio
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    create_sdk_mcp_server,
    tool,
)


@tool("add", "Add two numbers", {"a": float, "b": float})
async def add_numbers(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} + {args['b']} = {result}"}]
    }


@tool("divide", "Divide one number by another", {"a": float, "b": float})
async def divide_numbers(args: dict[str, Any]) -> dict[str, Any]:
    if args["b"] == 0:
        return {
            "content": [{"type": "text", "text": "Error: Division by zero is not allowed"}],
            "is_error": True,
        }
    result = args["a"] / args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} / {args['b']} = {result}"}]
    }


async def main():
    from claude_agent_sdk import ClaudeSDKClient

    calculator = create_sdk_mcp_server(
        name="calculator",
        version="2.0.0",
        tools=[add_numbers, divide_numbers],
    )

    options = ClaudeAgentOptions(
        mcp_servers={"calc": calculator},
        allowed_tools=["mcp__calc__add", "mcp__calc__divide"],
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Calculate 15 + 27")
        async for message in client.receive_response():
            print(message)
```

### `examples/hooks.py` — Hook System

Demonstrates `PreToolUse` hooks for blocking forbidden Bash commands and monitoring tool execution.

---

## 5. Starter Templates / Project Generators

There are no official project generators or CLI scaffolding tools. The recommended starting point is the demos repository:

```bash
git clone https://github.com/anthropics/claude-agent-sdk-demos.git
```

The demos repository contains these ready-to-use templates:

| Demo | Description |
|------|-------------|
| `hello-world/` | Minimal getting-started example |
| `hello-world-v2/` | Alternative hello-world variant |
| `research-agent/` | Multi-agent research system (Python) |
| `email-agent/` | IMAP email assistant |
| `excel-demo/` | Spreadsheet/Excel file handling |
| `resume-generator/` | Resume generation demo |
| `simple-chatapp/` | Simple chat application |

### Research Agent Quick Start

```bash
cd claude-agent-sdk-demos/research-agent
uv sync
export ANTHROPIC_API_KEY="your-api-key"
uv run python research_agent/agent.py
```

---

## 6. How Subagents / Tools Are Defined in Code

### Subagents

Subagents are defined using `AgentDefinition` and passed via the `agents` parameter in `ClaudeAgentOptions`. They are invoked through the built-in `Task` tool.

#### `AgentDefinition` dataclass

```python
@dataclass
class AgentDefinition:
    description: str                                          # When to use this agent
    prompt: str                                               # System prompt / behavior
    tools: list[str] | None = None                           # Allowed tools (None = inherit all)
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None  # Model override
```

#### Complete Subagent Example

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Task tool is REQUIRED for subagent invocation
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
                    tools=["Read", "Grep", "Glob"],  # Read-only access
                    model="sonnet",
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
                    prompt="You are a test execution specialist. Run tests and provide clear analysis of results.",
                    tools=["Bash", "Read", "Grep"],  # Can execute commands
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

#### Detecting Subagent Invocation

Messages from within a subagent's context include `parent_tool_use_id`. Subagent invocation appears as a `ToolUseBlock` with `name == "Task"`:

```python
async for message in query(prompt="Use the code-reviewer agent...", options=options):
    # Detect when a subagent is invoked
    if hasattr(message, "content") and message.content:
        for block in message.content:
            if getattr(block, "type", None) == "tool_use" and block.name == "Task":
                print(f"Subagent invoked: {block.input.get('subagent_type')}")

    # Messages from within a subagent's context
    if hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id:
        print("  (running inside subagent)")
```

#### Dynamic Agent Factory Pattern

```python
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        model="opus" if is_strict else "sonnet",
    )

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Task"],
    agents={"security-reviewer": create_security_agent("strict")}
)
```

#### Subagent Tool Restriction Patterns

| Use Case | Tools | Description |
|----------|-------|-------------|
| Read-only analysis | `Read`, `Grep`, `Glob` | Cannot modify or execute |
| Test execution | `Bash`, `Read`, `Grep` | Can run commands |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` | Full read/write, no commands |
| Full access | (omit `tools` field) | Inherits all tools from parent |

**Important:** Subagents cannot spawn their own subagents. Do not include `Task` in a subagent's `tools` array.

### Custom Tools (In-Process MCP Servers)

Custom tools are Python functions decorated with `@tool` and wrapped in an in-process MCP server. No subprocess management is required.

#### `@tool` Decorator

```python
def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any]
) -> Callable
```

**Input schema options:**

```python
# Simple type mapping (recommended)
{"text": str, "count": int, "enabled": bool}

# JSON Schema format (for complex validation)
{
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "count": {"type": "integer", "minimum": 0},
    },
    "required": ["text"],
}
```

#### `create_sdk_mcp_server()`

```python
def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: list[SdkMcpTool[Any]] | None = None
) -> McpSdkServerConfig
```

#### Full Custom Tool Example

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions, ClaudeSDKClient

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {
        "content": [
            {"type": "text", "text": f"Hello, {args['name']}!"}
        ]
    }

server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[greet_user]
)

options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__greet"]
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Greet Alice")
    async for msg in client.receive_response():
        print(msg)
```

**Tool naming convention for `allowed_tools`:** `mcp__{server_name}__{tool_name}`

#### Benefits Over External MCP Servers

| Feature | In-Process SDK Server | External MCP Server |
|---------|----------------------|---------------------|
| Subprocess management | Not needed | Required |
| IPC overhead | None | Present |
| Deployment | Single Python process | Multiple processes |
| Debugging | All in one process | Cross-process |

### Hooks

Hooks are Python callbacks invoked at specific lifecycle points. They intercept, modify, or block Claude's behavior.

```python
@dataclass
class HookMatcher:
    matcher: str | None = None        # Tool name or regex pattern (e.g., "Bash", "Write|Edit")
    hooks: list[HookCallback] = []    # List of callback functions
    timeout: float | None = None      # Timeout in seconds (default: 60)
```

**Available hook events:**

| Event | When Triggered |
|-------|---------------|
| `PreToolUse` | Before a tool executes |
| `PostToolUse` | After a tool executes |
| `PostToolUseFailure` | After a tool fails |
| `UserPromptSubmit` | When user submits a prompt |
| `Stop` | When agent stops |
| `SubagentStop` | When a subagent stops |
| `PreCompact` | Before message compaction |
| `Notification` | On notification |
| `SubagentStart` | When a subagent starts |
| `PermissionRequest` | On permission request |

**Hook callback signature:**

```python
async def my_hook(input_data: HookInput, tool_use_id: str | None, context: HookContext) -> HookJSONOutput:
    ...
```

**PreToolUse hook blocking example:**

```python
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, HookMatcher

async def check_bash_command(input_data, tool_use_id, context):
    command = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf /" in command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Dangerous command blocked",
            }
        }
    return {}

options = ClaudeAgentOptions(
    allowed_tools=["Bash"],
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_bash_command]),
        ],
    }
)
```

---

## 7. Main Technologies and Dependencies

### Core Dependencies (`pyproject.toml`)

```toml
[project]
name = "claude-agent-sdk"
version = "0.1.38"
requires-python = ">=3.10"

dependencies = [
    "anyio>=4.0.0",                                    # Async I/O framework
    "typing_extensions>=4.0.0; python_version<'3.11'", # Backported typing
    "mcp>=0.1.0",                                      # Model Context Protocol
]
```

| Dependency | Role |
|-----------|------|
| `anyio` | Cross-platform async I/O; enables both `asyncio` and `trio` backends |
| `typing_extensions` | Backports Python 3.11+ typing features to 3.10 |
| `mcp` | Model Context Protocol library; enables in-process MCP servers |
| Claude Code CLI | Bundled in wheel; the actual AI agent runtime |

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.20.0",
    "anyio[trio]>=4.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]
```

### Build System

- **Tool:** Hatchling
- **Wheel building:** Custom `scripts/build_wheel.py` that downloads and bundles the Claude Code CLI binary for the target platform (macOS, Linux, Windows)

### TypeScript SDK Dependencies

- **Runtime:** Node.js 18+ / Bun
- **Package manager:** npm
- **Package:** `@anthropic-ai/claude-agent-sdk`

---

## 8. Configuration Options

### `ClaudeAgentOptions` — Complete Reference

```python
@dataclass
class ClaudeAgentOptions:
    # Tool configuration
    tools: list[str] | ToolsPreset | None = None          # Base tool set
    allowed_tools: list[str] = []                          # Explicitly allowed tools
    disallowed_tools: list[str] = []                       # Explicitly blocked tools

    # System prompt
    system_prompt: str | SystemPromptPreset | None = None

    # MCP servers
    mcp_servers: dict[str, McpServerConfig] | str | Path = {}

    # Permission control
    permission_mode: PermissionMode | None = None
    # "default" | "acceptEdits" | "plan" | "bypassPermissions"
    can_use_tool: CanUseTool | None = None                # Custom permission callback

    # Session management
    continue_conversation: bool = False
    resume: str | None = None                             # Session ID to resume
    fork_session: bool = False                            # Fork instead of resume

    # Execution limits
    max_turns: int | None = None
    max_budget_usd: float | None = None                   # Spending limit in USD

    # Model selection
    model: str | None = None                              # Primary model
    fallback_model: str | None = None                     # Fallback if primary fails

    # Beta features
    betas: list[SdkBeta] = []

    # Thinking / reasoning
    max_thinking_tokens: int | None = None
    thinking: ThinkingConfig | None = None
    effort: Literal["low", "medium", "high", "max"] | None = None

    # Hooks
    hooks: dict[HookEvent, list[HookMatcher]] | None = None

    # Subagents
    agents: dict[str, AgentDefinition] | None = None

    # Filesystem settings
    setting_sources: list[SettingSource] | None = None   # ["user", "project", "local"]
    cwd: str | Path | None = None
    add_dirs: list[str | Path] = []

    # CLI configuration
    cli_path: str | Path | None = None
    settings: str | None = None
    env: dict[str, str] = {}
    extra_args: dict[str, str | None] = {}

    # Output
    output_format: dict[str, Any] | None = None          # Structured output schema
    include_partial_messages: bool = False

    # Plugins
    plugins: list[SdkPluginConfig] = []

    # Sandbox
    sandbox: SandboxSettings | None = None

    # Checkpointing
    enable_file_checkpointing: bool = False

    # Other
    user: str | None = None
    max_buffer_size: int | None = None
    stderr: Callable[[str], None] | None = None
    permission_prompt_tool_name: str | None = None
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Required. Anthropic API authentication |
| `CLAUDE_CODE_USE_BEDROCK=1` | Use Amazon Bedrock instead of Anthropic API |
| `CLAUDE_CODE_USE_VERTEX=1` | Use Google Vertex AI instead of Anthropic API |
| `CLAUDE_CODE_USE_FOUNDRY=1` | Use Microsoft Azure AI Foundry |
| `ANTHROPIC_MODEL` | Override the default Claude model |

### Permission Modes

```python
PermissionMode = Literal[
    "default",             # Standard permission behavior
    "acceptEdits",         # Auto-accept file edits without prompts
    "plan",                # Planning mode: no execution, only planning
    "bypassPermissions",   # Bypass ALL permission checks
]
```

### Setting Sources

Controls which filesystem configuration sources are loaded:

```python
SettingSource = Literal["user", "project", "local"]
# user    -> ~/.claude/settings.json
# project -> .claude/settings.json  (version controlled)
# local   -> .claude/settings.local.json  (gitignored)
```

By default (`setting_sources=None`), no filesystem settings are loaded. To load project CLAUDE.md:

```python
options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads .claude/settings.json and CLAUDE.md
)
```

### Structured Output

```python
options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "findings": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["summary"]
        }
    }
)
```

---

## 9. Key Classes and Their Relationships

### Class Hierarchy

```
ClaudeAgentOptions (configuration dataclass)
    |-- tools: list[str] | ToolsPreset
    |-- allowed_tools: list[str]
    |-- system_prompt: str | SystemPromptPreset
    |-- mcp_servers: dict[str, McpServerConfig]
    |   |-- McpStdioServerConfig
    |   |-- McpSSEServerConfig
    |   |-- McpHttpServerConfig
    |   └-- McpSdkServerConfig  (from create_sdk_mcp_server())
    |-- permission_mode: PermissionMode
    |-- agents: dict[str, AgentDefinition]
    |   └-- AgentDefinition(description, prompt, tools, model)
    |-- hooks: dict[HookEvent, list[HookMatcher]]
    |   └-- HookMatcher(matcher, hooks, timeout)
    |       └-- HookCallback: async fn(HookInput, tool_use_id, HookContext)
    |-- thinking: ThinkingConfig
    |   |-- ThinkingConfigAdaptive
    |   |-- ThinkingConfigEnabled(budget_tokens)
    |   └-- ThinkingConfigDisabled
    └-- sandbox: SandboxSettings
        └-- network: SandboxNetworkConfig

query(prompt, options) -> AsyncIterator[Message]
    |-- Message variants:
    |   |-- UserMessage(content, uuid, parent_tool_use_id)
    |   |-- AssistantMessage(content, model, parent_tool_use_id, error)
    |   |   └-- content: list[ContentBlock]
    |   |       |-- TextBlock(text)
    |   |       |-- ThinkingBlock(thinking, signature)
    |   |       |-- ToolUseBlock(id, name, input)
    |   |       └-- ToolResultBlock(tool_use_id, content, is_error)
    |   |-- SystemMessage(subtype, data)
    |   |-- ResultMessage(session_id, result, total_cost_usd, structured_output, ...)
    |   └-- StreamEvent(uuid, session_id, event, parent_tool_use_id)
    └-- Errors:
        |-- ClaudeSDKError (base)
        |-- CLINotFoundError
        |-- CLIConnectionError
        |-- ProcessError(exit_code, stderr)
        └-- CLIJSONDecodeError(line, original_error)

ClaudeSDKClient (bidirectional streaming client)
    |-- __init__(options: ClaudeAgentOptions)
    |-- connect(prompt) -> None
    |-- query(prompt, session_id) -> None
    |-- receive_messages() -> AsyncIterator[Message]
    |-- receive_response() -> AsyncIterator[Message]   (until ResultMessage)
    |-- interrupt() -> None
    |-- rewind_files(user_message_uuid) -> None
    |-- get_server_info() -> dict | None
    └-- disconnect() -> None

SdkMcpTool (created by @tool decorator)
    |-- name: str
    |-- description: str
    |-- input_schema: type | dict
    └-- handler: async fn(args) -> dict

create_sdk_mcp_server(name, version, tools) -> McpSdkServerConfig
```

### Key Relationships

1. **`query()` vs `ClaudeSDKClient`:** Both spawn the Claude Code CLI subprocess and communicate via a streaming control protocol. `query()` is a convenience wrapper; `ClaudeSDKClient` gives explicit lifecycle control.

2. **`AgentDefinition` and `Task` tool:** The main agent invokes subagents using the built-in `Task` tool. The `AgentDefinition` configuration is passed at initialization via the control protocol. Messages produced by subagents carry `parent_tool_use_id` matching the `Task` tool call's ID.

3. **`McpSdkServerConfig` (in-process MCP):** Created by `create_sdk_mcp_server()`, passed in `ClaudeAgentOptions.mcp_servers`. Runs as an in-process MCP server via the `mcp` library, communicated to the CLI through the `SDKControlMcpMessageRequest` control protocol message.

4. **`HookMatcher`:** Registered per `HookEvent`. Uses `matcher` as a regex pattern against tool names. Hooks receive strongly-typed `HookInput` variants. Return `SyncHookJSONOutput` to control execution flow (allow/deny/modify).

5. **Session management:** `ResultMessage.session_id` is captured and passed to `ClaudeAgentOptions(resume=session_id)` to continue a session across separate `query()` calls.

---

## 10. Additional: Multi-Agent Research System (from claude-agent-sdk-demos)

The `research-agent/` demo is the closest real-world analog to the project in this repository.

### Architecture

```
User Prompt
     |
Lead Agent (Task tool enabled)
     |
     |-- task --> Researcher-1 (WebSearch, Write tools)
     |-- task --> Researcher-2 (WebSearch, Write tools)
     |-- task --> Researcher-3 (WebSearch, Write tools)
     |
     |-- task --> Data Analyst (Glob, Read, Bash, Write tools)
     |
     └-- task --> Report Writer (Skill, Write, Glob, Read, Bash tools)
```

### Workflow

1. Lead Agent breaks request into 2-4 subtopics
2. Researcher subagents spawn in parallel to search the web
3. Each Researcher saves findings to `files/research_notes/`
4. Data Analyst extracts metrics and generates charts in `files/charts/`
5. Report Writer creates final PDF reports in `files/reports/`

### Subagent Activity Tracking via `parent_tool_use_id`

```python
# Lead Agent spawns a Researcher via Task tool -> ID becomes "task_123"
# All tool calls from that Researcher include parent_tool_use_id = "task_123"

hooks = {
    "PreToolUse": [tracker.pre_tool_use_hook],
    "PostToolUse": [tracker.post_tool_use_hook]
}
```

### Output Structure

```
files/
├── research_notes/    # Markdown files from researchers
├── data/             # Data summaries from analyst
├── charts/           # PNG visualizations
└── reports/          # Final PDF reports

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt      # Human-readable conversation log
    └── tool_calls.jsonl    # Structured tool usage log (JSON Lines)
```

---

## 11. Version History Highlights

| Version | Date | Key Changes |
|---------|------|-------------|
| 0.1.38 | Feb 2026 | Bundled CLI v2.1.47 (latest) |
| 0.1.36 | 2026 | `effort` field ("low"/"medium"/"high"/"max"), ThinkingConfig enhancements |
| 0.1.31 | 2026 | MCP tool annotations via `@tool` `annotations` param; fixed large agent definition ARG_MAX issue |
| 0.1.29 | 2026 | New hook events: Notification, SubagentStart, PermissionRequest |
| 0.1.26 | 2026 | PostToolUseFailure hook |
| 0.1.23 | 2026 | `get_mcp_status()` method on ClaudeSDKClient |
| 0.1.15 | 2025 | File checkpointing and `rewind_files()` |
| 0.1.12 | 2025 | `tools` option, SDK betas support |
| 0.1.8  | 2025 | Claude Code CLI bundled in wheel (no separate install) |
| 0.1.7  | 2025 | Structured outputs, fallback model handling |
| 0.1.6  | 2025 | `max_budget_usd`, `max_thinking_tokens` |
| **0.1.0** | 2025 | **Major: Rename from Claude Code SDK. `ClaudeCodeOptions` -> `ClaudeAgentOptions`. Settings isolation. Programmatic subagents.** |

---

## 12. Source URLs

- GitHub (Python): https://github.com/anthropics/claude-agent-sdk-python
- GitHub (TypeScript): https://github.com/anthropics/claude-agent-sdk-typescript
- GitHub (Demos): https://github.com/anthropics/claude-agent-sdk-demos
- PyPI: https://pypi.org/project/claude-agent-sdk/
- Official Docs Overview: https://platform.claude.com/docs/en/agent-sdk/overview
- Python API Reference: https://platform.claude.com/docs/en/agent-sdk/python
- Subagents Guide: https://platform.claude.com/docs/en/agent-sdk/subagents
- Changelog: https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md
