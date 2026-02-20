import os
import time
from datetime import datetime
from claude_agent_sdk import ( AssistantMessage, ResultMessage, TextBlock, ToolUseBlock,
)

def truncate(value, max_length=200):
    """Truncate a value for display."""
    text = str(value)
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def format_input(input_dict, max_length=200):
    """Format tool input for readable display."""
    if not input_dict:
        return "{}"
    parts = []
    for key, value in input_dict.items():
        val_str = str(value)
        if len(val_str) > 50:
            val_str = val_str[:50] + "..."
        parts.append(f"{key}={val_str}")
    result = ", ".join(parts)
    return truncate(result, max_length)

# Per-agent color mapping
AGENT_COLORS = {
    "docs_researcher": "\033[32m",  # Green
    "repo_analyzer":   "\033[33m",  # Yellow
    "web_researcher":  "\033[34m",  # Blue
    "blog_writer":     "\033[95m",  # Bright magenta
}
MAIN_COLOR = "\033[36m"     # Cyan
FALLBACK_COLOR = "\033[35m" # Magenta
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def _timestamp() -> str:
    """Return a dim-formatted current timestamp."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{DIM}{now}{RESET}"

# Track subagent names by their tool_use_id
subagent_registry = {}

def _get_agent_label(message: AssistantMessage) -> tuple[str, str]:
    """Return (formatted_label, agent_name) based on message source."""
    parent_id = getattr(message, 'parent_tool_use_id', None)
    if parent_id:
        name = subagent_registry.get(parent_id, 'unknown')
        color = AGENT_COLORS.get(name, FALLBACK_COLOR)
        return f"{color}[{name}]{RESET}", name
    return f"{MAIN_COLOR}[Main]{RESET}", "Main"

def append_stream_log(log_path: str, agent_name: str, text: str) -> None:
    """Append a text block to the streaming markdown log."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        ts = datetime.now().strftime("%H:%M:%S")
        f.write(f"**[{ts}] {agent_name}:** {text}\n\n")


def write_stream_log_header(log_path: str, round_num: int, query: str) -> None:
    """Write a round header to the streaming markdown log."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n---\n## Round {round_num} — {ts}\n**Query:** {query}\n\n")


# ── Pending Tool Tracker ─────────────────────────────────
# Tracks tools currently in-flight for watchdog reporting.

pending_tools: dict[str, dict] = {}  # tool_use_id → {name, start_time, agent_name}


def track_tool_start(tool_use_id: str, name: str, agent_name: str) -> None:
    """Register a tool as in-flight."""
    pending_tools[tool_use_id] = {
        "name": name,
        "start_time": time.time(),
        "agent_name": agent_name,
    }


def mark_tool_complete(tool_use_id: str) -> dict | None:
    """Remove a tool from the pending tracker. Returns its info or None."""
    return pending_tools.pop(tool_use_id, None)


def get_pending_tools_summary() -> str:
    """Format a summary of currently pending tools for watchdog output."""
    if not pending_tools:
        return ""
    now = time.time()
    parts = []
    for info in pending_tools.values():
        elapsed = now - info["start_time"]
        parts.append(f"{info['name']} ({elapsed:.0f}s, {info['agent_name']})")
    return ", ".join(parts)


def display_message(message: AssistantMessage, stream_log: str | None = None):
    agent_label, agent_name = _get_agent_label(message)

    for block in message.content:
        if isinstance(block, ToolUseBlock):
            tool_id_full = getattr(block, 'id', None)
            if tool_id_full:
                track_tool_start(tool_id_full, block.name, agent_name)

            if block.name == 'Task':
                subagent_type = block.input.get('subagent_type', 'unknown')
                description = block.input.get('description', '')
                if tool_id_full:
                    subagent_registry[tool_id_full] = subagent_type
                print(f"{_timestamp()} {agent_label} 🚀 Spawning subagent: {BOLD}{subagent_type}{RESET}")
                if description:
                    print(f"   Description: {description}")
            else:
                tool_id_short = (tool_id_full or 'unknown')[:8]
                print(f"{_timestamp()} {agent_label} 🔧 {BOLD}{block.name}{RESET} (id: {tool_id_short})")
                print(f"   Input: {format_input(block.input)}")

        elif isinstance(block, TextBlock):
            color = AGENT_COLORS.get(agent_name, MAIN_COLOR)
            print(f"{_timestamp()} {color}{BOLD}{agent_name}{RESET}: {block.text}\n")
            if stream_log:
                append_stream_log(stream_log, agent_name, block.text)


def display_result(message: ResultMessage, audit_log: list[dict], round_state: dict) -> None:
    """Print two-line summary: per-round metrics and cumulative session totals."""
    round_num = round_state.get("round", "?")
    round_elapsed = round_state.get("round_elapsed", 0.0)
    round_cost = round_state.get("round_cost", 0.0)
    round_turns = round_state.get("round_turns", 0)
    total_elapsed = round_state.get("total_elapsed", 0.0)

    total_cost = f"${message.total_cost_usd:.4f}" if hasattr(message, 'total_cost_usd') else "$?"
    total_turns = message.num_turns if hasattr(message, 'num_turns') else "?"
    session = message.session_id if hasattr(message, 'session_id') else "?"

    # Round line with tool counts
    tool_summary = ""
    if audit_log:
        tool_counts: dict[str, int] = {}
        for entry in audit_log:
            tool_counts[entry["tool"]] = tool_counts.get(entry["tool"], 0) + 1
        tool_summary = " | tools: " + ", ".join(
            f"{t}: {c}" for t, c in sorted(tool_counts.items(), key=lambda x: -x[1])
        )

    print(f"\n{DIM}Round {round_num}: {round_elapsed:.1f}s | ${round_cost:.4f} | "
          f"{round_turns} turns{tool_summary}{RESET}")
    print(f"{DIM}Total:   {total_elapsed:.1f}s | {total_cost} | "
          f"{total_turns} turns | session: {session}{RESET}")
    print()