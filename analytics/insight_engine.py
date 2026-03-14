import pandas as pd


def generate_insights(df):
    """
    Generate basic statistical insights from dataset
    """

    insights = []

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        insights.append("No numeric columns available for analysis.")
        return insights

    for col in numeric_cols:

        avg = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()

        insight = (
            f"{col}: average={avg:.2f}, "
            f"max={max_val:.2f}, "
            f"min={min_val:.2f}"
        )

        insights.append(insight)

    return insights