#!/usr/bin/env python3
"""Run the Superstore analysis end-to-end.

Usage: python src/analyze.py --input data/superstore.csv --output outputs
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(path: Path) -> pd.DataFrame:
      df = pd.read_csv(path, encoding="latin1")
      df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
      required = {"order_id", "order_date", "sales", "profit", "category", "sub_category", "region"}
      missing = required.difference(df.columns)
      if missing:
                raise ValueError(f"Missing required columns: {sorted(missing)}")
            for col in ("order_date", "ship_date"):
                      if col in df:
                                    df[col] = pd.to_datetime(df[col], errors="coerce")
                            for col in ("sales", "profit", "discount", "quantity"):
                                      if col in df:
                                                    df[col] = pd.to_numeric(df[col], errors="coerce")
                                            df = df.dropna(subset=["order_id", "order_date", "sales", "profit"]).copy()
    df["profit_margin"] = df["profit"].div(df["sales"].where(df["sales"].ne(0)))
    if "ship_date" in df:
              df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
    return df


def money(value: float) -> float:
      return round(float(value), 2)


def make_charts(df: pd.DataFrame, output: Path) -> None:
      sns.set_theme(style="whitegrid")
    output.mkdir(parents=True, exist_ok=True)
    category = df.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    sub = df.groupby("sub_category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("profit")
    region = df.groupby("region", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    monthly = df.assign(month=df["order_date"].dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    fig, ax = plt.subplots(figsize=(8, 4.5)); sns.barplot(data=category, x="category", y="sales", ax=ax); ax.set(title="Sales by Category", ylabel="Sales (USD)"); fig.tight_layout(); fig.savefig(output / "sales_by_category.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 5)); sns.barplot(data=sub, x="profit", y="sub_category", hue="sub_category", legend=False, palette=["#d95f02" if x < 0 else "#1b9e77" for x in sub["profit"]], ax=ax); ax.axvline(0, color="black", linewidth=.8); ax.set(title="Profitability by Sub-Category", xlabel="Profit (USD)"); fig.tight_layout(); fig.savefig(output / "profit_by_subcategory.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5)); region.set_index("region")[["sales", "profit"]].plot(kind="bar", ax=ax); ax.set(title="Regional Sales and Profit", ylabel="USD", xlabel=""); ax.tick_params(axis="x", rotation=0); fig.tight_layout(); fig.savefig(output / "regional_performance.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4.5)); ax.plot(monthly["month"], monthly["sales"], linewidth=2.2); ax.set(title="Monthly Sales Trend", ylabel="Sales (USD)"); fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(output / "monthly_sales_trend.png", dpi=180); plt.close(fig)


def run(input_path: Path, output: Path) -> dict:
      df = load_data(input_path)
    output.mkdir(parents=True, exist_ok=True)
    df.to_csv(output / "superstore_cleaned.csv", index=False)
    by_category = df.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("sales", ascending=False)
    by_region = df.groupby("region", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("profit")
    by_sub = df.groupby("sub_category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"), avg_discount=("discount", "mean") if "discount" in df else ("sales", "mean"))
    orders = df.groupby("order_id", as_index=False)["sales"].sum()
    summary = {"records": int(len(df)), "orders": int(df["order_id"].nunique()), "sales": money(df["sales"].sum()), "profit": money(df["profit"].sum()), "profit_margin": round(float(df["profit"].sum() / df["sales"].sum()), 4), "average_order_value": money(orders["sales"].mean()), "top_category": str(by_category.iloc[0]["category"]), "most_profitable_region": str(by_region.iloc[-1]["region"]), "weakest_profit_region": str(by_region.iloc[0]["region"]), "loss_making_subcategories": by_sub.loc[by_sub["profit"] < 0, "sub_category"].tolist(), "category_performance": by_category.round(2).to_dict("records"), "region_performance": by_region.round(2).to_dict("records")}
    with (output / "analysis_summary.json").open("w", encoding="utf-8") as f:
              json.dump(summary, f, indent=2)
    make_charts(df, output / "visuals")
    return summary


if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="Analyze Sample Superstore sales data")
    parser.add_argument("--input", type=Path, default=Path("data/superstore.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    result = run(args.input, args.output)
    print(json.dumps({k: result[k] for k in ("records", "orders", "sales", "profit", "profit_margin", "top_category", "loss_making_subcategories")}, indent=2))
