def clarify_question(query, df):

    """
    Detect ambiguous questions
    """

    columns = [c.lower() for c in df.columns]

    query_lower = query.lower()

    mentioned_columns = []

    for col in columns:

        if col in query_lower:

            mentioned_columns.append(col)

    if len(mentioned_columns) == 0:

        return "Your question is unclear. Please specify a metric or column from the dataset."

    if len(mentioned_columns) > 1:

        return "Your question references multiple metrics. Please specify which one you want to analyze."

    return None