# Superstore Sales & Profitability Analysis

A reproducible retail analytics project that turns transaction data into sales, profitability, regional, and product-level recommendations.

## Business questions

- Which categories, regions, and sub-categories drive sales and profit?
- Where are discounts associated with losses?
- How does sales performance evolve over time?

## Tools

- Python: Pandas for cleaning and analysis; Matplotlib and Seaborn for visualizations
- SQL: reusable business queries in `sql/analysis_queries.sql`
- Dataset: fictional Sample Superstore transactions, sourced from [leonism/sample-superstore](https://github.com/leonism/sample-superstore)

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

### Fastest path: automatic download

From the repository root, install dependencies and run:

```bash
python -m pip install -r requirements.txt
python src/analyze.py --download --output outputs
```

The `--download` option saves the public source CSV to `data/superstore.csv`. The script then writes:

- `outputs/superstore_cleaned.csv`
- `outputs/analysis_summary.json`
- `outputs/visuals/sales_by_category.png`
- `outputs/visuals/profit_by_subcategory.png`
- `outputs/visuals/regional_performance.png`
- `outputs/visuals/monthly_sales_trend.png`

### Use an existing CSV

```bash
python src/analyze.py --input data/superstore.csv --output outputs
```

The input file must contain the standard Superstore columns, including `Order ID`, `Order Date`, `Sales`, `Profit`, `Category`, `Sub-Category`, and `Region`.

## Run tests

The regression suite uses a small synthetic dataset, so it does not require network access or the full source CSV:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs syntax checks and this regression suite for every push to `main` and every pull request.

## Repository structure

```text
src/analyze.py                         reproducible Python pipeline
requirements.txt                       Python dependencies
tests/test_pipeline.py                 deterministic regression tests
.github/workflows/ci.yml               automated validation
sql/analysis_queries.sql               SQL analysis queries
notebooks/superstore_analysis.ipynb    notebook walkthrough
visuals/                               presentation charts
Superstore_Sales_Analysis_Presentation.pptx
```

The downloadable source archive contains the original project package, including the cleaned dataset and exported analysis outputs.
