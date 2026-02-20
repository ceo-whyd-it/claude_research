# Paper Deep Dive: Group-Evolving Agents

## Paper Details

| Field | Value |
|-------|-------|
| **Title** | Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing |
| **Authors** | Zhaotian Weng, Antonis Antoniades, Deepak Nathani, Zhen Zhang, Xiao Pu, Xin Eric Wang (UCSB) |
| **Published** | February 4, 2026 |
| **arXiv ID** | 2602.04837 |
| **Links** | [Abstract](https://arxiv.org/abs/2602.04837) · [HTML](https://arxiv.org/html/2602.04837v1) · [PDF](https://arxiv.org/pdf/2602.04837) |

## What This Paper Is About

Self-improving AI agents have a fundamental problem: when agents evolve independently in tree-structured lineages, useful discoveries made by one branch never reach others. Good ideas die with their branch. This paper proposes **Group-Evolving Agents (GEA)** — a paradigm shift where the *group*, not the individual, is the unit of evolution.

By pooling execution traces, code patches, and outcomes across a group of agents, GEA enables any agent's discovery to benefit the whole population. The result: GEA achieves **71.0% on SWE-bench Verified** (matching human-designed systems that cost far more to build) and **88.3% on Polyglot** — a 25–29% improvement over prior self-evolving methods — while integrating more tools, fixing bugs 3.6× faster, and producing consistently strong agents across the population.

## How to Use These Files

| File | Purpose |
|------|---------|
| `learning-path.md` | **Start here** — five progressive levels from motivation to advanced context |
| `summary.md` | Quick structured overview of the paper |
| `practical-takeaways.md` | What builders and researchers can use today |
| `resources.md` | All links — paper, discussions, related work, related frameworks |

## Reading Order

1. **New to self-evolving agents?** → Start with `learning-path.md` Levels 1 & 2
2. **Want the highlights?** → Read `summary.md`
3. **Building agent systems?** → Go to `practical-takeaways.md`
4. **Researching the space?** → `learning-path.md` Level 5 + `resources.md`

## TL;DR

Prior self-evolving agents are like isolated scientists who never read each other's lab notebooks. GEA creates a shared lab notebook. Discoveries compound. Performance jumps.

> *"Open-ended progress doesn't fail because exploration is hard — it fails because discoveries don't accumulate."*
> — Xin Eric Wang (lead author, on X)
