from agents.nontech_agent import run_nontech_agent
from agents.tech_agent import run_tech_agent


def route_persona(profile, query, context):

    if profile == "Non-technical Manager":
        return run_nontech_agent(query, context)
    else:
        return run_tech_agent(query, context)