# Hello World Example

## What This Demonstrates

- Creating a FastAPI application instance
- Defining path operations with decorators (`@app.get()`)
- Path parameters (`{item_id}`)
- Query parameters (`q`)
- Automatic type validation
- Automatic API documentation

## How to Run

```bash
# Install FastAPI if you haven't already
pip install "fastapi[standard]"

# Run the development server
fastapi dev main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

## What to Try

1. **Visit the root endpoint**
   - URL: http://127.0.0.1:8000/
   - Expected: `{"message": "Hello World"}`

2. **Try path parameters**
   - URL: http://127.0.0.1:8000/items/42
   - Expected: `{"item_id": 42, "q": null}`

3. **Try query parameters**
   - URL: http://127.0.0.1:8000/items/42?q=test
   - Expected: `{"item_id": 42, "q": "test"}`

4. **View automatic documentation**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc
   - Try out requests directly in the browser!

5. **Test type validation**
   - Try: http://127.0.0.1:8000/items/abc
   - Expected: Validation error (item_id must be integer)

## Key Takeaways

✅ FastAPI apps start with creating an `app = FastAPI()` instance

✅ Use decorators like `@app.get()` to define endpoints

✅ Type hints provide automatic validation

✅ Documentation is generated automatically

✅ `async def` is recommended for I/O operations
