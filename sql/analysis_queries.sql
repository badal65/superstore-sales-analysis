-- Superstore Sales Analysis (SQLite-compatible SQL)
-- Import data/superstore_cleaned.csv into a table named superstore_sales first.

-- 1. Executive KPIs
SELECT COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 2) AS profit_margin_pct
FROM superstore_sales;

-- 2. Category performance
SELECT category, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit
FROM superstore_sales GROUP BY category ORDER BY profit DESC;

-- 3. Loss-making sub-categories
SELECT sub_category, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit,
       ROUND(AVG(discount)*100,1) AS avg_discount_pct
FROM superstore_sales GROUP BY sub_category HAVING SUM(profit) < 0 ORDER BY profit;

-- 4. Regional performance
SELECT region, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit
FROM superstore_sales GROUP BY region ORDER BY profit DESC;
