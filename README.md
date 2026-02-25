# End-to-End Analytics Engineering Pipeline: UK Energy Grid Performance

## 🎯 Business Context & Problem Statement
The UK energy sector is transitioning to a decentralized, data-driven model. Operational efficiency depends on the ability to transform high-velocity smart meter data into actionable insights. 

**The Challenge:** Raw telemetry data is often "noisy," containing duplicates, missing values, and inconsistent schemas. This project builds a resilient Analytics Engineering pipeline to ensure a "Single Source of Truth" for grid performance metrics.

## 🏗️ Technical Architecture (The Modern Data Stack)
This project implements a modular architecture designed for scalability and data governance:
- **Cloud Warehouse:** Snowflake (Enterprise Layer)
- **Transformation:** dbt (Data Build Tool) - Staging, Intermediate, and Mart layers.
- **Orchestration & Ingestion:** Python & GitHub Actions.
- **Data Modeling:** Star Schema (Kimball Methodology).
- **Visualization:** Power BI (Semantic Layer modeling).

## 📂 Repository Structure
- `scripts/`: Python-based ingestion and automated data retrieval logic.
- `dbt_project/`: SQL transformation logic, data quality tests, and documentation.
- `sql_queries/`: Ad-hoc analysis and performance benchmarking.
- `docs/`: Technical design documents, ERDs, and data dictionaries.

## 🚀 Key Engineering Principles Applied
- **Version Control:** Strictly following Git-flow for all transformations.
- **Data Quality:** Automated testing for uniqueness, nulls, and relationship integrity.
- **SCD Type 2:** Tracking historical changes in household demographics for "As-Of-Reporting."
