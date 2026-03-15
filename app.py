import streamlit as st
import pandas as pd

# analytics
from analytics.analysis_pipeline import run_analysis

# agents
from agents.persona_router import route_persona
from agents.clarification_agent import clarify_question

# semantic layer
from semantic_layer.business_mapper import map_business_terms

# guardrails
from guardrails.guardrail_controller import (
    run_input_guardrail,
    run_context_guardrail,
    run_output_guardrail
)

st.set_page_config(
    page_title="AI Analyst",
    layout="wide"
)

st.title("AI Analyst")
st.caption("Conversational analytics with guardrails")

# ------------------------------
# Persona Selection
# ------------------------------

profile = st.selectbox(
    "Select User Profile",
    [
        "Non-technical Manager",
        "Technical Manager"
    ]
)

# ------------------------------
# File Upload
# ------------------------------

uploaded_file = st.file_uploader(
    "Upload Excel Dataset",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("Columns:", list(df.columns))

    # ------------------------------
    # Chat Input
    # ------------------------------

    query = st.chat_input("Ask a question about your data")

    if query:

        # ------------------------------
        # Semantic Business Mapping
        # ------------------------------

        query = map_business_terms(query)

        # ------------------------------
        # Guardrail 1: Input Validation
        # ------------------------------

        valid, message = run_input_guardrail(query, df)

        if not valid:

            st.error(message)
            st.stop()

        # ------------------------------
        # Clarification Agent
        # ------------------------------

        clarification = clarify_question(query, df)

        if clarification:

            st.warning(clarification)
            st.stop()

        # ------------------------------
        # Run Analytics Engine
        # ------------------------------

        insights, root_cause, chart = run_analysis(df)

        # ------------------------------
        # Guardrail 2: Context Protection
        # ------------------------------

        context = run_context_guardrail(
            df,
            insights,
            root_cause
        )

        # ------------------------------
        # Persona Routing
        # ------------------------------

        response = route_persona(
            profile,
            query,
            context
        )

        # ------------------------------
        # Guardrail 3: Output Validation
        # ------------------------------

        valid, message = run_output_guardrail(
            response,
            df
        )

        if not valid:

            st.warning("Output guardrail triggered")
            st.write(message)
            st.stop()

        # ------------------------------
        # Display Results
        # ------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Automatic Insights")

            for insight in insights:
                st.write("- ", insight)

            st.subheader("Root Cause Drivers")

            st.json(root_cause)

        with col2:

            st.subheader("Recommended Chart")

            if chart:
                st.plotly_chart(chart, use_container_width=True)

        st.subheader("AI Explanation")

        st.write(response)