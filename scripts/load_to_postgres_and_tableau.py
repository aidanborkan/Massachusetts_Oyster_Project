from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import URL, create_engine


# ---------------------------------------------------------------------
# Project setup
# ---------------------------------------------------------------------
# This script belongs in:
#   C:\Users\suzan\Downloads\MOP\scripts\
#
# PROJECT_DIR resolves to the MOP repository root.
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Allow this script to import config.py from the repository root.
sys.path.insert(0, str(PROJECT_DIR))

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# ---------------------------------------------------------------------
# File and database settings
# ---------------------------------------------------------------------

# Cleaned and geocoded source workbook.
INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "combined_westport_yarmouth_all_coordinates.xlsx"
)

# Tableau Public cannot connect directly to PostgreSQL, so this script
# also creates a Tableau-ready Excel file after updating PostgreSQL.
TABLEAU_OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "tableau_dashboard.xlsx"
)

SOURCE_SHEET_NAME = "Combined Data"
TABLEAU_SHEET_NAME = "Shell Recycling"

# Dedicated dashboard table. The older table is left untouched.
TABLE_NAME = "shell_recycling_dashboard"
SCHEMA = "public"


# ---------------------------------------------------------------------
# Column standardization
# ---------------------------------------------------------------------

COLUMN_MAP = {
    "Year": "year",
    "Week #": "week_number",
    "Date": "collection_date",
    "Day of Week": "day_of_week",
    "Restaurant Name": "restaurant_name",
    "Total Buckets": "total_buckets",
    "Total Weight (lbs)": "total_weight_lbs",
    "Shell Only Weight": "shell_only_weight_lbs",
    "Gallons Water Used": "gallons_water_used",
    "$ Saved from Waste": "waste_cost_saved",
    "Tax Credit $": "tax_credit",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Town": "town",
    "Region": "region",
}


def main() -> None:
    """Load the processed workbook into PostgreSQL and export for Tableau."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input workbook not found: {INPUT_FILE}")

    # Read the combined source data.
    df = pd.read_excel(
        INPUT_FILE,
        sheet_name=SOURCE_SHEET_NAME,
        engine="openpyxl",
    )

    # Confirm that the expected columns are present.
    missing_columns = [
        column for column in COLUMN_MAP if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            "The input workbook is missing required columns: "
            + ", ".join(missing_columns)
        )

    # Keep only the dashboard fields and standardize their names.
    df = df[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP)

    # Remove fully blank spreadsheet rows.
    df = df.dropna(how="all")

    # Convert Excel dates into real date values.
    df["collection_date"] = pd.to_datetime(
        df["collection_date"],
        errors="coerce",
    ).dt.date

    # Clean restaurant names and remove invalid rows.
    df["restaurant_name"] = (
        df["restaurant_name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )
    df = df[
        (df["restaurant_name"] != "")
        & df["collection_date"].notna()
    ].copy()

    # Create the PostgreSQL connection from config.py.
    url = URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    engine = create_engine(url, pool_pre_ping=True)

    # Refresh only the dedicated dashboard table.
    df.to_sql(
        TABLE_NAME,
        engine,
        schema=SCHEMA,
        if_exists="replace",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df)} rows into {SCHEMA}.{TABLE_NAME}")

    # Ensure the output folder exists.
    TABLEAU_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Export the same cleaned data for Tableau Public.
    # The filename stays the same so Tableau can keep using one source.
    with pd.ExcelWriter(
        TABLEAU_OUTPUT_FILE,
        engine="openpyxl",
    ) as writer:
        df.to_excel(
            writer,
            sheet_name=TABLEAU_SHEET_NAME,
            index=False,
        )

    print(f"Created Tableau extract: {TABLEAU_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
