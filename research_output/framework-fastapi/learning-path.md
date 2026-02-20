# FastAPI Learning Path

A progressive guide to mastering FastAPI, structured in 5 levels from beginner to advanced.

---

## Level 1: Overview & Motivation

**Goal**: Understand WHAT FastAPI is and WHY you should use it

**Time**: 15-20 minutes

### What Problem Does FastAPI Solve?

FastAPI addresses critical pain points in API development:

1. **Slow Development Speed**
   - Traditional frameworks require extensive boilerplate
   - Manual documentation writing and maintenance
   - Repetitive validation code
   - **FastAPI Solution**: Increases development speed by 200-300%

2. **High Error Rates**
   - Type mismatches discovered at runtime
   - Missing input validation
   - Inconsistent API contracts
   - **FastAPI Solution**: Reduces human-induced errors by ~40%

3. **Poor Developer Experience**
   - Minimal IDE support and autocomplete
   - Complex debugging workflows
   - Scattered documentation
   - **FastAPI Solution**: Editor support with auto-completion everywhere, minimal debugging time

4. **Performance Bottlenecks**
   - Synchronous frameworks block on I/O
   - Inefficient request handling
   - **FastAPI Solution**: Performance on par with NodeJS and Go (thanks to async/await)

5. **Documentation Burden**
   - Manual API documentation quickly becomes outdated
   - Separate tools for docs and code
   - **FastAPI Solution**: Automatic interactive documentation from code

### What Existed Before? Why is FastAPI Better?

#### The Python Web Framework Landscape

**Before FastAPI:**

| Framework | Strengths | Weaknesses |
|-----------|-----------|------------|
| **Flask** | Simple, flexible, minimal | No built-in validation, manual docs, no async support initially, slow |
| **Django** | Batteries-included, admin panel, ORM | Heavy, opinionated, complex for simple APIs, REST not native |
| **Pyramid** | Flexible, mature | Steep learning curve, less community support |

**FastAPI's Innovation:**

- **Type Hints as Foundation**: Uses Python 3.10+ type hints for validation, documentation, and IDE support
- **Async-Native**: Built on ASGI (Starlette) for high concurrency
- **Automatic Documentation**: Swagger UI and ReDoc generated from code
- **Standards-Based**: Full OpenAPI and JSON Schema compliance
- **Minimal Boilerplate**: One decorator + type hints = validated endpoint with docs
- **Fast**: Performance comparable to NodeJS and Go

### Who Uses FastAPI? For What?

#### Production Users (175+ Companies)

- **Uber**: Ride-sharing microservices
- **Netflix**: Content delivery APIs
- **Microsoft**: Internal tools and APIs
- **Expedia**: Travel booking services
- **Fintech Companies**: Payment processing, banking APIs

#### Common Application Types

1. **REST APIs** - Standard CRUD applications
2. **Microservices** - Lightweight, independent services
3. **ML Model Serving** - Deploy machine learning models as APIs
4. **Real-time Applications** - WebSocket-based chat, notifications
5. **Internal Tools** - Company APIs with automatic documentation
6. **Data Pipelines** - API-driven ETL and data processing
7. **Mobile Backends** - Backend services for iOS/Android apps

### When Should You NOT Use FastAPI?

FastAPI is excellent for APIs, but consider alternatives when:

1. **You Need a Full-Stack Framework**
   - FastAPI has no built-in template engine, admin panel, or ORM
   - **Better Choice**: Django (if you need all batteries included)

2. **You're Building a Traditional Web App** (Server-Rendered HTML)
   - FastAPI focuses on JSON APIs
   - **Better Choice**: Flask with Jinja2, Django

3. **You Need Mature Ecosystem & Plugins**
   - Django has more third-party packages and plugins
   - **Better Choice**: Django (especially for e-commerce, CMS)

4. **Team Lacks Python 3.10+ or Async Experience**
   - FastAPI requires modern Python and understanding of async/await
   - **Better Choice**: Flask (simpler learning curve)

5. **Simple Scripting or CLIs**
   - Overhead of a web framework is unnecessary
   - **Better Choice**: Click, Typer, or standard Python

6. **GraphQL-First API**
   - FastAPI supports GraphQL but it's not native
   - **Better Choice**: Strawberry (GraphQL), Ariadne

### Architecture Overview at a Glance

FastAPI uses a **middleware-based request-response architecture**:

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────┐
│   ASGI Server       │  (Uvicorn)
│   - Async I/O       │
│   - Request Parsing │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Middleware Stack  │  (CORS, Auth, Logging, etc.)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   FastAPI Router    │  (Path matching)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Dependencies      │  (Injection resolution)
│   - DB connections  │
│   - Auth tokens     │
│   - Shared logic    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Path Operation     │  (Your function)
│  - Validation       │
│  - Business Logic   │
│  - Pydantic Models  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Response           │
│  - Serialization    │
│  - Validation       │
│  - JSON encoding    │
└──────┬──────────────┘
       │ HTTP Response
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

**Key Architectural Principles:**

1. **ASGI-based**: Asynchronous Server Gateway Interface for concurrent request handling
2. **Dependency Injection**: Reusable components injected into endpoints
3. **Pydantic Validation**: Type-driven data validation and serialization
4. **Declarative**: Describe what you want, framework handles the how
5. **Starlette Foundation**: Built on proven ASGI framework

### Key Takeaways

✅ **FastAPI is best for**: Building modern APIs quickly with automatic documentation, validation, and high performance

✅ **Use FastAPI when**: You need REST APIs, microservices, ML endpoints, or WebSocket applications

✅ **Skip FastAPI if**: You need a full-stack framework, traditional web app, or GraphQL-first design

✅ **Core Innovation**: Type hints drive validation, documentation, and IDE support

✅ **Performance**: On par with NodeJS and Go, 200-300% faster development

---

## Level 2: Setup & First Project

**Goal**: Get FastAPI running locally and create your first API

**Time**: 30-45 minutes

### Prerequisites

Before starting, ensure you have:

- **Python 3.10 or higher** (check with `python --version` or `python3 --version`)
- **pip** (Python package manager, included with Python)
- **A code editor** (VS Code, PyCharm, or any text editor)
- **Terminal/Command Prompt** access

### Installation Steps

#### Step 1: Create a Project Directory

```bash
# Create and navigate to project folder
mkdir fastapi-tutorial
cd fastapi-tutorial
```

#### Step 2: (Recommended) Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install FastAPI

```bash
# Standard installation (includes Uvicorn and common dependencies)
pip install "fastapi[standard]"

# Or minimal installation
pip install fastapi uvicorn
```

**What gets installed:**

- `fastapi` - The framework
- `uvicorn` - ASGI server to run your app
- `pydantic` - Data validation (auto-installed with FastAPI)
- `starlette` - ASGI framework foundation (auto-installed)
- Optional: `python-multipart`, `email-validator`, `jinja2`, `httpx`

### Your First FastAPI Application

Create a file named `main.py`:

```python
from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI()

# Define a path operation
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Running the Development Server

```bash
# Run with FastAPI CLI (recommended)
fastapi dev main.py

# Or run with Uvicorn directly
uvicorn main:app --reload
```

**What you'll see:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify It Works

Open your browser and visit these URLs:

1. **Your API Endpoint**
   - URL: http://127.0.0.1:8000/
   - Response: `{"message": "Hello World"}`

2. **Path Parameter Example**
   - URL: http://127.0.0.1:8000/items/42?q=test
   - Response: `{"item_id": 42, "q": "test"}`

3. **Interactive API Docs (Swagger UI)**
   - URL: http://127.0.0.1:8000/docs
   - Try out requests directly in the browser!

4. **Alternative Docs (ReDoc)**
   - URL: http://127.0.0.1:8000/redoc
   - Beautiful, responsive documentation

### Project Scaffolding (Optional)

For larger projects, use the official full-stack template:

```bash
# Install copier
pip install copier

# Generate project from template
copier copy https://github.com/fastapi/full-stack-fastapi-template my-project --trust

cd my-project
```

**What you get:**

- ✅ FastAPI backend
- ✅ React frontend (Vite + TypeScript)
- ✅ PostgreSQL database
- ✅ SQLModel ORM
- ✅ Docker Compose setup
- ✅ GitHub Actions CI/CD
- ✅ Traefik reverse proxy with HTTPS
- ✅ Pre-configured authentication

### Recommended Project Structure (Manual Setup)

For a simple API project:

```
fastapi-tutorial/
├── venv/                 # Virtual environment (don't commit)
├── app/
│   ├── __init__.py
│   ├── main.py          # Application entry point
│   ├── dependencies.py  # Shared dependencies
│   ├── routers/         # Route modules
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   └── models.py        # Pydantic models
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt     # Dependencies
└── .env                 # Environment variables (don't commit)
```

Create this structure:

```bash
mkdir -p app/routers tests
touch app/__init__.py app/main.py app/dependencies.py app/models.py
touch app/routers/__init__.py tests/__init__.py tests/test_main.py
```

### requirements.txt

Create a requirements file:

```txt
fastapi==0.129.0
uvicorn[standard]==0.30.0
pydantic==2.7.0
python-multipart==0.0.12
```

Install from requirements:

```bash
pip install -r requirements.txt
```

### Minimal Working Project Code

**app/main.py:**

```python
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI(
    title="My API",
    description="A sample FastAPI application",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to My API"}
```

**app/routers/users.py:**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def read_users():
    return [{"username": "alice"}, {"username": "bob"}]

@router.get("/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id, "username": f"user_{user_id}"}
```

**app/routers/items.py:**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/")
async def read_items(skip: int = 0, limit: int = 10):
    return [{"item_id": i, "name": f"Item {i}"} for i in range(skip, skip + limit)]
```

Run it:

```bash
fastapi dev app/main.py
```

Visit http://127.0.0.1:8000/docs to see your organized API with tags!

### Expected Output

When you run `fastapi dev main.py`, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Visit the URLs and confirm:

- ✅ Root endpoint returns JSON
- ✅ Interactive docs work at `/docs`
- ✅ You can try out requests in the browser
- ✅ Type validation works (try http://127.0.0.1:8000/items/abc - should get validation error)

### Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Activate your virtual environment and run `pip install "fastapi[standard]"`

**Problem**: `Address already in use`
- **Solution**: Change port with `uvicorn main:app --reload --port 8001`

**Problem**: Changes not reflecting
- **Solution**: Ensure you're using `--reload` flag or `fastapi dev` (auto-reload enabled)

**Problem**: Import errors with `app/` structure
- **Solution**: Run from project root: `fastapi dev app/main.py`

### Key Takeaways

✅ **Installation**: `pip install "fastapi[standard]"` gets you started

✅ **Run**: `fastapi dev main.py` for development with auto-reload

✅ **Automatic Docs**: `/docs` and `/redoc` are generated automatically

✅ **Structure**: Use routers to organize larger applications

✅ **Type Hints**: `item_id: int` provides automatic validation and documentation

---

## Level 3: Architecture & Core Concepts

**Goal**: Understand FastAPI's mental model and fundamental concepts

**Time**: 1-2 hours

### Core Concept 1: Path Operations & Decorators

**What it is**: Path operations are functions that handle HTTP requests to specific URLs (paths) and methods (GET, POST, PUT, DELETE, etc.).

#### How It Works

```python
from fastapi import FastAPI

app = FastAPI()

# GET request to /items
@app.get("/items")
async def read_items():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

# POST request to /items
@app.post("/items")
async def create_item(name: str):
    return {"name": name, "created": True}

# Path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Multiple HTTP methods on same path
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"method": "GET", "user_id": user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"method": "DELETE", "user_id": user_id}
```

#### Available Decorators

```python
@app.get()      # Retrieve data
@app.post()     # Create data
@app.put()      # Update/replace data
@app.patch()    # Partial update
@app.delete()   # Delete data
@app.options()  # Get communication options
@app.head()     # Same as GET but no body
@app.trace()    # Echo received request
```

#### Path Parameters

```python
# Basic path parameter
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

# Multiple path parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

# Enum for predefined values
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model": "AlexNet", "description": "Deep CNN"}
    return {"model": model_name}
```

#### Common Mistakes

❌ **Mistake 1: Path order matters**

```python
# WRONG - specific path after generic
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")  # This will NEVER match! "me" matches {user_id} first
async def read_current_user():
    return {"user_id": "current"}

# CORRECT - specific paths first
@app.get("/users/me")
async def read_current_user():
    return {"user_id": "current"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

❌ **Mistake 2: Forgetting async/await**

```python
# If you use 'async def', you must 'await' async operations
@app.get("/users")
async def get_users():
    users = database.fetch_all()  # WRONG - should be 'await database.fetch_all()'
    return users
```

### Core Concept 2: Request Body & Pydantic Models

**What it is**: Use Pydantic's `BaseModel` to define request body schemas with automatic validation, serialization, and documentation.

#### Basic Request Body

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    # item is automatically validated and parsed
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

**Request example:**

```json
POST /items/
{
  "name": "Laptop",
  "description": "A powerful laptop",
  "price": 999.99,
  "tax": 99.99
}
```

**Response:**

```json
{
  "name": "Laptop",
  "description": "A powerful laptop",
  "price": 999.99,
  "tax": 99.99,
  "price_with_tax": 1099.98
}
```

#### Advanced Pydantic Features

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Validates email format
    age: int = Field(..., ge=0, le=150)  # Greater than or equal to 0, less than or equal to 150
    is_active: bool = True

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

@app.post("/users/")
async def create_user(user: User):
    return user
```

**Invalid request (triggers validation error):**

```json
{
  "username": "ab",  // Too short
  "email": "not-an-email",  // Invalid format
  "age": 200  // Out of range
}
```

**FastAPI automatic response:**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "username"],
      "msg": "String should have at least 3 characters"
    },
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    },
    {
      "type": "less_than_equal",
      "loc": ["body", "age"],
      "msg": "Input should be less than or equal to 150"
    }
  ]
}
```

#### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Company(BaseModel):
    name: str
    address: Address
    employees: list[str]

@app.post("/companies/")
async def create_company(company: Company):
    return company
```

#### Common Mistakes

❌ **Mistake 1: Not using Pydantic models for request bodies**

```python
# WRONG - dictionary without validation
@app.post("/items/")
async def create_item(item: dict):
    # No validation, no type safety, no auto-docs
    return item

# CORRECT - Pydantic model
class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item
```

❌ **Mistake 2: Confusing `Field(...)` with `Field(default=...)`**

```python
from pydantic import BaseModel, Field

# WRONG - `...` means required, but default makes it optional
class Item(BaseModel):
    name: str = Field(..., description="Item name")  # Required
    description: str = Field(default="No description")  # Optional with default

# CORRECT understanding:
# - Field(...) = required
# - Field(default=X) or Field(X) = optional with default
# - Field() without arguments = required (same as ...)
```

### Core Concept 3: Dependency Injection

**What it is**: A system to declare reusable components that FastAPI automatically provides to your path operations.

#### Basic Dependency

```python
from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency function
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Use dependency in multiple endpoints
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

Visit: `/items/?q=test&skip=10&limit=50`
Response: `{"q": "test", "skip": 10, "limit": 50}`

#### Database Dependency (Common Pattern)

```python
from fastapi import Depends

# Simulate database session
def get_db():
    db = {"connection": "fake-db-session"}
    try:
        yield db  # Provide database to endpoint
    finally:
        # Cleanup (close connection, etc.)
        print("DB connection closed")

@app.get("/users/")
async def read_users(db: dict = Depends(get_db)):
    # db is automatically provided
    users = db.get("users", [])
    return users
```

#### Class-Based Dependencies

```python
from fastapi import Depends, HTTPException, status

# Authentication dependency
class AuthChecker:
    def __init__(self, required_role: str):
        self.required_role = required_role

    def __call__(self, token: str = Header(...)):
        # Validate token and check role
        if token != "secret-token":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        # In real app, decode JWT and check role
        return {"user": "alice", "role": self.required_role}

# Use the dependency
@app.get("/admin/")
async def admin_route(user: dict = Depends(AuthChecker(required_role="admin"))):
    return {"message": f"Hello admin {user['user']}"}
```

#### Sub-Dependencies

```python
# Dependencies can depend on other dependencies
def get_db_connection():
    return {"connection": "database"}

def get_db_session(conn: dict = Depends(get_db_connection)):
    return {"session": "db-session", "conn": conn}

def get_current_user(session: dict = Depends(get_db_session)):
    # Use session to fetch user
    return {"username": "alice", "session": session}

@app.get("/me")
async def read_current_user(user: dict = Depends(get_current_user)):
    return user
```

Response includes nested dependency results:

```json
{
  "username": "alice",
  "session": {
    "session": "db-session",
    "conn": {"connection": "database"}
  }
}
```

#### Common Mistakes

❌ **Mistake 1: Calling dependency function instead of passing it**

```python
# WRONG - calling the function
@app.get("/items/")
async def read_items(commons: dict = common_parameters()):  # ❌
    return commons

# CORRECT - passing to Depends
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):  # ✅
    return commons
```

❌ **Mistake 2: Not understanding dependency execution**

Dependencies execute **for every request**, not once at startup:

```python
def expensive_operation():
    print("This runs on EVERY request!")  # Might be a problem
    return {"data": "loaded"}

@app.get("/data/")
async def get_data(data: dict = Depends(expensive_operation)):
    return data

# Solution: Use app lifespan events for startup-only operations
```

### Core Concept 4: Query Parameters & Validation

**What it is**: Extract and validate data from URL query strings (e.g., `?search=test&limit=10`).

#### Basic Query Parameters

```python
from fastapi import FastAPI, Query

app = FastAPI()

# Simple query parameters
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# With Query for additional validation
@app.get("/items/search")
async def search_items(
    q: str | None = Query(default=None, min_length=3, max_length=50),
    limit: int = Query(default=10, ge=1, le=100)
):
    return {"q": q, "limit": limit}
```

Visit: `/items/search?q=laptop&limit=20`
Response: `{"q": "laptop", "limit": 20}`

#### Advanced Query Validation

```python
from fastapi import Query
import re

@app.get("/items/")
async def read_items(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9 ]+$",  # Regex pattern
        title="Search Query",
        description="Search term for items",
        examples=["laptop", "phone"],
    ),
    tags: list[str] = Query(default=[]),  # Multiple values: ?tags=electronics&tags=sale
    hidden: bool = Query(default=False, include_in_schema=False)  # Hidden from docs
):
    return {"q": q, "tags": tags, "hidden": hidden}
```

Visit: `/items/?q=laptop&tags=electronics&tags=sale&hidden=true`
Response: `{"q": "laptop", "tags": ["electronics", "sale"], "hidden": true}`

#### Required vs Optional Query Parameters

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    required_param: str,  # Required (no default)
    optional_param: str | None = None,  # Optional (default None)
    default_param: int = 10,  # Optional (default 10)
    query_required: str = Query(...),  # Required with Query
    query_optional: str | None = Query(default=None)  # Optional with Query
):
    return {
        "required": required_param,
        "optional": optional_param,
        "default": default_param,
        "query_required": query_required,
        "query_optional": query_optional
    }
```

#### Common Mistakes

❌ **Mistake 1: Incorrect optional type hints**

```python
# WRONG - Not properly optional
@app.get("/items/")
async def read_items(q: str = None):  # Type mismatch: str cannot be None
    return {"q": q}

# CORRECT - Use Union or | for optional
@app.get("/items/")
async def read_items(q: str | None = None):  # ✅
    return {"q": q}
```

❌ **Mistake 2: Expecting list without Query**

```python
# WRONG - Won't work as expected
@app.get("/items/")
async def read_items(tags: list[str] = []):
    return {"tags": tags}

# CORRECT - Use Query for list parameters
@app.get("/items/")
async def read_items(tags: list[str] = Query(default=[])):
    return {"tags": tags}
```

### Core Concept 5: Automatic API Documentation

**What it is**: FastAPI automatically generates interactive API documentation from your code using OpenAPI and JSON Schema.

#### Built-in Documentation UIs

1. **Swagger UI** - `/docs`
   - Interactive "Try it out" functionality
   - Test requests directly from browser
   - See request/response examples

2. **ReDoc** - `/redoc`
   - Clean, responsive documentation
   - Great for sharing with external users
   - Focused on readability

3. **OpenAPI JSON** - `/openapi.json`
   - Raw OpenAPI schema
   - Can be imported into tools like Postman, Insomnia

#### Enhancing Documentation

```python
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

app = FastAPI(
    title="My API",
    description="A comprehensive API for managing items",
    version="2.0.0",
    contact={
        "name": "API Support",
        "email": "support@myapi.com",
    },
    license_info={
        "name": "MIT",
    },
)

class Item(BaseModel):
    name: str = Field(..., example="Laptop")
    description: str | None = Field(None, example="A powerful laptop")
    price: float = Field(..., gt=0, example=999.99)
    tax: float | None = Field(None, ge=0, example=99.99)

@app.post(
    "/items/",
    response_model=Item,
    status_code=201,
    summary="Create a new item",
    description="Create a new item with name, description, price, and optional tax",
    response_description="The created item",
    tags=["items"],
)
async def create_item(
    item: Item = Body(
        ...,
        examples=[
            {
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": 999.99,
                "tax": 99.99
            },
            {
                "name": "Phone",
                "description": "A smartphone",
                "price": 599.99
            }
        ]
    )
):
    """
    Create an item with all the information:

    - **name**: Each item must have a name
    - **description**: Optional long description
    - **price**: Required price, must be greater than 0
    - **tax**: Optional tax amount
    """
    return item
```

#### Organizing with Tags

```python
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Item 1"}]

@app.post("/items/", tags=["items"])
async def create_item(name: str):
    return {"name": name}

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "alice"}]
```

#### Metadata for Tags

```python
app = FastAPI(
    openapi_tags=[
        {
            "name": "items",
            "description": "Operations with items. The **items** logic is here.",
        },
        {
            "name": "users",
            "description": "Manage users. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://myapi.com/docs/items",
            },
        },
    ]
)
```

#### Common Mistakes

❌ **Mistake 1: Disabling docs in production**

Some developers disable `/docs` in production for "security". This is often unnecessary:

```python
# Questionable practice
from fastapi import FastAPI

app = FastAPI(docs_url=None, redoc_url=None)  # Disables docs
```

**Better approach**: Use authentication on docs endpoints or keep them enabled (they don't expose sensitive data that's not already in your API).

❌ **Mistake 2: Not providing examples**

Without examples, users have to guess:

```python
# BARE - No examples
class Item(BaseModel):
    name: str
    price: float

# BETTER - With examples
class Item(BaseModel):
    name: str = Field(..., example="Laptop")
    price: float = Field(..., example=999.99)
```

### Request/Data Lifecycle Summary

Understanding how data flows through FastAPI:

```
1. HTTP Request arrives
   ↓
2. ASGI Server (Uvicorn) receives request
   ↓
3. Middleware stack processes request (CORS, custom middleware)
   ↓
4. FastAPI Router matches path and method
   ↓
5. Dependency Injection resolves dependencies
   ↓
6. Path/Query/Body parameters extracted and validated (Pydantic)
   ↓
7. Your path operation function executes
   ↓
8. Return value serialized (Pydantic model → JSON)
   ↓
9. Response validation (if response_model declared)
   ↓
10. Middleware processes response
   ↓
11. HTTP Response sent to client
```

### Configuration and Convention Patterns

FastAPI follows these conventions:

1. **Type Hints = Validation**: If you declare a type, FastAPI validates it
2. **Default Values = Optional**: Parameters with defaults are optional
3. **No Default = Required**: Parameters without defaults are required
4. **async/def Choice Matters**:
   - `async def`: For I/O-bound operations (DB queries, HTTP requests)
   - `def`: For CPU-bound operations (runs in thread pool)
5. **Dependency Injection**: Use `Depends()` for reusable logic
6. **Router Organization**: Use `APIRouter` to split large apps into modules

### Key Takeaways

✅ **Path Operations**: Use decorators like `@app.get()` to define endpoints

✅ **Pydantic Models**: Define request/response schemas with automatic validation

✅ **Dependencies**: Reusable components injected with `Depends()`

✅ **Query Parameters**: Extract and validate URL parameters with `Query()`

✅ **Automatic Docs**: `/docs` and `/redoc` generated from code

✅ **Data Flow**: Request → Validation → Your Code → Response → Client

---

## Level 4: Building Real Applications

**Goal**: Build a complete TODO API with database, authentication, and testing

**Time**: 3-4 hours

### Project Overview

We'll build a **TODO API** with:

- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ SQLModel database integration (SQLite)
- ✅ User authentication (JWT tokens)
- ✅ Input validation
- ✅ Error handling
- ✅ Unit tests
- ✅ API documentation

### Project Structure

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database setup
│   ├── models.py         # SQLModel models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication logic
│   ├── dependencies.py   # Shared dependencies
│   └── routers/
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints
│       └── todos.py      # TODO endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   └── test_todos.py     # Tests
├── requirements.txt
├── .env
└── README.md
```

### Step 1: Setup and Dependencies

**requirements.txt:**

```txt
fastapi==0.129.0
uvicorn[standard]==0.30.0
sqlmodel==0.0.24
pydantic-settings==2.8.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
pytest==8.3.4
httpx==0.27.2
```

Install:

```bash
pip install -r requirements.txt
```

**app/config.py:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TODO API"
    database_url: str = "sqlite:///./todo.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

**.env:**

```
SECRET_KEY=your-super-secret-key-min-32-characters-long
DATABASE_URL=sqlite:///./todo.db
```

### Step 2: Database Models

**app/models.py:**

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    todos: list["Todo"] = Relationship(back_populates="owner")

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    # Foreign key
    user_id: int = Field(foreign_key="user.id")

    # Relationship
    owner: User = Relationship(back_populates="todos")
```

**app/database.py:**

```python
from sqlmodel import SQLModel, Session, create_engine
from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

def create_db_and_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
```

### Step 3: Pydantic Schemas

**app/schemas.py:**

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

# Todo schemas
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime | None
    user_id: int

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
```

### Step 4: Authentication

**app/auth.py:**

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.models import User
from app.database import get_session
from app.config import settings
from app.schemas import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(session: Session, username: str, password: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    statement = select(User).where(User.username == token_data.username)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Step 5: Auth Router

**app/routers/auth.py:**

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.database import get_session
from app.auth import get_password_hash, authenticate_user, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if username exists
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email exists
    statement = select(User).where(User.email == user_data.email)
    existing_email = session.exec(statement).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Step 6: TODO Router

**app/routers/todos.py:**

```python
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models import User, Todo
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.database import get_session
from app.auth import get_current_active_user

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    new_todo = Todo(**todo_data.model_dump(), user_id=current_user.id)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    todos = session.exec(statement).all()
    return todos

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return None
```

### Step 7: Main Application

**app/main.py:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routers import auth, todos
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="A TODO API with authentication",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Welcome to TODO API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Step 8: Testing

**tests/conftest.py:**

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    # In-memory database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

**tests/test_todos.py:**

```python
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user(client: TestClient):
    # First register
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )

    # Then login
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_todo(client: TestClient):
    # Register and login
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "securepassword123"}
    )
    token = login_response.json()["access_token"]

    # Create todo
    response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "A test todo"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["completed"] == False

def test_get_todos(client: TestClient):
    # Setup: register, login, create todo
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "securepassword123"}
    )
    token = login_response.json()["access_token"]

    client.post(
        "/todos/",
        json={"title": "Test todo"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get todos
    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test todo"

def test_unauthorized_access(client: TestClient):
    response = client.get("/todos/")
    assert response.status_code == 401
```

Run tests:

```bash
pytest tests/ -v
```

### Step 9: Running the Application

```bash
# Development
fastapi dev app/main.py

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 10: Testing the API

**1. Register a user:**

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepassword123"
  }'
```

**2. Login to get token:**

```bash
curl -X POST "http://127.0.0.1:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=securepassword123"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**3. Create a todo:**

```bash
curl -X POST "http://127.0.0.1:8000/todos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial"
  }'
```

**4. Get all todos:**

```bash
curl -X GET "http://127.0.0.1:8000/todos/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**5. Update a todo:**

```bash
curl -X PATCH "http://127.0.0.1:8000/todos/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "completed": true
  }'
```

**6. Delete a todo:**

```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Plugin/Extension Ecosystem

**Useful packages for extending your TODO API:**

1. **Database & ORM**
   - SQLModel (already using) - https://sqlmodel.tiangolo.com/
   - Alembic - Database migrations - https://alembic.sqlalchemy.org/

2. **Caching**
   - fastapi-cache2 - Response caching - https://github.com/long2ice/fastapi-cache
   - Redis - External cache - https://redis.io/

3. **Background Tasks**
   - Celery - Distributed task queue - https://docs.celeryq.dev/
   - ARQ - Async task queue - https://github.com/samuelcolvin/arq

4. **Monitoring**
   - prometheus-fastapi-instrumentator - Metrics - https://github.com/trallnag/prometheus-fastapi-instrumentator
   - OpenTelemetry - Distributed tracing

5. **Admin Panel**
   - sqladmin - Admin UI for SQLModel - https://github.com/aminalaee/sqladmin

### Deployment Considerations

#### Docker

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/tododb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=tododb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Production Checklist

- ✅ Use strong `SECRET_KEY` (min 32 characters)
- ✅ Use PostgreSQL instead of SQLite
- ✅ Enable HTTPS/TLS
- ✅ Set proper CORS origins
- ✅ Add rate limiting (SlowApi)
- ✅ Use environment variables for config
- ✅ Add logging and monitoring
- ✅ Run with multiple workers: `uvicorn app.main:app --workers 4`
- ✅ Use Gunicorn + Uvicorn workers for production
- ✅ Implement database migrations (Alembic)
- ✅ Add request ID tracking
- ✅ Set up health checks

### Key Takeaways

✅ **Complete CRUD API**: Created full TODO application with authentication

✅ **Database Integration**: Used SQLModel for ORM and database management

✅ **Authentication**: Implemented JWT-based auth with password hashing

✅ **Testing**: Wrote unit tests with pytest and TestClient

✅ **Project Structure**: Organized code with routers, models, schemas

✅ **Documentation**: Automatic API docs at `/docs`

✅ **Production-Ready**: Deployment considerations for real-world use

---

## Level 5: Next Steps

**Goal**: Know where to go deeper and continue learning

**Time**: Reference

### Advanced Topics to Explore

#### 1. Advanced Database Patterns

**Alembic Migrations:**

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users table"

# Run migration
alembic upgrade head
```

**Resources:**
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [SQLModel with Alembic](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/)

#### 2. Advanced Authentication

**OAuth2 with External Providers:**

- **FastAPI Azure Auth** - Azure AD integration
- **FastAPI Cloud Auth** - AWS Cognito, Auth0, Firebase
- **Social Login** - Google, GitHub, Facebook

**Resources:**
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth2 Scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/)

#### 3. WebSockets & Real-Time

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

**Resources:**
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Server-Sent Events with sse-starlette](https://github.com/sysid/sse-starlette)

#### 4. Background Tasks & Job Queues

**Built-in Background Tasks:**

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    print(f"Sending email to {email}")

@app.post("/send-email/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Email will be sent in the background"}
```

**Celery for Complex Jobs:**

```python
from celery import Celery

celery = Celery(__name__, broker="redis://localhost:6379/0")

@celery.task
def long_running_task(data):
    # Process data
    return "Done"

@app.post("/process/")
async def process_data(data: dict):
    long_running_task.delay(data)
    return {"status": "Processing started"}
```

**Resources:**
- [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [ARQ (async task queue)](https://github.com/samuelcolvin/arq)

#### 5. Microservices Architecture

**Service Communication:**

```python
import httpx

async def call_other_service():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://other-service:8000/api/data")
        return response.json()

@app.get("/aggregate/")
async def aggregate_data():
    data = await call_other_service()
    return {"data": data}
```

**Service Mesh:**
- **Kubernetes** - Container orchestration
- **Istio** - Service mesh for microservices
- **Consul** - Service discovery

**Resources:**
- [FastAPI Sub Applications](https://fastapi.tiangolo.com/advanced/sub-applications/)
- [Microservices with FastAPI (Medium)](https://medium.com/search?q=fastapi+microservices)

#### 6. GraphQL Integration

```python
from strawberry.fastapi import GraphQLRouter
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
```

**Resources:**
- [Strawberry GraphQL](https://strawberry.rocks/)
- [Graphene Python](https://graphene-python.org/)

#### 7. Performance Optimization

**Caching:**

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/cached/")
@cache(expire=60)
async def get_cached_data():
    return {"data": "This will be cached for 60 seconds"}
```

**Connection Pooling:**

```python
from sqlmodel import create_engine

engine = create_engine(
    "postgresql://user:password@localhost/db",
    pool_size=20,          # Number of connections
    max_overflow=0,        # Extra connections when pool is full
    pool_pre_ping=True,    # Verify connections before using
    pool_recycle=3600      # Recycle connections after 1 hour
)
```

**Resources:**
- [fastapi-cache2](https://github.com/long2ice/fastapi-cache)
- [Performance Best Practices](https://github.com/zhanymkanov/fastapi-best-practices#12-use-caching-techniques)

#### 8. Testing Strategies

**Advanced Testing:**

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

# Mock dependencies
def mock_get_db():
    return MockDatabase()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = mock_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

**Resources:**
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)

#### 9. Monitoring & Observability

**Structured Logging:**

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request", extra={"path": request.url.path, "method": request.method})
    response = await call_next(request)
    return response
```

**Prometheus Metrics:**

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

**Resources:**
- [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [OpenTelemetry](https://opentelemetry.io/)

### Best Resources for Each Topic

#### Official Documentation

- **Main Docs** - https://fastapi.tiangolo.com/ (Always start here)
- **Advanced User Guide** - https://fastapi.tiangolo.com/advanced/
- **Tutorial** - https://fastapi.tiangolo.com/tutorial/

#### Books

- **Building Data Science Applications with FastAPI** (Packt)
- **FastAPI Modern Python Web Development** (Various authors)

#### Video Courses

- **Udemy: FastAPI - The Complete Course 2026** (Bestseller, updated)
- **Real Python: FastAPI Learning Path** - https://realpython.com/learning-paths/fastapi/
- **freeCodeCamp YouTube** - Free comprehensive tutorial

#### Articles & Blogs

- **FastAPI Best Practices** - https://github.com/zhanymkanov/fastapi-best-practices
- **Real Python FastAPI Articles** - https://realpython.com/tutorials/fastapi/
- **Auth0 Blog** - https://auth0.com/blog/fastapi-best-practices/

#### Community Projects

- **Awesome FastAPI** - https://github.com/mjhea0/awesome-fastapi
- **Full Stack Template** - https://github.com/fastapi/full-stack-fastapi-template

### Community Resources

#### Official Channels

- **GitHub Discussions** - https://github.com/fastapi/fastapi/discussions (Recommended for questions)
- **Discord Server** - https://discord.gg/VQjSZaeJmf (Real-time chat)
- **GitHub Issues** - https://github.com/fastapi/fastapi/issues (Bug reports)
- **Twitter/X** - Follow @tiangolo (Creator Sebastián Ramírez)

#### Community Hubs

- **Reddit** - r/FastAPI
- **Stack Overflow** - [fastapi] tag
- **Dev.to** - #fastapi tag
- **Medium** - Search "FastAPI"

### How to Get Help

**When stuck:**

1. **Check Official Docs First** - Most answers are there
2. **GitHub Discussions** - Search existing discussions
3. **Discord** - Ask in real-time
4. **Stack Overflow** - For specific code problems
5. **GitHub Issues** - For bugs (search first!)

**How to ask good questions:**

- ✅ Show minimal reproducible example
- ✅ Include error messages
- ✅ Describe what you tried
- ✅ Mention FastAPI version
- ✅ Be specific about expected vs actual behavior

### Hands-On Exercises

**Mini-Project Ideas:**

1. **Blog API**
   - Posts, comments, categories
   - Markdown support
   - Full-text search
   - Pagination

2. **E-commerce API**
   - Products, cart, orders
   - Payment integration (Stripe)
   - Inventory management
   - Order status tracking

3. **Chat Application**
   - WebSocket-based real-time chat
   - Rooms and private messages
   - User presence
   - Message history

4. **File Upload Service**
   - Image upload and processing
   - S3/cloud storage integration
   - Thumbnail generation
   - CDN integration

5. **URL Shortener**
   - Short URL generation
   - Click tracking
   - Analytics dashboard
   - QR code generation

6. **Weather API Aggregator**
   - Fetch from multiple weather APIs
   - Caching
   - Location-based queries
   - Forecast aggregation

### Certification & Learning Paths

While there's no official FastAPI certification, consider:

- **Build a portfolio** of FastAPI projects on GitHub
- **Contribute to open source** FastAPI projects
- **Write blog posts** about your learnings
- **Create YouTube tutorials** teaching others

### Career Development

**FastAPI skills are valuable for:**

- Backend Python Developer
- API Developer
- Microservices Engineer
- ML Engineer (model serving)
- Full-Stack Python Developer

**Complement with:**

- Docker & Kubernetes
- PostgreSQL & Redis
- React/Vue.js (for full-stack)
- AWS/Azure/GCP
- CI/CD (GitHub Actions, GitLab CI)

### Final Thoughts

You've now learned:

✅ **What FastAPI is** and when to use it
✅ **How to set up** a FastAPI project
✅ **Core concepts**: path operations, dependencies, validation, docs
✅ **Building real apps**: Complete TODO API with auth
✅ **Where to go next**: Advanced topics and resources

**Next steps:**

1. Build your own project using FastAPI
2. Deploy it to production (Docker + cloud platform)
3. Join the community (Discord, GitHub Discussions)
4. Share your learnings (blog, open source)
5. Keep exploring advanced topics

**Remember:**

> "The best way to learn is by building." - Every developer ever

Start small, build incrementally, and don't be afraid to ask for help. The FastAPI community is friendly and supportive!

Happy building! 🚀

---

**Resources Summary:**

- **Documentation**: https://fastapi.tiangolo.com/
- **GitHub**: https://github.com/fastapi/fastapi
- **Discord**: https://discord.gg/VQjSZaeJmf
- **Discussions**: https://github.com/fastapi/fastapi/discussions
- **Awesome List**: https://github.com/mjhea0/awesome-fastapi
- **Full-Stack Template**: https://github.com/fastapi/full-stack-fastapi-template

**Created with ❤️ by the FastAPI community**
