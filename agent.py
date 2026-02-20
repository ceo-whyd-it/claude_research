import asyncio
import json
import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from claude_agent_sdk import (
    AgentDefinition, ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage,
    HookMatcher, ResultMessage,
)
from utils import (
    display_message, display_result, write_stream_log_header,
    mark_tool_complete, get_pending_tools_summary,
)

load_dotenv()

PROMPTS_DIR = "prompts"
MAX_TURNS = 100
MAX_BUDGET_USD = 5.00
MAX_RETRIES = 3
SESSION_STATE_FILE = "session_data/session_state.json"
STREAM_LOG_FILE = "session_data/stream_log.md"

CLI_DEBUG_LOG = "session_data/cli_debug.log"
SDK_LOG_FILE = "session_data/sdk.log"

BOLD = "\033[1m"
CYAN = "\033[36m"
DIM = "\033[2m"
RESET = "\033[0m"

# ── Operational Logging State ────────────────────────────
tool_start_times: dict[str, float] = {}
activity_state = {"last_activity": 0.0, "last_tool": "none", "last_tool_id": ""}

def print_welcome_banner():
    """Print a welcome banner with available topic types and example queries."""
    print()
    print(f"{BOLD}{CYAN}L7 Agent — Multi-Agent Research Orchestrator{RESET}")
    print(f"{DIM}Three specialized AI researchers working together to answer your questions.{RESET}")
    print()
    print(f"{BOLD}Available topic types:{RESET}")
    print(f"  {CYAN}Learn a Tool{RESET}        e.g. pytest, Docker CLI, ripgrep")
    print(f"  {CYAN}Learn a Concept{RESET}     e.g. GTD, Zettelkasten, TDD")
    print(f"  {CYAN}Learn a Framework{RESET}   e.g. Django, Next.js, FastAPI")
    print(f"  {CYAN}Research Arxiv{RESET}      \"What's new in RAG on arxiv?\"")
    print(f"  {CYAN}General Research{RESET}    \"What's out there on AI code review?\"")
    print(f"  {CYAN}Compare{RESET}             \"Compare FastAPI vs Django vs Flask\"")
    print(f"  {CYAN}Paper Deep Dive{RESET}     \"Explain the Attention Is All You Need paper\"")
    print()
    print(f"{BOLD}Example queries:{RESET}")
    print(f"  {DIM}>{RESET} Learn pytest from scratch")
    print(f"  {DIM}>{RESET} What's new in RAG on arxiv?")
    print(f"  {DIM}>{RESET} Compare FastAPI vs Django vs Flask")
    print()
    print(f"{DIM}Type 'exit' to quit.{RESET}")
    print()

def handle_stderr(line: str) -> None:
    """Append CLI stderr output to debug log file."""
    try:
        with open(CLI_DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {line}\n")
    except Exception:
        pass


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = f"{PROMPTS_DIR}/{filename}"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


# ── Session Persistence ──────────────────────────────────

def save_session_state(round_state: dict, last_query: str) -> None:
    """Persist session_id and round_state to disk after each round."""
    os.makedirs("session_data", exist_ok=True)
    state = {
        "session_id": round_state.get("session_id"),
        "round_state": round_state,
        "last_query": last_query,
        "timestamp": datetime.now().isoformat(),
    }
    with open(SESSION_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_session_state() -> dict | None:
    """Load saved session state from disk, or return None."""
    if os.path.exists(SESSION_STATE_FILE):
        with open(SESSION_STATE_FILE, "r") as f:
            return json.load(f)
    return None


def clear_session_state() -> None:
    """Remove the session state file on clean exit."""
    if os.path.exists(SESSION_STATE_FILE):
        os.remove(SESSION_STATE_FILE)


def make_options(system_prompt, agents, hooks, resume=None):
    """Build ClaudeAgentOptions, optionally resuming a previous session."""
    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        setting_sources=["user", "project"],
        allowed_tools=["Skill", "Task", "Write", "Bash", "WebSearch", "WebFetch"],
        model="sonnet",
        agents=agents,
        permission_mode="acceptEdits",
        max_turns=MAX_TURNS,
        max_budget_usd=MAX_BUDGET_USD,
        resume=resume,
        hooks=hooks,
        stderr=handle_stderr,
        debug_stderr=None,
    )


# ── Safety Hooks ──────────────────────────────────────────

audit_log: list[dict] = []


async def audit_tool_calls(input_data: dict, tool_use_id: str, context) -> dict:
    """Record every tool call for the session summary."""
    tool_name = input_data.get("tool_name", "unknown")
    audit_log.append({
        "timestamp": time.time(),
        "tool_use_id": tool_use_id,
        "tool": tool_name,
        "input_preview": str(input_data.get("tool_input", {}))[:80],
    })
    if tool_use_id:
        tool_start_times[tool_use_id] = time.time()
    activity_state["last_tool"] = tool_name
    activity_state["last_tool_id"] = tool_use_id or ""
    return {}


async def restrict_writes(input_data: dict, tool_use_id: str, context) -> dict:
    """Only allow Write to paths under research_output/."""
    if input_data.get("tool_name") == "Write":
        path = input_data.get("tool_input", {}).get("file_path", "")
        if path and not path.startswith("research_output/"):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Writes restricted to research_output/. "
                        f"Attempted path: {path}"
                    ),
                }
            }
    return {}


async def log_tool_completion(input_data: dict, tool_use_id: str, context) -> dict:
    """Log tool completion with execution duration."""
    tool_name = input_data.get("tool_name", "unknown")
    elapsed = 0.0
    if tool_use_id and tool_use_id in tool_start_times:
        elapsed = time.time() - tool_start_times.pop(tool_use_id)

    # Update the matching audit log entry with duration
    for entry in reversed(audit_log):
        if entry.get("tool_use_id") == tool_use_id:
            entry["duration_s"] = round(elapsed, 1)
            break

    # Clear from pending tracker
    mark_tool_complete(tool_use_id)

    # Display completion timing
    if elapsed > 15:
        print(f"{DIM}  \u26a0 {tool_name} took {elapsed:.1f}s (slow){RESET}")
    else:
        print(f"{DIM}  \u2713 {tool_name} completed in {elapsed:.1f}s{RESET}")

    return {}


def write_audit_log(entries: list[dict]) -> str | None:
    """Write audit log entries to a timestamped file. Returns the path or None."""
    if not entries:
        return None
    os.makedirs("research_output", exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"research_output/audit_{ts}.log"
    with open(path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return path


# ── Activity Watchdog ─────────────────────────────────────

async def watchdog():
    """Monitor for stalls — warn if no messages arrive for 30+ seconds."""
    while True:
        await asyncio.sleep(10)
        last = activity_state["last_activity"]
        if last == 0.0:
            continue
        elapsed = time.time() - last
        if elapsed > 30:
            pending = get_pending_tools_summary()
            if pending:
                print(f"\n{DIM}\u23f3 No activity for {elapsed:.0f}s. "
                      f"Pending: {pending}{RESET}")
            else:
                last_tool = activity_state["last_tool"]
                last_id = activity_state["last_tool_id"][:8] if activity_state["last_tool_id"] else "?"
                print(f"\n{DIM}\u23f3 No activity for {elapsed:.0f}s — "
                      f"last tool: {last_tool} ({last_id}). "
                      f"CLI subprocess may be stuck.{RESET}")


# ── Main ──────────────────────────────────────────────────

async def main():
    # ── Logging setup ────────────────────────────────────
    os.makedirs("session_data", exist_ok=True)
    logging.basicConfig(
        filename=SDK_LOG_FILE,
        level=logging.DEBUG,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    # Truncate CLI debug log for a fresh session
    with open(CLI_DEBUG_LOG, "w", encoding="utf-8") as f:
        f.write(f"# CLI Debug Log — {datetime.now().isoformat()}\n")

    main_agent_prompt = load_prompt("main_agent.md")
    docs_researcher_prompt = load_prompt("docs_researcher.md")
    repo_analyzer_prompt = load_prompt("repo_analyzer.md")
    web_researcher_prompt = load_prompt("web_researcher.md")
    blog_writer_prompt = load_prompt("blog_writer.md")

    agents = {
        "docs_researcher" : AgentDefinition(
            description="Finds and extracts information from official documentation sources.",
            prompt = docs_researcher_prompt,
            tools = ["WebSearch", "WebFetch"],
            model = "haiku"
        ),
        "repo_analyzer" : AgentDefinition(
            description="Analyzes code repositories for structure, examples, and implementation details.",
            prompt = repo_analyzer_prompt,
            tools = ["WebSearch","Bash"],
            model = "haiku"
        ),
        "web_researcher" : AgentDefinition(
            description="Finds articles, videos, and community content.",
            prompt = web_researcher_prompt,
            tools = ["WebSearch", "WebFetch"],
            model = "haiku"
        ),
        "blog_writer" : AgentDefinition(
            description="Transforms completed research output into a multi-part blog series.",
            prompt = blog_writer_prompt,
            tools = ["Read", "Glob", "Write"],
            model = "sonnet"
        ),
    }

    hooks = {
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[audit_tool_calls]),
            HookMatcher(matcher="Write", hooks=[restrict_writes]),
        ],
        "PostToolUse": [
            HookMatcher(matcher="*", hooks=[log_tool_completion]),
        ],
    }

    # ── Startup resume check ─────────────────────────────
    print_welcome_banner()

    resume_session = None
    round_state = {
        "round": 0,
        "start_time": 0.0,
        "prev_turns": 0,
        "prev_cost": 0.0,
        "total_elapsed": 0.0,
    }

    saved = load_session_state()
    if saved and saved.get("session_id"):
        print(f"Found previous session: {saved['session_id']}")
        print(f"  Last query: {saved['last_query']}")
        print(f"  Saved at: {saved['timestamp']}")
        if input("Resume this session? [y/N]: ").strip().lower() == 'y':
            resume_session = saved["session_id"]
            round_state = saved["round_state"]
        else:
            clear_session_state()

    # ── Retry loop ────────────────────────────────────────
    last_query = ""
    retries = 0
    while retries <= MAX_RETRIES:
        options = make_options(main_agent_prompt, agents, hooks, resume=resume_session)
        try:
            async with ClaudeSDKClient(options=options) as client:
                retries = 0  # reset on successful connection

                while True:
                    user_input = input(f'{BOLD}You{RESET}: ')
                    print('')
                    if user_input.lower() == 'exit':
                        clear_session_state()
                        break

                    last_query = user_input
                    audit_log.clear()
                    round_state["round"] += 1
                    round_state["start_time"] = time.time()
                    write_stream_log_header(STREAM_LOG_FILE, round_state["round"], user_input)
                    await client.query(user_input)

                    while True:
                        hit_limit = False
                        activity_state["last_activity"] = time.time()
                        wd_task = asyncio.create_task(watchdog())
                        try:
                            async for message in client.receive_response():
                                activity_state["last_activity"] = time.time()
                                if isinstance(message, AssistantMessage):
                                    display_message(message, stream_log=STREAM_LOG_FILE)
                                elif isinstance(message, ResultMessage):
                                    round_elapsed = time.time() - round_state["start_time"]
                                    round_state["total_elapsed"] += round_elapsed
                                    round_state["round_elapsed"] = round_elapsed

                                    round_turns = (message.num_turns - round_state["prev_turns"]
                                                   if hasattr(message, 'num_turns') else 0)
                                    round_cost = (message.total_cost_usd - round_state["prev_cost"]
                                                  if hasattr(message, 'total_cost_usd') else 0.0)
                                    round_state["round_turns"] = round_turns
                                    round_state["round_cost"] = round_cost

                                    # Persist session_id for crash recovery
                                    round_state["session_id"] = getattr(message, 'session_id', None)
                                    save_session_state(round_state, last_query)

                                    display_result(message, audit_log, round_state)
                                    log_path = write_audit_log(audit_log)
                                    if log_path:
                                        print(f"{DIM}  Audit log: {log_path}{RESET}")

                                    # Update prev values for next round
                                    if hasattr(message, 'num_turns'):
                                        round_state["prev_turns"] = message.num_turns
                                    if hasattr(message, 'total_cost_usd'):
                                        round_state["prev_cost"] = message.total_cost_usd

                                    # Check limits using per-round deltas
                                    at_turn_limit = round_turns >= MAX_TURNS
                                    at_budget_limit = round_cost >= MAX_BUDGET_USD
                                    if at_turn_limit or at_budget_limit:
                                        reason = "Turn limit" if at_turn_limit else "Budget limit"
                                        total_cost = f"${message.total_cost_usd:.4f}" if hasattr(message, 'total_cost_usd') else "$?"
                                        total_turns = message.num_turns if hasattr(message, 'num_turns') else "?"
                                        print(f"{BOLD}\u26a0 {reason} reached "
                                              f"(round: {round_turns} turns / ${round_cost:.2f}, "
                                              f"total: {total_turns} turns / {total_cost}).{RESET}")
                                        cont = input(f"Continue for another {MAX_TURNS} turns? [y/N]: ").strip().lower()
                                        if cont == 'y':
                                            hit_limit = True
                                            audit_log.clear()
                                            round_state["round"] += 1
                                            round_state["start_time"] = time.time()
                                            await client.query("/continue")
                                        else:
                                            hit_limit = False
                        finally:
                            wd_task.cancel()
                            try:
                                await wd_task
                            except asyncio.CancelledError:
                                pass
                        if not hit_limit:
                            break

                break  # clean exit from input loop — done

        except Exception as e:
            retries += 1
            resume_session = round_state.get("session_id")
            if retries > MAX_RETRIES or not resume_session:
                raise
            print(f"\n\u26a0 CLI crashed: {e}")
            print(f"  Resuming session {resume_session} (retry {retries}/{MAX_RETRIES})...")
            save_session_state(round_state, last_query)


asyncio.run(main())