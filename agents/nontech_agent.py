from langchain_community.llms import Ollama

llm = Ollama(model="llama3")


def run_nontech_agent(query, context):

    schema = context["schema"]
    insights = context["insights"]
    root_cause = context["root_cause"]

    prompt = f"""
You are a business analyst explaining insights to a NON-TECHNICAL manager.

Dataset Columns:
{schema}

Insights from analysis:
{insights}

Root cause drivers:
{root_cause}

User Question:
{query}

Instructions:
- Use simple business language
- Focus on key insights
- Highlight the most important drivers
- Give short recommendations
- DO NOT invent numbers
- Use ONLY the provided insights

Structure response:

1. Key Finding
2. Root Cause
3. Recommendation
"""

    response = llm.invoke(prompt)

    return response