# Example 3: Real Application - Cross-Layer Feature Development

This example demonstrates building a complete feature using agent teams working across frontend, backend, database, and testing layers in parallel.

## What This Example Shows

- Task decomposition for parallel work
- Managing dependencies between teammates
- Plan approval workflow
- File ownership to prevent conflicts
- Full-stack development with agent teams

## The Feature

Build a **User Profile Update** system with:
- Database migration for profile fields
- REST API endpoint (PUT /api/users/:id/profile)
- React frontend component (ProfileEdit)
- End-to-end tests

## Files

- `team_prompt.txt` — The prompt to create the development team
- `project_structure.md` — Initial project setup
- `task_plan.md` — How work is decomposed
- `expected_workflow.md` — What to expect during development

## Setup

```bash
# Create project structure
mkdir -p profile-feature/{backend,frontend,tests,migrations}
cd profile-feature

# Create placeholder files
touch backend/__init__.py
touch frontend/package.json
touch tests/conftest.py
touch migrations/.gitkeep

# Enable agent teams
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Start Claude Code
claude
```

## Run This Example

1. Read `team_prompt.txt`
2. Paste the prompt into Claude Code
3. Claude will:
   - Spawn 4 teammates
   - Each teammate requests plan approval
   - Review and approve plans
   - Teammates implement in parallel
   - Integration teammate verifies everything works

## Task Decomposition

### Database Teammate
**Files:** `migrations/001_add_profile_fields.sql`
**Dependencies:** None (can start immediately)
**Tools:** Read, Write, Bash

**Tasks:**
- Create migration for profile fields (bio, avatar_url, updated_at)
- Add indexes
- Write migration rollback
- Test migration

### API Teammate
**Files:** `backend/routes/profile.py`, `backend/tests/test_profile.py`
**Dependencies:** Database migration complete
**Tools:** Read, Write, Bash

**Tasks:**
- Implement PUT /api/users/:id/profile endpoint
- Add request validation
- Add authentication check
- Write unit tests

### Frontend Teammate
**Files:** `frontend/ProfileEdit.tsx`, `frontend/ProfileEdit.test.tsx`
**Dependencies:** None (can start immediately)
**Tools:** Read, Write, Bash

**Tasks:**
- Create ProfileEdit React component
- Add form validation
- Style with Tailwind
- Write component tests

### Integration Teammate
**Files:** `tests/e2e/test_profile_flow.py`
**Dependencies:** API and Frontend complete
**Tools:** Read, Write, Bash

**Tasks:**
- Write end-to-end test for full flow
- Test database → API → frontend chain
- Verify error handling
- Performance test

## Expected Timeline

1. **Minute 0-2:** Team spawns, teammates analyze requirements
2. **Minute 2-4:** Plan approval requests arrive, you review and approve
3. **Minute 4-10:** Parallel implementation
   - Database and Frontend work simultaneously
   - API starts after database completes
   - Integration waits for API and Frontend
4. **Minute 10-12:** Integration testing and final report

## Key Concepts Demonstrated

### 1. Task Dependencies

```
Database Teammate (no deps) ────┐
                                 ├──> API Teammate ────┐
Frontend Teammate (no deps) ────┘                       ├──> Integration Teammate
                                                        │
                                                        ┘
```

### 2. File Ownership

Each teammate owns distinct files:
- **Database:** migrations/
- **API:** backend/routes/, backend/tests/
- **Frontend:** frontend/
- **Integration:** tests/e2e/

No conflicts possible!

### 3. Plan Approval

Before implementation, each teammate sends a plan:

```
[database-teammate]:
## Migration Plan

ALTER TABLE users ADD COLUMN (
  bio TEXT,
  avatar_url VARCHAR(500),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_updated ON users(updated_at);

Awaiting approval.
```

You respond: `Approve the database teammate's plan`

### 4. Progress Monitoring

Use `Ctrl+T` to see task status:

```
┌─────────────────────────────────────────┐
│ IN PROGRESS                             │
├─────────────────────────────────────────┤
│ ⚡ Create profile migration             │  (database-teammate)
│ ⚡ Build ProfileEdit component          │  (frontend-teammate)
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PENDING (BLOCKED)                       │
├─────────────────────────────────────────┤
│ ⏸ Implement profile API                │  (waiting for database)
│ ⏸ Write E2E tests                      │  (waiting for API + frontend)
└─────────────────────────────────────────┘
```

## Modify This Example

Try building other features:

1. **Authentication System**
   - Auth teammate: JWT implementation
   - Middleware teammate: Auth middleware
   - Frontend teammate: Login/logout UI
   - Security teammate: Security review

2. **Search Feature**
   - Search teammate: Elasticsearch integration
   - API teammate: Search endpoints
   - Frontend teammate: Search UI
   - Performance teammate: Query optimization

3. **Notification System**
   - Backend teammate: Notification service
   - Websocket teammate: Real-time delivery
   - Frontend teammate: Notification UI
   - Integration teammate: End-to-end flow

## Common Issues

**Issue:** Teammates start before dependencies complete
**Solution:** Use explicit task dependencies in spawn prompt

**Issue:** File conflicts when teammates edit same files
**Solution:** Assign distinct file ownership to each teammate

**Issue:** Integration tests fail
**Solution:** Ensure all teammates mark tasks complete before integration starts

**Issue:** Plan approval bottleneck
**Solution:** Pre-approve common patterns, require approval only for risky changes
