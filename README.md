# Manufacturing Intelligence Dashboard

An end-to-end data analytics project that uses Python, PostgreSQL, SQL, and Power BI to analyze manufacturing production, quality, and machine performance.

## Project Overview

This project transforms manufacturing production data into actionable insights. It helps monitor production output, identify quality issues, analyze machine downtime, and compare machine-level performance.

## Business Objectives

- Monitor production output and defects.
- Compare defect rates across machines.
- Identify machines with high downtime.
- Analyze production trends over time.
- Support data-driven operational decisions.

## Tools and Technologies

- **Power BI:** Interactive dashboard and visualizations
- **PostgreSQL:** Relational data storage
- **SQL:** KPI calculations, rankings, and trend analysis
- **Python:** Data cleaning, exploratory data analysis, and KPI analysis
- **Pandas:** Data manipulation and processing
- **Git and GitHub:** Version control and project sharing

## Key Performance Indicators

- Total Production
- Total Defects
- Defect Rate (%)
- Total Downtime (Hours)
- Machines Monitored

## Dashboard Features

- Production trends over time
- Production output by machine
- Defect rate comparison by machine
- Downtime analysis by machine
- Machine filtering through an interactive slicer

## SQL Analysis

The project includes SQL queries for:

1. Machine performance analysis
2. High-defect machine identification
3. Machine performance ranking
4. Monthly production trend analysis

## Project Workflow

1. Prepare manufacturing production data using Python.
2. Clean and explore the dataset.
3. Load production records into PostgreSQL.
4. Execute SQL queries to analyze manufacturing KPIs.
5. Connect Power BI to PostgreSQL.
6. Build an interactive dashboard to visualize performance.

## Dataset

The project uses a **synthetic manufacturing dataset** created for analytical and educational purposes. It does not represent actual company production records.

## Business Value

The dashboard helps users investigate production patterns, identify machines that may need maintenance, and highlight potential quality issues. These insights can support further investigation and operational decision-making.

## Project Structure

- `data/` — Manufacturing datasets and reports
- `python/` — Data cleaning, EDA, KPI analysis, and database loading scripts
- `sql/` — SQL analysis queries
- `dashboard/` — Power BI dashboard file
- `requirements.txt` — Python dependencies

## How to Run

1. Clone this repository.
2. Install the Python dependencies listed in `requirements.txt`.
3. Configure PostgreSQL and create the required database.
4. Run the Python scripts as needed to prepare and load the data.
5. Open the `.pbix` file in Power BI Desktop.

**Note:** Update database connection settings for your own PostgreSQL installation before running the loading script. The dataset is synthetic, and the dashboard is intended as a portfolio project.

## Author

**Himanshu