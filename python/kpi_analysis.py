
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "cleaned_manufacturing_data.csv"

df = pd.read_csv(DATA_PATH)

total_production = df["production_quantity"].sum()
total_defects = df["defect_quantity"].sum()

defect_rate = (
    total_defects / total_production * 100
    if total_production > 0 else 0
)

total_downtime = df["downtime_minutes"].sum()
total_operating_hours = df["operating_hours"].sum()
unique_machines = df["machine_id"].nunique()

print("\n===== MANUFACTURING KPI REPORT =====")
print(f"Total production: {total_production:,.0f}")
print(f"Total defects: {total_defects:,.0f}")
print(f"Overall defect rate: {defect_rate:.2f}%")
print(f"Total downtime: {total_downtime:,.0f} minutes")
print(f"Operating hours: {total_operating_hours:,.2f}")
print(f"Machines monitored: {unique_machines}")

print("\n===== PRODUCTION BY MACHINE =====")

machine_report = (
    df.groupby("machine_id")
    .agg(
        total_production=("production_quantity", "sum"),
        total_defects=("defect_quantity", "sum"),
        downtime_minutes=("downtime_minutes", "sum"),
    )
    .reset_index()
)

machine_report["defect_rate_pct"] = (
    machine_report["total_defects"]
    / machine_report["total_production"].replace(0, pd.NA)
    * 100
).fillna(0).round(2)

machine_report = machine_report.sort_values(
    "total_production", ascending=False
)

print(machine_report.to_string(index=False))

print("\n===== MONTHLY PRODUCTION =====")

monthly_report = (
    df.groupby("production_month")
    ["production_quantity"]
    .sum()
    .reset_index()
    .sort_values("production_month")
)

print(monthly_report.to_string(index=False))

# Export reports for future dashboards
machine_report.to_csv(
    BASE_DIR / "data" / "machine_kpi_report.csv", index=False
)

monthly_report.to_csv(
    BASE_DIR / "data" / "monthly_production_report.csv", index=False
)

print("\nKPI reports exported successfully.")
