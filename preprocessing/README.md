# Preprocessing

## Current status

Inspection on **2026-11-14** found only `data/.gitkeep` under the repository
dataset root. No Sentinel-2 imagery, raster metadata, acquisition dates,
ground-truth masks or labels are available. See
[`band_information.md`](band_information.md) for the verified absence of
project bands and the separate Sentinel-2 reference specifications.

No image-processing pipeline is implemented in this checkout. In particular,
cloud masking, reprojection, resampling, scaling, normalization, band
selection, NDVI generation, chip generation and dataset splitting must not be
reported as completed.

## Requirements before preprocessing

1. **Inventory the supplied product.** Record the product level, scene IDs,
   dates, file format, files per scene and authoritative band descriptions.
2. **Inspect every raster.** Record dimensions, band count and order, native
   resolution, CRS, transform, bounds, data type, NoData and scale/offset.
3. **Confirm channels.** Verify whether B02, B03, B04, B08, B05-B07, B8A,
   B11 and B12 are actually present. Do not assume a complete Sentinel-2
   product or infer channel order from filenames.
4. **Choose one target grid.** If bands have different native resolutions,
   document the target CRS, pixel size, extent and resampling method. Preserve
   image/mask alignment.
5. **Handle quality values.** Identify the product's quality metadata and
   invalid/NoData policy before implementing cloud or invalid-pixel filtering.
   Cloud masking is not implemented here.
6. **Define numeric preprocessing.** Confirm whether values are reflectance,
   scaled integers or another product representation. Document scale factors,
   clipping and normalization statistics from the training data.
7. **Define labels separately.** If masks are supplied, verify dimensions,
   CRS, transform, class IDs, class names and NoData/unlabelled values. No
   masks are currently present.
8. **Generate and validate samples.** Record chip size/stride and use
   geographic groups for train/validation/test splits. Check finite values,
   channel order, alignment and leakage.

## Implemented versus pending

| Activity | Status | Evidence |
|---|---|---|
| Locate dataset root | Verified | `data/` contains only `.gitkeep` |
| Enumerate candidate files | Available | [`inspect_dataset.py`](inspect_dataset.py) |
| Read raster metadata | Not executed | No raster files are present |
| Band selection and ordering | Pending | Requires actual product metadata |
| Cloud/invalid-pixel handling | Not implemented | No quality bands or masks are present |
| Reprojection/resampling | Not implemented | Source grids are unavailable |
| Scaling/normalization | Not implemented | Product encoding and training statistics are unknown |
| NDVI using B08 and B04 | Proposed only | No imagery or NDVI implementation is present |
| Mask preprocessing | Not implemented | No ground-truth masks are present |
| Chip generation and splitting | Not implemented | No source dimensions or manifest are present |

## Run the inspection

From the repository root:

```powershell
python preprocessing\inspect_dataset.py
```

To inspect another directory:

```powershell
python preprocessing\inspect_dataset.py --root "C:\path\to\dataset"
```

For raster metadata, install the project's agreed raster dependency if it is
not already available:

```powershell
python -m pip install rasterio
```

The script reports missing optional raster support explicitly and never alters
source files.

After data is supplied, update [`band_information.md`](band_information.md)
with measured values and retain the command output as review evidence. Do not
install a raster dependency solely to claim preprocessing has been performed;
the inspection utility only needs `rasterio` when raster metadata is to be
read.
