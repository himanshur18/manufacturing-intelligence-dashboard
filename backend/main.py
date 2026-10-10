
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Load .env from the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
print("Environment file found:", ENV_FILE.exists())
print("Database URL loaded:", bool(DATABASE_URL))

app = FastAPI(
    title="Manufacturing Intelligence API",
    description="API for manufacturing production analytics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@app.get("/")
def home():
    return {"message": "Manufacturing Intelligence API is running"}


@app.get("/api/health")
def health_check():
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail="DATABASE_URL is missing from the .env file",
        )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Check your database settings.",
        )


@app.get("/api/kpis")
def get_kpis():
    if engine is None:
        raise HTTPException(status_code=500, detail="Database is not configured")

    query = text("""
        SELECT
            COALESCE(SUM(production_quantity), 0) AS total_production,
            COALESCE(SUM(defect_quantity), 0) AS total_defects,
            COUNT(DISTINCT machine_id) AS machines_monitored
        FROM production
    """)

    try:
        with engine.connect() as connection:
            row = connection.execute(query).mappings().one()

        total_production = row["total_production"]
        total_defects = row["total_defects"]

        defect_rate = (
            total_defects / total_production * 100
            if total_production
            else 0
        )

        return {
            "total_production": total_production,
            "total_defects": total_defects,
            "defect_rate": round(defect_rate, 2),
            "machines_monitored": row["machines_monitored"],
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve production KPIs",
        )
    

@app.get("/api/machines")
def get_machines():
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail="Database is not configured",
        )

    query = text("""
        SELECT
            machine_id,
            COALESCE(SUM(production_quantity), 0) AS production,
            COALESCE(SUM(defect_quantity), 0) AS defects
        FROM production
        GROUP BY machine_id
        ORDER BY machine_id
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()

        machines = []

        for row in rows:
            production = row["production"]
            defects = row["defects"]

            defect_rate = (
                defects / production * 100
                if production
                else 0
            )

            machines.append({
                "machine_id": row["machine_id"],
                "production": production,
                "defects": defects,
                "defect_rate": round(defect_rate, 2),
            })

        return machines

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve machine performance",
        )
    

@app.get("/api/production-trend")
def get_production_trend():
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail="Database is not configured",
        )

    query = text("""
        SELECT
            DATE_TRUNC('month', production_date) AS month,
            COALESCE(SUM(production_quantity), 0) AS production
        FROM production
        WHERE production_date IS NOT NULL
        GROUP BY DATE_TRUNC('month', production_date)
        ORDER BY month
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()

        return [
            {
                "month": row["month"].strftime("%Y-%m"),
                "production": row["production"],
            }
            for row in rows
        ]

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve production trends",
        )


