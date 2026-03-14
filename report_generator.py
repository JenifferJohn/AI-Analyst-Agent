import pandas as pd
import os

def export_report(df):

    if not os.path.exists("exports"):
        os.makedirs("exports")

    path = "exports/report.xlsx"

    df.to_excel(path, index=False)