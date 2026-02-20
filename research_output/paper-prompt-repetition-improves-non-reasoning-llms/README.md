# Paper Deep Dive: Prompt Repetition Improves Non-Reasoning LLMs

## Paper Details

| Field | Value |
|-------|-------|
| **Title** | Prompt Repetition Improves Non-Reasoning LLMs |
| **Authors** | Yaniv Leviathan, Matan Kalman, Yossi Matias (Google Research) |
| **Published** | December 17, 2025 |
| **arXiv ID** | 2512.14982 |
| **Links** | [Abstract](https://arxiv.org/abs/2512.14982) · [HTML](https://arxiv.org/html/2512.14982v1) · [PDF](https://arxiv.org/pdf/2512.14982) |

## What This Paper Is About

This paper proposes a deceptively simple technique: **repeat your input prompt twice** before sending it to an LLM. That's it. The authors show that this zero-cost trick (it doesn't increase output tokens or latency) improves accuracy across 47 out of 70 benchmark-model combinations tested — with **zero regressions** — on models including Gemini, GPT-4o, Claude, and DeepSeek.

The key insight is architectural: causal (left-to-right) transformers can't let early tokens attend to later tokens during the prefill stage. Repeating the prompt gives all tokens a second chance to attend to the full context, effectively providing richer bidirectional-like attention within the prompt.

## How to Use These Files

| File | Purpose |
|------|---------|
| `learning-path.md` | **Start here** — five progressive levels from background to advanced |
| `summary.md` | Quick structured overview of the paper |
| `practical-takeaways.md` | What you can actually use today |
| `resources.md` | All links — paper, discussions, implementations, related work |

## Reading Order

1. **New to the topic?** → Start with `learning-path.md` Level 1 & 2
2. **Want the highlights?** → Read `summary.md`
3. **Ready to apply it?** → Go to `practical-takeaways.md`
4. **Want to go deeper?** → `learning-path.md` Levels 4 & 5 + `resources.md`

## TL;DR

```python
# The entire contribution, in one line:
improved_response = llm(prompt + prompt)
```

Simple. Surprisingly effective. Worth knowing about.
