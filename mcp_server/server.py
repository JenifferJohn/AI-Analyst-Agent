from mcp.server import Server

from mcp_server.tools import (
    get_schema,
    run_insight_tool,
    run_root_cause_tool,
    run_chart_tool
)

# Global dataframe store
DATAFRAME = None


def set_dataframe(df):
    """
    Set dataset for MCP tools
    """
    global DATAFRAME
    DATAFRAME = df


# Initialize MCP server
server = Server("excel-ai-analytics-tools")


# DATASET SCHEMA TOOL

@server.tool()
def dataset_schema():
    """
    Return dataset schema information
    """

    try:

        if DATAFRAME is None:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload an Excel dataset first"
                ]
            }

        schema = get_schema()

        return {
            "status": "success",
            "message": None,
            "data": schema,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Schema retrieval failed.",
            "data": None,
            "suggestions": []
        }


# INSIGHT TOOL

@server.tool()
def generate_insights():
    """
    Generate statistical insights from dataset
    """

    try:

        if DATAFRAME is None:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload an Excel file"
                ]
            }

        insights = run_insight_tool()

        return {
            "status": "success",
            "message": None,
            "data": insights,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Insight generation failed.",
            "data": None,
            "suggestions": [
                "Check dataset structure"
            ]
        }



# ROOT CAUSE TOOL

@server.tool()
def root_cause_analysis(target_column: str = None):
    """
    Discover strongest drivers for a target column
    """

    try:

        if DATAFRAME is None:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload dataset first"
                ]
            }

        result = run_root_cause_tool(target_column)

        return {
            "status": "success",
            "message": None,
            "data": result,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Root cause analysis failed.",
            "data": None,
            "suggestions": []
        }


# CHART TOOL

@server.tool()
def generate_chart():
    """
    Generate recommended business chart
    """

    try:

        if DATAFRAME is None:

            return {
                "status": "warning",
                "message": "Dataset not loaded.",
                "data": None,
                "suggestions": [
                    "Upload dataset first"
                ]
            }

        chart = run_chart_tool()

        return {
            "status": "success",
            "message": None,
            "data": chart,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Chart generation failed.",
            "data": None,
            "suggestions": []
        }


# START SERVER

if __name__ == "__main__":
    server.run()