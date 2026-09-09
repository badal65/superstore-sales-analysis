# Superstore Sales & Profitability Analysis

A reproducible retail analytics project that turns transaction data into sales, profitability, regional, and product-level recommendations.

## Business questions

- Which categories, regions, and sub-categories drive sales and profit?
- Where are discounts associated with losses?
- How does sales performance evolve over time?

## Tools

- Python: Pandas for cleaning and analysis; Matplotlib and Seaborn for visualizations
- SQL: reusable business queries in `sql/analysis_queries.sql`
- Dataset: fictional Sample Superstore transactions, sourced from https://github.com/leonism/sample-superstore

## Executive findings

| KPI | Result |
|---|---:|
| Total sales | $2,297,201 |
| Total profit | $286,397 |
| Profit margin | 12.5% |
| Average order value | $458 |

- Technology is the strongest category by sales.
- Tables, Bookcases, and Supplies are loss-making sub-categories.
- West produces the largest profit; Central has the weakest profit performance.

## Run the analysis

1. Clone this repository and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Download the source CSV from the dataset link above and save it as `data/superstore.csv`.

3. Run the pipeline:

   ```bash
   python src/analyze.py --input data/superstore.csv --output outputs
   ```

The pipeline cleans the data, writes `outputs/superstore_cleaned.csv` and `outputs/analysis_summary.json`, and generates four PNG charts in `outputs/visuals/`.

## Repository structure

```text
src/analyze.py                         reproducible Python pipeline
requirements.txt                       Python dependencies
data/                                  input data location
sql/analysis_queries.sql               SQL analysis queries
notebooks/superstore_analysis.ipynb    notebook walkthrough
visuals/                               presentation charts
Superstore_Sales_Analysis_Presentation.pptx
```

The downloadable source archive contains the complete original project package, including the cleaned dataset and exported analysis outputs.
