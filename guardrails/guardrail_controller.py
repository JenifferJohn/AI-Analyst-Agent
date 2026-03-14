from guardrails.input_guardrail import validate_user_query
from guardrails.context_guardrail import build_safe_context
from guardrails.output_guardrail import validate_output


def run_input_guardrail(query, df):
    """
    Run query validation
    """

    return validate_user_query(query, df)


def run_context_guardrail(df, insights, root_cause):
    """
    Construct safe LLM context
    """

    return build_safe_context(df, insights, root_cause)


def run_output_guardrail(response, df):
    """
    Validate LLM output
    """

    return validate_output(response, df)