# Ground-truth and Validation Plan

**Responsible member:** Ajay Surya (Member 5)  
**Project:** Implementation of LLMs in Agriculture: Crop Analytics Using Sentinel-2A Satellite Data  
**Status:** Proposed methodology – to be finalized after dataset inspection

## 1. Objective

Define a reproducible process for checking reference labels and evaluating crop-segmentation results produced from Sentinel-2A imagery. The primary deep-learning model identified in the project abstract is U-Net. Random Forest, Support Vector Machine (SVM) and Naïve Bayes may be explored for comparison.

## 2. Ground-truth/reference data

Ground-truth data provides the reference crop labels against which model predictions are compared.

For every reference dataset, record:

| Item | What the team must record |
|---|---|
| Dataset name and provider | Exact name, provider and download/reference link |
| Geographic coverage | State/district/region and coordinates or boundary |
| Reference date | Label survey/date or period represented |
| Sentinel-2A date | Acquisition date of the paired satellite scene |
| Label method | Field survey, authoritative map, expert annotation or other verified method |
| Class mapping | Crop/land-cover name and corresponding integer mask value |
| Spatial reference | CRS, pixel size, transform and grid alignment |
| Limitations | Missing labels, uncertain boundaries, mixed pixels or temporal mismatch |

The project abstract does not yet specify a particular ground-truth provider, crop-class list or reference date. These must be confirmed from the actual dataset; they must not be invented in the report.

## 3. Mask quality review

Before training or evaluation:

1. Confirm that each image chip has the correct corresponding mask.
2. Check image and mask width, height, CRS and affine transform.
3. Confirm that the mask contains only documented class IDs and the agreed NoData value.
4. Visually compare image chips and masks, including boundaries and mixed-pixel areas.
5. Flag incomplete, ambiguous, misaligned or questionable labels for review.
6. Keep a record of corrections, exclusions and the reason for each decision.

A mask should not be silently edited to make model predictions look better. Any correction must be traceable and, where possible, reviewed independently.

## 4. Dataset split and leakage prevention

Use three partitions:

- **Training:** used to fit model parameters.
- **Validation:** used for model selection, tuning and early stopping.
- **Test:** held back until the final evaluation.

A proposed starting split is 70% training, 15% validation and 15% testing. These are target proportions, not a claim about the current dataset.

Split at the geographic group level (such as field, parcel, tile or non-overlapping region) so chips from the same group do not appear in multiple partitions. This reduces spatial leakage and gives a more meaningful estimate of performance on unseen areas. If multiple dates from the same location exist, keep those related observations in one partition unless the team has a justified temporal evaluation design.

Save the final split manifest, random seed, group definition and counts so the experiment can be reproduced. Check class representation in each partition; if a rare class is absent from a partition, report that limitation rather than hiding it.

## 5. Evaluation metrics

Compare predicted class masks with reference masks on labelled test pixels only. Use a consistent class-ID mapping and exclude only the agreed NoData/unlabelled value.

For each class, report:

- **Precision:** proportion of pixels predicted as that class that are correct.
- **Recall:** proportion of reference pixels of that class that are correctly detected.
- **F1-score:** harmonic mean of precision and recall.
- **Intersection over Union (IoU):** intersection divided by union between predicted and reference pixels.
- **Dice score:** twice the intersection divided by the total number of predicted and reference pixels.

Also report overall pixel accuracy and class support (number of reference pixels). Include macro averages where appropriate so small classes are not hidden by dominant classes. State how undefined values are handled when a class has no reference or predicted pixels.

The project abstract identifies Accuracy, F1-score, IoU and Dice score as evaluation measures. Precision and recall are included here to make class-level F1 results interpretable.

## 6. Independent validation

After model selection is complete:

1. Freeze the selected model and preprocessing configuration.
2. Run inference on the held-out test groups only.
3. Compare predictions with the corresponding reference masks.
4. Calculate the agreed metrics using the same class mapping and NoData policy.
5. Preserve the test manifest, model/checkpoint identifier, configuration and metric output.
6. Report per-class results, aggregate results, sample/pixel counts and known limitations.

If an independent reference dataset or field-verified labels are available, evaluate them separately and describe their provenance. Do not call a random subset of the training data an independent validation dataset.

## 7. Risks and limitations

- Cloud contamination may reduce usable observations.
- Mixed pixels and similar spectral signatures may cause class confusion.
- Ground-truth labels may be incomplete, outdated or spatially misaligned.
- Class imbalance can make overall accuracy misleading.
- Spatial or temporal overlap between splits can inflate reported performance.
- Exact yield estimation requires suitable yield-reference data; segmentation metrics alone do not validate yield estimates.

These limitations are consistent with the challenges and scope stated in the project abstract.

## 8. Evidence to retain

Keep the following artifacts in the repository when they become available:

- Dataset/source description and class mapping.
- Reviewed image-mask sample evidence.
- Final split manifest and split-generation seed.
- Model and preprocessing configuration.
- Test predictions or reproducible inference instructions.
- Metric report with per-class support.
- Notes on exclusions, corrections and independent reference evaluation.

## 9. Completion criteria

The validation contribution can be considered implemented when the team can trace each reported test metric to a documented reference source, reviewed mask, saved test split and identified model run. Until then, mark the relevant work as planned or in progress.
