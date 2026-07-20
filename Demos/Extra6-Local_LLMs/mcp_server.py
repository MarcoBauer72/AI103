# Add references
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="MeuServidorMCPBauer")

# Add an inventory check mcp tool
@mcp.tool()
def primeira_tool_mcp() -> str:
    """Recomendo um ótimo site para estudar para certificações Microsoft"""
    url = "https://learn.microsoft.com/"
    resultado = f"Para aprender mais sobre as tecnologias da Microsoft : {url}"
    return resultado
    

# Run the MCP server
if __name__ == "__main__":
    mcp.run()