# Progressive Learning Framework — Frameworks

Structure for teaching software frameworks and SDKs in digestible levels.

## The Five Levels

### Level 1: Overview & Motivation

**Goal**: Understand WHAT and WHY

Cover:

- What problem does this framework solve?
- What existed before? Why is this better?
- Who uses it? For what types of applications?
- When should you NOT use it?
- Architecture overview at a glance (e.g., MVC, component-based, event-driven)

### Level 2: Setup & First Project

**Goal**: Get a project running locally

Cover:

- Prerequisites
- Installation steps
- Project scaffolding (CLI generators, starter templates)
- Directory structure walkthrough
- Minimal working project
- Run it, see output
- Verify it works

### Level 3: Architecture & Core Concepts

**Goal**: Understand the mental model and how the framework is structured

Cover:

- 3-5 fundamental concepts (e.g., routing, middleware, components, state)
- How they relate to each other
- Request/data lifecycle — how information flows through the framework
- Configuration and convention patterns
- One example per concept
- Common mistakes for each

### Level 4: Building Real Applications

**Goal**: Build something meaningful

Cover:

- A realistic mini-project that exercises core features
- Provide code examples progressively. For example, if the framework is a web framework:
  - first show a basic route/endpoint
  - then add data models and persistence
  - then add authentication or middleware
  - then add testing
- Plugin/extension ecosystem — the most useful packages
- Deployment considerations

### Level 5: Next Steps

**Goal**: Know where to go deeper

Cover:

- Advanced topics to explore (performance, scaling, advanced patterns)
- Best resources for each
- Community resources
- How to get help
- Propose a mini-project or hands-on exercises

## Code Example Principles

- Every example must be complete and runnable
- Start minimal, add complexity incrementally
- Show expected output
- Include comments for non-obvious parts
- Show common mistakes and fixes
- Use the framework's recommended project structure
