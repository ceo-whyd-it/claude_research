# L7 Agent

A multi-agent system built with the Claude Agent SDK that includes documentation research, repository analysis, and web research capabilities.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude access |

### Getting an Anthropic API Key

1. Go to the <a href="https://console.anthropic.com/" target="_blank">Anthropic Console</a>
2. Sign up or log in to your account
3. Navigate to **API Keys** in the settings
4. Click **Create Key** and copy the generated key

## Running the Agent

```bash
uv run python agent.py
```

Once running, type your messages and press Enter. Type `exit` to quit.

## Example Requests

```
Learn pytest from scratch
What's new in RAG on arxiv?
Compare FastAPI vs Django vs Flask
Explain the Attention Is All You Need paper
Create a blog series from my Claude Agent SDK research
```

## Debug Mode

Enable verbose debug logging to see CLI stderr output (including full tool schemas sent to the API) printed to the console in real time.

**Via CLI flag:**
```bash
uv run python agent.py --debug
```

**Via environment variable:**
```bash
L7_DEBUG=1 uv run python agent.py
```

Debug output includes:
- Full CLI stderr from the Claude Code process
- Tool schemas being sent to the API
- Internal SDK debug messages

All debug output is also written to `session_data/cli_debug.log` regardless of debug mode.

## Diagnostic Tool (`test_sdk.py`)

A minimal single-query agent for A/B testing between Claude and local LLMs (e.g. `gpt-oss-120b` via LiteLLM proxy). Uses only the main orchestrator + one subagent (`web_researcher`). Always outputs full debug info.

**Basic usage (default Claude model):**
```bash
uv run python test_sdk.py "What is Python pattern matching?"
```

**Test with a local LLM:**
```bash
uv run python test_sdk.py --model gpt-oss-120b "What is Python pattern matching?"
```

**Test basic chat without tools (bypasses Harmony tool validation):**
```bash
uv run python test_sdk.py --no-tools "What is 2+2?"
```

**Show raw stream events:**
```bash
uv run python test_sdk.py --raw "What is Python pattern matching?"
```

| Flag | Description |
|------|-------------|
| `--model MODEL` | Model to use (default: `sonnet`). Use for A/B testing. |
| `--no-tools` | Disable all tools. Tests basic chat without Harmony tool issues. |
| `--raw` | Print raw stream event metadata for each message. |

Debug output is written to `session_data/test_sdk_debug.log`.

## Harmony Protocol Fix (LiteLLM)

If using vLLM with the Harmony protocol via a LiteLLM proxy, tool descriptions with `None` values cause pydantic `ValidationError`s. The included `litellm_tool_fix.py` provides a LiteLLM callback with two hooks:

- **`async_pre_call_hook`** — fires *before* provider translation, patches null `description` fields on tools in both Anthropic flat format (`{"name", "description", "input_schema"}`) and OpenAI nested format (`{"type": "function", "function": {...}}`).
- **`log_pre_api_call`** — fires *after* translation (read-only), logs the final outgoing tool schemas so you can verify what vLLM actually receives.

Register in your LiteLLM proxy config:
```yaml
litellm_settings:
  callbacks: ["litellm_tool_fix.HarmonyToolFixer"]
```

All activity is logged to `litellm_tool_fix.log` on the proxy server. To verify the fix is working:
```bash
# Check for patched descriptions
grep "Patched null descriptions" litellm_tool_fix.log

# Check outgoing tool format (should show schema_type: openai, param_key: parameters)
grep "Outgoing tools" litellm_tool_fix.log
```

If tools are being patched but model behavior is still wrong, the issue is likely model capability rather than tool schema formatting.
