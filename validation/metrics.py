"""Metrics for integer-label semantic segmentation masks.

Inputs must be same-shaped arrays of class IDs (not probability/logit arrays).
Only pixels equal to ignore_index in y_true are excluded.
"""
from __future__ import annotations

import numpy as np


def segmentation_metrics(y_true, y_pred, class_ids, ignore_index=None):
    """Return pixel accuracy and per-class precision/recall/F1/IoU/Dice.

    Undefined per-class ratios are returned as None when their denominator
    is zero. Macro averages ignore undefined classes.
    """
    true = np.asarray(y_true)
    pred = np.asarray(y_pred)

    if true.shape != pred.shape:
        raise ValueError(f"Shape mismatch: y_true {true.shape} vs y_pred {pred.shape}")
    if true.size == 0:
        raise ValueError("Masks are empty")
    if not np.issubdtype(true.dtype, np.integer):
        raise TypeError("y_true must contain integer class IDs")
    if not np.issubdtype(pred.dtype, np.integer):
        raise TypeError("y_pred must contain integer class IDs")

    classes = [int(c) for c in class_ids]
    if not classes or len(set(classes)) != len(classes):
        raise ValueError("class_ids must be a non-empty list of unique IDs")

    valid = np.ones(true.shape, dtype=bool)
    if ignore_index is not None:
        valid &= true != ignore_index

    true_v = true[valid].astype(np.int64, copy=False)
    pred_v = pred[valid].astype(np.int64, copy=False)
    if true_v.size == 0:
        raise ValueError("No labelled pixels remain after applying ignore_index")

    unknown_true = set(np.unique(true_v).tolist()) - set(classes)
    unknown_pred = set(np.unique(pred_v).tolist()) - set(classes)
    if unknown_true:
        raise ValueError(f"Unknown class IDs in y_true: {sorted(unknown_true)}")
    if unknown_pred:
        raise ValueError(f"Unknown class IDs in y_pred: {sorted(unknown_pred)}")

    per_class = {}
    f1_values, iou_values, dice_values = [], [], []
    for class_id in classes:
        tp = int(np.sum((true_v == class_id) & (pred_v == class_id)))
        fp = int(np.sum((true_v != class_id) & (pred_v == class_id)))
        fn = int(np.sum((true_v == class_id) & (pred_v != class_id)))
        support = int(np.sum(true_v == class_id))

        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = (2 * tp / (2 * tp + fp + fn)) if (2 * tp + fp + fn) else None
        iou = (tp / (tp + fp + fn)) if (tp + fp + fn) else None
        dice = (2 * tp / (2 * tp + fp + fn)) if (2 * tp + fp + fn) else None

        per_class[class_id] = {
            "support": support,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "iou": iou,
            "dice": dice,
        }
        if f1 is not None:
            f1_values.append(f1)
        if iou is not None:
            iou_values.append(iou)
        if dice is not None:
            dice_values.append(dice)

    return {
        "pixel_accuracy": float(np.mean(true_v == pred_v)),
        "labelled_pixel_count": int(true_v.size),
        "per_class": per_class,
        "macro_f1": float(np.mean(f1_values)) if f1_values else None,
        "macro_iou": float(np.mean(iou_values)) if iou_values else None,
        "macro_dice": float(np.mean(dice_values)) if dice_values else None,
    }


if __name__ == "__main__":
    # Small self-check only; this is not a project result.
    truth = np.array([[0, 1], [1, 2]], dtype=np.uint8)
    prediction = np.array([[0, 1], [2, 2]], dtype=np.uint8)
    print(segmentation_metrics(truth, prediction, class_ids=[0, 1, 2]))
