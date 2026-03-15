from langchain_community.llms import Ollama

llm = Ollama(model="llama3")


def run_tech_agent(query, context):

    try:

        schema = context.get("schema", "")
        insights = context.get("insights", "")
        root_cause = context.get("root_cause", "")

        prompt = f"""
You are a SENIOR DATA SCIENTIST answering a technical manager.

Dataset Schema:
{schema}

Insights from analytics engine:
{insights}

Root cause correlation drivers:
{root_cause}

User Question:
{query}

Instructions:

- Provide deeper analytical explanation
- Explain correlations and possible drivers
- Suggest further investigation steps
- Do NOT invent numbers
- Only use provided context

Structure response:

1. Analytical Insight
2. Root Cause Interpretation
3. Technical Recommendation
"""

        response = llm.invoke(prompt)

        return {
            "status": "success",
            "message": None,
            "data": response,
            "suggestions": []
        }

    except Exception:

        return {
            "status": "warning",
            "message": "Technical analysis failed",
            "data": None,
            "suggestions": [
                "Ask about correlations",
                "Ask which variables influence the outcome",
                "Ask what further analysis can be performed"
            ]
        }