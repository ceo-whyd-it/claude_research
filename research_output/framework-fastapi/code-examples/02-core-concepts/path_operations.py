"""
Core Concept 1: Path Operations & Decorators

Demonstrates HTTP methods, path parameters, and operation organization.
Run with: fastapi dev path_operations.py
"""

from fastapi import FastAPI
from enum import Enum

app = FastAPI(title="Path Operations Examples")

# ===== HTTP Method Examples =====

fake_items_db = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

@app.get("/items")
async def read_items():
    """GET: Retrieve all items"""
    return fake_items_db

@app.post("/items")
async def create_item(name: str):
    """POST: Create a new item"""
    new_id = len(fake_items_db) + 1
    new_item = {"id": new_id, "name": name}
    fake_items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str):
    """PUT: Replace an entire item"""
    return {"item_id": item_id, "name": name, "action": "replaced"}

@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int, name: str | None = None):
    """PATCH: Partially update an item"""
    return {"item_id": item_id, "name": name, "action": "partially updated"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """DELETE: Remove an item"""
    return {"item_id": item_id, "action": "deleted"}

# ===== Path Parameters =====

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    """Path parameter with type validation"""
    return {"user_id": user_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int):
    """Multiple path parameters"""
    return {"user_id": user_id, "item_id": item_id}

# ===== Order Matters Example =====

# IMPORTANT: More specific paths must come BEFORE generic ones!

@app.get("/users/me")
async def read_current_user():
    """Specific path - must be defined BEFORE /users/{user_id}"""
    return {"user_id": "current_user"}

@app.get("/users/{user_id}/profile")
async def read_user_profile(user_id: int):
    """Another specific path"""
    return {"user_id": user_id, "section": "profile"}

# ===== Enum for Predefined Values =====

class ModelName(str, Enum):
    """Enum to restrict path parameter to specific values"""
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    Path parameter with Enum validation.
    Only accepts: alexnet, resnet, or lenet

    Try:
    - /models/alexnet ✅
    - /models/vgg ❌ (validation error)
    """
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# ===== Path with File Paths =====

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    Path parameter that accepts slashes.

    Try: /files/home/user/myfile.txt
    """
    return {"file_path": file_path}
