def clarify_question(query, df):

    columns = [c.lower() for c in df.columns]
    matches = [c for c in columns if c in query.lower()]

    if len(matches) == 0:
        return "Please specify which metric you want to analyze."

    if len(matches) > 1:
        return "Multiple metrics detected. Please clarify."

    return None