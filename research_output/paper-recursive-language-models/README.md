# Recursive Language Models — Paper Deep Dive

**Paper**: Recursive Language Models
**arXiv ID**: [2512.24601](https://arxiv.org/abs/2512.24601)
**Authors**: Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)
**Published**: December 31, 2025 (v1); January 28, 2026 (v2)

---

## What's Inside

This folder contains a comprehensive deep dive into the "Recursive Language Models" paper, organized to help you understand both the theory and practice.

### Files

- **`summary.md`** — Quick overview: what the paper does, key results, and why it matters
- **`learning-path.md`** — Progressive learning guide (5 levels from motivation to advanced topics)
- **`practical-takeaways.md`** — Actionable insights: how to use RLMs, when to apply them, implementation tips
- **`resources.md`** — Complete collection of links (paper, code, discussions, related work)

---

## Quick Start

1. **New to this paper?** Start with `summary.md`
2. **Want to understand deeply?** Work through `learning-path.md` level by level
3. **Ready to implement?** Jump to `practical-takeaways.md`
4. **Need references?** Check `resources.md` for all links

---

## What Are Recursive Language Models?

Instead of forcing language models to process massive documents all at once (hitting context limits), RLMs treat long prompts as external objects stored in a Python environment. The model writes code to search, decompose, and recursively process relevant chunks—like giving an LLM a searchable library instead of forcing it to memorize an encyclopedia.

**Key Result**: RLMs process inputs **100x beyond model context windows** while outperforming frontier models like GPT-5 on complex long-context tasks.

---

## Why This Paper Matters

- **Paradigm Shift**: Moves from expanding context windows to treating context as an interactive object
- **Practical Impact**: Enables processing of 10M+ token inputs on models with 272k context windows
- **Performance**: RLM(GPT-5-mini) beats vanilla GPT-5 by 114% on long-context reasoning benchmarks
- **Efficiency**: Maintains comparable costs despite 100x larger inputs
- **Open Source**: MIT-licensed implementation and fine-tuned 8B model available

---

## Research Status

This paper is very recent (published Dec 31, 2025; revised Jan 28, 2026). It has already generated:
- **2.6k+ GitHub stars** on the official implementation
- **Extensive community discussion** on HN (380 tweets, 166k+ likes tracked)
- **Multiple blog posts** from industry researchers
- **Active development** by Prime Intellect and others

Expect rapid evolution of techniques, implementations, and applications throughout 2026.

---

## For Practitioners

**Use RLMs when:**
- Processing documents beyond your model's context window (100k+ tokens)
- Complex reasoning over large unstructured datasets (thousands of entries)
- Code repository analysis requiring deep multi-file understanding
- Research over massive document collections (100k+ documents)

**Available Now:**
- Official library: `pip install rlms` ([GitHub](https://github.com/alexzhang13/rlm))
- Fine-tuned model: RLM-Qwen3-8B-v0.1 ([HuggingFace](https://huggingface.co/mit-oasys/rlm-qwen3-8b-v0.1))
- Multiple sandbox options: Local, Docker, Modal, Prime Intellect, Daytona, E2B

---

## Authors & Context

- **Alex L. Zhang** (MIT CSAIL PhD) — GPU MODE leaderboard, SWE-bench, VideoGameBench
- **Tim Kraska** (MIT Professor) — Learned Indexes, ML for Systems, AWS Applied Science
- **Omar Khattab** (MIT Professor) — Creator of DSPy and ColBERT, widely adopted retrieval frameworks

This paper emerges from the DSPy/ColBERT research lineage focused on language model programming and efficient retrieval.

---

**Last Updated**: February 2026
**Research Compiled By**: L7 Agent Research System
