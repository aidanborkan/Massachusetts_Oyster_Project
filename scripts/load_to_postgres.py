from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

PROJECT_DIR = Path(r"C:\Users\suzan\Downloads\MOP")

INPUT_FILE = PROJECT_DIR / "data" / "processed" / "combined_westport_yarmouth_all_coordinates.xlsx"
SHEET_NAME = "Combined Data"

TABLE_NAME = "shell_recycling_dashboard"
SCHEMA = "public"

COLUMN_MAP = {
    "Year":"year",
    "Week #":"week_number",
    "Date":"collection_date",
    "Day of Week":"day_of_week",
    "Restaurant Name":"restaurant_name",
    "Total Buckets":"total_buckets",
    "Total Weight (lbs)":"total_weight_lbs",
    "Shell Only Weight":"shell_only_weight_lbs",
    "Gallons Water Used":"gallons_water_used",
    "$ Saved from Waste":"waste_cost_saved",
    "Tax Credit $":"tax_credit",
    "Latitude":"latitude",
    "Longitude":"longitude",
    "Town":"town",
    "Region":"region",
}

def main():
    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME, engine="openpyxl")
    df = df[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP)
    df["collection_date"] = pd.to_datetime(df["collection_date"]).dt.date

    url = URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    engine = create_engine(url)

    df.to_sql(
        TABLE_NAME,
        engine,
        schema=SCHEMA,
        if_exists="replace",
        index=False,
        method="multi"
    )

    print(f"Loaded {len(df)} rows into {SCHEMA}.{TABLE_NAME}")

if __name__ == "__main__":
    main()
