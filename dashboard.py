import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Customer Behavior Dashboard | Data Analytics Portfolio",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Power BI aesthetic styling
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #1E293B;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-sub {
        color: #10B981;
        font-size: 0.8rem;
        margin-top: 4px;
        font-weight: 500;
    }
    
    /* Header Container */
    .dashboard-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 24px 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.2);
    }
    .dashboard-header h1 {
        color: white !important;
        margin: 0 0 6px 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .dashboard-header p {
        color: #BFDBFE !important;
        margin: 0;
        font-size: 1rem;
    }
    
    /* Content block cards */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    /* SQL Code Box */
    .sql-box {
        background-color: #0F172A;
        color: #38BDF8;
        padding: 14px;
        border-radius: 8px;
        font-family: 'Consolas', monospace;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# Data Loading & Preparation
# ==============================================================================
@st.cache_data
def load_dataset():
    """Loads and cleans dataset, falling back to raw if needed."""
    cleaned_file = "cleaned_customer_shopping_behavior.csv"
    raw_file = "customer_shopping_behavior.csv"
    
    if os.path.exists(cleaned_file):
        df = pd.read_csv(cleaned_file)
    elif os.path.exists(raw_file):
        df = pd.read_csv(raw_file)
        # Apply transformation if uncleaned
        df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        if 'purchase_amount_(usd)' in df.columns:
            df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
        labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
        df['age_group'] = pd.qcut(df['age'], q=4, labels=labels).astype(str)
        freq_map = {'Weekly': 7, 'Fortnightly': 14, 'Bi-Weekly': 14, 'Monthly': 30, 'Every 3 Months': 90, 'Quarterly': 90, 'Annually': 365}
        df['purchase_frequency_days'] = df['frequency_of_purchases'].map(freq_map)
        df['customer_segment'] = df['previous_purchases'].apply(lambda p: 'New' if p == 1 else ('Returning' if p <= 10 else 'Loyal'))
        if 'promo_code_used' in df.columns:
            df = df.drop(columns=['promo_code_used'])
    else:
        st.error("Dataset not found! Please make sure customer_shopping_behavior.csv is in the project folder.")
        st.stop()
        
    return df


df = load_dataset()

# Ensure SQLite database exists
DB_PATH = "customer_behavior.db"
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("customer", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


# ==============================================================================
# Sidebar - Power BI Slicers & Filters
# ==============================================================================
st.sidebar.image("https://img.icons8.com/color/96/power-bi.png", width=60)
st.sidebar.title("🎛️ Dashboard Slicers")
st.sidebar.markdown("*Filter visualizations dynamically in real-time:*")

# Slicers matching Power BI report
gender_options = ["All"] + sorted(df["gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("👤 Gender", gender_options)

category_options = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("🏷️ Category", category_options)

subscription_options = ["All"] + sorted(df["subscription_status"].unique().tolist())
selected_subscription = st.sidebar.selectbox("⭐ Subscription Status", subscription_options)

shipping_options = ["All"] + sorted(df["shipping_type"].unique().tolist())
selected_shipping = st.sidebar.selectbox("🚚 Shipping Type", shipping_options)

age_options = ["All"] + sorted(df["age_group"].unique().tolist())
selected_age_group = st.sidebar.selectbox("🎂 Age Group", age_options)

season_options = ["All"] + sorted(df["season"].unique().tolist())
selected_season = st.sidebar.selectbox("🍂 Season", season_options)

# Filter Dataframe based on selections
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_subscription != "All":
    filtered_df = filtered_df[filtered_df["subscription_status"] == selected_subscription]
if selected_shipping != "All":
    filtered_df = filtered_df[filtered_df["shipping_type"] == selected_shipping]
if selected_age_group != "All":
    filtered_df = filtered_df[filtered_df["age_group"] == selected_age_group]
if selected_season != "All":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]

# Sidebar Reset & Summary
st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records ({len(filtered_df)/len(df)*100:.1f}%)")


# ==============================================================================
# Main Dashboard Header
# ==============================================================================
st.markdown("""
<div class="dashboard-header">
    <h1>🛍️ Customer Behavior Dashboard</h1>
    <p>End-to-End Retail Data Analytics Portfolio Project | Built with Python, SQL & Interactive Visualizations</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_overview, tab_sql, tab_segments, tab_presentation, tab_data = st.tabs([
    "📊 Power BI Dashboard",
    "💻 SQL Business Studio",
    "👥 Customer Segmentation",
    "🎯 Executive Insights & Slides",
    "📁 Dataset Explorer"
])


# ==============================================================================
# TAB 1: Power BI Dashboard Replica
# ==============================================================================
with tab_overview:
    # 1. Top KPI Cards (matching visual 0 from Power BI pbix)
    total_customers = len(filtered_df)
    total_revenue = filtered_df["purchase_amount"].sum()
    avg_purchase = filtered_df["purchase_amount"].mean() if total_customers > 0 else 0
    avg_rating = filtered_df["review_rating"].mean() if total_customers > 0 else 0
    discount_pct = (filtered_df["discount_applied"] == "Yes").mean() * 100 if total_customers > 0 else 0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Number of Customers</div>
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-sub">Total Transactions</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">${total_revenue:,.0f}</div>
            <div class="metric-sub">Gross Sales (USD)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Purchase Amount</div>
            <div class="metric-value">${avg_purchase:.2f}</div>
            <div class="metric-sub">Per Customer Order</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Review Rating</div>
            <div class="metric-value">{avg_rating:.2f} ⭐</div>
            <div class="metric-sub">Out of 5.0 Rating</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Discount Usage</div>
            <div class="metric-value">{discount_pct:.1f}%</div>
            <div class="metric-sub">Discount Applied Orders</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Main Row: Subscription Donut Chart + Category Revenue / Sales Charts
    row1_col1, row1_col2, row1_col3 = st.columns([1.1, 1.4, 1.4])
    
    # Donut Chart: % of Customers by Subscription Status
    with row1_col1:
        st.markdown("##### % of Customers by Subscription Status")
        if total_customers > 0:
            sub_counts = filtered_df["subscription_status"].value_counts().reset_index()
            sub_counts.columns = ["Subscription Status", "Count"]
            
            fig_sub = px.pie(
                sub_counts, 
                values="Count", 
                names="Subscription Status",
                hole=0.6,
                color="Subscription Status",
                color_discrete_map={"Yes": "#2563EB", "No": "#94A3B8"}
            )
            fig_sub.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_sub.update_layout(
                showlegend=True,
                margin=dict(t=10, b=10, l=10, r=10),
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_sub, use_container_width=True)
        else:
            st.warning("No data for current filters.")

    # Clustered Column Chart: Revenue by Category
    with row1_col2:
        st.markdown("##### Revenue by Category")
        if total_customers > 0:
            cat_rev = filtered_df.groupby("category")["purchase_amount"].sum().reset_index()
            cat_rev = cat_rev.sort_values(by="purchase_amount", ascending=False)
            
            fig_cat_rev = px.bar(
                cat_rev,
                x="category",
                y="purchase_amount",
                text="purchase_amount",
                labels={"category": "Category", "purchase_amount": "Total Revenue ($)"},
                color="category",
                color_discrete_sequence=["#1E3A8A", "#2563EB", "#3B82F6", "#60A5FA"]
            )
            fig_cat_rev.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='outside'
            )
            fig_cat_rev.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=300,
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9")
            )
            st.plotly_chart(fig_cat_rev, use_container_width=True)
        else:
            st.warning("No data for current filters.")

    # Clustered Column Chart: Sales (Orders) by Category
    with row1_col3:
        st.markdown("##### Sales by Category")
        if total_customers > 0:
            cat_sales = filtered_df.groupby("category")["customer_id"].count().reset_index()
            cat_sales = cat_sales.rename(columns={"customer_id": "total_sales"})
            cat_sales = cat_sales.sort_values(by="total_sales", ascending=False)
            
            fig_cat_sales = px.bar(
                cat_sales,
                x="category",
                y="total_sales",
                text="total_sales",
                labels={"category": "Category", "total_sales": "Total Orders"},
                color="category",
                color_discrete_sequence=["#0D9488", "#14B8A6", "#2DD4BF", "#5EEAD4"]
            )
            fig_cat_sales.update_traces(
                texttemplate='%{text:,}', 
                textposition='outside'
            )
            fig_cat_sales.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=300,
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9")
            )
            st.plotly_chart(fig_cat_sales, use_container_width=True)
        else:
            st.warning("No data for current filters.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Second Row: Age Group Visuals (matching visual 15 & 18 from Power BI pbix)
    row2_col1, row2_col2 = st.columns(2)
    
    # Clustered Bar Chart: Revenue by Age Group
    with row2_col1:
        st.markdown("##### Revenue by Age Group")
        if total_customers > 0:
            age_rev = filtered_df.groupby("age_group")["purchase_amount"].sum().reset_index()
            age_rev = age_rev.sort_values(by="purchase_amount", ascending=True)
            
            fig_age_rev = px.bar(
                age_rev,
                x="purchase_amount",
                y="age_group",
                orientation='h',
                text="purchase_amount",
                labels={"age_group": "Age Group", "purchase_amount": "Total Revenue ($)"},
                color_discrete_sequence=["#4F46E5"]
            )
            fig_age_rev.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='outside'
            )
            fig_age_rev.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=280,
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9")
            )
            st.plotly_chart(fig_age_rev, use_container_width=True)
        else:
            st.warning("No data for current filters.")

    # Clustered Bar Chart: Sales by Age Group
    with row2_col2:
        st.markdown("##### Sales by Age Group")
        if total_customers > 0:
            age_sales = filtered_df.groupby("age_group")["customer_id"].count().reset_index()
            age_sales = age_sales.rename(columns={"customer_id": "total_sales"})
            age_sales = age_sales.sort_values(by="total_sales", ascending=True)
            
            fig_age_sales = px.bar(
                age_sales,
                x="total_sales",
                y="age_group",
                orientation='h',
                text="total_sales",
                labels={"age_group": "Age Group", "total_sales": "Total Orders"},
                color_discrete_sequence=["#D97706"]
            )
            fig_age_sales.update_traces(
                texttemplate='%{text:,}', 
                textposition='outside'
            )
            fig_age_sales.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=280,
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9")
            )
            st.plotly_chart(fig_age_sales, use_container_width=True)
        else:
            st.warning("No data for current filters.")

    st.markdown("---")
    # Quick Summary Callout
    st.markdown("""
    💡 **Power BI Dashboard Replication Insights:**
    - **Clothing** constitutes the highest revenue and transaction volume ($104K+ across 1,737 sales), followed by Accessories.
    - **Young Adults** represent the largest spending demographic segment ($62.1K), with high purchasing velocity.
    - **Non-subscribers (73%)** represent an untapped subscription upsell opportunity to expand high-frequency loyal cohorts.
    """)


# ==============================================================================
# TAB 2: SQL Business Studio (Live execution of 10 queries + Custom SQL)
# ==============================================================================
with tab_sql:
    st.markdown("### 💻 SQL Business Analysis Studio")
    st.markdown("Run and analyze the **10 core SQL business questions** from the tutorial directly against the SQLite database.")

    queries_dict = {
        "Q1: Revenue by Gender": {
            "sql": """SELECT 
    gender, 
    SUM(purchase_amount) AS revenue,
    COUNT(customer_id) AS total_orders,
    ROUND(AVG(purchase_amount), 2) AS avg_order_value
FROM customer
GROUP BY gender
ORDER BY revenue DESC;""",
            "chart_type": "bar",
            "x": "gender",
            "y": "revenue",
            "insight": "Male customers generate $157,890 across 2,652 transactions, while Female customers account for $75,191 across 1,248 transactions. Male shoppers form ~68% of total retail orders."
        },
        "Q2: High Spenders with Discount": {
            "sql": """SELECT 
    customer_id, 
    gender,
    category,
    item_purchased,
    purchase_amount 
FROM customer 
WHERE discount_applied = 'Yes' 
  AND purchase_amount >= (SELECT AVG(purchase_amount) FROM customer)
ORDER BY purchase_amount DESC
LIMIT 15;""",
            "chart_type": "table",
            "insight": "Customers frequently use discounts while maintaining basket values above the $59.76 store average (up to $100). These represent price-aware 'Smart Shoppers' receptive to premium bundles."
        },
        "Q3: Top 5 Products by Rating": {
            "sql": """SELECT 
    item_purchased, 
    ROUND(AVG(review_rating), 2) AS avg_rating,
    COUNT(customer_id) AS review_count
FROM customer
GROUP BY item_purchased
ORDER BY avg_rating DESC
LIMIT 5;""",
            "chart_type": "bar",
            "x": "item_purchased",
            "y": "avg_rating",
            "insight": "Gloves (3.86), Sandals (3.84), Boots (3.82), Hat (3.80), and T-shirt (3.78) maintain the highest satisfaction scores across the retail catalog."
        },
        "Q4: Standard vs Express Shipping Spend": {
            "sql": """SELECT 
    shipping_type, 
    COUNT(customer_id) AS total_orders,
    ROUND(AVG(purchase_amount), 2) AS avg_spend,
    ROUND(SUM(purchase_amount), 2) AS total_revenue
FROM customer
WHERE shipping_type IN ('Standard', 'Express')
GROUP BY shipping_type;""",
            "chart_type": "bar",
            "x": "shipping_type",
            "y": "avg_spend",
            "insight": "Express shipping customers spend an average of $60.48 vs $58.46 for Standard shipping—a premium of ~3.5% higher basket size due to urgency and buyer confidence."
        },
        "Q5: Subscribers vs Non-Subscribers Spend": {
            "sql": """SELECT 
    subscription_status,
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(purchase_amount), 2) AS avg_spend,
    ROUND(SUM(purchase_amount), 2) AS total_revenue
FROM customer
GROUP BY subscription_status
ORDER BY total_revenue DESC;""",
            "chart_type": "pie",
            "names": "subscription_status",
            "values": "total_revenue",
            "insight": "Non-subscribers contribute $170,436 (73.1% of revenue) while subscribers contribute $62,645. Average basket size remains comparable (~$59.50-$59.87), meaning subscription drives loyalty frequency rather than order inflate."
        },
        "Q6: Top 5 Discounted Products": {
            "sql": """SELECT 
    item_purchased, 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) AS discount_orders,
    ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS discount_rate_pct
FROM customer
GROUP BY item_purchased
ORDER BY discount_rate_pct DESC
LIMIT 5;""",
            "chart_type": "bar",
            "x": "item_purchased",
            "y": "discount_rate_pct",
            "insight": "Hats (50.0%), Sneakers (49.66%), Coats (49.07%), Sweaters (48.17%), and Pants (47.37%) are heavily discounted, indicating price elasticity and promotional reliance."
        },
        "Q7: Customer Segmentation by Purchase History": {
            "sql": """WITH customer_type AS (
    SELECT 
        customer_id, 
        previous_purchases,
        CASE 
            WHEN previous_purchases = 1 THEN 'New'
            WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
            ELSE 'Loyal'
        END AS customer_segment
    FROM customer
)
SELECT 
    customer_segment, 
    COUNT(*) AS number_of_customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer), 2) AS pct_share
FROM customer_type 
GROUP BY customer_segment
ORDER BY number_of_customers DESC;""",
            "chart_type": "bar",
            "x": "customer_segment",
            "y": "number_of_customers",
            "insight": "Loyal customers (>10 purchases) form 79.9% (3,116 customers) of repeat shoppers, Returning (2-10 purchases) form 18.0% (701), and New (1 purchase) form 2.1% (83)."
        },
        "Q8: Top 3 Most Purchased Products per Category": {
            "sql": """WITH item_counts AS (
    SELECT 
        category,
        item_purchased,
        COUNT(customer_id) AS total_orders,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY COUNT(customer_id) DESC) AS item_rank
    FROM customer
    GROUP BY category, item_purchased
)
SELECT 
    item_rank, 
    category, 
    item_purchased, 
    total_orders
FROM item_counts
WHERE item_rank <= 3
ORDER BY category, item_rank;""",
            "chart_type": "table",
            "insight": "Leading items by category: Accessories (Jewelry 171, Sunglasses 161, Belt 161); Clothing (Pants 171, Blouse 171, Shirt 169); Footwear (Sandals 160, Shoes 150, Sneakers 145); Outerwear (Jacket 163, Coat 161)."
        },
        "Q9: Repeat Buyers Subscription Likelihood": {
            "sql": """SELECT 
    subscription_status,
    COUNT(customer_id) AS repeat_buyers,
    ROUND(100.0 * COUNT(customer_id) / (SELECT COUNT(*) FROM customer WHERE previous_purchases > 5), 2) AS pct_share
FROM customer
WHERE previous_purchases > 5
GROUP BY subscription_status;""",
            "chart_type": "pie",
            "names": "subscription_status",
            "values": "repeat_buyers",
            "insight": "Of buyers with >5 previous purchases, 2,518 (72.4%) are NOT subscribed, while 958 (27.6%) ARE subscribed. This highlights an immense subscription expansion opportunity among proven repeat shoppers."
        },
        "Q10: Revenue Contribution by Age Group": {
            "sql": """SELECT 
    age_group, 
    COUNT(customer_id) AS customer_count,
    SUM(purchase_amount) AS total_revenue,
    ROUND(100.0 * SUM(purchase_amount) / (SELECT SUM(purchase_amount) FROM customer), 2) AS revenue_share_pct
FROM customer
GROUP BY age_group
ORDER BY total_revenue DESC;""",
            "chart_type": "bar",
            "x": "age_group",
            "y": "total_revenue",
            "insight": "Young Adults generate the highest revenue ($62,143 / 26.6%), followed by Middle-aged ($59,197 / 25.4%), Adults ($55,978 / 24.0%), and Seniors ($55,763 / 23.9%)."
        }
    }

    selected_query_key = st.selectbox("📌 Select Business Question:", list(queries_dict.keys()))
    q_data = queries_dict[selected_query_key]

    st.markdown("**SQL Query:**")
    st.code(q_data["sql"], language="sql")

    # Live Execute against SQLite
    conn = sqlite3.connect(DB_PATH)
    res_df = pd.read_sql(q_data["sql"], conn)
    conn.close()

    res_col1, res_col2 = st.columns([1.2, 1])
    with res_col1:
        st.markdown("**Query Output Table:**")
        st.dataframe(res_df, use_container_width=True)

    with res_col2:
        st.markdown("**Visualization:**")
        if q_data.get("chart_type") == "bar":
            fig_q = px.bar(
                res_df, 
                x=q_data["x"], 
                y=q_data["y"], 
                text=q_data["y"],
                color=q_data["x"],
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_q.update_traces(textposition='outside')
            fig_q.update_layout(showlegend=False, height=280, margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig_q, use_container_width=True)
        elif q_data.get("chart_type") == "pie":
            fig_q = px.pie(
                res_df, 
                names=q_data["names"], 
                values=q_data["values"], 
                hole=0.45,
                color_discrete_sequence=["#3B82F6", "#94A3B8"]
            )
            fig_q.update_layout(height=280, margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig_q, use_container_width=True)
        else:
            st.info("📊 Tabular visualization displayed on the left.")

    st.success(f"**Business Takeaway:** {q_data['insight']}")

    st.markdown("---")
    st.markdown("#### ⚡ Custom SQL Console")
    custom_sql = st.text_area(
        "Execute your own SQL query on the `customer` table:",
        value="SELECT category, payment_method, COUNT(*) AS count, ROUND(AVG(purchase_amount), 2) AS avg_spend FROM customer GROUP BY category, payment_method ORDER BY count DESC LIMIT 10;"
    )
    if st.button("🚀 Run Custom SQL", type="primary"):
        try:
            conn = sqlite3.connect(DB_PATH)
            custom_res = pd.read_sql(custom_sql, conn)
            conn.close()
            st.dataframe(custom_res, use_container_width=True)
            st.caption(f"Query returned {len(custom_res)} row(s).")
        except Exception as e:
            st.error(f"SQL Error: {str(e)}")


# ==============================================================================
# TAB 3: Customer Segmentation & RFM Analysis
# ==============================================================================
with tab_segments:
    st.markdown("### 👥 Customer Lifecycle & Demographic Segmentation")

    seg_col1, seg_col2, seg_col3 = st.columns(3)
    with seg_col1:
        st.markdown("##### Customer Segment Distribution")
        seg_df = df["customer_segment"].value_counts().reset_index()
        seg_df.columns = ["Segment", "Count"]
        fig_seg = px.pie(
            seg_df, 
            values="Count", 
            names="Segment", 
            hole=0.5,
            color="Segment",
            color_discrete_map={"Loyal": "#10B981", "Returning": "#3B82F6", "New": "#F59E0B"}
        )
        st.plotly_chart(fig_seg, use_container_width=True)
        
    with seg_col2:
        st.markdown("##### Purchase Frequency Distribution")
        freq_df = df["frequency_of_purchases"].value_counts().reset_index()
        freq_df.columns = ["Frequency", "Count"]
        fig_freq = px.bar(
            freq_df,
            x="Frequency",
            y="Count",
            text="Count",
            color="Frequency",
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        fig_freq.update_traces(textposition="outside")
        fig_freq.update_layout(showlegend=False)
        st.plotly_chart(fig_freq, use_container_width=True)

    with seg_col3:
        st.markdown("##### Top Payment Methods")
        pay_df = df["payment_method"].value_counts().reset_index()
        pay_df.columns = ["Payment Method", "Count"]
        fig_pay = px.bar(
            pay_df,
            x="Count",
            y="Payment Method",
            orientation="h",
            text="Count",
            color="Payment Method",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_pay.update_traces(textposition="outside")
        fig_pay.update_layout(showlegend=False)
        st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 📍 Location & Basket Value Deep Dive")
    loc_col1, loc_col2 = st.columns(2)
    
    with loc_col1:
        top_states = df.groupby("location")["purchase_amount"].agg(["sum", "count", "mean"]).reset_index()
        top_states = top_states.sort_values(by="sum", ascending=False).head(10)
        fig_state = px.bar(
            top_states,
            x="location",
            y="sum",
            text="sum",
            title="Top 10 States by Total Revenue ($)",
            labels={"location": "State", "sum": "Revenue ($)"},
            color_discrete_sequence=["#2563EB"]
        )
        fig_state.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_state, use_container_width=True)

    with loc_col2:
        fig_box = px.box(
            df,
            x="category",
            y="purchase_amount",
            color="category",
            title="Purchase Amount Distribution by Category",
            labels={"category": "Category", "purchase_amount": "Amount ($)"}
        )
        st.plotly_chart(fig_box, use_container_width=True)


# ==============================================================================
# TAB 4: Executive Insights & Presentation Slides
# ==============================================================================
with tab_presentation:
    st.markdown("### 🎯 Executive Presentation & Strategic Recommendations")
    st.markdown("*Summary of findings from the 10-slide portfolio presentation deck (`Customer-Shopping-Behavior-Analysis.pptx`):*")

    slides_info = [
        {"slide": "Slide 1", "title": "Project Introduction", "content": "Comprehensive retail analysis covering 3,900 purchase transactions across 18 demographic & behavioral dimensions."},
        {"slide": "Slide 2", "title": "Dataset & Quality Overview", "content": "3,900 Total Purchases, 18 Data Columns, and 37 missing values exclusively in Review Rating (imputed via category median)."},
        {"slide": "Slide 3", "title": "Data Pipeline Workflow", "content": "Five rigorous phases: Ingestion -> EDA & Validation -> Missing Value Imputation -> Feature Engineering -> SQL & BI Integration."},
        {"slide": "Slide 4", "title": "Revenue by Gender Analysis", "content": "Male customers generate $157.9K revenue vs $75.2K for Female shoppers, offering clear targets for tailored catalog ads."},
        {"slide": "Slide 5", "title": "High-Value Discount Users", "content": "Identified 'Smart Shoppers' who utilize promotional discounts but spend substantially above the $59.76 average order value."},
        {"slide": "Slide 6", "title": "Top-Rated Products", "content": "Gloves (3.86), Sandals (3.84), Boots (3.82), and Blouse/Dress hold highest customer satisfaction—prime candidates for hero ads."},
        {"slide": "Slide 7", "title": "Shipping Preferences Impact", "content": "Express Shipping orders average $60.48 vs $58.46 for Standard, proving expedited shoppers yield 3.5% higher basket sizes."},
        {"slide": "Slide 8", "title": "Subscription Economics", "content": "Subscribers account for 27% of customers ($62.6K revenue). Repeat buyers with >5 purchases are 72.4% unsubscribed—massive expansion pool."},
        {"slide": "Slide 9", "title": "Customer Segmentation Model", "content": "79.9% Loyal (>10 purchases), 18% Returning (2-10 purchases), 2.1% New (1 purchase). Retention and conversion funnel is paramount."},
        {"slide": "Slide 10", "title": "Strategic Recommendations", "content": "1. Boost Subscriptions with exclusive perks\n2. Introduce Tiered Loyalty Rewards\n3. Upsell Express Delivery at checkout\n4. Hero-position high-rated items in digital ads."}
    ]

    selected_slide = st.selectbox("📑 Select Presentation Slide:", [f"{s['slide']}: {s['title']}" for s in slides_info])
    chosen = next(s for s in slides_info if f"{s['slide']}: {s['title']}" == selected_slide)

    st.info(f"### {chosen['slide']}: {chosen['title']}\n\n{chosen['content']}")

    st.markdown("#### 🚀 Four Strategic Growth Pillars")
    rec1, rec2, rec3, rec4 = st.columns(4)
    with rec1:
        st.markdown("""
        **1. Subscription Conversion**
        - Target 2,518 repeat non-subscribers
        - Offer free shipping trials
        - Projected +15% revenue lift
        """)
    with rec2:
        st.markdown("""
        **2. Smart Shopper Bundles**
        - Pair discounted items with high-margin accessories
        - Prevent margin erosion
        - Maintain $65+ basket size
        """)
    with rec3:
        st.markdown("""
        **3. Express Shipping Upsell**
        - Dynamic checkout prompt for Express
        - Express users spend 3.5% more
        - Higher urgency conversion
        """)
    with rec4:
        st.markdown("""
        **4. Age-Tailored Marketing**
        - Young Adult ($62.1K): Mobile & trendy
        - Middle-aged ($59.2K): Quality apparel
        - Seniors ($55.8K): Reliability & service
        """)


# ==============================================================================
# TAB 5: Dataset Explorer
# ==============================================================================
with tab_data:
    st.markdown("### 📁 Dataset Explorer & Export")
    st.markdown(f"Displaying **{len(filtered_df):,}** records based on active slicers.")

    st.dataframe(filtered_df, use_container_width=True, height=400)

    csv_export = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_export,
        file_name="filtered_customer_shopping_behavior.csv",
        mime="text/csv",
        type="primary"
    )
