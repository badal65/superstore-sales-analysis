# Superstore Sales & Profitability Analysis

A portfolio data-analysis project that turns retail transactions into sales, profitability, regional, and product-level recommendations.

## Business questions
- Which categories, regions, and sub-categories drive sales and profit?
- Where are discounts associated with losses?
- How does sales performance evolve over time?

## Tools
- **Python:** Pandas for cleaning/analysis; Matplotlib and Seaborn for visualizations
- **SQL:** reusable business queries in `sql/analysis_queries.sql`
- **Dataset:** Sample Superstore transaction data, sourced from [leonism/sample-superstore](https://github.com/leonism/sample-superstore). This is a fictional dataset for learning/portfolio use.

## Dataset and preparation
The analysis includes **10,800 transaction rows** and **5,015 unique orders**. Dates were converted to datetime, column names standardized to snake_case, and derived `profit_margin` and `shipping_days` fields added. The cleaned CSV is stored in `data/superstore_cleaned.csv`.

## Executive findings
| KPI | Result |
|---|---:|
| Total sales | $2,297,201 |
| Total profit | $286,397 |
| Profit margin | 12.5% |
| Average order value | $458 |

- **West** produces the largest profit, while the **Central** region has the weakest profit performance.
- The main loss-making sub-categories are **Tables, Bookcases, Supplies**.
- The strongest category by sales is **Technology**.

## Recommendations
1. Review discount guardrails for consistently loss-making sub-categories before expanding promotions.
2. Diagnose the weakest-profit region at product and discount level, then pilot targeted pricing or assortment changes.
3. Protect high-margin category/region combinations and use them to offset lower-margin growth initiatives.
4. Track sales and profit together—revenue alone can conceal unprofitable volume.

## Repository structure
```
superstore-sales-analysis/
+-- data/                 # raw and cleaned CSV data
+-- notebooks/            # reproducible analysis notebook
+-- sql/                  # SQL business queries
+-- visuals/              # exported charts
+-- analysis_summary.json # key output tables/KPIs
+-- README.md
```

## Run locally
```bash
pip install pandas matplotlib seaborn jupyter
jupyter notebook notebooks/superstore_analysis.ipynb
```
