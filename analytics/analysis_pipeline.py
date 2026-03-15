from analytics.insight_engine import generate_insights
from analytics.root_cause_engine import discover_root_cause
from analytics.chart_selector import choose_chart


def run_analysis(df):
    """
    Full analytics pipeline
    Runs insights → root cause → visualization
    """

    try:

        # -------- DATASET VALIDATION --------
        if df is None or df.empty:
            return {
                "status": "warning",
                "message": "Dataset is empty.",
                "data": None,
                "suggestions": [
                    "Upload a valid dataset",
                    "Check if Excel file loaded correctly"
                ]
            }

        # -------- PRECOMPUTE NUMERIC COLUMNS (avoid recomputation) --------
        numeric_cols = df.select_dtypes(include="number").columns

        # -------- INSIGHT ENGINE --------
        insights = generate_insights(df)

        # -------- ROOT CAUSE ENGINE --------
        root_cause = {}

        if len(numeric_cols) >= 2:

            # choose first numeric column as target
            target_column = numeric_cols[0]

            root_cause = discover_root_cause(df, target_column)

        elif len(numeric_cols) == 1:

            root_cause = {
                "message": "Only one numeric column available. Root cause requires multiple variables."
            }

        else:

            root_cause = {
                "message": "No numeric columns available for root cause analysis."
            }

        # -------- CHART SELECTION --------
        chart = choose_chart(df)

        # -------- SUGGESTIONS FOR USER --------
        suggestions = []

        if len(numeric_cols) > 1:
            suggestions.append("Ask which variables influence the target metric")

        if len(df.columns) > 2:
            suggestions.append("Ask for correlations between variables")

        suggestions.append("Ask for trend insights")

        # -------- FINAL RESPONSE --------
        return {
            "status": "success",
            "message": None,
            "data": {
                "insights": insights,
                "root_cause": root_cause,
                "chart": chart
            },
            "suggestions": suggestions
        }

    except Exception as e:

        return {
            "status": "warning",
            "message": f"Analysis pipeline failed: {str(e)}",
            "data": None,
            "suggestions": [
                "Upload dataset with numeric columns",
                "Check dataset format",
                "Try a different dataset"
            ]
        }