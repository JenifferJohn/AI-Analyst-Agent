from analytics.insight_engine import generate_insights
from analytics.root_cause_engine import discover_root_cause
from analytics.chart_selector import choose_chart


def run_analysis(df):
    """
    Full analytics pipeline
    """

    insights = generate_insights(df)

    numeric_cols = df.select_dtypes(include="number").columns

    root_cause = {}

    if len(numeric_cols) > 0:

        target = numeric_cols[0]

        root_cause = discover_root_cause(df, target)

    chart = choose_chart(df)

    return insights, root_cause, chart