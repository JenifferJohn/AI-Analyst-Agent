import pandas as pd


def discover_root_cause(df, target_column=None):
    """
    Identify strongest drivers using correlation analysis
    """

    try:

        if df is None or df.empty:
            return {"message": "Dataset is empty."}

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.shape[1] < 2:
            return {"message": "Not enough numeric columns for root cause analysis."}

        # ---------- TARGET COLUMN SELECTION ----------
        if target_column is None or target_column not in numeric_df.columns:
            target_column = numeric_df.columns[0]

        # ---------- CORRELATION ----------
        correlations = numeric_df.corr()[target_column]
        correlations = correlations.drop(target_column)

        sorted_corr = correlations.sort_values(ascending=False)

        top_positive = sorted_corr.head(5)
        top_negative = sorted_corr.sort_values().head(3)

        root_cause = {
            "target_column": target_column,
            "top_positive_drivers": top_positive.to_dict(),
            "top_negative_drivers": top_negative.to_dict()
        }

        # ---------- ADDITIONAL INSIGHTS ----------
        insights = []

        # strongest correlation
        if not sorted_corr.empty:
            strongest_driver = sorted_corr.idxmax()
            strongest_value = sorted_corr.max()

            insights.append(
                f"{strongest_driver} shows strongest positive correlation with "
                f"{target_column} ({strongest_value:.2f})"
            )

        # strongest negative
        if not sorted_corr.empty:
            weakest_driver = sorted_corr.idxmin()
            weakest_value = sorted_corr.min()

            insights.append(
                f"{weakest_driver} shows strongest negative correlation with "
                f"{target_column} ({weakest_value:.2f})"
            )

        root_cause["insights"] = insights

        return root_cause

    except Exception:

        return {
            "message": "Root cause analysis failed."
        }