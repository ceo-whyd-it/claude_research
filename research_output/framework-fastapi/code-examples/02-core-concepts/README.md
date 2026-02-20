# Core Concepts Examples

## Files in This Directory

1. **path_operations.py** - HTTP methods, path parameters, Enums
2. **request_bodies.py** - Pydantic models, validation, nested models
3. **dependencies.py** - Dependency injection patterns

## How to Run

Each file can be run independently:

```bash
# Path operations
fastapi dev path_operations.py

# Request bodies
fastapi dev request_bodies.py

# Dependencies
fastapi dev dependencies.py
```

## What to Try

### Path Operations (path_operations.py)

1. **Test different HTTP methods**
   - GET: http://127.0.0.1:8000/items
   - POST: http://127.0.0.1:8000/items?name=NewItem
   - Try all methods in `/docs`

2. **Path parameters**
   - http://127.0.0.1:8000/users/42
   - http://127.0.0.1:8000/users/me (specific path)

3. **Enum validation**
   - http://127.0.0.1:8000/models/alexnet ✅
   - http://127.0.0.1:8000/models/vgg ❌ (should fail)

### Request Bodies (request_bodies.py)

1. **Basic POST request** (use `/docs` or curl):
   ```bash
   curl -X POST "http://127.0.0.1:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop", "price": 999.99, "tax": 99.99}'
   ```

2. **Test validation** - Try invalid data:
   ```json
   {
     "name": "Product",
     "price": -10,
     "quantity": -5
   }
   ```
   Should get validation errors!

3. **Nested models** - Create a company:
   ```json
   {
     "name": "Tech Corp",
     "address": {
       "street": "123 Main St",
       "city": "SF",
       "state": "CA",
       "zip_code": "94102"
     },
     "employees": ["Alice", "Bob"],
     "founded_year": 2020
   }
   ```

### Dependencies (dependencies.py)

1. **Common parameters**
   - http://127.0.0.1:8000/items/?q=laptop&skip=10&limit=20
   - http://127.0.0.1:8000/users/?q=john&skip=0&limit=5

2. **Database dependency**
   - http://127.0.0.1:8000/db-items/
   - Check console for connection messages!

3. **Authentication**
   ```bash
   # Without auth header (should fail)
   curl http://127.0.0.1:8000/user-area

   # With auth header (should succeed)
   curl -H "Authorization: Bearer secret-token" \
     http://127.0.0.1:8000/user-area
   ```

4. **Pagination**
   - http://127.0.0.1:8000/paginated-items/?skip=20&limit=10

## Key Concepts Demonstrated

### Path Operations
- ✅ HTTP method decorators (GET, POST, PUT, PATCH, DELETE)
- ✅ Path parameters with type validation
- ✅ Path order importance (specific before generic)
- ✅ Enum constraints for path parameters

### Request Bodies
- ✅ Pydantic models for validation
- ✅ Field-level constraints (min, max, regex)
- ✅ Custom validators
- ✅ Nested models
- ✅ Response models (exclude sensitive data)

### Dependencies
- ✅ Reusable dependency functions
- ✅ Sub-dependencies (dependencies with dependencies)
- ✅ Class-based dependencies
- ✅ Dependencies with cleanup (yield)
- ✅ Authentication patterns
- ✅ Path operation dependencies

## Common Mistakes to Avoid

❌ **Path Order**: Define specific paths before generic ones
```python
# WRONG
@app.get("/users/{user_id}")
@app.get("/users/me")  # Never matches!

# CORRECT
@app.get("/users/me")
@app.get("/users/{user_id}")
```

❌ **Optional Types**: Use `str | None` for optional parameters
```python
# WRONG
async def func(q: str = None):  # Type error

# CORRECT
async def func(q: str | None = None):  # ✅
```

❌ **Calling Dependencies**: Pass to Depends, don't call
```python
# WRONG
commons: dict = common_parameters()

# CORRECT
commons: dict = Depends(common_parameters)
```

## Next Steps

After understanding these core concepts, move to Level 4 in the learning path to build a complete TODO API!
