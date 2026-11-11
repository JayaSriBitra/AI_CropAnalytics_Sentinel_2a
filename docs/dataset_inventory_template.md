# Dataset inventory template

**Inspection date:** 2026-11-11  
**Repository:** `AI_CropAnalytics_Sentinel_2a`  
**Dataset root inspected:** `data/`

## Evidence currently available

| Field | Verified value |
|---|---|
| Dataset source/provider | TODO — no dataset files are present |
| Product name/level | TODO — no dataset files are present |
| Dataset location | `data/` (contains only `.gitkeep`) |
| Image file count | 0 |
| Image formats | TODO — no image files found |
| Image filenames | None |
| Acquisition dates | TODO — no filenames or metadata available |
| Geographic coverage | TODO — no spatial files available |
| Ground-truth files | None found |
| Ground-truth format | TODO — no labels/masks available |
| Mask folder | TODO — no labels/masks available |
| Class IDs and names | TODO — no labels/masks available |
| Label NoData/unlabelled value | TODO — no labels/masks available |

## Raster metadata

No raster metadata could be read because no raster file exists under the
inspected dataset root.

| File | Bands/descriptions | Width × height | Resolution | CRS | Data type | NoData | Transform/bounds |
|---|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Preprocessing record

| Step | Status | Parameters/evidence |
|---|---|---|
| File inventory | Completed | `data/` contains only `.gitkeep` |
| Raster metadata inspection | Ready but not executed on data | Run `preprocessing\inspect_dataset.py` after adding data |
| Band selection/order | TODO | Must be confirmed from the actual product |
| Reprojection/resampling | TODO | No source CRS/grid available |
| Scaling/normalization | TODO | No product range or model contract available |
| Cloud/invalid-pixel handling | TODO | No quality bands or masks available |
| Chip generation | TODO | No source dimensions available |
| Train/validation/test split | TODO | No manifest or groups available |

## Required follow-up evidence

After the dataset is supplied, rerun the inspection script and replace TODOs
with values supported by file metadata. Confirm image/mask alignment and obtain
the authoritative class mapping from the label owner before training or
evaluation.

