from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from pydantic import BaseModel
from typing import TypedDict

mcp = FastMCP(name="Tool Example")


class Response(BaseModel):
    a: int
    b: int
    result: int


class AdditionResponse(TypedDict):
    a: int
    b: int
    result: int


@mcp.tool()
def multiply(a: int, b: int) -> Response:
    """Multiply given two numbers"""
    return Response(a=a, b=b, result=a * b)


@mcp.tool()
def add(a: int, b: int) -> AdditionResponse:
    """Add two numbers"""
    return {"a": a, "b": b, "result": a + b}


@mcp.tool()
def subtract(a: int, b: int) -> dict[str, int]:
    """Subtract two numbers"""
    return {"value": a - b}


@mcp.tool()
def division(a: int, b: int) -> int | str:
    """Divide two numbers"""
    return a // b if b > 0 else "Not Valid"


@mcp.tool()
async def long_running_task(
    task_name: str, ctx: Context[ServerSession, None], steps: int = 5
) -> str:
    """Execute a task with progress updates."""
    await ctx.info(f"Starting: {task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Step {i + 1}/{steps}",
        )
        await ctx.debug(f"Completed step {i + 1}")

    return f"Task '{task_name}' completed"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
