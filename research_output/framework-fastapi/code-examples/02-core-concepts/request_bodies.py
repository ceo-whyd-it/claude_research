"""
Core Concept 2: Request Bodies & Pydantic Models

Demonstrates data validation, Pydantic models, and request bodies.
Run with: fastapi dev request_bodies.py
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

app = FastAPI(title="Request Body Examples")

# ===== Basic Pydantic Model =====

class Item(BaseModel):
    """Basic item model with optional fields"""
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    """
    POST endpoint that accepts Item model.

    Example request body:
    {
      "name": "Laptop",
      "description": "A powerful laptop",
      "price": 999.99,
      "tax": 99.99
    }
    """
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# ===== Advanced Validation with Field =====

class Product(BaseModel):
    """Product with field-level validation"""
    name: str = Field(..., min_length=1, max_length=100, example="Smartphone")
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0, le=1000000, example=599.99)
    tax_rate: float = Field(default=0.0, ge=0, le=1, example=0.1)
    quantity: int = Field(..., ge=0, example=10)
    tags: list[str] = Field(default=[], example=["electronics", "mobile"])

@app.post("/products/")
async def create_product(product: Product):
    """
    Create a product with advanced validation.

    Validation rules:
    - name: 1-100 characters
    - price: > 0 and <= 1,000,000
    - tax_rate: 0-1 (0% to 100%)
    - quantity: >= 0
    """
    return product

# ===== Custom Validators =====

class User(BaseModel):
    """User model with custom validation"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str  # Could use EmailStr if email-validator is installed
    age: int = Field(..., ge=0, le=150)
    password: str = Field(..., min_length=8)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Ensure username is alphanumeric"""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Basic password strength check"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

@app.post("/users/")
async def create_user(user: User):
    """
    Create a user with custom validation.

    Try invalid data to see validation errors:
    - username: "ab" (too short)
    - username: "user@123" (invalid characters)
    - age: 200 (out of range)
    - password: "weak" (no number or uppercase)
    """
    # In real app, hash the password before storing!
    return {"username": user.username, "email": user.email, "age": user.age}

# ===== Nested Models =====

class Address(BaseModel):
    """Address model"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

class Company(BaseModel):
    """Company with nested address"""
    name: str
    address: Address
    employees: list[str]
    founded_year: int = Field(..., ge=1800, le=2100)

@app.post("/companies/")
async def create_company(company: Company):
    """
    Create a company with nested address model.

    Example request:
    {
      "name": "Tech Corp",
      "address": {
        "street": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "country": "USA"
      },
      "employees": ["Alice", "Bob", "Charlie"],
      "founded_year": 2020
    }
    """
    return company

# ===== Multiple Body Parameters =====

class User(BaseModel):
    username: str
    email: str

class Item(BaseModel):
    name: str
    price: float

@app.post("/offers/")
async def create_offer(user: User, item: Item, discount: float = 0.0):
    """
    Multiple body parameters.

    Request body:
    {
      "user": {
        "username": "alice",
        "email": "alice@example.com"
      },
      "item": {
        "name": "Laptop",
        "price": 999.99
      },
      "discount": 0.1
    }
    """
    final_price = item.price * (1 - discount)
    return {
        "user": user,
        "item": item,
        "discount": discount,
        "final_price": final_price
    }

# ===== Response Model Example =====

class UserIn(BaseModel):
    """User input model (includes password)"""
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    """User output model (no password!)"""
    username: str
    email: str

@app.post("/register/", response_model=UserOut)
async def register_user(user: UserIn):
    """
    Register user - password is in request but NOT in response.

    This is how you prevent sensitive data from leaking.
    """
    # In real app, hash password and save to database
    return user  # Password automatically excluded from response!
