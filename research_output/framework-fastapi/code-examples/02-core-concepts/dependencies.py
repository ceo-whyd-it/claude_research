"""
Core Concept 3: Dependency Injection

Demonstrates reusable dependencies, sub-dependencies, and classes as dependencies.
Run with: fastapi dev dependencies.py
"""

from fastapi import Depends, FastAPI, HTTPException, Header, status
from typing import Annotated

app = FastAPI(title="Dependency Injection Examples")

# ===== Basic Dependency =====

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """
    Common query parameters used across multiple endpoints.
    This is reusable logic!
    """
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Use common_parameters dependency.

    Try: /items/?q=laptop&skip=10&limit=20
    """
    return {"params": commons, "data": "items"}

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Same dependency reused in different endpoint!
    """
    return {"params": commons, "data": "users"}

# ===== Database Dependency (Simulated) =====

def get_db():
    """
    Simulated database session with cleanup.
    In real app, this would be a SQLModel/SQLAlchemy session.
    """
    db = {"connection": "fake-db-connection", "data": [1, 2, 3]}
    try:
        print("Opening database connection")
        yield db
    finally:
        print("Closing database connection")

@app.get("/db-items/")
async def get_db_items(db: Annotated[dict, Depends(get_db)]):
    """
    Use database dependency.
    Check console to see connection open/close messages!
    """
    return {"data": db["data"]}

# ===== Sub-Dependencies =====

def get_db_connection():
    """First level: database connection"""
    print("Getting DB connection")
    return {"connection": "db-conn-123"}

def get_db_session(conn: Annotated[dict, Depends(get_db_connection)]):
    """Second level: database session (depends on connection)"""
    print(f"Creating session with {conn}")
    return {"session": "session-456", "conn": conn}

def get_current_user(session: Annotated[dict, Depends(get_db_session)]):
    """Third level: current user (depends on session)"""
    print(f"Fetching user with {session}")
    return {"username": "alice", "id": 1, "session": session}

@app.get("/me")
async def read_user_me(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Endpoint with nested dependencies.
    FastAPI automatically resolves the entire dependency tree:
    get_current_user -> get_db_session -> get_db_connection

    Check console to see execution order!
    """
    return current_user

# ===== Class-Based Dependencies =====

class Pagination:
    """Reusable pagination class"""
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

    def paginate(self, items: list):
        """Apply pagination to a list"""
        return items[self.skip : self.skip + self.limit]

fake_items = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]

@app.get("/paginated-items/")
async def get_paginated_items(pagination: Annotated[Pagination, Depends(Pagination)]):
    """
    Use class as dependency.

    Try: /paginated-items/?skip=10&limit=5
    """
    paginated = pagination.paginate(fake_items)
    return {
        "skip": pagination.skip,
        "limit": pagination.limit,
        "total": len(fake_items),
        "items": paginated
    }

# ===== Authentication Dependency =====

class AuthChecker:
    """
    Class-based authentication checker.
    Can be initialized with different required roles.
    """
    def __init__(self, required_role: str = "user"):
        self.required_role = required_role

    async def __call__(self, authorization: Annotated[str | None, Header()] = None):
        """
        Check authorization header.
        In real app, this would decode JWT token.
        """
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Simulate token validation
        if authorization != "Bearer secret-token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # In real app, decode token and check role
        return {"username": "alice", "role": self.required_role}

# Different auth dependencies for different roles
require_user = AuthChecker(required_role="user")
require_admin = AuthChecker(required_role="admin")

@app.get("/user-area")
async def user_area(user: Annotated[dict, Depends(require_user)]):
    """
    Requires user authentication.

    Try:
    - Without header: 401 error
    - With header "Authorization: Bearer secret-token": success
    """
    return {"message": f"Hello {user['username']}, you are a {user['role']}"}

@app.get("/admin-area")
async def admin_area(user: Annotated[dict, Depends(require_admin)]):
    """
    Requires admin authentication.
    Same auth check, different required role.
    """
    return {"message": f"Hello admin {user['username']}"}

# ===== Dependency with Yield for Cleanup =====

def get_resource():
    """
    Dependency with cleanup logic.
    Code after yield runs after the response is sent.
    """
    resource = {"id": "resource-123", "status": "allocated"}
    print(f"Allocating resource: {resource['id']}")
    try:
        yield resource
    finally:
        print(f"Releasing resource: {resource['id']}")
        resource["status"] = "released"

@app.get("/resource")
async def use_resource(resource: Annotated[dict, Depends(get_resource)]):
    """
    Use resource dependency with cleanup.
    Check console to see allocation and release!
    """
    return {"resource": resource}

# ===== Dependencies in Path Operation Decorator =====

async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    """
    Dependency that doesn't return a value.
    Just performs validation.
    """
    if x_api_key != "secret-api-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

@app.get("/protected", dependencies=[Depends(verify_api_key)])
async def protected_route():
    """
    Protected endpoint using dependencies parameter.
    The dependency runs but its return value is not used.

    Try with header: X-API-Key: secret-api-key
    """
    return {"message": "You have access!"}
