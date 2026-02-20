# Real Application: TODO API

A complete, production-ready TODO API with authentication, database, and tests.

## Features

✅ **User Registration & Authentication** (JWT tokens)
✅ **CRUD Operations** for TODO items
✅ **Database Integration** (SQLModel + SQLite)
✅ **Data Validation** (Pydantic)
✅ **Authorization** (Users can only access their own TODOs)
✅ **Unit Tests** (pytest)
✅ **Automatic API Documentation** (/docs)
✅ **Error Handling**
✅ **Docker Support** (optional)

## Project Structure

```
03-real-app/
├── app/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── config.py         # Settings and configuration
│   ├── database.py       # Database setup
│   ├── models.py         # SQLModel database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── auth.py           # Authentication logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints (register, login)
│       └── todos.py      # TODO CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures
│   └── test_todos.py     # Test cases
├── requirements.txt
├── .env.example
└── README.md (this file)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
SECRET_KEY=your-super-secret-key-min-32-characters-long
DATABASE_URL=sqlite:///./todo.db
```

### 3. Run the Application

```bash
# Development mode (auto-reload)
fastapi dev app/main.py

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Usage Guide

### 1. Register a User

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "is_active": true,
  "created_at": "2026-02-20T10:00:00"
}
```

### 2. Login to Get Token

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=SecurePass123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save this token!** You'll need it for all authenticated requests.

### 3. Create a TODO

**Request:**
```bash
TOKEN="your-access-token-here"

curl -X POST "http://127.0.0.1:8000/todos/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "completed": false,
  "created_at": "2026-02-20T10:05:00",
  "updated_at": null,
  "user_id": 1
}
```

### 4. Get All TODOs

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/todos/" \
  -H "Authorization: Bearer $TOKEN"
```

**With filters:**
```bash
# Only completed TODOs
curl -X GET "http://127.0.0.1:8000/todos/?completed=true" \
  -H "Authorization: Bearer $TOKEN"

# Pagination
curl -X GET "http://127.0.0.1:8000/todos/?skip=10&limit=5" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get a Specific TODO

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/todos/1" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Update a TODO

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:8000/todos/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true,
    "description": "Completed the FastAPI tutorial!"
  }'
```

### 7. Delete a TODO

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1" \
  -H "Authorization: Bearer $TOKEN"
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_todos.py -v
```

**Expected output:**
```
tests/test_todos.py::test_register_user PASSED
tests/test_todos.py::test_login_user PASSED
tests/test_todos.py::test_create_todo PASSED
tests/test_todos.py::test_get_todos PASSED
tests/test_todos.py::test_unauthorized_access PASSED
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/token` | Login and get JWT token | No |

### TODOs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/todos/` | Create a TODO | Yes |
| GET | `/todos/` | Get all TODOs (with filters) | Yes |
| GET | `/todos/{todo_id}` | Get specific TODO | Yes |
| PATCH | `/todos/{todo_id}` | Update TODO | Yes |
| DELETE | `/todos/{todo_id}` | Delete TODO | Yes |

### Other

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Welcome message | No |
| GET | `/health` | Health check | No |

## Docker Deployment (Optional)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
# Build image
docker build -t todo-api .

# Run container
docker run -d -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="sqlite:///./todo.db" \
  --name todo-api \
  todo-api
```

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong, random value (min 32 characters)
- [ ] Use PostgreSQL instead of SQLite
  ```
  DATABASE_URL=postgresql://user:password@localhost/tododb
  ```
- [ ] Enable HTTPS/TLS
- [ ] Set proper CORS origins (not `["*"]`)
- [ ] Add rate limiting
- [ ] Set up logging and monitoring
- [ ] Run with multiple workers:
  ```bash
  uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
  ```
- [ ] Use Gunicorn with Uvicorn workers:
  ```bash
  gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
  ```
- [ ] Set up database migrations (Alembic)
- [ ] Add health checks and readiness probes
- [ ] Configure proper error tracking (Sentry, etc.)

## Extending This Application

Ideas for additional features:

1. **TODO Categories/Tags**
   - Add category model and relationship
   - Filter TODOs by category

2. **Due Dates & Reminders**
   - Add due_date field
   - Background task to send reminders

3. **Shared TODOs**
   - Allow sharing TODOs with other users
   - Permissions system

4. **File Attachments**
   - Allow file uploads on TODOs
   - S3/cloud storage integration

5. **Search Functionality**
   - Full-text search across titles/descriptions
   - ElasticSearch integration

6. **Admin Panel**
   - Use SQLAdmin or FastAPI Admin
   - Manage users and TODOs

7. **WebSocket Notifications**
   - Real-time updates when TODOs change
   - Collaborative TODO lists

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'app'`
- **Solution**: Run from the `03-real-app` directory: `fastapi dev app/main.py`

**Problem**: Database locked error
- **Solution**: SQLite doesn't handle concurrent writes well. Use PostgreSQL for production.

**Problem**: 401 Unauthorized errors
- **Solution**: Ensure you're passing the token correctly:
  ```bash
  curl -H "Authorization: Bearer YOUR_TOKEN" http://...
  ```

**Problem**: Validation errors
- **Solution**: Check the `/docs` page for expected request format

## Learning Objectives

After working through this example, you should understand:

✅ How to structure a FastAPI project
✅ How to integrate a database (SQLModel)
✅ How to implement JWT authentication
✅ How to use dependency injection for auth and database
✅ How to organize code with routers
✅ How to write tests for FastAPI applications
✅ How to validate input data with Pydantic
✅ How to handle errors and authorization
✅ How to deploy a FastAPI application

## Next Steps

1. **Modify the application** - Add new features
2. **Deploy to cloud** - Try Heroku, AWS, or Azure
3. **Add a frontend** - Build a React or Vue.js UI
4. **Explore advanced topics** - See Level 5 in learning-path.md

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **JWT Tokens**: https://jwt.io/

---

**Built with ❤️ using FastAPI**
