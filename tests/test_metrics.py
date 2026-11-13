
import unittest
import sys
from pathlib import Path

import numpy as np

# Add the project root to Python's import path
REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from validation.metrics import segmentation_metrics


class TestAdditionalSegmentationMetrics(unittest.TestCase):

    def test_perfect_prediction(self):
        y_true = np.array([[0, 1], [1, 0]])
        y_pred = np.array([[0, 1], [1, 0]])

        result = segmentation_metrics(
            y_true, y_pred, class_ids=[0, 1]
        )

        self.assertEqual(result["pixel_accuracy"], 1.0)
        self.assertEqual(result["macro_iou"], 1.0)
        self.assertEqual(result["macro_dice"], 1.0)
        self.assertEqual(result["macro_f1"], 1.0)

    def test_class_predicted_but_not_present_in_ground_truth(self):
        y_true = np.array([[0, 0]])
        y_pred = np.array([[0, 1]])

        result = segmentation_metrics(
            y_true, y_pred, class_ids=[0, 1]
        )

        class_one = result["per_class"][1]

        self.assertEqual(class_one["precision"], 0.0)
        self.assertIsNone(class_one["recall"])
        self.assertEqual(class_one["f1"], 0.0)
        self.assertEqual(class_one["iou"], 0.0)
        self.assertEqual(class_one["dice"], 0.0)

    def test_unknown_prediction_on_ignored_pixel(self):
        y_true = np.array([[0, 1, 255]])
        y_pred = np.array([[0, 1, 99]])

        result = segmentation_metrics(
            y_true,
            y_pred,
            class_ids=[0, 1],
            ignore_index=255
        )

        self.assertEqual(result["labelled_pixel_count"], 2)
        self.assertEqual(result["pixel_accuracy"], 1.0)
        self.assertEqual(result["macro_iou"], 1.0)


if __name__ == "__main__":
    unittest.main()
