# Executive Project Report: Customer Shopping Behavior Analysis
**Strategic Insights, Customer Segmentation & Retail Analytics**  
*Author: Data Analytics Portfolio Project | Built with Python, SQL, and Power BI / Localhost Dashboard*

---

## 1. Executive Summary

This report delivers an exhaustive analysis of retail customer behavior based on **3,900 transaction records** across 18 demographic and purchasing dimensions. The objective of this project is to model the customer journey, evaluate promotional efficiency, measure subscription adoption, and provide data-backed strategic recommendations to accelerate top-line revenue and retention.

### Key Headline Metrics:
- **Total Revenue:** $233,081.00 USD
- **Total Transactions / Customers:** 3,900
- **Average Order Value (AOV):** $59.76
- **Average Customer Review Rating:** 3.75 / 5.00
- **Active Subscription Adoption:** 27.0% (1,053 subscribers vs. 2,847 non-subscribers)
- **Discount Utilization Rate:** 43.1% (1,679 orders used discounts)

---

## 2. Exploratory Data Analysis & Data Quality

### Missing Data & Imputation
During the initial inspection of raw data, exactly **37 missing values** were identified in the `Review Rating` column. Rather than utilizing global mean imputation which introduces bias across distinct product categories, an imputation using the **median rating per product category** was implemented:
$$\text{Review Rating}_{i, c} = \text{median}(\text{Review Rating}_c) \quad \text{for null records}$$
This preserved category-specific rating dynamics without distorting variance.

### Feature Engineering
1. **Age Group Quartile Binning:**
   - **Young Adult:** 18 – 31 years old (1,028 customers, 26.4%)
   - **Adult:** 32 – 44 years old (942 customers, 24.2%)
   - **Middle-aged:** 45 – 57 years old (986 customers, 25.3%)
   - **Senior:** 58 – 70 years old (944 customers, 24.2%)
2. **Frequency of Purchases Standardized in Days:**
   - Weekly (7 days), Fortnightly / Bi-Weekly (14 days), Monthly (30 days), Quarterly / Every 3 Months (90 days), Annually (365 days).
3. **Customer Lifecycle Segmentation:**
   - **New (1 purchase):** 83 customers (2.1%)
   - **Returning (2 – 10 purchases):** 701 customers (18.0%)
   - **Loyal (>10 purchases):** 3,116 customers (79.9%)
4. **Redundancy Removal:**
   - Confirmed `discount_applied` and `promo_code_used` are 100% collinear; dropped `promo_code_used`.

---

## 3. SQL Business Intelligence Findings

### Q1: Revenue Contribution by Gender
| Gender | Revenue ($) | Total Orders | Avg Order Value ($) | Revenue Share (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Male** | $157,890.00 | 2,652 | $59.54 | 67.7% |
| **Female** | $75,191.00 | 1,248 | $60.25 | 32.3% |

*Insight:* While Male shoppers generate over two-thirds of total volume, Female shoppers display a slightly higher average order value ($60.25 vs. $59.54). Tailoring personalized campaigns for women can unlock substantial high-margin revenue.

---

### Q2: High-Value Discount Users ("Smart Shoppers")
- Identified customers who utilized promotional discounts yet spent above the store average ($59.76), reaching up to $100 per transaction.
*Insight:* These shoppers are not low-value bargain hunters; they are high-intent shoppers leveraging promotions to justify larger basket sizes.

---

### Q3: Top 5 Highest-Rated Products
1. **Gloves:** 3.86 ⭐ (140 reviews)
2. **Sandals:** 3.84 ⭐ (160 reviews)
3. **Boots:** 3.82 ⭐ (144 reviews)
4. **Hat:** 3.80 ⭐ (154 reviews)
5. **T-shirt:** 3.78 ⭐ (147 reviews)

*Insight:* Footwear and Accessories maintain the highest customer satisfaction scores. These items should be front-and-center in customer acquisition ads.

---

### Q4: Shipping Preferences & Spend Elasticity
| Shipping Type | Total Orders | Avg Spend ($) | Total Revenue ($) |
| :--- | :--- | :--- | :--- |
| **Express** | 646 | $60.48 | $39,072.00 |
| **Standard** | 654 | $58.46 | $38,233.00 |

*Insight:* Express shipping users spend **3.5% more per order** ($60.48 vs $58.46). Customers willing to pay for speed exhibit lower price resistance.

---

### Q5: Subscription Economics & Impact
| Subscription Status | Customer Count | Share (%) | Avg Spend ($) | Total Revenue ($) | Revenue Share (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Non-Subscribers (No)** | 2,847 | 73.0% | $59.87 | $170,436.00 | 73.1% |
| **Subscribers (Yes)** | 1,053 | 27.0% | $59.49 | $62,645.00 | 26.9% |

*Insight:* Average order value remains virtually identical between cohorts (~$59.50-$59.87). The primary value driver of subscriptions is not inflated basket size, but **purchase frequency and lifetime retention**.

---

### Q6: Most Heavily Discounted Products
1. **Hat:** 50.00% discount rate
2. **Sneakers:** 49.66% discount rate
3. **Coat:** 49.07% discount rate
4. **Sweater:** 48.17% discount rate
5. **Pants:** 47.37% discount rate

*Insight:* Half of all Hat and Sneaker purchases rely on discounts. To prevent margin erosion, discounts on these items should require minimum cart thresholds.

---

### Q7: Customer Lifecycle Distribution
- **Loyal (>10 purchases):** 3,116 customers (79.9%)
- **Returning (2–10 purchases):** 701 customers (18.0%)
- **New (1 purchase):** 83 customers (2.1%)

*Insight:* The customer base possesses strong repeat-buyer affinity. The strategic focus must be moving the 701 "Returning" customers into the "Loyal" cohort.

---

### Q8: Category Champions (Window Functions)
- **Accessories:** Jewelry (171 orders, $10,010), Sunglasses (161 orders, $9,649), Belt (161 orders, $9,635)
- **Clothing:** Pants (171 orders, $10,090), Blouse (171 orders, $10,410), Shirt (169 orders, $10,332)
- **Footwear:** Sandals (160 orders, $9,200), Shoes (150 orders, $8,985), Sneakers (145 orders, $8,688)
- **Outerwear:** Jacket (163 orders, $9,750), Coat (161 orders, $9,275)

---

### Q9: Subscription Conversion Opportunity
- Among customers with **more than 5 previous purchases**, **2,518 (72.4%)** are **NOT subscribed**, while only **958 (27.6%)** are subscribed.
*Insight:* This represents an immediate, high-probability pool of 2,518 established repeat shoppers who can be converted into paying subscribers with minimal friction.

---

### Q10: Revenue Contribution by Age Cohort
| Age Group | Total Customers | Total Revenue ($) | Share of Revenue (%) | Avg Order ($) |
| :--- | :--- | :--- | :--- | :--- |
| **Young Adult (18-31)** | 1,028 | $62,143.00 | 26.66% | $60.45 |
| **Middle-aged (45-57)** | 986 | $59,197.00 | 25.40% | $60.04 |
| **Adult (32-44)** | 942 | $55,978.00 | 24.02% | $59.42 |
| **Senior (58-70)** | 944 | $55,763.00 | 23.92% | $59.07 |

*Insight:* Young Adults represent both the highest volume and highest per-order spend.

---

## 4. Strategic Business Recommendations

1. **Launch a Targeted Subscription Onboarding Funnel:**
   - Run automated email and push campaigns targeting the 2,518 repeat non-subscribers offering a 30-day free trial or free express shipping on their next 3 orders.
   - *Estimated Revenue Uplift:* Converting just 20% (500 customers) yields significant recurring revenue and higher annual purchase frequency.

2. **Capitalize on Express Shipping Propensity:**
   - Introduce dynamic checkout recommendations: "Upgrade to Express Shipping for only $4.99 and get guaranteed delivery in 2 days."
   - Express users already spend 3.5% more per transaction.

3. **Protect Margins via Bundled Promotions:**
   - Rather than offering standalone 20% discounts on high-discount items like Hats and Sneakers, enforce threshold bundling: "Buy a pair of Sneakers and get 25% off any Accessory."

4. **Demographic Tailoring:**
   - **Young Adults (18-31):** Prioritize mobile-first checkouts, digital wallets (Venmo, PayPal), and social-first seasonal drops.
   - **Seniors & Middle-Aged (45-70):** Highlight durability, customer satisfaction reviews, and easy returns.
