---
title: "Hands-On Code Examples: Complete Runnable Examples"
description: "Complete, runnable examples covering everything from hello world to complex production workflows. Copy, paste, and learn by doing."
date: 2026-02-21
part: 7
series: "Mastering Claude Code"
series_order: 7
prev: "../chapters/05-next-steps.md"
next: null
tags: ["claude-code", "examples", "code", "hands-on", "tutorial"]
---

# Part 7: Hands-On Code Examples

This part provides complete, runnable examples you can try immediately. Each example includes the full interaction pattern, expected output, and key learnings.

---

## Section 1: Getting Started Examples

# Hello World Examples

First interactions with Claude Code.

## Example 1: Your First Claude Code Session

```bash
# Start Claude Code
claude

# Ask about the current directory
You: what files are in this directory?

# Create a simple file
You: create a hello.py file that prints "Hello from Claude Code!"

# Run the file
You: run the python file

# Expected output:
# Hello from Claude Code!
```

## Example 2: Simple Bug Fix

```bash
# Start with broken code
echo 'def greet(name):
    print("Hello, " + name + "!")

greet()  # Missing argument!' > buggy.py

# Start Claude
claude

# Ask Claude to fix it
You: fix the bug in buggy.py - it's missing an argument

# Claude will:
# 1. Read buggy.py
# 2. Identify the issue (missing name parameter)
# 3. Ask how you want it fixed
# 4. Update the code
```

## Example 3: Understanding Existing Code

```bash
claude

# Paste this code and ask Claude to explain it
You: Explain what this Python code does:

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Claude will:
# - Identify it as a recursive Fibonacci implementation
# - Explain how it works
# - Point out performance issues (exponential time)
# - Suggest optimizations (memoization)
```

## Common Commands for Beginners

| Command | What It Does |
|---------|-------------|
| `claude` | Start new session |
| `claude -c` | Continue last session |
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `Ctrl+C` | Exit Claude Code |
| `Esc` | Stop current action |
| `Shift+Tab` | Change permission mode |

## Tips

- Start simple: Ask Claude to explain files before changing them
- Be specific: "create a Python script that..." vs "make a script"
- Let Claude run commands: Say "run the tests" not just "write tests"
- Press Esc to stop: You can interrupt Claude anytime


---

## Section 2: Context Management in Practice

# Context Management Examples

Practical examples of managing Claude's context window.

## Example 1: Monitoring Context

```bash
claude

# Check current context usage
You: /context

# Expected output:
# Token usage: 12,450 / 200,000 (6%)
#
# Breakdown:
# - System prompt: 8,200 tokens
# - Conversation: 3,100 tokens
# - Tool outputs: 1,150 tokens
```

## Example 2: When to Clear Context

**❌ Bad: Polluted Context**
```bash
# Session 1: Debug authentication (30k tokens)
You: fix the login bug
[...long debugging session...]

# Session continues: Add unrelated feature (context now 65k tokens)
You: add a dark mode toggle
[...Claude struggles, slower responses...]

# Session continues: Refactor (context 95k tokens)
You: refactor the API layer
[...Claude makes mistakes, forgets earlier decisions...]
```

**✅ Good: Fresh Context**
```bash
# Session 1: Debug authentication
You: fix the login bug
[...debugging complete...]
You: /context
# Result: 30k tokens used

You: /clear

# Session 2: New feature with clean context
You: add a dark mode toggle
[...fast, accurate responses...]
```

## Example 3: Document & Clear Pattern

**For multi-hour features:**

```bash
# Hour 1: Start feature
You: build a user profile page with avatar upload

[...work happens...]

# Hour 1 end: Document progress
You: "Document your implementation to PROFILE_PROGRESS.md with:
- What's complete
- What's pending
- Architecture decisions
- Files changed"

[Claude creates detailed progress doc]

You: /context
# Result: 58k tokens (29%)

You: /clear

# Hour 2: Resume fresh
You: read PROFILE_PROGRESS.md and continue with the pending items

[...continues with fresh context...]
```

## Example 4: Using CLAUDE.md for Persistent Rules

**Instead of this (repeated each session):**
```bash
claude
You: use TypeScript strict mode, prefer async/await, put tests in __tests__/

# Next session:
claude
You: remember to use TypeScript strict mode, prefer async/await...
[Wasteful, pollutes context]
```

**Do this (one-time setup):**
```bash
# Create CLAUDE.md in project root
cat > CLAUDE.md << 'EOF'
# Project: My App

## Code Style
- TypeScript strict mode
- Prefer async/await over callbacks
- Tests in __tests__/ directories

## Commands
- Test: npm test
- Build: npm run build
- Dev: npm run dev
EOF

# Now every session has these rules automatically
claude
You: add a new API endpoint
# Claude automatically follows CLAUDE.md rules
```

## Example 5: Subagents for Research

**Keep main context clean by delegating research:**

```bash
claude

# Main task: Implement feature
You: add OAuth authentication

# Need to research but don't want to pollute context:
You: use a subagent to research which OAuth library to use for Next.js.
Compare next-auth vs auth0 vs clerk. Don't pollute our current context.

[Subagent spawns, researches in separate context, returns findings]
[Your main context stays focused on implementation]

You: based on the research, use next-auth and implement Google OAuth
```

## Token Budgets by Activity

| Activity | Typical Token Usage | Recommendation |
|----------|---------------------|----------------|
| Simple bug fix | 5k - 15k | No need to clear |
| Feature implementation | 30k - 60k | Clear when done |
| Large refactor | 60k - 100k | Document & clear midway |
| Long debugging | 40k - 80k | Clear after solving |
| Research/exploration | 20k - 40k | Use subagent or clear after |

## Best Practices Summary

1. **Check context regularly**: `/context` every 30-60 minutes
2. **Clear at 60-70%**: Don't wait until 100%
3. **Document before clearing**: Create progress markdown files
4. **Use CLAUDE.md**: For rules that apply to all sessions
5. **Use subagents**: For research that would pollute context
6. **Start fresh for new tasks**: New feature = new session


---

## Section 3: Production CLAUDE.md Configuration

# CLAUDE.md Example

This is a template for a production-ready CLAUDE.md file.

---

# Project: E-Commerce Platform

Modern e-commerce platform built with Next.js 14, TypeScript, Prisma, and Tailwind CSS.

## Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Database**: PostgreSQL via Prisma ORM
- **Styling**: Tailwind CSS + shadcn/ui components
- **Auth**: NextAuth.js v5
- **Payments**: Stripe
- **Email**: Resend
- **Testing**: Vitest + React Testing Library + Playwright

## Code Style

### TypeScript
- Use strict mode (`strict: true` in tsconfig.json)
- Prefer `type` over `interface` for object shapes
- Use Zod for runtime validation
- No `any` types - use `unknown` if type is truly unknown

### React
- Prefer Server Components by default
- Use "use client" directive only when needed (interactivity, hooks, browser APIs)
- Keep components small (<150 lines)
- Extract logic into custom hooks or utilities

### File Structure
```
app/                    # Next.js app router pages
  ├── (auth)/          # Auth pages (grouped route)
  ├── (shop)/          # Shop pages (grouped route)
  └── api/             # API routes
components/            # React components
  ├── ui/              # shadcn/ui components (auto-generated)
  └── [feature]/       # Feature-specific components
lib/                   # Utilities and shared logic
  ├── db/              # Database queries and schemas
  ├── auth/            # Authentication helpers
  └── utils/           # General utilities
prisma/                # Database schema and migrations
tests/                 # Test files
  ├── unit/
  ├── integration/
  └── e2e/
```

### Naming Conventions
- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatCurrency.ts`)
- Constants: UPPER_SNAKE_CASE (`MAX_CART_ITEMS`)
- Database models: PascalCase singular (`User`, `Product`)
- API routes: lowercase with hyphens (`/api/user-profile`)

## Commands

### Development
```bash
npm run dev          # Start dev server (localhost:3000)
npm run build        # Build for production
npm run start        # Start production server
```

### Database
```bash
npx prisma studio    # Open Prisma Studio (database GUI)
npx prisma migrate dev --name <name>   # Create and apply migration
npx prisma generate  # Regenerate Prisma Client
npm run db:seed      # Seed database with test data
npm run db:reset     # Reset database (dev only!)
```

### Testing
```bash
npm test                     # Run all unit/integration tests
npm test -- path/to/file     # Run specific test file
npm run test:e2e             # Run Playwright E2E tests
npm run test:coverage        # Generate coverage report
```

### Linting & Formatting
```bash
npm run lint         # Run ESLint
npm run lint:fix     # Fix auto-fixable issues
npm run format       # Format with Prettier
npm run typecheck    # Run TypeScript compiler check
```

## Development Workflow

### Before Committing
1. Run typecheck: `npm run typecheck`
2. Run tests: `npm test`
3. Run lint: `npm run lint`
4. All three must pass before committing

### Adding a New Feature
1. Create feature branch: `git checkout -b feature/name`
2. Implement with tests
3. Run full test suite
4. Create PR with description and test plan
5. Ensure CI passes before merging

### Database Changes
1. Update `prisma/schema.prisma`
2. Create migration: `npx prisma migrate dev --name descriptive-name`
3. Verify in Prisma Studio
4. Update seed data if needed
5. Test locally before committing

## Architecture Patterns

### API Routes
- Use Next.js Route Handlers (app/api/)
- Return standardized responses:
  ```typescript
  // Success
  return NextResponse.json({ data: result }, { status: 200 })

  // Error
  return NextResponse.json({ error: "Message" }, { status: 400 })
  ```
- Validate input with Zod schemas
- Handle errors with try/catch
- Use middleware for auth checks

### Database Queries
- All queries go in `lib/db/[model].ts`
- Export functions, don't export raw Prisma client
- Example:
  ```typescript
  // lib/db/users.ts
  export async function getUserById(id: string) {
    return prisma.user.findUnique({ where: { id } })
  }
  ```

### Error Handling
- Use custom error classes (in `lib/errors.ts`)
- Log errors with structured logging
- Return user-friendly messages to clients
- Never expose stack traces to users in production

### Authentication
- All API routes requiring auth should check `await auth()` from NextAuth
- Protected pages use middleware (see `middleware.ts`)
- Store minimal data in JWT (just id, email, role)

## Testing Guidelines

### Unit Tests
- Test utilities and business logic
- Use Vitest
- Aim for 80%+ coverage on critical paths
- Mock external dependencies

### Integration Tests
- Test API routes
- Use test database (configured in `.env.test`)
- Clean up after tests

### E2E Tests
- Test critical user flows (signup, checkout, etc.)
- Use Playwright
- Run against local dev server
- Keep under 20 tests (they're slow)

## Environment Variables

Required variables (see `.env.example`):

- `DATABASE_URL`: PostgreSQL connection string
- `NEXTAUTH_SECRET`: Secret for NextAuth
- `NEXTAUTH_URL`: App URL
- `STRIPE_SECRET_KEY`: Stripe API key
- `RESEND_API_KEY`: Resend email API key
- `NEXT_PUBLIC_APP_URL`: Public app URL

**Never commit `.env` files!**

## Common Gotchas

1. **Prisma Client**: Regenerate after schema changes (`npx prisma generate`)
2. **Cache**: Clear Next.js cache if builds act weird (rm -rf .next)
3. **Server Components**: Can't use hooks or browser APIs
4. **Environment Variables**: Must restart dev server after changes
5. **Prisma in Development**: Use `prisma migrate dev`, not `migrate deploy`

## Helpful Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Prisma Docs](https://www.prisma.io/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [NextAuth.js v5](https://authjs.dev/)

---

**Last Updated**: 2024-02-20
**Team**: Keep this file under 200 lines. Remove outdated information.


---

## Section 4: Real-World Workflow Examples

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


---

## Summary: Key Principles from All Examples

After reviewing all these examples, you'll notice several universal patterns:

### 1. Always Verify

Every example includes verification steps:
- Run tests after code changes
- Check typecheck/lint after refactors
- Manual testing for UI changes
- Use `/context` to monitor token usage

### 2. Incremental Progress

Break large tasks into smaller steps:
- Fix one file at a time in refactors
- Test after each increment
- Document progress for long sessions
- Clear context between unrelated tasks

### 3. Clear Communication

Be specific with Claude:
- Provide full error messages and stack traces
- Define success criteria explicitly
- Specify test frameworks and patterns
- Include context about your project setup

### 4. Context is Currency

Manage your context window actively:
- Use `/clear` between tasks
- Document before clearing for continuity
- Use CLAUDE.md for persistent rules
- Delegate research to subagents

### 5. Plan Before Executing

For complex features:
- Start in Plan Mode
- Review the plan
- Execute in Auto-Accept Mode
- Verify manually when needed

### 6. Leverage Automation

Create reusable workflows:
- Custom skills for repeated patterns
- Hooks for safety and compliance
- CI/CD integration for team workflows
- MCP servers for external integrations

## Next Steps: Apply What You've Learned

Now that you've seen these examples, try building something real:

1. **Choose a small feature** in your current project
2. **Use Plan Mode** to create an implementation plan
3. **Execute incrementally** with tests at each step
4. **Document your progress** if it's a multi-hour task
5. **Commit and create PR** using Claude

Remember: The best way to learn Claude Code is by using it. Start small, build confidence, then tackle bigger challenges.

---

## Additional Resources

- **Official Examples**: [GitHub Repository](https://github.com/anthropics/claude-code/tree/main/examples)
- **Video Tutorials**: [Support Portal](https://support.claude.com/en/collections/10548294-video-tutorials)
- **Community Discord**: [Join 61k+ developers](https://discord.com/invite/6PPFFzqPDZ)
- **Blog Posts**: [Builder.io Guide](https://www.builder.io/blog/claude-code)

---

**Series Navigation**:
- [← Part 5: Next Steps](../chapters/05-next-steps.md)
- **Part 7: Hands-On Code Examples** (You are here)
- [↑ Back to Series Introduction](../00-introduction.md)

---

*Part of the "Mastering Claude Code" series*
*All examples verified with Claude Code 2.1.50+*
