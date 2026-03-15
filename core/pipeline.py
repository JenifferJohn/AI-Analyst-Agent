from semantic_layer.business_mapper import map_business_terms
from agents.clarification_agent import clarify_question
from guardrails.guardrail_controller import (
    run_input_guardrail,
    run_context_guardrail,
    run_output_guardrail
)
from analytics.analysis_pipeline import run_analysis
from agents.persona_router import route_persona
from core.intent_classifier import classify_intent


def run_ai_pipeline(query, df, persona):

    result = {
        "status": "success",
        "message": None,
        "insights": [],
        "root_cause": {},
        "chart": None,
        "response": None
    }

    query = map_business_terms(query)

    clarification = clarify_question(query, df)

    if clarification:
        result["message"] = clarification

    guard = run_input_guardrail(query, df)

    if guard["status"] != "success":
        result["message"] = guard["message"]

    intent = classify_intent(query)

    analysis = run_analysis(df)

    if analysis["status"] == "success":

        data = analysis["data"]

        insights = data["insights"]
        root_cause = data["root_cause"]
        chart = data["chart"]

        if intent == "chart":
            insights = []

        elif intent == "root_cause":
            chart = None

        result["insights"] = insights
        result["root_cause"] = root_cause
        result["chart"] = chart

    context = run_context_guardrail(
        df,
        result["insights"],
        result["root_cause"]
    )["data"]

    persona_result = route_persona(persona, query, context)

    output = run_output_guardrail(
        persona_result["data"],
        df
    )

    if output["status"] == "success":
        result["response"] = output["data"]

    return result