from langchain_community.llms import Ollama

llm = Ollama(model="llama3")


def run_tech_agent(query, context):

    schema = context["schema"]
    insights = context["insights"]
    root_cause = context["root_cause"]

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

    return response