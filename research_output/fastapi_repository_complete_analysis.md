# FastAPI Repository Complete Analysis

## Repository Metadata

**Repository URL:** https://github.com/tiangolo/fastapi
**Creator:** Sebastián Ramírez (@tiangolo)
**License:** MIT (Copyright 2018)
**Documentation:** https://fastapi.tiangolo.com
**Latest Commit:** 2026-02-18 21:31:13 UTC
**Total Commits:** 6,946
**Python Support:** 3.10, 3.11, 3.12, 3.13, 3.14
**Current Version:** 0.129.0

---

## Project Overview

FastAPI is a modern, high-performance web framework for building APIs with Python. It combines Starlette and Uvicorn with Pydantic for type validation and automatic API documentation.

### Key Features

- **Performance:** On par with NodeJS and Go
- **Developer Speed:** 200-300% faster development
- **Fewer Bugs:** 40% reduction in errors
- **Standards:** Full OpenAPI and JSON Schema compliance
- **Production-Ready:** Automatic interactive documentation

---

## Core System Architecture

### Main Components

**fastapi/applications.py** (4,666 lines)
- FastAPI application class
- HTTP method decorators
- Middleware management
- OpenAPI configuration

**fastapi/routing.py** (4,626 lines)
- APIRouter class for modular routes
- Route prefix management
- Tag organization
- Dependencies at router level

**fastapi/dependencies/** 
- Dependency injection system
- Supports generator functions
- Testing overrides

**fastapi/security/**
- OAuth2 support
- API key authentication
- HTTP authentication (Basic, Bearer)
- OpenID Connect

**fastapi/middleware/**
- CORS middleware
- GZip compression
- HTTPS redirect
- Trusted hosts
- WSGI compatibility

**fastapi/openapi/**
- OpenAPI schema generation
- Swagger UI customization
- ReDoc support
- Documentation UI handlers

**docs_src/** 
- 73 comprehensive example directories
- Complete feature coverage
- Testing patterns

---

## Core Dependencies

**Required:**
- starlette>=0.40.0 - ASGI framework
- pydantic>=2.7.0 - Data validation
- typing-extensions>=4.8.0 - Type support
- typing-inspection>=0.4.2 - Introspection
- annotated-doc>=0.0.2 - Documentation

**Optional (standard):**
- fastapi-cli - CLI tools
- httpx - Test client
- jinja2 - Templates
- python-multipart - Forms/files
- email-validator - Email validation
- uvicorn - ASGI server
- pydantic-settings - Configuration
- pydantic-extra-types - Extra types

---

## Quick Start

### Installation

```bash
pip install "fastapi[standard]"
```

### Minimal Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Running

```bash
fastapi dev main.py
```

Visit http://127.0.0.1:8000/docs for Swagger UI.

---

## Examples (73 Total)

Organized by feature:

- first_steps - Basic API
- path_params - URL parameters
- query_params - Query strings
- body - Request bodies
- dependencies - Dependency injection
- security - Authentication
- middleware - Custom middleware
- cors - CORS configuration
- background_tasks - Async tasks
- websockets - WebSocket communication
- templates - Jinja2 rendering
- sql_databases - Database patterns
- bigger_applications - Project structure
- graphql - GraphQL integration
- custom_docs_ui - Custom documentation
- generate_clients - SDK generation

---

## Project Structure Pattern

```
app/
├── main.py              # Entry point
├── dependencies.py      # Shared dependencies
├── routers/
│   ├── users.py
│   └── items.py
└── internal/
    └── admin.py
```

**Example main.py:**
```python
from fastapi import FastAPI, Depends
from app.routers import items, users
from app.dependencies import get_query_token

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello"}
```

---

## Extension Points

### Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dependency Injection

```python
def get_db():
    db = DBConnection()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db = Depends(get_db)):
    return db.query("SELECT * FROM items")

# Testing
app.dependency_overrides[get_db] = lambda: FakeDB()
```

### Exception Handlers

```python
@app.exception_handler(CustomException)
async def handler(request: Request, exc: CustomException):
    return JSONResponse(status_code=418, content={"detail": str(exc)})
```

### APIRouter

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def read_users():
    return []

app.include_router(router)
```

### Security

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/secure/")
async def read_secure(credentials = Depends(security)):
    return credentials
```

### OpenAPI Customization

```python
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API",
        version="1.0.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Lifespan Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    yield
    print("Shutdown")

app = FastAPI(lifespan=lifespan)
```

---

## Technologies & Stack

### Core

- Starlette 0.40.0+ - ASGI framework
- Pydantic 2.7.0+ - Data validation
- Uvicorn 0.12.0+ - ASGI server
- Python 3.10+ - Runtime

### Additional

- Pydantic Settings - Configuration
- Pydantic Extra Types - Extended types
- Jinja2 - Templates
- Python-Multipart - Forms/files
- Email-Validator - Email validation
- HTTPX - HTTP client
- Typing Extensions - Type hints

### Security

- OAuth2 with Password/Bearer
- HTTP Basic/Bearer
- API keys (header, query, cookie)
- OpenID Connect
- Dependency-based auth

### Async/Concurrency

- Full asyncio support
- Async validators
- Async database drivers
- Background tasks
- WebSocket connections

---

## Key Statistics

- Repository: https://github.com/tiangolo/fastapi
- License: MIT (2018 Sebastián Ramírez)
- Commits: 6,946
- Language: Python
- Core Modules: 2 (total 9,292 lines)
- Examples: 73 tutorials
- Python: 3.10, 3.11, 3.12, 3.13, 3.14
- Updated: 2026-02-18
- Docs: 13 languages
- Testing: Comprehensive with benchmarks

---

## Notable Features

1. Automatic API Documentation - Swagger UI and ReDoc
2. Type Hints First-Class - Validation, documentation, IDE support
3. Zero Code Duplication - Single source of truth
4. Production Ready - Error handling, CORS, security
5. Easy Testing - Built-in TestClient
6. Async/Sync Support - Both endpoint types
7. Dependency Injection - Elegant and testable
8. Modular Routing - APIRouter composition
9. WebSocket Support - Full protocol support
10. Middleware Ecosystem - CORS, GZip, HTTPS, hosts, WSGI

