
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "manufacturing_production_data.csv"
OUTPUT_PATH = BASE_DIR / "data" / "cleaned_manufacturing_data.csv"

# Load raw data
df = pd.read_csv(DATA_PATH)

print("Original shape:", df.shape)

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Convert production_date to datetime
df["production_date"] = pd.to_datetime(
    df["production_date"], errors="coerce"
)

# 3. Remove rows with invalid dates
df = df.dropna(subset=["production_date"])

# 4. Handle missing values
numeric_columns = [
    "operating_hours",
    "production_quantity",
    "defect_quantity",
    "downtime_minutes",
    "temperature_c",
    "pressure_bar",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=numeric_columns)

# 5. Validate important business values
df = df[
    (df["operating_hours"] >= 0)
    & (df["production_quantity"] >= 0)
    & (df["defect_quantity"] >= 0)
    & (df["downtime_minutes"] >= 0)
    & (df["defect_quantity"] <= df["production_quantity"])
]

# 6. Create useful analytical columns
df["defect_rate_pct"] = (
    df["defect_quantity"]
    .div(df["production_quantity"].replace(0, pd.NA))
    .fillna(0)
    .mul(100)
    .round(2)
)

df["production_month"] = (
    df["production_date"].dt.to_period("M").astype(str)
)

# 7. Save cleaned data
df.to_csv(OUTPUT_PATH, index=False)

print("Cleaned shape:", df.shape)
print("Duplicates remaining:", df.duplicated().sum())
print("Missing values remaining:", df.isnull().sum().sum())
print("Saved to:", OUTPUT_PATH)
