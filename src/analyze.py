#!/usr/bin/env python3
"""Run the Superstore analysis end-to-end.

The script can download the public source CSV when it is not present:

    python src/analyze.py --download --output outputs

It writes a cleaned dataset, a JSON summary, and four PNG charts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DEFAULT_SOURCE_URL = "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv"


def download_data(target: Path, url: str = DEFAULT_SOURCE_URL) -> Path:
    """Download the source CSV to *target* and return the saved path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "superstore-sales-analysis/1.0"})
    with urlopen(request, timeout=60) as response:
        target.write_bytes(response.read())
    return target


def load_data(path: Path) -> pd.DataFrame:
    """Load and standardize the Sample Superstore transaction data."""
    df = pd.read_csv(path, encoding="latin1")
    df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    required = {"order_id", "order_date", "sales", "profit", "category", "sub_category", "region"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    for col in ("order_date", "ship_date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in ("sales", "profit", "discount", "quantity"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["order_id", "order_date", "sales", "profit"]).copy()
    df["profit_margin"] = df["profit"].div(df["sales"].where(df["sales"].ne(0)))
    if "ship_date" in df.columns:
        df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
    return df


def make_charts(df: pd.DataFrame, output: Path) -> None:
    """Create the four presentation-ready charts."""
    sns.set_theme(style="whitegrid")
    output.mkdir(parents=True, exist_ok=True)
    category = df.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    sub = df.groupby("sub_category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("profit")
    region = df.groupby("region", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    monthly = df.assign(month=df["order_date"].dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=category, x="category", y="sales", ax=ax)
    ax.set(title="Sales by Category", ylabel="Sales (USD)")
    fig.tight_layout()
    fig.savefig(output / "sales_by_category.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#d95f02" if value < 0 else "#1b9e77" for value in sub["profit"]]
    ax.barh(sub["sub_category"], sub["profit"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set(title="Profitability by Sub-Category", xlabel="Profit (USD)")
    fig.tight_layout()
    fig.savefig(output / "profit_by_subcategory.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    region.set_index("region")[["sales", "profit"]].plot(kind="bar", ax=ax)
    ax.set(title="Regional Sales and Profit", ylabel="USD", xlabel="")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(output / "regional_performance.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly["month"], monthly["sales"], linewidth=2.2)
    ax.set(title="Monthly Sales Trend", ylabel="Sales (USD)")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output / "monthly_sales_trend.png", dpi=180)
    plt.close(fig)


def run(input_path: Path, output: Path) -> dict:
    """Run cleaning, aggregation, summary generation, and chart creation."""
    df = load_data(input_path)
    output.mkdir(parents=True, exist_ok=True)
    df.to_csv(output / "superstore_cleaned.csv", index=False)
    by_category = df.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("sales", ascending=False)
    by_region = df.groupby("region", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("profit")
    by_sub = df.groupby("sub_category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    orders = df.groupby("order_id", as_index=False)["sales"].sum()
    summary = {
        "records": int(len(df)),
        "orders": int(df["order_id"].nunique()),
        "sales": round(float(df["sales"].sum()), 2),
        "profit": round(float(df["profit"].sum()), 2),
        "profit_margin": round(float(df["profit"].sum() / df["sales"].sum()), 4),
        "average_order_value": round(float(orders["sales"].mean()), 2),
        "top_category": str(by_category.iloc[0]["category"]),
        "most_profitable_region": str(by_region.iloc[-1]["region"]),
        "weakest_profit_region": str(by_region.iloc[0]["region"]),
        "loss_making_subcategories": by_sub.loc[by_sub["profit"] < 0, "sub_category"].tolist(),
        "category_performance": by_category.round(2).to_dict("records"),
        "region_performance": by_region.round(2).to_dict("records"),
    }
    with (output / "analysis_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    make_charts(df, output / "visuals")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Sample Superstore sales data")
    parser.add_argument("--input", type=Path, default=Path("data/superstore.csv"), help="Input CSV path")
    parser.add_argument("--output", type=Path, default=Path("outputs"), help="Output directory")
    parser.add_argument("--download", action="store_true", help="Download the source CSV when --input is missing")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help="Source CSV URL used with --download")
    args = parser.parse_args()
    if not args.input.exists():
        if not args.download:
            parser.error(f"Input file not found: {args.input}. Re-run with --download to fetch the public dataset.")
        print(f"Downloading source data to {args.input} ...")
        download_data(args.input, args.source_url)
    result = run(args.input, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
