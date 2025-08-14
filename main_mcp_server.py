from fastmcp import FastMCP
import mcp_tools.db_search as db_search
import mcp_tools.db_crud as db_crud
import mcp_tools.mitre_visualize as mitre_visualize
import mcp_tools.show_stats as show_stats

mcp = FastMCP("POC Policy Helper")

# Mount the sub-server's mcp instance
mcp.mount(db_search.mcp)
mcp.mount(db_crud.mcp)
mcp.mount(mitre_visualize.mcp)
mcp.mount(show_stats.mcp)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=11111)
