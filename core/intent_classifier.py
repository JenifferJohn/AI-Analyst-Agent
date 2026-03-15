def classify_intent(query):

    q = query.lower()

    if any(x in q for x in ["chart","plot","graph","visualize"]):
        return "chart"

    if any(x in q for x in ["why","driver","cause","impact"]):
        return "root_cause"

    if any(x in q for x in ["insight","trend","pattern"]):
        return "insight"

    if any(x in q for x in ["summary","overview","describe"]):
        return "summary"

    return "general"