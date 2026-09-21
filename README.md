# 👨🏻‍💻 Customer Behavior Data Analytics Portfolio Project
> **End-to-End Industry Standard Retail Data Analytics Workflow using Python, SQL, and Interactive Localhost Dashboard (Power BI Replica)**  
> *Inspired by and built following the tutorial by Amlan Mohanty.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20Postgres%20%7C%20MySQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit%20%7C%20Plotly-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PowerBI](https://img.shields.io/badge/Power%20BI-Report%20File%20Included-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)

---

## 📌 1. Project Overview & Business Problem Statement
Modern retail organizations generate millions of transactional data points. However, translating raw behavioral logs into actionable merchandising, retention, and subscription strategies is a critical challenge.

This project delivers an **end-to-end data analytics pipeline**:
1. **Extract & Inspect:** Ingest 3,900 customer shopping records across 18 demographic and purchase dimensions.
2. **Data Cleaning & Transformation (Python):** Handle missing values, snake-case column names, engineer age quartiles and frequency metrics, and remove data redundancy.
3. **Database Integration & Querying (SQL):** Load cleaned records into a relational database (`customer_behavior.db`) and execute **10 core business analysis queries** covering revenue by gender, discount sensitivity, review rankings, shipping behaviors, and repeat-buyer loyalty.
4. **Interactive Localhost Dashboard:** Experience the **Power BI dashboard directly in your browser on `localhost`** (complete with KPI cards, donut charts, bar/column charts, dynamic multi-slicers, and an interactive SQL analysis studio).
5. **Double-Click Execution:** Launch the entire application with a single double-click on `run_dashboard.bat`.

---

## 🚀 2. Quick Start: How to Run the Dashboard on Localhost

### Option A: One-Click Launch (Easiest)
Simply **double-click** the file:
```
run_dashboard.bat
```
This batch script will automatically:
1. Validate Python and required packages.
2. Verify the dataset and SQLite database.
3. Launch the dashboard server.
4. Open your default web browser to **`http://localhost:8501`**.

---

### Option B: Command-Line Launch
```bash
# 1. Run the ETL pipeline (generates cleaned CSV and SQLite database)
python data_pipeline.py

# 2. Start the interactive localhost dashboard
streamlit run dashboard.py
```
Then open your browser to **`http://localhost:8501`**.

---

## 📊 3. The 6 Project Phases (Step-by-Step)

```
  ┌────────────────────────┐
  │ 1. Raw Dataset         │ 3,900 rows, 18 features (demographics, basket, reviews)
  └───────────┬────────────┘
              │
  ┌───────────▼────────────┐
  │ 2. Python ETL & EDA    │ Missing value imputation (Category median)
  │    (data_pipeline.py)  │ Feature engineering (age_group, frequency_days, segment)
  └───────────┬────────────┘
              │
  ┌───────────▼────────────┐
  │ 3. Relational SQL DB   │ SQLite / PostgreSQL database `customer_behavior.db`
  │    (queries.sql)       │ 10 Core Business Queries with CTEs and Window Functions
  └───────────┬────────────┘
              │
  ┌───────────▼────────────┐
  │ 4. Localhost Dashboard │ Power BI Visual Replica + Interactive Slicers
  │    (dashboard.py)      │ Live SQL Studio + Customer Segmentation + Slides Viewer
  └────────────────────────┘
```

### Step 1: Business Problem Definition
- **Objective:** Evaluate retail customer transactions to optimize revenue, drive subscription enrollment, evaluate discount effectiveness, and increase repeat purchase frequency.

### Step 2: Dataset Exploration & Validation
- **Records:** 3,900 customer purchases.
- **Key Columns:** `Customer ID`, `Age`, `Gender`, `Item Purchased`, `Category`, `Purchase Amount (USD)`, `Location`, `Size`, `Color`, `Season`, `Review Rating`, `Subscription Status`, `Shipping Type`, `Discount Applied`, `Previous Purchases`, `Payment Method`, `Frequency of Purchases`.
- **Data Quality:** Found exactly **37 missing values** in `Review Rating`. All other 17 columns are complete.

### Step 3: Python Data Preprocessing (`data_pipeline.py`)
- **Imputation:** Missing `Review Rating` values imputed with the median of each product `Category`.
- **Standardization:** Column headers transformed into lowercase `snake_case`.
- **Quartile Binning:** Engineered `age_group` into 4 cohorts:
  - *Young Adult* (18 - 31)
  - *Adult* (32 - 44)
  - *Middle-aged* (45 - 57)
  - *Senior* (58 - 70)
- **Time Conversion:** Mapped `frequency_of_purchases` into `purchase_frequency_days` (e.g. Weekly = 7 days, Monthly = 30 days, Annually = 365 days).
- **Customer Segmentation:** Classify shoppers based on purchase history:
  - *New:* 1 purchase (2.1%)
  - *Returning:* 2 to 10 purchases (18.0%)
  - *Loyal:* > 10 purchases (79.9%)
- **Redundancy Elimination:** Identified that `promo_code_used` is 100% identical to `discount_applied`; removed the redundant column.

### Step 4: SQL Business Analysis (`customer_behavior_sql_queries.sql`)
1. **Revenue by Gender:** Male shoppers account for $157,890 (67.6%) across 2,652 orders, while Female shoppers generate $75,191 (32.4%) across 1,248 orders.
2. **High-Value Discount Users:** Identified "Smart Shoppers" using discounts while spending above average ($59.76 - up to $100).
3. **Top 5 Rated Products:** Gloves (3.86), Sandals (3.84), Boots (3.82), Hat (3.80), T-shirt (3.78).
4. **Shipping Impact:** Express Shipping customers spend an average of $60.48 vs $58.46 for Standard Shipping (+3.5% premium).
5. **Subscription Economics:** Non-subscribers drive $170,436 (73.1%) and subscribers contribute $62,645 (26.9%). Average basket sizes are virtually equal (~$59.50 vs ~$59.87).
6. **Highest Discounted Products:** Hats (50.0%), Sneakers (49.7%), and Coats (49.1%) show high promotional reliance.
7. **Customer Lifecycle:** 3,116 Loyal customers (79.9%), 701 Returning (18.0%), 83 New (2.1%).
8. **Top 3 Products per Category:** Window function `ROW_NUMBER() OVER (PARTITION BY category ORDER BY count DESC)` extracts top items per category.
9. **Repeat Buyers Subscription Potential:** 2,518 customers with >5 previous purchases are **not yet subscribed** (huge target market).
10. **Revenue by Age Group:** Young Adults lead overall spend at $62,143 (26.6%), followed by Middle-aged ($59,197), Adults ($55,978), and Seniors ($55,763).

### Step 5: Interactive Localhost Dashboard (`dashboard.py`)
Features 5 dedicated tabs:
- 📊 **Power BI Dashboard Replica:** Executive KPI cards, Donut chart (`% Customers by Subscription Status`), Column charts (`Revenue by Category`, `Sales by Category`), and Bar charts (`Revenue by Age Group`, `Sales by Age Group`), with live sidebar slicers.
- 💻 **SQL Business Studio:** Live interactive SQL query engine running against SQLite with preloaded buttons for all 10 project questions + custom query editor.
- 👥 **Customer Segmentation:** Visual breakdown of loyalty tiers, purchase frequencies, payment methods, and geographic sales.
- 🎯 **Executive Presentation & Insights:** Interactive slide-by-slide viewer of the 10 portfolio presentation slides with strategic recommendations.
- 📁 **Dataset Explorer:** Filterable data viewer with one-click CSV download.

### Step 6: Strategic Growth Recommendations
1. **Accelerate Subscription Conversion:** Convert the 2,518 repeat non-subscribers with exclusive member discounts and free express shipping perks.
2. **Upsell Express Shipping:** Implement dynamic checkout triggers for Express Shipping to capitalize on urgency-driven higher basket values.
3. **Smart Promotion Bundling:** Protect margins on heavily discounted items (hats, sneakers) by bundling them with high-margin accessories (jewelry, belts).
4. **Targeted Demographics:** Channel high-energy digital campaigns toward Young Adults while featuring quality and reliability for Middle-aged and Senior cohorts.

---

## 📂 4. Project Directory Structure

```
data2/
├── customer_shopping_behavior.csv         # Original raw retail dataset (3,900 rows)
├── cleaned_customer_shopping_behavior.csv # Cleaned & feature-engineered dataset
├── customer_behavior.db                   # SQLite database with 'customer' table
├── customer_behavior_sql_queries.sql      # 10 Business analysis SQL queries
├── Customer_Shopping_Behavior_Analysis.ipynb # End-to-end Jupyter Notebook
├── Customer-Shopping-Behavior-Analysis.pptx  # 10-slide executive presentation
├── customer_behavior_dashboard.pbix       # Power BI desktop report file
├── data_pipeline.py                       # Automated Python ETL pipeline script
├── dashboard.py                           # Streamlit + Plotly interactive dashboard
├── run_dashboard.bat                      # Double-click Windows launcher
├── launch_dashboard.py                    # Python launcher script
├── project_report.md                      # Comprehensive analytical report
└── .streamlit/
    └── config.toml                        # Enterprise UI theme configuration
```

---

## 🛠️ 5. Requirements & Installation

If running on a new machine, install dependencies using:
```bash
pip install pandas numpy streamlit plotly sqlalchemy
```
All dependencies are already pre-installed in your environment. Simply double-click `run_dashboard.bat` to begin!
