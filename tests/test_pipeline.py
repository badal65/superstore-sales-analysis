from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("analyze", ROOT / "src" / "analyze.py")
ANALYZE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ANALYZE)


class PipelineTests(unittest.TestCase):
    def test_run_creates_outputs_and_expected_metrics(self) -> None:
        rows = [
            {"Order ID": "A-1", "Order Date": "01/01/2024", "Ship Date": "01/03/2024", "Sales": 100, "Profit": 20, "Discount": 0.0, "Quantity": 2, "Category": "Technology", "Sub-Category": "Phones", "Region": "West"},
            {"Order ID": "A-1", "Order Date": "01/01/2024", "Ship Date": "01/03/2024", "Sales": 50, "Profit": -10, "Discount": 0.2, "Quantity": 1, "Category": "Furniture", "Sub-Category": "Tables", "Region": "West"},
            {"Order ID": "B-1", "Order Date": "02/15/2024", "Ship Date": "02/18/2024", "Sales": 200, "Profit": 40, "Discount": 0.1, "Quantity": 3, "Category": "Technology", "Sub-Category": "Phones", "Region": "East"},
            {"Order ID": "C-1", "Order Date": "03/20/2024", "Ship Date": "03/22/2024", "Sales": 80, "Profit": -20, "Discount": 0.3, "Quantity": 2, "Category": "Furniture", "Sub-Category": "Tables", "Region": "East"},
        ]
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            input_path = directory / "data.csv"
            output_path = directory / "outputs"
            pd.DataFrame(rows).to_csv(input_path, index=False)
            summary = ANALYZE.run(input_path, output_path)
            self.assertEqual(summary["records"], 4)
            self.assertEqual(summary["orders"], 3)
            self.assertEqual(summary["sales"], 430.0)
            self.assertEqual(summary["profit"], 30.0)
            self.assertEqual(summary["top_category"], "Technology")
            self.assertIn("Tables", summary["loss_making_subcategories"])
            self.assertTrue((output_path / "superstore_cleaned.csv").exists())
            self.assertTrue((output_path / "visuals" / "sales_by_category.png").exists())
            with (output_path / "analysis_summary.json").open(encoding="utf-8") as handle:
                self.assertEqual(json.load(handle)["average_order_value"], 143.33)

    def test_missing_input_is_clear(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.csv"
            with self.assertRaises(FileNotFoundError):
                ANALYZE.run(missing, Path(temp) / "outputs")


if __name__ == "__main__":
    unittest.main()
