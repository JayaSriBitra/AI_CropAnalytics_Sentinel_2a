# Dataset inventory

## Verified repository state

Inspection date: 2026-11-11

The repository's dataset location is [`data/`](../data/). It currently contains
only [`data/.gitkeep`](../data/.gitkeep). No Sentinel-2A image, product
directory, archive, raster, vector label, or mask file was found in the
repository.

The root README mentions a `SEN-2 LULC/` layout with train/validation/test
images and masks, but that directory is not present in this checkout. That
description is therefore treated as project documentation, not as verified
dataset evidence.

## Available files and raster metadata

| Item | Verified value |
|---|---|
| Dataset root | `data/` |
| Image files | None found |
| File formats | None found |
| Band names/descriptions | Not available |
| Dimensions | Not available |
| Acquisition dates | Not available |
| CRS and transform | Not available |
| Data types | Not available |
| NoData values | Not available |

These fields must be updated after the actual imagery is placed in `data/` and
inspected with [`preprocessing/inspect_dataset.py`](../preprocessing/inspect_dataset.py).

## Ground-truth masks and labels

No ground-truth mask or label file is present in this checkout. Consequently,
the mask format, location, class values, class names, label-generation method,
and mask NoData value cannot be verified.

The validation documentation describes masks as an expected input for future
evaluation; it does not establish that masks currently exist. Do not create a
class mapping or use a NoData value until the label files and their metadata
have been reviewed.

## Dataset requirements to confirm

When the dataset becomes available, record:

- the exact source/provider and product name;
- scene or chip filenames and acquisition dates;
- band names, order, dimensions, resolution and scaling;
- CRS, affine transform and bounds;
- raster data types and per-band NoData values;
- image/mask pairing and spatial alignment;
- mask class IDs, class names and unlabelled/NoData policy; and
- geographic and temporal coverage.

