# Example 2: Core Concepts - Agent Definitions and Specialized Teams

This example demonstrates how to create specialized agents programmatically using the Claude Agent SDK.

## What This Example Shows

- Defining agents with specific expertise
- Assigning tools to agents
- Creating specialized system prompts
- Running agents in parallel
- Synthesizing results from multiple reviewers

## Files

- `agent_definitions.py` — Main example showing how to define and use agents
- `app.py` — Sample code with intentional issues for the team to review
- `requirements.txt` — Python dependencies

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=your-key-here
```

## Run This Example

```bash
python agent_definitions.py
```

## What Happens

1. Three specialized agents are defined:
   - **security-reviewer**: Looks for security vulnerabilities
   - **performance-reviewer**: Identifies performance issues
   - **test-coverage-reviewer**: Finds testing gaps

2. The lead agent spawns all three teammates

3. Each teammate reviews `app.py` from their specialized perspective

4. The lead synthesizes all findings into a prioritized action list

## Expected Issues Found

**Security:**
- SQL injection in `get_users()`, `create_user()`, `get_user()`, `delete_user()`
- No authentication/authorization on `delete_user()`
- Debug mode exposed in production
- No input validation

**Performance:**
- Database connections not closed (resource leaks)
- No connection pooling
- Missing indexes on search columns
- No query result caching

**Testing:**
- No tests exist
- Missing 404 error case tests
- No security tests
- No edge case coverage

## Key Concepts Demonstrated

1. **Agent Definition Structure**
   ```python
   AgentDefinition(
       description="What this agent does",
       prompt="Detailed system prompt",
       tools=["Read", "Grep"],
       model="sonnet"
   )
   ```

2. **Tool Assignment**
   - Security and performance reviewers: Read-only (`["Read", "Grep"]`)
   - Test reviewer: Can run tests (`["Read", "Grep", "Bash"]`)

3. **Model Selection**
   - All teammates use `"sonnet"` for cost efficiency
   - Lead inherits from parent or uses default

4. **Parallel Execution**
   - All three reviewers work simultaneously
   - Results combined by lead

## Modify This Example

Try these variations:

1. **Add more reviewers:**
   ```python
   "accessibility-reviewer": AgentDefinition(...)
   "documentation-reviewer": AgentDefinition(...)
   ```

2. **Change tool permissions:**
   ```python
   tools=["Read", "Write", "Bash"]  # Let reviewer fix issues
   ```

3. **Use different models:**
   ```python
   model="opus"  # Higher capability for complex reviews
   ```

4. **Review your own code:**
   ```python
   prompt = "Review the files in ./src/ directory..."
   ```
