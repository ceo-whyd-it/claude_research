"""
02-core-concepts/custom_tools_demo.py
---------------------------------------
Demonstrates creating custom tools via in-process MCP servers.

Shows:
  - @tool decorator for defining custom tools
  - create_sdk_mcp_server to bundle tools
  - Registering the server with ClaudeAgentOptions
  - Claude calling your custom tools autonomously

Run:
  python custom_tools_demo.py
"""

import asyncio
from typing import Any
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)


# ─────────────────────────────────────────────
# Define custom tools with @tool decorator
# ─────────────────────────────────────────────

@tool(
    "add",                          # Tool name (used in allowed_tools)
    "Add two numbers together",     # Description (shown to Claude)
    {"a": float, "b": float},       # Input schema {param_name: type}
)
async def add(args: dict[str, Any]) -> dict:
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} + {args['b']} = {result}"}]
    }


@tool(
    "multiply",
    "Multiply two numbers",
    {"a": float, "b": float},
)
async def multiply(args: dict[str, Any]) -> dict:
    result = args["a"] * args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} × {args['b']} = {result}"}]
    }


@tool(
    "get_product_info",
    "Look up product information by product ID",
    {"product_id": str},
)
async def get_product_info(args: dict[str, Any]) -> dict:
    """
    Simulates a database lookup.
    In real code, you'd query your actual database here.
    """
    # Mock database
    products = {
        "P001": {"name": "Widget Pro", "price": 29.99, "stock": 142},
        "P002": {"name": "Gadget Elite", "price": 99.99, "stock": 7},
        "P003": {"name": "Doohickey Plus", "price": 14.99, "stock": 0},
    }

    product_id = args["product_id"].upper()
    if product_id in products:
        p = products[product_id]
        status = "In Stock" if p["stock"] > 0 else "Out of Stock"
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"Product: {p['name']}\n"
                    f"Price: ${p['price']:.2f}\n"
                    f"Stock: {p['stock']} units ({status})"
                )
            }]
        }
    else:
        return {
            "content": [{"type": "text", "text": f"Product '{product_id}' not found in database."}]
        }


@tool(
    "calculate_discount",
    "Calculate discounted price",
    {"original_price": float, "discount_percent": float},
)
async def calculate_discount(args: dict[str, Any]) -> dict:
    original = args["original_price"]
    discount = args["discount_percent"]
    discounted = original * (1 - discount / 100)
    savings = original - discounted
    return {
        "content": [{
            "type": "text",
            "text": (
                f"Original price: ${original:.2f}\n"
                f"Discount: {discount}%\n"
                f"Final price: ${discounted:.2f}\n"
                f"You save: ${savings:.2f}"
            )
        }]
    }


# ─────────────────────────────────────────────
# Bundle tools into in-process MCP servers
# ─────────────────────────────────────────────

# Server 1: Calculator tools
calculator_server = create_sdk_mcp_server(
    name="calculator",
    version="1.0.0",
    tools=[add, multiply, calculate_discount],
)

# Server 2: E-commerce tools
ecommerce_server = create_sdk_mcp_server(
    name="ecommerce",
    version="1.0.0",
    tools=[get_product_info],
)


# ─────────────────────────────────────────────
# Demo 1: Calculator agent
# ─────────────────────────────────────────────
async def demo_calculator():
    print("=== Demo 1: Calculator Agent ===\n")

    options = ClaudeAgentOptions(
        mcp_servers={
            "calc": calculator_server,   # Register server under alias "calc"
        },
        # Tool naming: mcp__{server-alias}__{tool-name}
        allowed_tools=[
            "mcp__calc__add",
            "mcp__calc__multiply",
            "mcp__calc__calculate_discount",
        ],
        permission_mode="acceptEdits",
    )

    async for message in query(
        prompt=(
            "I need help with some calculations: "
            "1. What is 15.5 + 23.7? "
            "2. What is 7 × 8? "
            "3. A jacket costs $120. There's a 25% discount. What's the final price?"
        ),
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n  [Cost: ${message.total_cost_usd:.4f}]")


# ─────────────────────────────────────────────
# Demo 2: E-commerce support agent
# ─────────────────────────────────────────────
async def demo_ecommerce():
    print("\n\n=== Demo 2: E-commerce Support Agent ===\n")

    options = ClaudeAgentOptions(
        system_prompt=(
            "You are a helpful e-commerce customer support agent. "
            "Use your tools to look up product information and help customers."
        ),
        mcp_servers={
            "calc": calculator_server,
            "store": ecommerce_server,
        },
        allowed_tools=[
            "mcp__calc__calculate_discount",
            "mcp__store__get_product_info",
        ],
        permission_mode="acceptEdits",
    )

    async for message in query(
        prompt=(
            "Customer inquiry: I'm interested in products P001 and P002. "
            "Can you check availability and pricing? "
            "Also, if I get a 10% loyalty discount on P002, what would I pay?"
        ),
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n  [Cost: ${message.total_cost_usd:.4f}]")


async def main():
    await demo_calculator()
    await demo_ecommerce()


asyncio.run(main())
