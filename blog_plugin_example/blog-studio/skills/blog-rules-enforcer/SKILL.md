---
name: blog-rules-enforcer
description: Monitors for topic drift - catches when multiple concepts are being explained in detail instead of one focused topic.
---

# Blog Rules Enforcer

## Purpose
This skill ensures blog posts follow the "one topic per post" rule by detecting when writers start explaining sidequests or tangential concepts in detail.

## When This Skill Activates
- During drafting when multiple concepts are being explained
- When sidequests start getting detailed explanations
- When post length suggests multiple topics

## Trigger Patterns

### Topic Drift (VIOLATION)
**Triggers:**
- Draft contains 2+ concepts with detailed explanations (multiple headings, examples, code for each)
- Sidequests getting full paragraphs instead of mentions
- Explaining prerequisite concepts in depth

**Response:**
```
⚠️ Blog Rule Violation: Multiple Topics

This post is explaining TWO things:
1. [Topic A]
2. [Topic B]

Which one are we writing? The other should be:
- A mention with a link, OR
- A separate post for later
```

**Example:**
```
This post is explaining TWO things:
1. How useEffect cleanup works (main topic)
2. How React's batching algorithm works (sidequest)

Which one are we writing? The batching explanation should be:
- A mention like "React batches updates (more on this later)", OR
- A separate post for later
```

### Missing Visual/Code (VIOLATION)
**Triggers:**
- Draft over 500 words with no code blocks or mermaid diagrams
- Final review phase without visual elements
- All prose, no concrete examples

**Response:**
```
⚠️ Blog Rule Violation: No Visual or Code

Every post needs at least one visual or working code snippet.

Suggestions:
- Add a Mermaid diagram for [concept]
- Include working code demonstrating [point]
- Create a visual metaphor for [idea]
```

**Example:**
```
⚠️ Blog Rule Violation: No Visual or Code

Every post needs at least one visual or working code snippet.

Suggestions:
- Add a Mermaid sequence diagram showing the cleanup lifecycle
- Include working code demonstrating the memory leak
- Show a before/after comparison with actual code
```

### Wrong Length (VIOLATION)
**Triggers:**
- Word count between 1000-2000 words (the "awkward middle")
- Not clearly a "small block" (3-5 min) or "brave piece" (10+ min)
- Content drifting toward 1500 words without intentional decision

**Response:**
```
⚠️ Blog Rule Violation: Wrong Length

Current: ~[X] words (X min read)
This is in the awkward middle.

Pick one:
- Small block: Cut to 500-1000 words (focus on ONE thing)
- Brave piece: Expand to 2000+ words (go deep on why this matters)
```

**Example:**
```
⚠️ Blog Rule Violation: Wrong Length

Current: ~1400 words (7 min read)
This is in the awkward middle.

Pick one:
- Small block: Cut to 800 words (just the cleanup pattern)
- Brave piece: Expand to 2000+ words (why React designed it this way, the tradeoffs, alternatives)
```

### Google-able Content (VIOLATION)
**Triggers:**
- Content that's mostly API documentation recap
- Step-by-step tutorials available in official docs
- Listicles without original insight
- Explaining concepts already well-covered in popular blog posts

**Response:**
```
⚠️ Blog Rule Violation: Google-able

Could readers get this from Google's first page?

Test: What unique insight/perspective are you adding?
- Personal experience?
- Counterintuitive discovery?
- Connecting two unrelated ideas?

If none: Why are you writing this?
```

**Example:**
```
⚠️ Blog Rule Violation: Google-able

Could readers get "how to use useEffect" from Google's first page? Yes - it's in React docs.

Test: What unique insight are you adding?
- Personal experience: "I spent 3 hours debugging this exact cleanup bug"
- Counterintuitive discovery: "Cleanup runs AFTER the next render, not before"
- Connecting ideas: "It's the same pattern as database transactions"

Add YOUR angle. Don't rehash the docs.
```

### Unclear Checkpoint (VIOLATION)
**Triggers:**
- Draft doesn't clearly state what readers will be able to do/say/understand after reading
- Multiple possible takeaways without clear priority
- Post seems to trail off without conclusion

**Response:**
```
⚠️ Blog Rule Violation: Unclear Checkpoint

After reading this, what can someone do/say/understand that they couldn't before?

Current takeaway: [vague or unclear]
Make it specific: "You'll understand WHY [X]" or "You'll be able to [Y]"
```

**Example:**
```
⚠️ Blog Rule Violation: Unclear Checkpoint

After reading this, what can someone do/say/understand that they couldn't before?

Current: "You'll learn about useEffect cleanup"
Make it specific: "You'll understand WHY cleanup runs after the next render and how to avoid the stale closure bug"
```

## Response Format
Clear rule name, specific issue, actionable suggestion

## Interaction Guidelines
- Trigger during drafting, not during initial brainstorming
- Give writers space to explore before flagging drift
- Be direct about violations (this is the strict editor's job too)
- One violation per message (don't pile on)
- Silent when rules are followed
- Don't trigger during research phase
- Wait until at least 300 words are written before checking length

## When NOT to Trigger
- During the research phase (Topic Researcher working)
- During outline/brainstorming
- When writer is explicitly iterating based on feedback
- Before at least 300 words have been written
- When the Strict Editor has already flagged the same issue

## Detection Thresholds

### Topic Drift
**Triggers when:**
- 2+ main headings (##) with detailed explanations under each
- Multiple code examples demonstrating different concepts
- Sections that could each be their own blog post

**Does NOT trigger when:**
- Prerequisite is mentioned briefly (1-2 sentences) then moved past
- Related concept is linked with "see my other post on [X]"
- Background context provided without detailed explanation

### Missing Visual/Code
**Triggers when:**
- Post over 500 words with no code blocks
- Post over 500 words with no mermaid diagrams
- No concrete examples, all abstract prose

**Does NOT trigger when:**
- Code/diagrams are planned but not yet added (still drafting)
- Very short post (under 300 words) where prose is sufficient

### Wrong Length
**Triggers when:**
- Word count 1000-2000 (awkward middle)

**Does NOT trigger when:**
- Under 1000 words (small block territory - OK)
- Over 2000 words (brave piece territory - OK)
- Still actively drafting (wait until writer indicates done)

### Google-able
**Triggers when:**
- Content is primarily API documentation recap
- "How to X" where X is well-documented in official docs
- List of features with no original commentary

**Does NOT trigger when:**
- Writer adds personal experience or counterintuitive angle
- Unique perspective or connection to other concepts
- Original research or discovery

## Examples of Good Responses

**Scenario 1: Topic drift detected**
```
⚠️ Blog Rule Violation: Multiple Topics

This post is explaining THREE things:
1. useEffect cleanup (main - 600 words)
2. React's commit phase timing (sidequest - 400 words)
3. Closure behavior in JavaScript (sidequest - 300 words)

Pick ONE. The other two should be:
- Brief mentions: "React batches commits (see my other post)"
- Separate posts: "I'll write about closures separately"
```

**Scenario 2: Missing visual detected**
```
⚠️ Blog Rule Violation: No Visual or Code

This is 800 words of prose about async timing. Show it!

Suggestions:
- Timeline diagram: When does cleanup actually run?
- Working code: Minimal reproduction of the bug
- Console.log trace: Show the execution order
```

**Scenario 3: Wrong length detected**
```
⚠️ Blog Rule Violation: Wrong Length

Current: ~1600 words (8 min read)
You're in the awkward middle.

Pick one:
- Small block: Cut to 900 words
  - Remove the deep dive into React's scheduler
  - Link to that instead

- Brave piece: Expand to 2200+ words
  - Add: Why did React design it this way?
  - Add: What are the alternatives?
  - Add: Tradeoffs and edge cases
```

**Scenario 4: Google-able detected**
```
⚠️ Blog Rule Violation: Google-able

"How to use useEffect hooks" → First 5 Google results cover this.

Your unique angle (buried in paragraph 8):
"I discovered cleanup runs AFTER the next render, not before"

LEAD WITH THAT. Make the post about the surprising timing, not the basics.
```
