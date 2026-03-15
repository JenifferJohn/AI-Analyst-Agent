import re


# -------- BUSINESS TERM MAPPING --------
# Maps business words → dataset columns

BUSINESS_TERMS = {

    # sales / revenue
    "revenue": "sales_value_in_inr",
    "sales": "sales_value_in_inr",
    "sales value": "sales_value_in_inr",
    "income": "sales_value_in_inr",

    # volume
    "volume": "sales_volume",
    "units sold": "sales_volume",
    "sales volume": "sales_volume",

    # product
    "product": "products",
    "sku": "products",

    # markets
    "market": "markets",
    "region": "markets",
    "territory": "markets",

    # time
    "month": "month",
    "time": "month",
    "period": "month",

    # growth
    "growth": "sales_value_pct_change_ya",
    "sales growth": "sales_value_pct_change_ya",
    "volume growth": "sales_volume_pct_change_ya",

    # market share
    "share": "share_of_sales_value_product",
    "market share": "share_of_sales_value_product",
    "volume share": "share_of_sales_volume_product",

    # distribution
    "distribution": "numeric_distribution_category",
    "reach": "weighted_distribution_reach_category",

    # pricing
    "price": "price_per_sales_unit",
    "unit price": "price_per_sales_unit",
    "price index": "price_index_product",

    # inventory
    "stock": "stocks_volume",
    "inventory": "stocks_volume",
    "days of supply": "days_of_supply_volume",

    # purchase
    "purchase": "purchase_volume",
    "buy": "purchase_volume"
}


# -------- COLUMN SEMANTIC MAPPING --------
# Maps messy column names → clean internal names

COLUMN_SEMANTIC_MAP = {

    "Month": "month",
    "Markets": "markets",
    "Products": "products",

    "Sales Value (In INR)": "sales_value_in_inr",
    "Sales (Volume)": "sales_volume",

    "Sales Value % Chg YA": "sales_value_pct_change_ya",
    "Sales (Volume) % Chg YA": "sales_volume_pct_change_ya",

    "Share of Sales Value - Product": "share_of_sales_value_product",
    "Share of Sales - Sales (Volume) - Product": "share_of_sales_volume_product",

    "Value Shr in Handlers (C) - Product - CATEGORY": "value_share_handlers_category",

    "Numeric Distribution Handling (C)": "numeric_distribution_category",

    "Weighted Distribution - Reach - CATEGORY": "weighted_distribution_reach_category",

    "Value / Wghtd Dist Reach (C) - CATEGORY": "value_per_weighted_reach_category",

    "(Volume) / Wghtd Dist Reach (C) - CATEGORY": "volume_per_weighted_reach_category",

    "Price per Sales Unit": "price_per_sales_unit",
    "Price per Sales (Volume)": "price_per_sales_volume",

    "Sales (Volume) Price Index - Product": "price_index_product",

    "Days of Supply (Volume)": "days_of_supply_volume",

    "Stocks (Volume)": "stocks_volume",
    "Stocks Forward (Volume)": "stocks_forward_volume",
    "Stocks Backward (Volume)": "stocks_backward_volume",

    "Stocks (Volume) Shr - Product": "stocks_volume_share_product",
    "Stocks Forward (Volume) Shr - Product": "stocks_forward_share_product",

    "Purchase (Volume)": "purchase_volume",
    "Purchase (Volume) Shr - Product": "purchase_volume_share_product",

    "Sales Value % Chg Prev": "sales_value_pct_change_prev",
    "Sales (Volume) % Chg Prev": "sales_volume_pct_change_prev",

    "Share of Sales Value Chg YA - Product": "share_sales_value_change_ya_product",
    "Share of Sales Value Chg Prev - Product": "share_sales_value_change_prev_product",

    "Share of Sales - Sales (Volume) Chg YA - Product": "share_sales_volume_change_ya_product",
    "Share of Sales - Sales (Volume) Chg Prev - Product": "share_sales_volume_change_prev_product",

    "Price per Sales (Volume) % Chg YA": "price_sales_volume_pct_change_ya",
    "Price per Sales (Volume) % Chg Prev": "price_sales_volume_pct_change_prev"
}


# -------- QUERY TERM MAPPING --------

def map_business_terms(query):
    """
    Replace business terms in user query with dataset column names.
    """

    if not query:
        return query

    query = query.lower()

    # sort terms by length to prevent partial matches
    sorted_terms = sorted(BUSINESS_TERMS.keys(), key=len, reverse=True)

    for term in sorted_terms:

        column = BUSINESS_TERMS[term]

        pattern = rf"\b{re.escape(term)}\b"

        query = re.sub(pattern, column, query)

    return query


# -------- OPTIONAL DATAFRAME COLUMN NORMALIZATION --------

def normalize_dataframe_columns(df):
    """
    Convert dataset column names into normalized semantic names.
    """

    if df is None:
        return df

    rename_map = {}

    for col in df.columns:

        if col in COLUMN_SEMANTIC_MAP:
            rename_map[col] = COLUMN_SEMANTIC_MAP[col]

    df = df.rename(columns=rename_map)

    return df