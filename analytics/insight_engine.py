import pandas as pd


def generate_insights(df):
    """
    Generate statistical insights from dataset
    """

    insights = []

    try:

        if df is None or df.empty:
            insights.append("Dataset is empty.")
            return insights

        # ---------- Dataset Overview ----------
        insights.append(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

        # ---------- Numeric Analysis ----------
        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            insights.append("No numeric columns available for analysis.")
        else:

            for col in numeric_cols:

                avg = df[col].mean()
                max_val = df[col].max()
                min_val = df[col].min()
                std_val = df[col].std()

                insight = (
                    f"{col}: average={avg:.2f}, "
                    f"max={max_val:.2f}, "
                    f"min={min_val:.2f}, "
                    f"std_dev={std_val:.2f}"
                )

                insights.append(insight)

            # ---------- Describe Summary ----------
            describe_stats = df[numeric_cols].describe()

            for col in numeric_cols:
                insights.append(
                    f"{col} median={describe_stats.loc['50%', col]:.2f}, "
                    f"25th percentile={describe_stats.loc['25%', col]:.2f}, "
                    f"75th percentile={describe_stats.loc['75%', col]:.2f}"
                )

        # ---------- Missing Values ----------
        missing = df.isnull().sum()
        missing = missing[missing > 0]

        for col, val in missing.items():
            insights.append(f"{col} has {val} missing values.")

        # ---------- Categorical Insights ----------
        categorical_cols = df.select_dtypes(include="object").columns

        for col in categorical_cols:

            top_values = df[col].value_counts().head(3)

            for category, count in top_values.items():
                insights.append(
                    f"Top category in {col}: {category} ({count} occurrences)"
                )

        # ---------- Correlation Insights ----------
        if len(numeric_cols) > 1:

            corr_matrix = df[numeric_cols].corr()

            for col in numeric_cols:

                correlations = corr_matrix[col].drop(col)

                if not correlations.empty:
                    top_corr = correlations.abs().idxmax()
                    corr_val = correlations[top_corr]

                    insights.append(
                        f"{col} is strongly correlated with {top_corr} (correlation={corr_val:.2f})"
                    )

        return insights

    except Exception:

        insights.append("Insight generation failed.")
        return insights