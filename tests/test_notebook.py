import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "superstore_analysis.ipynb"


class NotebookStructureTests(unittest.TestCase):
      def test_notebook_json_and_code_cells_are_valid(self):
            notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
            self.assertEqual(notebook["nbformat"], 4)
            self.assertGreater(len(notebook["cells"]), 0)
            [compile("".join(cell.get("source", [])), str(NOTEBOOK), "exec") for cell in notebook["cells"] if cell.get("cell_type") == "code"]
