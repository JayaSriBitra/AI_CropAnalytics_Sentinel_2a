"""Unit tests for the repository's validation utilities.

Run from the repository root:
    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import csv
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from validation.metrics import segmentation_metrics  # noqa: E402


class TestSegmentationMetrics(unittest.TestCase):
    """Tests for validation.metrics.segmentation_metrics."""

    def test_exact_metrics_on_known_masks(self) -> None:
        y_true = np.array([[0, 1], [1, 2]], dtype=np.int64)
        y_pred = np.array([[0, 1], [2, 2]], dtype=np.int64)

        result = segmentation_metrics(y_true, y_pred, class_ids=[0, 1, 2])

        self.assertAlmostEqual(result["pixel_accuracy"], 0.75)
        self.assertEqual(result["labelled_pixel_count"], 4)

        # Class 0: TP=1, FP=0, FN=0 -> all 1.0
        c0 = result["per_class"][0]
        self.assertEqual(c0["support"], 1)
        self.assertAlmostEqual(c0["precision"], 1.0)
        self.assertAlmostEqual(c0["recall"], 1.0)
        self.assertAlmostEqual(c0["f1"], 1.0)
        self.assertAlmostEqual(c0["iou"], 1.0)
        self.assertAlmostEqual(c0["dice"], 1.0)

        # Class 1: TP=1, FP=0, FN=1 -> P=1.0, R=0.5, F1=2/3, IoU=0.5, Dice=2/3
        c1 = result["per_class"][1]
        self.assertEqual(c1["support"], 2)
        self.assertAlmostEqual(c1["precision"], 1.0)
        self.assertAlmostEqual(c1["recall"], 0.5)
        self.assertAlmostEqual(c1["f1"], 2 / 3)
        self.assertAlmostEqual(c1["iou"], 0.5)
        self.assertAlmostEqual(c1["dice"], 2 / 3)

        # Class 2: TP=1, FP=1, FN=0 -> P=0.5, R=1.0, F1=2/3, IoU=0.5, Dice=2/3
        c2 = result["per_class"][2]
        self.assertEqual(c2["support"], 1)
        self.assertAlmostEqual(c2["precision"], 0.5)
        self.assertAlmostEqual(c2["recall"], 1.0)
        self.assertAlmostEqual(c2["f1"], 2 / 3)
        self.assertAlmostEqual(c2["iou"], 0.5)
        self.assertAlmostEqual(c2["dice"], 2 / 3)

        self.assertAlmostEqual(result["macro_f1"], (1.0 + 2 / 3 + 2 / 3) / 3)
        self.assertAlmostEqual(result["macro_iou"], (1.0 + 0.5 + 0.5) / 3)
        self.assertAlmostEqual(result["macro_dice"], (1.0 + 2 / 3 + 2 / 3) / 3)

    def test_ignore_index_and_absent_class_returns_none(self) -> None:
        # Pixel (0, 0) is NoData (255) in y_true and must be ignored even if y_pred differs.
        y_true = np.array([[255, 0], [1, 1]], dtype=np.int64)
        y_pred = np.array([[2, 0], [1, 0]], dtype=np.int64)

        result = segmentation_metrics(
            y_true, y_pred, class_ids=[0, 1, 2], ignore_index=255
        )

        self.assertEqual(result["labelled_pixel_count"], 3)
        self.assertAlmostEqual(result["pixel_accuracy"], 2 / 3)

        # Class 2 has 0 true and 0 predicted among valid pixels -> undefined (None).
        c2 = result["per_class"][2]
        self.assertEqual(c2["support"], 0)
        self.assertIsNone(c2["precision"])
        self.assertIsNone(c2["recall"])
        self.assertIsNone(c2["f1"])
        self.assertIsNone(c2["iou"])
        self.assertIsNone(c2["dice"])

        # Macro averages ignore undefined class 2 and average over classes 0 and 1.
        self.assertAlmostEqual(result["macro_f1"], 2 / 3)
        self.assertAlmostEqual(result["macro_iou"], 0.5)

    def test_invalid_inputs_raise_expected_errors(self) -> None:
        with self.assertRaises(ValueError):
            segmentation_metrics(np.array([0, 1]), np.array([[0, 1]]), [0, 1])

        with self.assertRaises(ValueError):
            segmentation_metrics(
                np.array([], dtype=np.int64), np.array([], dtype=np.int64), [0, 1]
            )

        with self.assertRaises(TypeError):
            segmentation_metrics(
                np.array([0.0, 1.0]), np.array([0, 1], dtype=np.int64), [0, 1]
            )

        with self.assertRaises(TypeError):
            segmentation_metrics(
                np.array([0, 1], dtype=np.int64), np.array([0.0, 1.0]), [0, 1]
            )

        with self.assertRaises(ValueError):
            segmentation_metrics(np.array([0, 1]), np.array([0, 1]), [])

        with self.assertRaises(ValueError):
            segmentation_metrics(np.array([0, 1]), np.array([0, 1]), [0, 0])

        with self.assertRaises(ValueError):
            segmentation_metrics(
                np.array([255, 255]), np.array([0, 1]), [0, 1], ignore_index=255
            )

        with self.assertRaises(ValueError):
            segmentation_metrics(np.array([0, 9]), np.array([0, 1]), [0, 1])

        with self.assertRaises(ValueError):
            segmentation_metrics(np.array([0, 1]), np.array([0, 9]), [0, 1])


class TestCreateSplitCLI(unittest.TestCase):
    """Tests for validation/create_split.py CLI workflow."""

    def _run_split(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "validation" / "create_split.py"), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_reproducible_group_leakage_free_split(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest = tmp / "manifest.csv"
            out_a = tmp / "split_a.csv"
            out_b = tmp / "split_b.csv"

            rows = []
            for g_idx in range(10):
                group_id = f"field_{g_idx}"
                for chip_idx in range(3):
                    idx = g_idx * 3 + chip_idx
                    rows.append(
                        {
                            "sample_id": f"chip_{idx:03d}",
                            "image_path": f"data/images/chip_{idx:03d}.tif",
                            "mask_path": f"data/masks/chip_{idx:03d}.tif",
                            "group_id": group_id,
                        }
                    )

            with manifest.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["sample_id", "image_path", "mask_path", "group_id"]
                )
                writer.writeheader()
                writer.writerows(rows)

            res_a = self._run_split(
                ["--input", str(manifest), "--output", str(out_a), "--seed", "42"]
            )
            res_b = self._run_split(
                ["--input", str(manifest), "--output", str(out_b), "--seed", "42"]
            )

            self.assertEqual(res_a.returncode, 0, msg=res_a.stderr)
            self.assertEqual(res_b.returncode, 0, msg=res_b.stderr)
            self.assertEqual(out_a.read_text(encoding="utf-8"), out_b.read_text(encoding="utf-8"))

            with out_a.open(newline="", encoding="utf-8") as f:
                split_rows = list(csv.DictReader(f))

            self.assertEqual(len(split_rows), 30)
            group_splits: dict[str, set[str]] = {}
            split_counts = {"train": 0, "validation": 0, "test": 0}
            for row in split_rows:
                group_splits.setdefault(row["group_id"], set()).add(row["split"])
                split_counts[row["split"]] += 1

            # Each group_id must belong to exactly one split (no group leakage).
            for gid, splits in group_splits.items():
                self.assertEqual(len(splits), 1, msg=f"Group {gid} leaked across {splits}")

            self.assertTrue(all(count > 0 for count in split_counts.values()))

    def test_invalid_ratios_and_missing_group_id_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            bad_manifest = tmp / "bad.csv"
            out_csv = tmp / "out.csv"

            with bad_manifest.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["sample_id", "image_path", "mask_path", "group_id"]
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "sample_id": "chip_001",
                        "image_path": "img.tif",
                        "mask_path": "msk.tif",
                        "group_id": "",
                    }
                )

            res_empty_gid = self._run_split(
                ["--input", str(bad_manifest), "--output", str(out_csv)]
            )
            self.assertNotEqual(res_empty_gid.returncode, 0)

            res_bad_ratio = self._run_split(
                [
                    "--input",
                    str(REPO_ROOT / "validation" / "sample_manifest.csv"),
                    "--output",
                    str(out_csv),
                    "--train",
                    "0.5",
                    "--validation",
                    "0.2",
                    "--test",
                    "0.2",
                ]
            )
            self.assertNotEqual(res_bad_ratio.returncode, 0)


class TestCheckMasksCLI(unittest.TestCase):
    """CLI contract tests for validation/check_masks.py."""

    def test_help_flag_exits_zero(self) -> None:
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "validation" / "check_masks.py"), "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn("--image", res.stdout)
        self.assertIn("--mask", res.stdout)

    def test_missing_rasterio_reports_exit_code_2(self) -> None:
        if importlib.util.find_spec("rasterio") is not None:
            self.skipTest("rasterio is installed in this environment")
        res = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "validation" / "check_masks.py"),
                "--image",
                "dummy_img.tif",
                "--mask",
                "dummy_msk.tif",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 2)
        self.assertIn("rasterio", res.stderr.lower())


if __name__ == "__main__":
    unittest.main()

