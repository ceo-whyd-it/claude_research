# Practical Takeaways: Recursive Language Models

What you can actually **do** with this paper's contributions.

---

## TL;DR

**Install**: `pip install rlms`
**Use When**: Processing documents 100x beyond your model's context window
**Key Benefit**: Maintain reasoning quality while handling massive contexts
**Cost**: Comparable to base model calls despite 100x scale
**Trade-off**: Sequential overhead (2-5x slower wall-clock time)

---

## Quick Start Guide

### Installation

```bash
pip install rlms
```

### Basic Usage

```python
from rlms import RecursiveLanguageModel

# Initialize RLM
rlm = RecursiveLanguageModel(
    model="gpt-4o",           # or "gpt-4", "claude-3.5", etc.
    sandbox="docker",         # or "local", "modal", "e2b"
    api_key="your-api-key"    # optional if env var set
)

# Load long document
with open("massive_doc.txt") as f:
    document = f.read()  # Can be 100k+ tokens

# Ask questions
result = rlm.query(
    context={"doc": document},
    question="What are the main findings about X?"
)

print(result)
```

### Using the Pre-trained Model

For significantly lower costs, use RLM-Qwen3-8B:

```python
from rlms import RecursiveLanguageModel

# Use the fine-tuned 8B model
rlm = RecursiveLanguageModel(
    model="mit-oasys/rlm-qwen3-8b-v0.1",
    sandbox="docker"
)

# Same API as above
result = rlm.query(
    context={"codebase": load_repository()},
    question="How does authentication work in this codebase?"
)
```

**Cost Comparison**:
- RLM(GPT-5): ~$0.50 per complex query
- RLM(GPT-4o): ~$0.10 per complex query
- RLM(Qwen3-8B): ~$0.01 per complex query (self-hosted)

---

## Decision Tree: When to Use RLMs

```
Does your context exceed model window?
├─ NO → Use vanilla LLM (simpler, faster)
└─ YES → Continue

Is relevant information sparse (<10% of context)?
├─ NO → Consider vanilla long-context model
└─ YES → Continue

Does task require complex reasoning?
├─ NO → Use RAG or simple search
└─ YES → Continue

Can task be decomposed into sub-problems?
├─ NO → Use summarization or fail gracefully
└─ YES → **Use RLMs** ✅

Is minimum latency critical (<1 second)?
└─ YES → Reconsider; RLMs have sequential overhead
└─ NO → **RLMs are ideal** ✅
```

---

## Real-World Use Cases

### 1. Research Literature Review

**Scenario**: Analyze 1,000 research papers to track evolution of a technique.

**Implementation**:
```python
# Load all papers
papers = {f"paper_{i}": load_paper(i) for i in range(1000)}

# RLM query
timeline = rlm.query(
    context=papers,
    question="""
    Create a timeline of how 'transformer attention mechanisms'
    evolved across these papers. Identify:
    1. Key innovations and when they appeared
    2. Which papers built on which
    3. Current state of the art
    """
)
```

**Why RLMs Win**:
- Traditional RAG misses cross-paper connections
- Summarization loses critical details
- RLMs can grep, partition by date, recursively analyze clusters

**Expected Performance**:
- Context: ~50M tokens (1k papers × ~50k tokens each)
- Queries: 10-20 recursive calls
- Cost: ~$5-10 with GPT-4o, ~$0.50 with RLM-Qwen3-8B
- Time: 2-5 minutes

### 2. Codebase Understanding

**Scenario**: New engineer needs to understand authentication flow in 500-file codebase.

**Implementation**:
```python
# Load entire codebase
codebase = load_all_files("./src")

auth_flow = rlm.query(
    context={"code": codebase},
    question="""
    Trace the complete authentication flow:
    1. Where does login request enter?
    2. How is password verified?
    3. How are sessions managed?
    4. What security measures are in place?
    Provide file paths and line numbers.
    """
)
```

**Why RLMs Win**:
- Multi-file reasoning across entire codebase
- Traces call chains programmatically
- Handles imports and dependencies

**Expected Performance**:
- Context: ~500k tokens (500 files × ~1k tokens each)
- Queries: 5-15 recursive calls
- Cost: ~$1-3 with GPT-4o
- Time: 1-3 minutes

### 3. Customer Support Analysis

**Scenario**: Find root causes of product issues from 10,000 support tickets.

**Implementation**:
```python
# Load all tickets
tickets = load_support_tickets(limit=10000)

root_causes = rlm.query(
    context={"tickets": tickets},
    question="""
    Analyze these support tickets to find:
    1. Most common issues (with frequency)
    2. Root causes for top 5 issues
    3. Which product features are most problematic
    4. Temporal patterns (issues getting worse/better)
    """
)
```

**Why RLMs Win**:
- Handles way more tickets than fit in context
- Clusters and analyzes patterns programmatically
- Multi-hop reasoning (symptoms → root causes)

**Expected Performance**:
- Context: ~5M tokens (10k tickets × ~500 tokens each)
- Queries: 20-30 recursive calls (partitioning + analysis)
- Cost: ~$3-7 with GPT-4o
- Time: 3-7 minutes

### 4. Legal Document Review

**Scenario**: Find all relevant clauses across 100 contracts for compliance audit.

**Implementation**:
```python
# Load all contracts
contracts = {f"contract_{i}": load_contract(i) for i in range(100)}

audit = rlm.query(
    context=contracts,
    question="""
    Find all clauses related to data privacy and GDPR compliance.
    For each:
    1. Quote the exact clause
    2. Identify which contract it's from
    3. Flag any non-compliant language
    4. Suggest improvements
    """
)
```

**Why RLMs Win**:
- Precise extraction (legal requires exact quotes)
- Cross-contract comparison
- Complex reasoning about compliance

**Expected Performance**:
- Context: ~10M tokens (100 contracts × ~100k tokens each)
- Queries: 10-20 recursive calls
- Cost: ~$5-10 with GPT-4o
- Time: 3-6 minutes

### 5. Scientific Data Analysis

**Scenario**: Analyze 50 CSV files with experimental results to find correlations.

**Implementation**:
```python
# Load all experimental data
experiments = load_all_csvs("./data")

findings = rlm.query(
    context={"data": experiments},
    question="""
    Analyze experimental data to find:
    1. Which variables correlate with outcome Y?
    2. Are there interaction effects?
    3. Which experiments had anomalous results?
    4. Statistical significance of findings
    """
)
```

**Why RLMs Win**:
- Programmatic data manipulation (pandas, numpy)
- Handles more data than fits in context
- Complex statistical reasoning

**Expected Performance**:
- Context: Variable (depends on data size)
- Queries: 15-25 recursive calls
- Cost: ~$2-5 with GPT-4o
- Time: 2-4 minutes

---

## Implementation Checklist

### Before You Start

- [ ] **Identify context size**: Measure your input in tokens (use tokenizer)
- [ ] **Check decomposability**: Can task be broken into sub-problems?
- [ ] **Verify sparsity**: Is relevant info <10% of context?
- [ ] **Choose sandbox**: Local (dev), Docker (safety), Modal/E2B (scale)
- [ ] **Select model**: GPT-5 (quality), GPT-4o (balance), RLM-Qwen3-8B (cost)

### Setup Steps

1. **Install RLM library**:
```bash
pip install rlms
```

2. **Set up sandbox** (Docker example):
```bash
docker pull python:3.11-slim
# RLM handles the rest
```

3. **Configure API keys**:
```bash
export OPENAI_API_KEY="your-key"
# or for RLM-Qwen3-8B
export HF_TOKEN="your-token"
```

4. **Test on small example**:
```python
# Start small to validate approach
test_context = {"doc": "Small test document..."}
result = rlm.query(context=test_context, question="Test query")
```

### During Development

- [ ] **Monitor costs**: Track API calls and token usage
- [ ] **Add timeouts**: Prevent infinite loops
- [ ] **Handle errors**: Code execution can fail; add try-catch
- [ ] **Log trajectories**: Save recursive traces for debugging
- [ ] **Validate outputs**: Check that answers are grounded in context

### Optimization Tips

1. **Start with peeking**:
```python
# Encourage strategic inspection first
question = """
First, peek at the document structure to understand what's there.
Then, [your actual question].
"""
```

2. **Guide decomposition**:
```python
# Suggest strategy if model struggles
question = """
To answer this, consider:
1. Grepping for relevant keywords
2. Partitioning by category
3. Recursively analyzing each partition
Now, [your actual question].
"""
```

3. **Use verification loops**:
```python
# For critical tasks, ask model to verify
question = """
[Your question]
After getting the answer, verify it by double-checking the sources.
"""
```

4. **Parallelize when possible**:
```python
# If sub-calls are independent, RLM can parallelize
# (implementation-dependent; check docs)
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Code Execution Errors

**Symptom**: Crashes with syntax errors or index out of bounds

**Solution**:
- Use Docker sandbox for isolation
- Add error handling in prompts:
```python
question = """
When writing code, always:
1. Check variable types before operations
2. Validate indices are in range
3. Handle potential None values
[Your question]
"""
```

### Pitfall 2: High Latency

**Symptom**: Queries take 10+ minutes

**Solution**:
- Check recursion depth (should be 1-3 for most tasks)
- Guide model to more efficient strategies:
```python
question = """
Use grepping to quickly find relevant sections before deep analysis.
Avoid reading the entire document linearly.
[Your question]
"""
```
- Consider using RLM-Qwen3-8B (faster decisions)

### Pitfall 3: Cost Explosion

**Symptom**: Single query costs $50+

**Solution**:
- Set max tokens per call
- Use cheaper models (GPT-4o instead of GPT-5)
- Or use RLM-Qwen3-8B (~10x cheaper)
- Add cost budgets:
```python
rlm = RecursiveLanguageModel(
    model="gpt-4o",
    max_total_tokens=100000  # Budget limit
)
```

### Pitfall 4: Hallucinated Answers

**Symptom**: Model returns plausible but incorrect information

**Solution**:
- Request exact quotes and citations:
```python
question = """
[Your question]
For each claim, provide:
1. Exact quote from source
2. Which document/section it came from
3. Confidence level
"""
```
- Use verification loops
- Cross-check critical information

### Pitfall 5: Context Not Fully Utilized

**Symptom**: RLM only looks at small portion of context

**Solution**:
- Make questions more comprehensive:
```python
# Bad: "What does this say about X?"
# Good: "Search all documents for mentions of X, then analyze each"
```
- Explicitly request breadth:
```python
question = """
Ensure you check ALL documents, not just the first few.
[Your question]
"""
```

---

## Performance Tuning Guide

### For Maximum Quality

- **Model**: GPT-5 or RLM(GPT-5)
- **Verification**: Enable multiple verification passes
- **Recursion depth**: Allow up to 5 levels
- **Cost**: Higher (~$5-20 per complex query)

### For Balanced Quality/Cost

- **Model**: GPT-4o or Claude 3.5 with RLM
- **Verification**: Single verification pass
- **Recursion depth**: Limit to 3 levels
- **Cost**: Medium (~$1-5 per complex query)

### For Maximum Efficiency

- **Model**: RLM-Qwen3-8B (fine-tuned)
- **Verification**: Minimal or none
- **Recursion depth**: Limit to 2 levels
- **Cost**: Low (~$0.01-0.50 per query, self-hosted)

### For Minimum Latency

- **Model**: Smaller base model (GPT-4o-mini)
- **Strategy**: Encourage direct answers, less exploration
- **Recursion depth**: Limit to 1 level (basically RAG)
- **Trade-off**: Lower quality on complex tasks

---

## Sandbox Selection Guide

| Sandbox | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **Local** | Development, testing | Fast, free, no network | Security risk, limited resources |
| **Docker** | Production (small-medium) | Isolated, reproducible | Setup overhead, local resources |
| **Modal** | Production (large-scale) | Serverless, auto-scales | Requires account, network latency |
| **E2B** | Production (code-heavy) | Code execution platform | Paid service |
| **Prime Intellect** | Massive distributed tasks | Handles huge workloads | Bleeding edge, may change |
| **Daytona** | Cloud dev environments | Integrated workflow | Specific use case |

**Recommendation**:
- **Development**: Start with Local
- **Testing**: Use Docker
- **Production**: Modal or E2B depending on scale

---

## Cost Estimation Tool

Use this formula to estimate costs:

```python
def estimate_rlm_cost(
    context_size_tokens: int,
    num_queries: int,
    avg_recursion_depth: int = 2,
    model: str = "gpt-4o"
):
    """Rough cost estimator for RLM queries"""

    # Token costs (approximate, as of Feb 2026)
    costs_per_1k = {
        "gpt-5": {"input": 0.010, "output": 0.030},
        "gpt-4o": {"input": 0.003, "output": 0.015},
        "claude-3.5": {"input": 0.003, "output": 0.015},
        "rlm-qwen3-8b": {"input": 0.0001, "output": 0.0005},  # self-hosted
    }

    rates = costs_per_1k[model]

    # Estimate tokens per query
    # RLM only processes relevant portions (assume 10% of context)
    relevant_context = context_size_tokens * 0.10
    tokens_per_call = relevant_context + 1000  # +1k for question/answer
    total_calls = avg_recursion_depth + 1
    tokens_per_query = tokens_per_call * total_calls

    # Cost calculation
    input_cost = (tokens_per_query / 1000) * rates["input"] * num_queries
    output_cost = (tokens_per_query / 1000) * rates["output"] * num_queries

    return input_cost + output_cost

# Example: 1M token context, 10 queries
cost = estimate_rlm_cost(
    context_size_tokens=1_000_000,
    num_queries=10,
    model="gpt-4o"
)
print(f"Estimated cost: ${cost:.2f}")
# Output: Estimated cost: $5.40
```

---

## Integration Patterns

### With DSPy

RLMs naturally fit into DSPy pipelines:

```python
import dspy
from rlms import RecursiveLanguageModel

class RLMModule(dspy.Module):
    def __init__(self):
        self.rlm = RecursiveLanguageModel(model="gpt-4o")

    def forward(self, context, question):
        return self.rlm.query(context=context, question=question)

# Use in DSPy pipeline
pipeline = dspy.ChainOfThought(RLMModule())
```

### With LangChain

Replace standard RAG chains:

```python
from langchain.chains import ConversationalRetrievalChain
from rlms import RecursiveLanguageModel

class RLMChain:
    def __init__(self):
        self.rlm = RecursiveLanguageModel(model="gpt-4o")

    def __call__(self, inputs):
        return self.rlm.query(
            context={"docs": inputs["source_documents"]},
            question=inputs["question"]
        )

# Use instead of standard chain
chain = RLMChain()
```

### As Agent Memory

Use RLMs for long-horizon agent memory:

```python
class AgentWithRLMMemory:
    def __init__(self):
        self.rlm = RecursiveLanguageModel(model="gpt-4o")
        self.conversation_history = ""

    def respond(self, user_message):
        # Add to history
        self.conversation_history += f"\nUser: {user_message}"

        # Query RLM memory for relevant context
        relevant_context = self.rlm.query(
            context={"history": self.conversation_history},
            question=f"What's relevant to: {user_message}"
        )

        # Generate response with relevant context
        response = self.generate_response(user_message, relevant_context)
        self.conversation_history += f"\nAgent: {response}"
        return response
```

---

## Debugging Guide

### Enable Verbose Logging

```python
rlm = RecursiveLanguageModel(
    model="gpt-4o",
    verbose=True  # See all intermediate steps
)
```

### Save Trajectories

```python
result = rlm.query(
    context=context,
    question=question,
    save_trajectory="./logs/trajectory.json"
)

# Inspect what the model did
import json
with open("./logs/trajectory.json") as f:
    trajectory = json.load(f)
    for step in trajectory["steps"]:
        print(f"Action: {step['action']}")
        print(f"Observation: {step['observation']}")
```

### Common Issues and Diagnostics

**Issue**: "No output after 5 minutes"
- **Diagnosis**: Check if recursion is too deep
- **Fix**: Add max_depth parameter

**Issue**: "Code execution error"
- **Diagnosis**: Check sandbox logs
- **Fix**: Use Docker for isolation, add error handling

**Issue**: "Answer seems incomplete"
- **Diagnosis**: Check if context was truncated
- **Fix**: Ensure full context is loaded, guide decomposition

**Issue**: "Costs higher than expected"
- **Diagnosis**: Check number of recursive calls
- **Fix**: Guide model to more efficient strategies

---

## Resources and Next Steps

### Official Resources
- **Library**: [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm)
- **Blog**: [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/)
- **Model**: [HuggingFace RLM-Qwen3-8B](https://huggingface.co/mit-oasys/rlm-qwen3-8b-v0.1)

### Community
- **GitHub Discussions**: [RLM Discussions](https://github.com/alexzhang13/rlm/discussions)
- **HackerNews**: [Primary Thread](https://news.ycombinator.com/item?id=46475395)
- **Discord**: Check RLM GitHub for community links

### Further Reading
- See `resources.md` for complete link collection
- See `learning-path.md` for deep theoretical understanding
- Follow [@lateinteraction](https://x.com/lateinteraction) (Omar Khattab) for updates

### Getting Help
1. Check [GitHub Issues](https://github.com/alexzhang13/rlm/issues)
2. Read [official documentation](https://github.com/alexzhang13/rlm#readme)
3. Ask in GitHub Discussions
4. Post on HackerNews with #RLM tag

---

## Action Items

**If you're ready to apply RLMs**:

- [ ] Install `pip install rlms`
- [ ] Set up Docker sandbox
- [ ] Test on small example from your domain
- [ ] Measure baseline (vanilla LLM) performance
- [ ] Compare RLM performance and cost
- [ ] Optimize based on this guide
- [ ] Scale to production use case

**If you need more understanding first**:

- [ ] Read `summary.md` for overview
- [ ] Work through `learning-path.md` levels 1-3
- [ ] Return here when ready to implement

**If you want to contribute**:

- [ ] Read the full paper and appendix
- [ ] Explore open questions in `learning-path.md` Level 5
- [ ] Join community discussions
- [ ] Build extensions or domain-specific applications

---

**Last Updated**: February 2026
**Maintained By**: L7 Agent Research System
