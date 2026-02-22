# test_sdk.py — Minimal diagnostic agent for testing LLM compatibility
"""
Stripped-down version of agent.py for A/B testing between Claude (standard)
and local LLMs (e.g. gpt-oss-120b via LiteLLM proxy). Only uses the main
orchestrator + one subagent (web_researcher). Maximum debug output.

Usage:
  uv run python test_sdk.py "What is Python pattern matching?"
  uv run python test_sdk.py --model gpt-oss-120b "What is Python pattern matching?"
  uv run python test_sdk.py --no-tools "Just answer: what is 2+2?"
  uv run python test_sdk.py --raw "What is Python pattern matching?"
"""
import argparse
import asyncio
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from claude_agent_sdk import (
    AgentDefinition, ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage,
    HookMatcher, ResultMessage, TextBlock, ToolUseBlock,
)

load_dotenv()

# ── ANSI Colors ──────────────────────────────────────────
BOLD = "\033[1m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

LOG_DIR = "session_data"
DEBUG_LOG = os.path.join(LOG_DIR, "test_sdk_debug.log")


def stderr_handler(line: str) -> None:
    """Print all CLI stderr to console and log file."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{DIM}[stderr {ts}] {line}{RESET}")
    try:
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {line}\n")
    except Exception:
        pass


async def log_tool_call(input_data: dict, tool_use_id: str, context) -> dict:
    """PreToolUse hook — log every tool call with full input."""
    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{YELLOW}[{ts}] PreToolUse: {BOLD}{tool_name}{RESET}")
    print(f"{DIM}  id: {tool_use_id}")
    print(f"  input: {json.dumps(tool_input, indent=2, default=str)[:500]}{RESET}")
    return {}


def display_message(message: AssistantMessage, raw: bool = False):
    """Display assistant messages with agent labeling."""
    parent_id = getattr(message, "parent_tool_use_id", None)
    label = f"{GREEN}[web_researcher]{RESET}" if parent_id else f"{CYAN}[Main]{RESET}"

    for block in message.content:
        if isinstance(block, TextBlock):
            print(f"{label} {block.text}\n")
        elif isinstance(block, ToolUseBlock):
            tool_id = (getattr(block, "id", None) or "?")[:8]
            print(f"{label} {BOLD}{block.name}{RESET} (id: {tool_id})")
            input_preview = json.dumps(block.input, default=str)[:200]
            print(f"{DIM}  {input_preview}{RESET}")

    if raw:
        print(f"{DIM}[raw] content_types: {[type(b).__name__ for b in message.content]}{RESET}")


def display_result(message: ResultMessage):
    """Display result summary."""
    cost = f"${message.total_cost_usd:.4f}" if hasattr(message, "total_cost_usd") else "$?"
    turns = message.num_turns if hasattr(message, "num_turns") else "?"
    session = message.session_id if hasattr(message, "session_id") else "?"
    print(f"\n{DIM}Result: {cost} | {turns} turns | session: {session}{RESET}\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Minimal diagnostic agent for testing LLM compatibility"
    )
    parser.add_argument("query", help="The query to send to the agent")
    parser.add_argument(
        "--model", default="sonnet",
        help="Model to use (default: sonnet). E.g. gpt-oss-120b"
    )
    parser.add_argument(
        "--no-tools", action="store_true",
        help="Run with zero tools (tests basic chat without Harmony tool issues)"
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="Enable include_partial_messages to see raw stream events"
    )
    args = parser.parse_args()

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(DEBUG_LOG, "w", encoding="utf-8") as f:
        f.write(f"# test_sdk debug log — {datetime.now().isoformat()}\n")
        f.write(f"# model: {args.model} | no-tools: {args.no_tools} | raw: {args.raw}\n")
        f.write(f"# query: {args.query}\n\n")

    print(f"{BOLD}{CYAN}test_sdk.py — Diagnostic Agent{RESET}")
    print(f"{DIM}Model: {args.model} | Tools: {'disabled' if args.no_tools else 'enabled'} | Raw: {args.raw}{RESET}")
    print()

    # ── System prompt ────────────────────────────────────
    system_prompt = (
        "You are a research assistant. "
        "Use web_researcher to find information when needed. "
        "Give concise, well-structured answers."
    )

    # ── Agents (single subagent) ─────────────────────────
    agents = {}
    if not args.no_tools:
        agents["web_researcher"] = AgentDefinition(
            description="Finds articles, videos, and community content.",
            prompt=(
                "You are a web researcher. Use WebSearch to find relevant results, "
                "then use WebFetch to retrieve and summarize the most promising pages. "
                "Return a concise summary of findings."
            ),
            tools=["WebSearch", "WebFetch"],
            model="haiku",
        )

    # ── Hooks (tool logging) ─────────────────────────────
    hooks = {
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[log_tool_call]),
        ],
    }

    # ── Allowed tools ────────────────────────────────────
    allowed_tools = [] if args.no_tools else ["Task", "WebSearch", "WebFetch"]

    # ── Options ──────────────────────────────────────────
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=allowed_tools,
        model=args.model,
        agents=agents,
        permission_mode="acceptEdits",
        max_turns=20,
        max_budget_usd=1.00,
        hooks=hooks,
        stderr=stderr_handler,
        debug_stderr=None,
        extra_args={"debug-to-stderr": None},
    )

    # ── Run ──────────────────────────────────────────────
    print(f"{BOLD}Query:{RESET} {args.query}\n")
    start = time.time()

    try:
        async with ClaudeSDKClient(options=options) as client:
            await client.query(args.query)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    display_message(message, raw=args.raw)
                elif isinstance(message, ResultMessage):
                    display_result(message)
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n{RED}{BOLD}Error after {elapsed:.1f}s:{RESET} {e}")
        print(f"{DIM}Check {DEBUG_LOG} for full stderr output.{RESET}")
        raise

    elapsed = time.time() - start
    print(f"{DIM}Completed in {elapsed:.1f}s{RESET}")


asyncio.run(main())
