from mcp.server import Server
from mcp_server.tools import (
    get_schema,
    run_insight_tool,
    run_root_cause_tool,
    run_chart_tool
)

server = Server("excel-ai-analytics-tools")


@server.tool()
def dataset_schema():
    """
    Return dataset columns
    """
    return get_schema()


@server.tool()
def generate_insights():
    """
    Generate dataset insights
    """
    return run_insight_tool()


@server.tool()
def root_cause_analysis(target_column: str = None):
    """
    Run root cause discovery
    """
    return run_root_cause_tool(target_column)


@server.tool()
def generate_chart():
    """
    Generate recommended chart
    """
    return run_chart_tool()


if __name__ == "__main__":
    server.run()