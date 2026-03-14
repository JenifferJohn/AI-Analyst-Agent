import re


# Example business dictionary
# maps business terms to dataset column names
BUSINESS_TERMS = {
    "revenue": "sales_amount",
    "sales": "sales_amount",
    "income": "sales_amount",
    "profit": "net_profit",
    "margin": "profit_margin",
    "marketing": "marketing_spend",
    "marketing spend": "marketing_spend",
    "customers": "customer_count",
    "orders": "order_volume"
}


def map_business_terms(query):
    """
    Replace business terms in user query with dataset column names.
    """

    query_lower = query.lower()

    for term, column in BUSINESS_TERMS.items():

        if re.search(rf"\b{term}\b", query_lower):

            query_lower = query_lower.replace(term, column)

    return query_lower