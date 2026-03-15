def clarify_question(query, df):

    query_lower = query.lower()

    columns = [c.lower() for c in df.columns]

    matched_columns = []

    for col in columns:

        # split column name into keywords
        parts = col.split("_")

        for p in parts:

            if p in query_lower:
                matched_columns.append(col)
                break

    if len(matched_columns) == 0:

        return (
            "Please specify which metric you want to analyze. "
            f"Available metrics: {', '.join(columns[:5])}"
        )

    if len(matched_columns) > 1:

        return (
            "Your question refers to multiple metrics. "
            f"Please clarify which one: {', '.join(matched_columns)}"
        )

    return None