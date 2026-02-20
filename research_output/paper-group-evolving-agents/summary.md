# Summary: Group-Evolving Agents (GEA)

## One-Line Summary

GEA evolves *groups* of agents instead of individuals, enabling explicit experience sharing so that any agent's discovery can benefit the entire population — producing substantially stronger self-improving agents at the same computational budget.

---

## The Problem

State-of-the-art self-evolving agent systems (like the Darwin Gödel Machine) use **tree-structured evolution**: each agent independently improves itself, spawning child agents that branch off and evolve separately.

This creates a critical failure mode:

```
Root Agent
├── Branch A → A1 → A2 → A3  (discovers Tool T4 at step 9)
├── Branch B → B1 → B2        (discovers Tool T7 at step 6)
└── Branch C → C1              (discovers improved search strategy)
```

**Innovations are isolated.** Branch A's Tool T4 never reaches Branch B or C. Branch B's Tool T7 never reaches A or C. When you eventually pick the "best" agent at the end, it only contains the discoveries from *its* lineage — not the collective wisdom of the entire search.

---

## The Solution: Group-Level Evolution

GEA replaces isolated branches with **co-evolving groups**:

```
Parent Group (selected by Performance-Novelty criterion)
├── Agent A  ─┐
└── Agent B  ─┴─► Shared Experience Pool ─► Both agents evolve
                  (traces, patches, outcomes)    with full group knowledge
```

**Two key algorithms:**

### Algorithm 1: Parent Group Selection
Selects K parents (K=2 in experiments) that are both *high-performing* and *diverse* from each other, using:

```
score(i) = α_i · √nov(i)
```

Where:
- `α_i` = performance priority (task success rate)
- `nov(i)` = novelty (average cosine distance to M nearest neighbors in task-success space)
- `√` dampens novelty to prevent sacrificing performance for diversity

### Algorithm 2: Open-Ended Group Evolution
1. Collect all execution traces from both parent agents (code patches, logs, outcomes)
2. Aggregate into a **shared experience pool**
3. Each agent runs a **reflection module** over the full shared pool → generates evolution directives
4. An **evolution module** applies these directives → framework-level patches
5. Updated agents are evaluated; only functionally-correct updates are kept
6. Repeat, building an ever-richer shared pool

---

## Key Results at a Glance

| Benchmark | GEA | Prior Best (DGM) | Human-Designed |
|-----------|-----|-----------------|-----------------|
| SWE-bench Verified | **71.0%** | 56.7% | 71.8% (OpenHands+GPT-5) |
| Polyglot | **88.3%** | 68.3% | 52.0% (Aider+GPT-5) |

| Metric | GEA | DGM |
|--------|-----|-----|
| Key tools integrated | **8 / 9** | 5 / 9 |
| Unique ancestors in best agent | **17** (28.3% of pop.) | 9 |
| Iterations to fix framework bug | **1.4** | 5 |
| Worst-case top-5 agent score | **58.3%** | 56.7% (best single) |

---

## Experimental Setup

**Models used during evolution:**
- First 20 iterations: Claude Haiku 4.5 (efficient exploration)
- Final 10 iterations: Claude Sonnet 4.5 (quality refinement)
- Reflection module: GPT-o1

**Benchmarks:**
- **SWE-bench Verified** (500 tasks) — real-world bug fixing in open-source Python repositories
- **Polyglot** — multi-language code synthesis (Python, JavaScript, TypeScript, Java, Go, Rust, etc.)

**Cost:** ~$13,000 per method for SWE-bench; ~$1,500 for Polyglot (academic research budget)

---

## Why It Works

The shared experience pool transforms **transient diversity into long-term useful experience**:

| Property | Individual Evolution | Group Evolution |
|----------|---------------------|-----------------|
| Innovation propagation | Stays in one branch | Shared across all agents |
| Tool integration | Depends on lineage luck | Systematically consolidated |
| Bug repair | Requires re-discovering fix | Borrows from better sibling |
| Population diversity | Erodes over iterations | Maintained by selection criterion |

---

## Limitations

1. **Coding-task focus** — benchmarks are SWE-bench and Polyglot; generalization to non-coding tasks unproven
2. **High compute cost** — $13K per run is not a research budget most labs have
3. **No official code release** — paper is recent (Feb 2026); code not yet public
4. **Safety/interpretability risks** — evolved systems may be complex and hard to audit
5. **Single comparison baseline** — only DGM is directly compared as a self-evolving method
