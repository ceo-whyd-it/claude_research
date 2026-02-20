# Practical Takeaways: Prompt Repetition

## Implementation

The technique is trivially simple. No library, no model change, no special tooling required.

### Minimal Python

```python
def repeat_prompt(prompt: str, n: int = 2) -> str:
    """Repeat a prompt n times to improve LLM performance."""
    return prompt * n

# Usage
response = llm_call(repeat_prompt(user_prompt))
```

### With Separator (Optional)

```python
def repeat_prompt(prompt: str, n: int = 2, separator: str = "\n\n") -> str:
    return separator.join([prompt] * n)
```

### Drop-in Decorator Pattern

```python
import functools

def with_prompt_repetition(n: int = 2):
    def decorator(llm_func):
        @functools.wraps(llm_func)
        def wrapper(prompt, **kwargs):
            return llm_func(prompt * n, **kwargs)
        return wrapper
    return decorator

@with_prompt_repetition(n=2)
def call_gpt4(prompt, **kwargs):
    return openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )
```

---

## When to Use It

### Use Prompt Repetition When:

- **Short-to-medium prompts** — doubling is feasible within context window limits
- **Non-reasoning tasks** — direct question answering, multiple choice, classification, lookup
- **Position-sensitive tasks** — anything where the model needs to locate or index items in a list
- **API deployments** — zero latency cost means it's truly free for most production setups
- **Models without built-in reasoning** — standard GPT-4o, Claude (non-extended-thinking), Gemini Flash, DeepSeek

### Avoid or Evaluate Carefully When:

- **Long prompts** — If your prompt is already 50% of the context window, doubling may be infeasible
- **Reasoning-enabled calls** — When using `o1`, `o3`, Claude "extended thinking," or `chain_of_thought=True`, gains are neutral at best
- **Token-budget-critical production** — Input tokens double; run a cost/accuracy tradeoff analysis
- **Summarization / translation / generation** — Gains documented mainly on Q&A and structured tasks; your mileage may vary on open-ended generation

---

## Cost / Benefit Analysis

| Input Token Multiple | Expected Accuracy Gain | Net Cost Change |
|---------------------|------------------------|-----------------|
| 2× (basic repetition) | ~14% average on benchmarks | ~+5% net (output unchanged) |
| 3× (triple) | Larger on hard tasks | ~+10% net |

The asymmetry (input tokens double, output unchanged) means **the effective cost increase is much less than 2×**. For typical tasks where output is longer than input, total cost increase may be only 5–20%.

---

## Production Checklist

- [ ] Measure the prompt length — will 2× fit in context?
- [ ] Confirm the task is non-reasoning (direct Q&A, classification, structured extraction)
- [ ] A/B test on a sample of your actual prompts before full rollout
- [ ] Monitor for latency changes, especially if using Claude on long prompts
- [ ] Check output format — paper confirms format is unchanged, but verify on your use case
- [ ] Consider triple repetition (3×) if accuracy is still insufficient and context allows

---

## Use Cases Where It Shines

### 1. Multiple Choice / Exam-Style Tasks
Options appearing before the question (options-first format) benefit most. The model can attend to all options when processing the question stem.

### 2. List Indexing / Retrieval
"Find the 25th item in this list" — one of the paper's custom benchmarks showed improvement from **21% to 97%** on this type of task.

### 3. Multi-Constraint Problems
"Find an item that satisfies condition A, B, and C" — repetition helps the model simultaneously hold all constraints in attention.

### 4. Customer Service / Chatbots
Non-reasoning chat models that need to correctly parse user intent from a complex message.

### 5. Classification / Routing
Models that need to categorize inputs against a set of labeled options benefit from the enhanced cross-token attention.

---

## Community Tips

- **Start with 2× before trying 3×** — double is more cost-efficient and covers most use cases
- **Triple repetition** (`<QUERY><QUERY><QUERY>`) provides extra gains on custom/hard tasks but increases cost proportionally
- **Verbose connectors** ("Let me repeat that:") don't add value over plain repetition — don't bother
- **The padding control study proves it's not just about length** — repeating garbage text doesn't help; the semantic content of the repetition is what matters
- **No fine-tuning required** — this is a pure inference-time technique; no model changes needed

---

## Limitations to Keep in Mind

1. **No official code repo** — but the technique needs none; implement it yourself in one line
2. **English-only evaluation** — multilingual performance is unverified
3. **Benchmark skew** — tested primarily on structured Q&A; creative/summarization tasks not benchmarked
4. **Statistical threshold** — paper uses p<0.1 without multiple-comparison correction; be appropriately skeptical of borderline cases
5. **Model versions may drift** — tested against API snapshots (Feb–Mar 2025); behavior may shift with model updates
