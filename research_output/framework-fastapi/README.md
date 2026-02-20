# FastAPI Learning Path

A comprehensive, progressive learning guide for FastAPI — the modern, high-performance Python web framework for building APIs.

## What is FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.10+ based on standard Python type hints. It's designed to be:

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic)
- **Fast to code**: Increase development speed by 200-300%
- **Fewer bugs**: Reduce human-induced errors by approximately 40%
- **Intuitive**: Great editor support with auto-completion everywhere
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication with multiple features per parameter
- **Robust**: Get production-ready code with automatic interactive documentation
- **Standards-based**: Based on OpenAPI and JSON Schema

## Who Should Use This Guide?

This learning path is for:

- Python developers wanting to build modern REST APIs
- Backend engineers transitioning from Flask or Django
- Developers building microservices or ML model APIs
- Anyone needing automatic API documentation
- Teams prioritizing developer experience and productivity

**Prerequisites:**
- Python 3.10+ knowledge
- Basic understanding of HTTP and REST APIs
- Familiarity with async/await is helpful but not required

## How to Use This Learning Path

This guide is structured into **5 progressive levels**:

### Level 1: Overview & Motivation (15-20 minutes)
Understand what FastAPI is, what problems it solves, and when to use it.

### Level 2: Setup & First Project (30-45 minutes)
Get FastAPI installed and run your first API with automatic documentation.

### Level 3: Architecture & Core Concepts (1-2 hours)
Learn the fundamental concepts: path operations, request bodies, dependency injection, validation, and documentation.

### Level 4: Building Real Applications (3-4 hours)
Build a complete TODO API with database, authentication, testing, and deployment.

### Level 5: Next Steps (Reference)
Advanced topics, best resources, community channels, and where to go deeper.

## File Structure

```
framework-fastapi/
├── README.md              # This file - start here
├── resources.md           # All links organized by source
├── learning-path.md       # Main learning content (5 levels)
└── code-examples/         # Runnable code for each section
    ├── 01-hello-world/    # Your first FastAPI app
    ├── 02-core-concepts/  # Examples for each core concept
    └── 03-real-app/       # Complete TODO API application
```

## Recommended Learning Flow

1. **Read `learning-path.md`** from Level 1 through Level 5 sequentially
2. **Run the code examples** in `code-examples/` as you progress
3. **Refer to `resources.md`** for official docs, tutorials, and community resources
4. **Build your own project** after completing Level 4

## Quick Start

If you want to dive in immediately:

```bash
# Install FastAPI with all standard dependencies
pip install "fastapi[standard]"

# Create your first API (main.py)
echo 'from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}' > main.py

# Run the development server
fastapi dev main.py

# Visit http://127.0.0.1:8000/docs for interactive API docs
```

## Time Commitment

- **Minimum (basics)**: 2-3 hours (Levels 1-3)
- **Recommended (complete)**: 5-7 hours (Levels 1-4)
- **Comprehensive (with practice)**: 10-15 hours (Levels 1-5 + building projects)

## What You'll Build

By the end of this learning path, you'll have:

1. A working understanding of FastAPI's architecture
2. A complete TODO API with:
   - RESTful endpoints (CRUD operations)
   - Database integration (SQLModel)
   - Authentication (OAuth2 + JWT)
   - Data validation (Pydantic)
   - Automatic API documentation
   - Unit tests
   - Deployment configuration
3. Knowledge of where to find help and go deeper

## Additional Resources

- **Official Documentation**: https://fastapi.tiangolo.com/
- **GitHub Repository**: https://github.com/tiangolo/fastapi
- **Full Resources List**: See `resources.md` in this directory

## Getting Help

- **Discord**: https://discord.gg/VQjSZaeJmf
- **GitHub Discussions**: https://github.com/fastapi/fastapi/discussions
- **Official Help Page**: https://fastapi.tiangolo.com/help-fastapi/

## Version Information

- **FastAPI Version**: 0.129.0 (February 2026)
- **Python Requirement**: 3.10+
- **Last Updated**: February 2026

## Ready to Start?

Open `learning-path.md` and begin with Level 1: Overview & Motivation.

Happy learning! 🚀
