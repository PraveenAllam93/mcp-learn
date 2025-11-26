from mcp.server.fastmcp import FastMCP

from pathlib import Path
from urllib.parse import unquote
import fitz

mcp = FastMCP(name="Resorece Example")


@mcp.resource("file:///{name}")
def read_document(name: str) -> str:
    """Read a document by name."""
    name = name.strip()
    decoded_name = unquote(name).strip()
    file_path = Path() / "files" / decoded_name

    try:
        if not file_path.exists():
            return f"File not found: {name}"

        if not file_path.is_file():
            return f"Not a file: {name}"

        with fitz.open(file_path) as pdf:
            text = ""
            pages = len(pdf)
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text += page.get_text()

        response = f"[PDF - Size: {file_path.stat().st_size/1024:.2f} KB"
        response += f" - Pages: {pages}]\n---\n{text[:100]}"
        return response
    except PermissionError:
        return f"Permission denied: {name}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.resource("config://settings")
def get_settings() -> str:
    "Get Application settings."
    return """{
        "theme": "dark",
        "language": "en",
        "debug": false
    }"""


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
