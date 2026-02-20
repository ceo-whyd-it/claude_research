# Expected Workflow for Profile Feature Development

This document shows what to expect when running the cross-layer feature development example.

## Phase 1: Team Initialization (0-2 minutes)

```
🎯 Creating agent team with 4 teammates...
✓ Spawned database-teammate
✓ Spawned api-teammate
✓ Spawned frontend-teammate
✓ Spawned integration-teammate

Setting up task list at ~/.claude/tasks/profile-feature-team/
```

**What's happening:**
- Lead spawns all 4 teammates
- Each teammate gets its own context window
- Shared task list created
- Teammates begin analyzing requirements

## Phase 2: Plan Submission (2-4 minutes)

### Database Teammate Plan

```
[database-teammate]:
## Database Migration Plan

File: migrations/001_add_profile_fields.sql

### Up Migration
ALTER TABLE users ADD COLUMN bio TEXT;
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500);
ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE INDEX idx_users_updated_at ON users(updated_at);

### Down Migration (Rollback)
DROP INDEX IF EXISTS idx_users_updated_at;
ALTER TABLE users DROP COLUMN updated_at;
ALTER TABLE users DROP COLUMN avatar_url;
ALTER TABLE users DROP COLUMN bio;

### Testing Plan
1. Run migration up, verify columns exist
2. Insert test data
3. Run migration down, verify rollback
4. Re-run migration up to confirm repeatability

Awaiting approval to proceed.
```

**Your response:**
```
Approve the database teammate's plan
```

### API Teammate Plan

```
[api-teammate]:
## API Implementation Plan

File: backend/routes/profile.py

### Endpoint Specification
PUT /api/users/:id/profile

Request body:
{
  "bio": "string (max 500 chars)",
  "avatar_url": "string (valid URL)"
}

Responses:
- 200: {"bio": "...", "avatar_url": "...", "updated_at": "..."}
- 400: {"error": "Validation failed: ..."}
- 401: {"error": "Authentication required"}
- 403: {"error": "Can only update own profile"}
- 404: {"error": "User not found"}

### Implementation Steps
1. Add route decorator and handler function
2. Extract user_id from JWT token
3. Verify user_id matches :id parameter (authorization)
4. Validate bio length <= 500
5. Validate avatar_url is valid HTTP(S) URL
6. Update database
7. Return updated profile

### Test Coverage
- test_update_profile_success()
- test_update_profile_bio_too_long()
- test_update_profile_invalid_url()
- test_update_profile_unauthorized()
- test_update_profile_user_not_found()

File: backend/tests/test_profile.py

Waiting for database migration to complete.
Awaiting approval to proceed after dependency resolved.
```

**Your response:**
```
Approve the API teammate's plan
```

### Frontend Teammate Plan

```
[frontend-teammate]:
## ProfileEdit Component Plan

File: frontend/src/components/ProfileEdit.tsx

### Component Structure
- Form with 2 inputs (bio textarea, avatar URL text input)
- Real-time validation feedback
- Loading state during save
- Success/error message display
- Cancel and Save buttons

### Validation Rules
- Bio: Max 500 characters, show count
- Avatar URL: Must be valid HTTP(S) URL
- Show errors inline below each field

### State Management
- formData: {bio, avatar_url}
- errors: {bio, avatar_url}
- loading: boolean
- message: {type: 'success'|'error', text: string}

### API Integration
- PUT /api/users/:id/profile on submit
- Extract user ID from auth context
- Handle 200, 400, 401, 403, 404 responses

### Test Coverage (ProfileEdit.test.tsx)
- Renders form fields
- Shows validation errors
- Disables submit when invalid
- Shows loading state
- Displays success message
- Displays error message

Awaiting approval to proceed.
```

**Your response:**
```
Approve the frontend teammate's plan
```

### Integration Teammate Plan

```
[integration-teammate]:
## End-to-End Test Plan

File: tests/e2e/test_profile_update.py

### Test Scenarios

1. test_complete_profile_update_flow()
   - Create test user
   - Login to get auth token
   - Submit profile update via API
   - Verify database updated
   - Load profile in frontend
   - Verify UI shows updated data

2. test_profile_update_validation()
   - Submit bio >500 chars
   - Verify 400 response
   - Verify UI shows error message

3. test_profile_update_auth_required()
   - Submit without auth token
   - Verify 401 response
   - Verify redirect to login

4. test_profile_update_authorization()
   - User A tries to update User B's profile
   - Verify 403 response
   - Verify error message

### Test Infrastructure
- Use pytest-playwright for browser automation
- Use temporary test database
- Clean up after each test

Waiting for API and Frontend teammates to complete.
Awaiting approval to proceed after dependencies resolved.
```

**Your response:**
```
Approve the integration teammate's plan
```

## Phase 3: Parallel Implementation (4-10 minutes)

### Task Status View (Ctrl+T)

**Minute 4:**
```
┌─────────────────────────────────────────┐
│ IN PROGRESS                             │
├─────────────────────────────────────────┤
│ ⚡ Create database migration            │  (database-teammate)
│ ⚡ Build ProfileEdit component          │  (frontend-teammate)
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PENDING (BLOCKED BY DEPENDENCIES)       │
├─────────────────────────────────────────┤
│ ⏸ Implement profile API endpoint       │  (waiting: database)
│ ⏸ Write end-to-end tests               │  (waiting: api + frontend)
└─────────────────────────────────────────┘
```

**Minute 6:**
```
┌─────────────────────────────────────────┐
│ COMPLETED                               │
├─────────────────────────────────────────┤
│ ✅ Create database migration            │  (database-teammate)
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ IN PROGRESS                             │
├─────────────────────────────────────────┤
│ ⚡ Implement profile API endpoint       │  (api-teammate)
│ ⚡ Build ProfileEdit component          │  (frontend-teammate)
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PENDING (BLOCKED BY DEPENDENCIES)       │
├─────────────────────────────────────────┤
│ ⏸ Write end-to-end tests               │  (waiting: api + frontend)
└─────────────────────────────────────────┘
```

**Minute 9:**
```
┌─────────────────────────────────────────┐
│ COMPLETED                               │
├─────────────────────────────────────────┤
│ ✅ Create database migration            │
│ ✅ Implement profile API endpoint       │
│ ✅ Build ProfileEdit component          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ IN PROGRESS                             │
├─────────────────────────────────────────┤
│ ⚡ Write end-to-end tests               │  (integration-teammate)
└─────────────────────────────────────────┘
```

### Progress Updates

```
[database-teammate]: ✅ Migration created: migrations/001_add_profile_fields.sql
                     ✅ Migration tested: up and down both work
                     ✅ Task complete

[frontend-teammate]: ✅ Component created: ProfileEdit.tsx
                     ✅ Tests passing: 6/6
                     ✅ Task complete

[api-teammate]: ✅ Endpoint implemented: PUT /api/users/:id/profile
                ✅ All validations working
                ✅ Tests passing: 5/5
                ✅ Task complete

[integration-teammate]: ✅ E2E tests created: test_profile_update.py
                        ✅ All scenarios passing: 4/4
                        ✅ Full stack integration verified
                        ✅ Task complete
```

## Phase 4: Synthesis and Cleanup (10-12 minutes)

```
[Lead]: All teammates have completed their tasks. Here's the summary:

✅ Database Layer
   - Migration: migrations/001_add_profile_fields.sql
   - Adds: bio, avatar_url, updated_at columns
   - Indexed on updated_at for performance
   - Rollback script included

✅ API Layer
   - Endpoint: PUT /api/users/:id/profile
   - Validation: bio <=500 chars, avatar_url is valid URL
   - Auth: Requires login, users can only update own profile
   - Tests: 5/5 passing

✅ Frontend Layer
   - Component: ProfileEdit.tsx
   - Features: Real-time validation, loading states, error handling
   - Tests: 6/6 passing

✅ Integration Layer
   - E2E tests: 4/4 passing
   - Full stack verified working

Feature is complete and ready for deployment!

Cleaning up team resources...
✓ Team cleaned up successfully
```

## Key Observations

1. **Parallel Efficiency**
   - Database and Frontend worked simultaneously (no dependencies)
   - API started as soon as database completed
   - Integration ran last after all dependencies met
   - Total time: ~10 minutes (would be ~30 minutes sequential)

2. **No File Conflicts**
   - Each teammate owned distinct files
   - No overwrites or merge conflicts
   - Clean separation of concerns

3. **Plan Approval Workflow**
   - All plans reviewed before implementation
   - Ensured design consistency
   - Caught potential issues early

4. **Automatic Dependency Resolution**
   - API teammate automatically started when database completed
   - Integration automatically started when API + Frontend completed
   - No manual coordination needed

5. **Quality Assurance**
   - Each layer includes tests
   - Integration tests verify end-to-end flow
   - High confidence in implementation

## Cost Analysis

**Token Usage Estimate:**
- Database teammate: ~15k tokens
- API teammate: ~25k tokens
- Frontend teammate: ~30k tokens
- Integration teammate: ~20k tokens
- Lead coordination: ~10k tokens
- **Total: ~100k tokens**

**Sequential Equivalent:** ~30k tokens (but 3x longer time)

**Tradeoff:** 3x token cost for 3x speed improvement
