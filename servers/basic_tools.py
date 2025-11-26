from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import CallToolResult, TextContent

from pydantic import BaseModel
from typing import TypedDict, Annotated

mcp = FastMCP(name="Tool Example")


class Response(BaseModel):
    a: int
    b: int
    result: int


class AdditionResponse(TypedDict):
    a: int
    b: int
    result: int


class ValidationModel(BaseModel):
    """Model for validating structured output."""

    status: str
    data: dict[str, int]


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


@mcp.tool()
def advanced_tool() -> CallToolResult:
    """Return CallToolResult directly for full control including _meta field"""
    return CallToolResult(
        content=[TextContent(type="text", text="Response visible to the model")],
        _meta={"hidden": "data for client applications only"},
    )


@mcp.tool()
def validated_tool() -> Annotated[CallToolResult, ValidationModel]:
    """Return CallToolResult with structured output validation."""
    return CallToolResult(
        content=[TextContent(type="text", text="Validated response")],
        structuredContent={"status": "success", "data": {"result": 42}},
        _meta={"internal": "metadata"},
    )


@mcp.tool()
def empty_result_tool() -> CallToolResult:
    """For empty results, return CallToolResult with empty content."""
    return CallToolResult(content=[])


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
