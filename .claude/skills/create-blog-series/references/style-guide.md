# Blog Series Style Guide

Adapted from Paul Graham's essay style and editorial best practices. These rules apply to every post in a blog series.

## Voice

### Be Direct
- Use "I" and "you" — write like you're talking to one person
- "I noticed" not "Research indicates"
- "You'll find" not "One might observe"
- State things confidently. If you're unsure, say so explicitly rather than hedging.

### Be Personal
- Share observations: "The first thing that surprised me..."
- Use specific details: "three API calls" not "several requests"
- Take positions: "This is the wrong approach" not "This might not be ideal"

### Be Concise
- Short sentences first. Explain after if needed.
- Cut words that don't add meaning: "very", "really", "quite", "basically", "essentially"
- One idea per sentence. If you used "and" or "which" to add a clause, consider splitting.

## Structure

### Openings
Lead with the counterintuitive thing. What's surprising about this topic?

**Good openings:**
- "Most tutorials get this backwards."
- "I spent three hours debugging something that should've taken five minutes."
- "The official docs don't mention the most important feature."

**Bad openings (never use these):**
- "X is defined as..." (definition)
- "Since the early days of..." (history)
- "In this post, we will explore..." (meta-description)
- "Everyone knows that..." (obvious statement)
- "Have you ever wondered..." (rhetorical question cliche)

### Body
- One topic per post — if you're explaining a sidequest in detail, it belongs in its own post
- Mention related topics briefly and link to them, don't explain them inline
- Use concrete examples before abstract explanations
- Every post needs at least one code block or mermaid diagram

### Closings
- End with what the reader can now do or understand
- Be specific: "You can now set up a multi-agent system" not "You've learned about agents"
- Don't summarize everything — pick the one thing that matters most

## Adaptation Rules

Blog posts are NOT copy-paste from research sources. You must:

1. **Restructure**: Research organizes by source; blogs organize by narrative arc
2. **Add transitions**: Connect ideas. "This matters because..." or "But here's the catch..."
3. **Add framing**: Give the reader a reason to care about each section
4. **Simplify**: Research captures everything; blogs focus on what's essential
5. **Add personality**: Observations, opinions, reactions — make it human

## Length Targets

| Post Type | Target Length | Read Time |
|-----------|-------------|-----------|
| Part 0 (Introduction) | 400-600 words | 2-3 min |
| Parts 1-5 (Chapters) | 800-1500 words | 4-8 min |
| Part 6 (Practical Takeaways) | 600-1200 words | 3-6 min |
| Part 7 (Hands-On Code) | 600-1200 words | 3-6 min |

If a chapter is under 800 words, you're probably not going deep enough.
If a chapter is over 1500 words, you're probably covering too many topics.

## Anti-Patterns

### Never Do These

| Anti-Pattern | Example | Fix |
|-------------|---------|-----|
| Definition opener | "React hooks are a feature that..." | Lead with what's surprising about hooks |
| History opener | "Since React 16.8 introduced hooks..." | Lead with the problem hooks solve |
| Meta-description | "In this post, we will cover..." | Just start covering it |
| Over-explaining | "This is important because..." | Show why it's important with an example |
| Run-on sentence | 40+ word sentence with multiple clauses | Split into 2-3 sentences |
| Excessive hedging | "It might perhaps possibly..." | State it or say you're unsure |
| Feature listing | "Feature 1... Feature 2... Feature 3..." | Explain why features matter, not just what they are |
| Copy-paste from docs | Reproducing API reference | Adapt with context and opinion |

### Watch For

- **Passive voice creep**: "The function is called by..." → "Call the function..."
- **Weasel words**: "some people think", "it's generally accepted" → who thinks? say specifically
- **Filler transitions**: "Furthermore", "Moreover", "Additionally" → just say the next thing
- **Explaining the obvious**: If the code example shows it clearly, don't re-explain in prose
