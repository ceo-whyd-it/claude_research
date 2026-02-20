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
