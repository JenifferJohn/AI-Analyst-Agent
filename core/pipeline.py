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
        "status":"success",
        "message":None,
        "insights":[],
        "root_cause":{},
        "chart":None,
        "response":None,
        "suggestions":[]
    }

    query = map_business_terms(query)

    clarification = clarify_question(query, df)

    if clarification:
        result["status"]="warning"
        result["message"]=clarification
        result["suggestions"]=[f"Analyze {df.columns[0]}"]
        return result

    guard = run_input_guardrail(query, df)

    if guard["status"]!="success":
        result["status"]="warning"
        result["message"]=guard["message"]
        result["suggestions"]=guard["suggestions"]
        return result

    intent = classify_intent(query)

    analysis = run_analysis(df)

    if analysis["status"]=="success":

        data = analysis["data"]

        if intent=="chart":
            result["chart"]=data["chart"]

        elif intent=="root_cause":
            result["root_cause"]=data["root_cause"]

        elif intent=="insight":
            result["insights"]=data["insights"]

        else:
            result["insights"]=data["insights"]
            result["root_cause"]=data["root_cause"]
            result["chart"]=data["chart"]

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

    if output["status"]=="success":
        result["response"]=output["data"]

    return result