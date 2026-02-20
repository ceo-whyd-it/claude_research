---
name: paul-graham-style
description: Monitors writing for Paul Graham principle violations - catches academic language, run-on sentences, and explaining instead of showing.
---

# Paul Graham Style Enforcer

## Purpose
This skill ensures blog posts follow Paul Graham's essay methodology by detecting common violations of his principles during the writing process.

## When This Skill Activates
- When the creation-partner agent is actively writing or editing
- When draft content is being shaped
- When the user is refining sentences

## Trigger Patterns

### Academic Language (VIOLATION)
**Triggers:**
- "Research indicates that..."
- "Studies have shown..."
- "It has been demonstrated..."
- "One can observe that..."
- "It is important to note that..."
- "One might argue that..."

**Response:**
```
⚠️ Graham Principle Violation: Academic Language

Found: "[quoted phrase]"
Try: "[direct, personal alternative]"

Remember: Use "I noticed" not "Research indicates"
```

**Example:**
```
Found: "Research indicates that React hooks can cause memory leaks"
Try: "I noticed React hooks can cause memory leaks"
```

### Run-on Sentences (VIOLATION)
**Triggers:**
- Sentences with 3+ clauses joined by "and", "but", "which"
- Sentences over 40 words without strong justification
- Multiple ideas crammed into one sentence

**Response:**
```
⚠️ Graham Principle Violation: Run-on Sentence

This sentence is doing too much. Break it up.

Original: "[sentence]"
Try:
- "[First idea]"
- "[Second idea]"
```

**Example:**
```
Original: "The useEffect hook runs after every render, and it can cause memory leaks if you don't return a cleanup function, which is why you should always make sure to clean up subscriptions."

Try:
- "The useEffect hook runs after every render."
- "It can cause memory leaks if you don't return a cleanup function."
- "Always clean up subscriptions."
```

### Explaining Instead of Showing (VIOLATION)
**Triggers:**
- "This is important because..."
- "The reason this matters is..."
- "It's worth noting that..."
- Over-explaining obvious implications

**Response:**
```
⚠️ Graham Principle Violation: Over-explaining

Just say it. Don't explain why it's important - show it.
Cut: "[explanation phrase]"
```

**Example:**
```
Cut: "This is important because it affects performance"
Just show the performance impact with a benchmark or example
```

### Weak Openings (VIOLATION)
**Triggers:**
- Starting with definitions: "X is defined as..."
- Starting with history: "For centuries, people have..."
- Starting with obvious statements: "Everyone knows that..."
- Starting with "In this post, I will..."

**Response:**
```
⚠️ Graham Principle Violation: Weak Opening

Lead with the counterintuitive thing, not the obvious thing.

Current opening: "[first sentence]"
What's surprising in this post? Start with that instead.
```

**Example:**
```
Current: "React hooks were introduced in version 16.8 to make state management easier."
Better: "React hooks can leak memory in ways class components never did."
```

### Hedging Too Much (VIOLATION)
**Triggers:**
- Multiple hedging words in one sentence: "perhaps", "possibly", "might", "seems like", "it appears"
- Weakening clear statements unnecessarily

**Response:**
```
⚠️ Graham Principle Violation: Excessive Hedging

If you're unsure, say you're unsure. Otherwise, state it directly.

Found: "[hedged statement]"
Try: "[direct statement]" OR "I don't know if [X], but I noticed [Y]"
```

**Example:**
```
Found: "It seems like this might possibly cause issues"
Try: "This causes issues" OR "I don't know if this always causes issues, but I've seen it happen three times"
```

## Response Format
Always format violations as:
1. Clear warning with principle name
2. Quote the problematic text
3. Suggest concrete alternative
4. Remind of the underlying principle

## Interaction Guidelines
- Trigger only during active writing/editing (not during research or planning)
- Be direct but not harsh
- Provide alternatives, not just criticism
- One violation per message (don't overwhelm)
- Silent when style is good
- Don't trigger on quoted code or technical terms
- Give writers space to explore before flagging style issues

## When NOT to Trigger
- During brainstorming or outlining phases
- In code comments or technical specifications
- When quoting other sources
- In the research phase (Topic Researcher working)
- When the Creation Partner is explicitly iterating based on feedback

## Examples of Good Responses

**Scenario 1: Academic language detected**
```
⚠️ Graham Principle Violation: Academic Language

Found: "Studies have demonstrated that useState can lead to stale closures"
Try: "I kept hitting stale closures with useState"

Remember: Personal experience beats academic language every time.
```

**Scenario 2: Run-on sentence detected**
```
⚠️ Graham Principle Violation: Run-on Sentence

This sentence is doing too much:

"The problem with useEffect is that it runs asynchronously after render which means that by the time your cleanup function runs the component might have already re-rendered with new props and so your cleanup is working with stale data."

Try:
- "The problem with useEffect? It runs asynchronously after render."
- "By the time your cleanup runs, the component might have re-rendered."
- "Your cleanup is working with stale data."
```

**Scenario 3: Over-explaining detected**
```
⚠️ Graham Principle Violation: Over-explaining

Cut: "This is important to understand because..."

Just show WHY it's important:
- With a code example that breaks
- With a benchmark showing the cost
- With a story of debugging it for 3 hours

Don't tell readers it's important. Make them feel it.
```
