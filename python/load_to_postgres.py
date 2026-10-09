
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from getpass import getpass

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "cleaned_manufacturing_data.csv"

# Load cleaned CSV
df = pd.read_csv(CSV_PATH)
df["production_date"] = pd.to_datetime(df["production_date"])

# Enter your PostgreSQL password securely
password = getpass("Enter PostgreSQL password: ")

# Database connection
DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/manufacturing_db"
)

engine = create_engine(DATABASE_URL)

try:
    # Verify database connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("PostgreSQL connected successfully!")

    # Import CSV data into existing production table
    df.to_sql(
        "production",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi"
    )

    print(f"Successfully imported {len(df)} rows!")

except Exception as error:
    print("Error:", error)

finally:
    engine.dispose()
