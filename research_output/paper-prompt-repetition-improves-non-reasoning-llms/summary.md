# Summary: Prompt Repetition Improves Non-Reasoning LLMs

## One-Line Summary

Duplicating your input prompt — sending `<QUERY><QUERY>` instead of `<QUERY>` — consistently improves LLM accuracy on non-reasoning tasks with no increase in output length or latency.

---

## The Problem

Transformer-based LLMs use **causal attention masks**: each token can only attend to tokens that came before it. This means:

- The **first token** in your prompt has almost no context when processed
- Constraints or keywords near the **end** of your prompt are invisible to earlier tokens
- Prompt structure and ordering materially affects performance in ways users can't easily control

This is an inherent architectural limitation of autoregressive transformers — not a bug, but a consequence of how they're trained.

---

## The Solution

Simply **repeat the prompt**:

```
Original:  <QUERY>
Modified:  <QUERY><QUERY>
```

During the parallelized **prefill stage**, the first copy of the prompt can now attend to the second copy. This gives every token bidirectional-like access to the full context — at no cost to the generation stage.

---

## Key Results at a Glance

| Metric | Result |
|--------|--------|
| Statistically significant wins | **47 / 70** model-benchmark combinations |
| Losses | **0** |
| Best single improvement | **+76 pp** (Gemini 2.0 Flash-Lite on NameIndex: 21% → 97%) |
| Models tested | Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, GPT-4o, GPT-4o-mini, Claude 3 Haiku, Claude 3.7 Sonnet, DeepSeek V3 |
| Benchmarks | ARC Challenge, OpenBookQA, GSM8K, MMLU-Pro, MATH, NameIndex, MiddleMatch |
| Increase in output tokens | **None** |
| Increase in latency | **None** (for most models; slight increase on very long prompts for Claude) |

---

## Conditions: When It Helps vs. Doesn't

| Scenario | Effect |
|----------|--------|
| Non-reasoning tasks (direct Q&A, multiple choice, lookup) | ✅ Strong improvement |
| Options-first multiple choice format | ✅ Best gains |
| Position-dependent tasks (e.g., find item at index 25) | ✅ Dramatic gains |
| Chain-of-thought / reasoning enabled | ➖ Neutral to slight positive |
| Already-trained reasoning models (o1/o3 style) | ➖ Minimal benefit |
| Very long prompts | ⚠️ May hit context limit; slight latency hit on Claude |

---

## Ablation Findings

| Variant | Relative Effect |
|---------|-----------------|
| `<QUERY><QUERY>` (baseline) | Strong improvement |
| `<QUERY> Let me repeat that: <QUERY>` | Similar to baseline |
| `<QUERY><QUERY><QUERY>` (triple) | Often outperforms double on hard tasks |
| Padding with irrelevant content (control) | No improvement — confirms gains are from repetition, not length |

---

## Why Non-Reasoning Models?

Reasoning models (trained with RL to produce chain-of-thought) naturally learn to **rephrase and restate** the user's query during their reasoning trace. This implicitly gives all tokens bidirectional access to the full context — the same benefit that explicit prompt repetition provides. Explicit repetition adds little on top of what reasoning already provides.

---

## Authors

- **Yaniv Leviathan** — Google Research
- **Matan Kalman** — Google Research *(equal contribution)*
- **Yossi Matias** — Google Research
