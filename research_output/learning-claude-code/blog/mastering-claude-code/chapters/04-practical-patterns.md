---
title: "Practical Patterns: Build Real Workflows"
description: "Learn battle-tested patterns for fixing bugs, implementing features, writing tests, refactoring, and debugging with Claude Code."
date: 2026-02-21
part: 4
series: "Mastering Claude Code"
series_order: 4
prev: "03-core-concepts.md"
next: "05-next-steps.md"
tags: ["claude-code", "patterns", "workflows", "best-practices"]
---

# Part 4: Practical Patterns

Build real workflows and solve actual problems.

### Pattern 1: Fix a Bug (Beginner)

**Scenario**: You have a failing test or error message.

**Workflow**:
```bash
# Start with error information
claude

You: "I'm seeing this error when I run npm test:
     TypeError: Cannot read property 'id' of undefined
     at UserService.getUser (src/services/user.ts:42)"

# Claude's process:
# 1. Reads the error stack trace
# 2. Opens src/services/user.ts:42
# 3. Analyzes context around line 42
# 4. Identifies null/undefined issue
# 5. Searches for how getUser is called
# 6. Proposes fix with null check
# 7. Updates code
# 8. Runs npm test to verify
# 9. Reports: "✓ All tests pass"
```

**Key success factors**:
- ✅ Paste full error message (stack trace helps)
- ✅ Mention how to reproduce (what command)
- ✅ Let Claude run tests to verify fix

**What not to do**:
- ❌ "Fix the bug" (too vague - which bug?)
- ❌ Only paste error snippet (need full context)
- ❌ Skip test verification (how do you know it worked?)

---

### Pattern 2: Implement a Feature (Intermediate)

**Scenario**: Add new functionality across multiple files.

**Recommended workflow**: **Plan → Review → Execute**

**Step 1: Start in Plan Mode**
```bash
claude --permission-mode plan

You: "I want to add a 'forgot password' flow. Users should be able to:
1. Request a password reset link via email
2. Click the link to get a reset form
3. Set a new password

We're using Next.js 14 with Prisma and NextAuth. What files need to change?"
```

**Claude in Plan Mode**:
- ✅ Reads existing auth code
- ✅ Identifies relevant files
- ✅ Creates detailed plan
- ❌ Doesn't make any changes yet

**Step 2: Review the Plan**
```
Claude's plan:
1. Database: Add passwordResetToken and passwordResetExpires to User model
2. API Route: Create /api/auth/reset-password (request reset)
3. API Route: Create /api/auth/reset-password/[token] (verify and reset)
4. Email Service: Add sendPasswordResetEmail function
5. UI Component: Create ResetPasswordForm component
6. Page: Add app/reset-password/[token]/page.tsx
7. Tests: Add tests for new API routes

Would you like me to proceed with this plan?
```

**You**: "Yes, but use Resend instead of our current email service. Let's also add rate limiting to prevent abuse."

**Step 3: Execute with Modifications**
```bash
Shift+Tab  # Switch to Normal or Auto-Accept mode

You: "Implement the plan with the changes I mentioned. After each major step, run tests."
```

**Claude's execution**:
```
[Step 1] Updating Prisma schema...
[Step 1] Running: npm run db:push
[Step 1] ✓ Database updated

[Step 2] Creating /api/auth/reset-password route...
[Step 2] Adding rate limiting with upstash/ratelimit...
[Step 2] Running: npm test api/auth/reset-password.test.ts
[Step 2] ✓ 8/8 tests pass

[Step 3] Integrating Resend for emails...
[... continues through all steps ...]

[Complete] All 7 steps done. 24/24 tests pass.
```

**Step 4: Manual Verification**
```bash
You: "Start the dev server and open the reset password page"
Claude: [Runs npm run dev, provides URL]

# You test manually in browser

You: "Works! Create a commit and PR"
Claude: [Creates descriptive commit, pushes, opens PR with summary]
```

**Key success factors**:
- ✅ **Clear requirements up front** (user stories, acceptance criteria)
- ✅ **Plan first** for multi-file changes
- ✅ **Test after each major step** (not just at the end)
- ✅ **Manual verification** for UI/UX changes

---

### Pattern 3: Write Tests for Existing Code (Intermediate)

**Scenario**: You have untested code that needs coverage.

**Workflow**:
```bash
claude

You: "The functions in src/utils/validation.ts have no tests. Write comprehensive tests covering:
- Happy path cases
- Edge cases (empty strings, null, undefined)
- Invalid inputs
- Boundary conditions

Use Vitest (our testing framework). Put tests in src/utils/validation.test.ts.
Run the tests when done and make sure they all pass."
```

**Claude's process**:
```
[Read] src/utils/validation.ts
[Analyze] Found 5 functions: validateEmail, validatePhone, validateZipCode, validateUrl, validateUsername

[Write] src/utils/validation.test.ts
  ├── describe('validateEmail')
  │   ├── it('accepts valid email addresses')
  │   ├── it('rejects invalid formats')
  │   ├── it('handles edge cases')
  │   └── it('handles null/undefined')
  ├── describe('validatePhone')
  │   ├── ... (similar structure)
  └── ... (for each function)

[Run] npm test src/utils/validation.test.ts
[Result] ✓ 43/43 tests pass
[Coverage] 100% line coverage on validation.ts
```

**Pro workflow: Test-Driven Development (TDD)**

**Write tests FIRST, then implementation**:
```bash
You: "I need a function calculateShippingCost(weight, distance, expedited).
Write tests first covering:
- Standard shipping: $5 base + $0.50/lb + $0.10/mile
- Expedited adds 50% surcharge
- Free shipping over $50
- Weight and distance must be positive

The tests should fail initially. Then implement the function to make them pass."
```

**Claude follows Red-Green-Refactor**:
```
[Red] Write tests -> Run -> ✗ 8/8 tests fail (function doesn't exist)
[Green] Implement calculateShippingCost -> Run -> ✓ 8/8 pass
[Refactor] Extract constants, simplify logic -> Run -> ✓ 8/8 pass
```

**Key success factors**:
- ✅ Specify test framework (Vitest, Jest, pytest, etc.)
- ✅ Define what to test (happy path + edge cases)
- ✅ Ask Claude to run tests and verify
- ✅ For TDD: Explicitly say "write tests first"

---

### Pattern 4: Refactor Across Multiple Files (Advanced)

**Scenario**: Update a pattern throughout your codebase.

**Example**: Migrate from CommonJS to ES Modules

**Workflow**:
```bash
claude --permission-mode plan  # Start safe

You: "Search for all files using CommonJS (require/module.exports).
List them and show me how many files are affected. Don't change anything yet."
```

**Claude's reconnaissance**:
```
[Search] grep -r "require\(.*\)" --include="*.js"
[Search] grep -r "module\.exports" --include="*.js"

Found 23 files using CommonJS:
- src/utils/*.js (8 files)
- src/services/*.js (12 files)
- src/config/*.js (3 files)

Total: 23 files, ~400 import/export statements to update
```

**You (review scope)**: "That's more than I expected. Let's start with just src/utils/ first. Convert those 8 files to ESM. After each file, run tests."

**Switch to Auto-Accept for batch operations**:
```bash
Shift+Tab  # to Auto-Accept mode

You: "Convert the 8 utils files. After each file conversion, run: npm test -- src/utils/"
```

**Claude's execution** (auto-accept = no prompts per file):
```
[1/8] src/utils/string.js
  ├── Changed: const foo = require('./bar') -> import foo from './bar'
  ├── Changed: module.exports = {...} -> export default {...}
  ├── Renamed: string.js -> string.mjs
  ├── Run: npm test -- src/utils/string.test.js
  └── ✓ 12/12 tests pass

[2/8] src/utils/array.js
  ├── ...
  └── ✓ 8/8 tests pass

... [continues through all 8 files] ...

[Complete] All 8 files converted. 67/67 tests passing.
```

**Verify and commit**:
```bash
You: "Show me a summary git diff"
Claude: [Runs git diff --stat, shows changes]

You: "Looks good. Create a commit with a clear message"
Claude: [Commits with: "refactor(utils): migrate from CommonJS to ESM"]
```

**Key success factors**:
- ✅ **Scope discovery first** (understand impact before changing)
- ✅ **Incremental changes** (8 files, not 23 at once)
- ✅ **Test after each unit** (catches breaks immediately)
- ✅ **Use Auto-Accept for batch work** (reduces friction)

**What could go wrong**:
- ❌ Changing all 23 files at once (too much to verify)
- ❌ Skipping tests (silent breakage)
- ❌ Losing track of changes (hard to review)

---

### Pattern 5: Debug from Logs/Errors (Advanced)

**Scenario**: Production error or complex debugging.

**Workflow**:
```bash
claude

You: "We're seeing intermittent 500 errors in production. Here's the log:

2026-02-20 14:32:18 ERROR [api] POST /api/orders 500 Internal Server Error
   at OrderService.create (src/services/order.ts:156)
   at async POST /api/orders +142ms
   Error: Cannot read property 'total' of undefined

This happens about 5% of the time. Can you investigate?"
```

**Claude's debugging strategy**:
```
[Read] src/services/order.ts:156
[Analyze] Line 156: const tax = order.cart.total * 0.08
[Hypothesis] order.cart might be null/undefined sometimes

[Search] How is order.cart populated?
[Read] src/services/cart.ts
[Find] cart might be null if session expired

[Search] Error logs for pattern
[Find] Errors correlate with old session IDs

[Diagnosis] Race condition: User's cart session expires between
            adding items and checking out

[Propose Fix]
1. Add null check for order.cart
2. Return 400 Bad Request with clear error if cart expired
3. Add logging to track session expiry events
4. Add test case for expired cart scenario
```

**You**: "Good analysis. Implement the fix with all four improvements."

**Claude implements**:
```
[Edit] src/services/order.ts
  ├── Added: if (!order.cart) throw new BadRequestError('Cart expired')
  ├── Added: logger.warn('Cart expiry during checkout', { userId, sessionId })

[Edit] src/services/order.test.ts
  ├── Added: test('returns 400 when cart expired')

[Run] npm test src/services/order.test.ts
[Result] ✓ 24/24 tests pass (including new test)

[Create] Error message improvement:
  └── "Your shopping cart has expired. Please add items again."
```

**Key success factors**:
- ✅ Provide **full error messages** (stack traces are gold)
- ✅ Provide **context** (when does it happen? how often?)
- ✅ Let Claude **search** and **read** code to understand root cause
- ✅ Ask for **tests** that reproduce the bug

**Pro tip**: For hard-to-reproduce bugs, ask Claude to add logging first, then fix.

---

### Pattern 6: Context Management for Long Sessions (Advanced)

**Scenario**: Multi-hour session building a complex feature.

**Anti-pattern (what NOT to do)**:
```bash
# Hour 1: Implement authentication
# Hour 2: Add API endpoints
# Hour 3: Build UI components
# Hour 4: Debug integration
# [Context at 95%]
# Hour 5: Claude starts making mistakes, forgetting earlier decisions
# Hour 6: You're correcting Claude's corrections
```

**Recommended pattern: "Document & Clear"**

**Hour 1**:
```bash
You: "Build authentication system for our app. Use NextAuth with Prisma."
[...work happens...]
Claude: "Authentication complete. Tests passing."

You: "Document your implementation to AUTH_PROGRESS.md including:
- What you built
- Architecture decisions
- What still needs to be done
- Any issues or TODOs

Then check context usage with /context"
```

**Claude creates**:
```markdown
# AUTH_PROGRESS.md

## ✅ Completed (2024-02-20, 2:30 PM)

### Implementation
- Installed NextAuth.js v5
- Configured providers: GitHub, Google, Email
- Prisma schema: User, Account, Session, VerificationToken tables
- API route: /api/auth/[...nextauth]

### Architecture Decisions
- Using JWT strategy (not database sessions) for better performance
- Email verification required for email/password signups
- Session expires after 30 days

### Files Created/Modified
- app/api/auth/[...nextauth]/route.ts
- lib/auth/config.ts
- prisma/schema.prisma (updated)
- .env (added AUTH_SECRET, GITHUB_ID, GOOGLE_ID)

## 🔄 TODO Next
- Add protected route middleware
- Create login/signup UI components
- Add role-based permissions
- Test OAuth flows manually

## ⚠️ Issues
- None currently
```

**Context check**:
```bash
Claude: /context
[Result] Token usage: 67,234 / 200,000 (34%)
```

**Hour 2** (fresh start):
```bash
You: /clear
[Context reset]

You: "Read AUTH_PROGRESS.md and continue with the TODO items. Start with protected route middleware."
```

**Benefits**:
- ✅ Fresh context (fast, accurate responses)
- ✅ Documented decisions (searchable, reviewable)
- ✅ Clear handoff between sessions
- ✅ Can resume days later

**Alternative: Use subagents for investigation**:
```bash
You: "Use a subagent to investigate how to implement rate limiting for our API.
Don't pollute our current context. Report back with findings."

[Subagent spawns with separate context]
[Subagent researches, returns summary]
[Main context remains clean]
```

**Key success factors**:
- ✅ **Monitor context**: Run `/context` every hour
- ✅ **Clear at 60-70%**: Don't wait until 100%
- ✅ **Document before clearing**: Create progress files
- ✅ **Use subagents for research**: Keep main context focused

---

---

**Next**: [Part 5: Next Steps →](05-next-steps.md)

**Series Navigation**:
- [← Part 3: Core Concepts](03-core-concepts.md)
- **Part 4: Practical Patterns** (You are here)
- [Part 5: Next Steps →](05-next-steps.md)

---

*Part of the "Mastering Claude Code" series*
