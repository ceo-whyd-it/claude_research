"""
Hello World - Your First FastAPI Application

This is the simplest possible FastAPI application.
Run with: fastapi dev main.py
Then visit: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(
    title="Hello World API",
    description="The simplest FastAPI application",
    version="1.0.0"
)

@app.get("/")
async def root():
    """
    Root endpoint - returns a simple greeting.
    """
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """
    Example of path and query parameters.

    - item_id: Path parameter (required, must be int)
    - q: Query parameter (optional, string)

    Try: /items/42?q=test
    """
    return {"item_id": item_id, "q": q}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    """
    Another path parameter example.

    Try: /users/1
    """
    return {"user_id": user_id, "username": f"user_{user_id}"}
