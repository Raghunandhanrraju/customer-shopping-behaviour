"""
==============================================================================
End-to-End Customer Shopping Behavior Data Pipeline
Inspired by: "COMPLETE Data Analytics Portfolio Project | Python + SQL + Power BI"
Author: Amlan Mohanty Portfolio Project (Implementation)
==============================================================================
This script performs:
1. Data Extraction & Loading (Raw CSV)
2. Comprehensive Exploratory Data Analysis (EDA)
3. Data Cleaning & Missing Value Imputation (Category Median)
4. Column Standardization (snake_case)
5. Feature Engineering (Age Groups, Frequency in Days, Customer Segmentation)
6. Data Quality Checks & Redundancy Removal
7. Exporting to Cleaned CSV and SQLite Database
==============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np


def load_raw_data(filepath="customer_shopping_behavior.csv"):
    """Loads raw retail shopping behavior data."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Source file not found at {filepath}")
    df = pd.read_csv(filepath)
    print(f"[*] Successfully loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df


def perform_eda(df):
    """Prints exploratory data analysis summary statistics."""
    print("\n" + "="*50)
    print("EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*50)
    print("\nDataset Info:")
    df.info()
    
    print("\nNull Values per Column:")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0] if (null_counts > 0).any() else "No missing values!")
    
    print("\nSummary Statistics (Numeric):")
    print(df.describe())
    
    print("\nSummary Statistics (Categorical):")
    print(df.describe(include=['O']))


def clean_and_transform(df):
    """Cleans raw data and applies business feature engineering."""
    df_clean = df.copy()
    
    # 1. Impute missing values in Review Rating using Category median
    if 'Review Rating' in df_clean.columns and df_clean['Review Rating'].isnull().sum() > 0:
        missing_count = df_clean['Review Rating'].isnull().sum()
        df_clean['Review Rating'] = df_clean.groupby('Category')['Review Rating'].transform(
            lambda x: x.fillna(x.median())
        )
        print(f"[*] Imputed {missing_count} missing values in 'Review Rating' using Category median.")
    
    # 2. Standardize column names to snake_case
    df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_')
    if 'purchase_amount_(usd)' in df_clean.columns:
        df_clean = df_clean.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
    
    # 3. Feature Engineering: Age Group Binning (Quartiles)
    labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
    df_clean['age_group'] = pd.qcut(df_clean['age'], q=4, labels=labels).astype(str)
    
    # 4. Feature Engineering: Purchase Frequency in Days
    frequency_mapping = {
        'Weekly': 7,
        'Fortnightly': 14,
        'Bi-Weekly': 14,
        'Monthly': 30,
        'Every 3 Months': 90,
        'Quarterly': 90,
        'Annually': 365
    }
    df_clean['purchase_frequency_days'] = df_clean['frequency_of_purchases'].map(frequency_mapping)
    
    # 5. Feature Engineering: Customer Segmentation based on previous purchases
    def segment_customer(p):
        if p == 1:
            return 'New'
        elif 2 <= p <= 10:
            return 'Returning'
        else:
            return 'Loyal'
            
    df_clean['customer_segment'] = df_clean['previous_purchases'].apply(segment_customer)
    
    # 6. Check redundancy between discount_applied and promo_code_used
    if 'promo_code_used' in df_clean.columns and 'discount_applied' in df_clean.columns:
        is_identical = (df_clean['discount_applied'] == df_clean['promo_code_used']).all()
        if is_identical:
            print("[*] Verified: 'promo_code_used' is 100% identical to 'discount_applied'. Dropping redundant column.")
            df_clean = df_clean.drop(columns=['promo_code_used'])
            
    print(f"[*] Cleaning completed. Clean dataset shape: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns.")
    return df_clean


def save_data(df_clean, csv_path="cleaned_customer_shopping_behavior.csv", db_path="customer_behavior.db"):
    """Exports cleaned dataframe to CSV and SQLite database."""
    # Save CSV
    df_clean.to_csv(csv_path, index=False)
    print(f"[*] Cleaned data saved to '{csv_path}'.")
    
    # Save to SQLite Database
    conn = sqlite3.connect(db_path)
    df_clean.to_sql('customer', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print(f"[*] Cleaned data loaded into table 'customer' in SQLite database '{db_path}'.")


def run_sample_sql_queries(db_path="customer_behavior.db"):
    """Executes the 10 core business queries to verify database integrity."""
    conn = sqlite3.connect(db_path)
    print("\n" + "="*50)
    print("VERIFYING 10 SQL BUSINESS QUERIES")
    print("="*50)
    
    queries = [
        ("Q1: Revenue by Gender",
         "SELECT gender, SUM(purchase_amount) AS total_revenue FROM customer GROUP BY gender ORDER BY total_revenue DESC;"),
        ("Q5: Spend by Subscription Status",
         "SELECT subscription_status, COUNT(customer_id) AS customers, ROUND(AVG(purchase_amount), 2) AS avg_spend, ROUND(SUM(purchase_amount), 2) AS total_revenue FROM customer GROUP BY subscription_status;"),
        ("Q7: Customer Segmentation Breakdown",
         "SELECT customer_segment, COUNT(*) AS count, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer), 2) AS pct FROM customer GROUP BY customer_segment ORDER BY count DESC;"),
        ("Q10: Revenue by Age Group",
         "SELECT age_group, SUM(purchase_amount) AS revenue FROM customer GROUP BY age_group ORDER BY revenue DESC;")
    ]
    
    for title, q in queries:
        print(f"\n{title}:")
        df_res = pd.read_sql(q, conn)
        print(df_res.to_string(index=False))
        
    conn.close()


def main():
    print("="*60)
    print("STARTING CUSTOMER SHOPPING BEHAVIOR ETL PIPELINE")
    print("="*60)
    
    raw_df = load_raw_data()
    perform_eda(raw_df)
    clean_df = clean_and_transform(raw_df)
    save_data(clean_df)
    run_sample_sql_queries()
    
    print("\n" + "="*60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)


if __name__ == "__main__":
    main()
