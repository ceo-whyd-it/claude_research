# Example Workflows

Real-world patterns for common Claude Code tasks.

## Workflow 1: TDD (Test-Driven Development)

```bash
claude

You: "I need a function calculateDiscount(price, discountPercent, isVIP).

Write tests FIRST that cover:
- Standard discount: $100 with 20% = $80
- VIP gets extra 5%: $100, 20%, VIP = $75
- 0% discount returns original price
- 100% discount returns $0
- Negative values throw error
- Non-VIP doesn't get extra discount

After tests are written and FAILING, implement the function to make them pass."
```

**Claude's process:**
```
[RED] Write tests in calculateDiscount.test.ts
[RED] Run: npm test
[RED] ✗ 6/6 tests fail (function doesn't exist)

[GREEN] Write calculateDiscount function
[GREEN] Run: npm test
[GREEN] ✓ 6/6 tests pass

[REFACTOR] Extract VIP_BONUS constant
[REFACTOR] Add input validation helper
[REFACTOR] Run: npm test
[REFACTOR] ✓ 6/6 tests still pass

✅ Complete: Function implemented with full test coverage
```

---

## Workflow 2: Understanding Unfamiliar Code

```bash
# Joined new project, need to understand auth system
claude --permission-mode plan  # Read-only mode

You: "I need to understand how authentication works in this codebase.

Find and explain:
1. What auth library/system is used
2. Where users are authenticated (middleware? route guards?)
3. How sessions are stored
4. Where user roles/permissions are checked
5. How to add a new protected route

Create a summary document with code references."
```

**Claude's process:**
```
[Search] grep -r "auth" --include="*.ts" --include="*.tsx"
[Read] middleware.ts
[Read] lib/auth/config.ts
[Read] app/api/auth/[...nextauth]/route.ts
[Analyze] How components interact

[Create] AUTH_SYSTEM.md with:
├── Architecture diagram
├── Flow explanation
├── Code examples
├── How to add protected routes
└── References to key files
```

---

## Workflow 3: Incremental Refactoring

**Goal**: Update error handling across 15 API routes

```bash
# Phase 1: Assess scope
claude --permission-mode plan

You: "Find all API routes in app/api/ and check their error handling.
List which ones don't use try/catch or proper error responses.
Don't change anything yet."

[Claude analyzes and reports: 12 out of 15 routes need updates]

# Phase 2: Create standard pattern
You: "Create a reusable error handler utility in lib/errors.ts following this pattern:
- Custom error classes (BadRequestError, UnauthorizedError, etc.)
- Helper function handleRouteError(error) that returns NextResponse
- Structured logging of errors

Write the utility and tests for it."

[Claude creates error handling utilities]

# Phase 3: Incremental updates
Shift+Tab  # Switch to Auto-Accept mode

You: "Update API routes one at a time. After each route:
1. Update to use new error utilities
2. Run tests for that specific route
3. Only proceed if tests pass

Start with app/api/users/route.ts"

[Claude updates routes incrementally, verifying each]

# Phase 4: Verify all
You: "Run the full test suite to ensure nothing broke"

[Claude runs: npm test]
[Result: ✓ 127/127 tests pass]

You: "Create a commit with a clear message explaining the refactor"
```

---

## Workflow 4: Feature Development (End-to-End)

**Build a "Save for Later" feature for e-commerce app**

### Phase 1: Planning
```bash
claude --permission-mode plan

You: "I want to add a 'Save for Later' feature. Users can:
1. Click 'Save for Later' on product cards
2. View saved items in their account
3. Move saved items to cart
4. Remove from saved list

We use Next.js 14, Prisma, NextAuth. Create a detailed plan."
```

**Claude creates plan:**
```markdown
## Implementation Plan: Save for Later

### Database (Prisma)
1. Create SavedItem model
   - userId (relation to User)
   - productId (relation to Product)
   - savedAt timestamp

### API Routes
1. POST /api/saved-items - Add item
2. GET /api/saved-items - List user's saved items
3. DELETE /api/saved-items/[id] - Remove item

### UI Components
1. SaveButton component (for product cards)
2. SavedItemsList component (for account page)
3. Update ProductCard to include SaveButton

### Tests
1. API route tests (Vitest)
2. Component tests (React Testing Library)
3. E2E test (Playwright)

### Files to Create/Modify
[Detailed file list...]
```

### Phase 2: Review & Adjust
```
You: "Good plan. Add rate limiting to the API routes (max 30 saves per hour).
Also use optimistic UI updates on the frontend."

Claude: [Updates plan with those requirements]

You: "Perfect. Let's proceed."
```

### Phase 3: Implementation
```bash
Shift+Tab  # to Auto-Accept mode

You: "Implement step by step. After each major component, run relevant tests.

Start with the database migration."
```

**Claude executes:**
```
[Step 1] Database
├── Update schema.prisma with SavedItem model
├── Run: npx prisma migrate dev --name add-saved-items
└── ✓ Migration applied successfully

[Step 2] API Routes (with rate limiting)
├── Create app/api/saved-items/route.ts
├── Create app/api/saved-items/[id]/route.ts
├── Add rate limiting middleware
├── Run: npm test -- app/api/saved-items/
└── ✓ 9/9 API tests pass

[Step 3] UI Components
├── Create components/SaveButton.tsx with optimistic updates
├── Create components/SavedItemsList.tsx
├── Update components/ProductCard.tsx
├── Run: npm test -- components/
└── ✓ 15/15 component tests pass

[Step 4] E2E Test
├── Create tests/e2e/saved-items.spec.ts
├── Run: npm run test:e2e -- saved-items
└── ✓ E2E test passes

[Complete] All components implemented. 24/24 tests passing.
```

### Phase 4: Manual Verification
```bash
You: "Start the dev server so I can test it manually"
Claude: [Runs: npm run dev]
Claude: "Server running at http://localhost:3000"

# You test in browser...

You: "Working perfectly! Commit and create PR"

Claude: [Creates commit and PR with detailed description]
```

---

## Workflow 5: Debugging Production Issues

**Scenario**: Users reporting "Payment failed" errors sporadically

```bash
claude

You: "We're getting reports of payment failures. Here's a Sentry error:

Error: Stripe payment failed
  at processPayment (app/api/checkout/route.ts:87)
  at POST (app/api/checkout/route.ts:34)

Sentry context:
- Occurs ~3% of checkouts
- Only on mobile browsers
- Usually between 6-8 PM
- User has valid card

Investigate and propose fixes."
```

**Claude's investigation:**
```
[Read] app/api/checkout/route.ts:87
[Analyze] Line 87: await stripe.paymentIntents.create(...)

[Read] Stripe SDK documentation
[Hypothesis] Possible timeout on slow mobile connections

[Search] Error logs for "timeout" near payment
[Find] Correlation with request timeouts

[Search] Stripe API configuration
[Find] Default timeout: 30 seconds
[Find] Mobile connections in evening: avg 45s response time

[Diagnosis]
- Stripe API calls timeout on slow connections
- No retry logic
- Error not caught gracefully

[Propose Fix]
1. Increase Stripe timeout to 90 seconds
2. Add retry logic (max 3 attempts)
3. Add loading state on frontend
4. Improve error messages for users
5. Add logging for slow payment requests
```

**You**: "Good analysis. Implement all 5 improvements. Add tests for the retry logic."

```
[Implement]
├── Update Stripe config with 90s timeout
├── Add retry helper with exponential backoff
├── Update frontend with loading states
├── Improve error messages
├── Add structured logging
├── Write tests for retry scenarios
├── Run: npm test
└── ✓ All tests pass including new retry tests

[Document]
└── Created PAYMENT_DEBUGGING.md with findings and solution
```

---

## Workflow 6: Code Review Automation

**Use Claude Code in CI/CD for PR reviews**

```yaml
# .github/workflows/claude-review.yml
name: Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          curl -fsSL https://claude.ai/install.sh | bash

          claude -p "Review this PR for:

          **Security**:
          - SQL injection vulnerabilities
          - XSS vulnerabilities
          - Exposed secrets or credentials
          - Improper authentication checks

          **Code Quality**:
          - Consistent with project patterns in CLAUDE.md
          - Proper error handling
          - Edge cases covered by tests
          - Performance issues (N+1 queries, etc.)

          **Tests**:
          - New code has tests
          - Tests cover edge cases
          - E2E tests for user-facing features

          Output as markdown. Be concise but thorough.
          Use ✅ for good, ⚠️ for warnings, ❌ for issues." \
          --output-format json > review.json

      - name: Post Review
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json'));

            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🤖 Claude Code Review\n\n${review.output}`
            });
```

---

## Workflow 7: Batch Operations

**Update 50 React components to use new icon library**

```bash
claude --permission-mode auto-accept

You: "We're migrating from react-icons to lucide-react.

Search for all files importing from 'react-icons'.
For each file:
1. Find the icon imports (e.g., import { FaUser } from 'react-icons/fa')
2. Find equivalent in lucide-react (FaUser -> User from lucide-react)
3. Update imports
4. Update icon usage (lucide uses different syntax)
5. Run typecheck after each file
6. Only proceed if typecheck passes

Start with components/ directory only (we'll do pages/ later)."
```

**Claude's process:**
```
[Search] Found 23 files in components/ using react-icons

[1/23] components/UserAvatar.tsx
├── Changed: FaUser -> User from lucide-react
├── Updated usage: <FaUser /> -> <User className="..." />
├── Run: npm run typecheck
└── ✓ No type errors

[2/23] components/Header.tsx
├── Changed: FaBars, FaSearch -> Menu, Search
├── Updated usage and props
├── Run: npm run typecheck
└── ✓ No type errors

... [continues for all 23 files] ...

[Complete] 23 files migrated. All typechecks passing.
[Summary] Changed 47 icon imports across 23 files.
```

---

## Key Patterns Summary

1. **TDD**: Write tests first, implement to make them pass
2. **Understand**: Use Plan Mode for read-only exploration
3. **Incremental Refactor**: One file at a time, test between each
4. **Feature Development**: Plan → Review → Execute → Verify
5. **Debug**: Let Claude investigate, propose, implement, test
6. **Automation**: Use Claude in CI/CD for reviews
7. **Batch Operations**: Auto-Accept mode for repetitive tasks

**Universal principle**: Always include verification (tests, typechecks, manual testing).
