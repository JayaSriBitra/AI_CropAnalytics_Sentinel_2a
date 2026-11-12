# Preprocessing

## Current status

The preprocessing contribution is **not complete**. No Sentinel-2A imagery is
present in [`data/`](../data/), so no image loading, reprojection, resampling,
cloud filtering, scaling, normalization, band selection, chip generation, or
train/validation/test split has been executed or checked for this repository.

The currently implemented utility is
[`inspect_dataset.py`](inspect_dataset.py). It recursively lists candidate
dataset files and, when `rasterio` is installed, reports raster metadata. It
does not modify imagery or generate derived data.

## Planned workflow

The following steps are planned and must be adapted to the verified product
metadata and the model input contract:

1. **Inventory** image and label files, including product type, acquisition
   dates and any existing split information.
2. **Inspect spatial metadata**: dimensions, bands, CRS, transform, bounds,
   resolution, data type and NoData.
3. **Confirm band selection and order** from the actual product metadata. Do
   not infer channel positions from filenames alone.
4. **Check image/label alignment** when masks exist: dimensions, CRS, transform,
   extent and pixel correspondence.
5. **Apply product-appropriate quality handling**, such as cloud or invalid
   pixel exclusion, only after the required quality bands/metadata are
   identified.
6. **Apply documented scaling/normalization** using values confirmed for the
   product and training pipeline.
7. **Create chips or resize inputs**, preserving the spatial relationship
   between images and masks and recording the chosen parameters.
8. **Create geographic-grouped splits** using the existing validation utility
   once a manifest and group definition are available.
9. **Validate outputs** by checking shapes, finite values, class IDs, alignment
   and representative visual samples.

## Implemented versus planned

| Activity | Status | Evidence |
|---|---|---|
| Locate the repository dataset root | Implemented | `data/` was inspected |
| Enumerate available dataset files | Implemented | No dataset files found |
| Read raster metadata | Implemented as an inspection capability | `inspect_dataset.py`; no raster was available to read |
| Image preprocessing | Not implemented/executed | No imagery is present |
| Mask preprocessing | Not implemented/executed | No masks are present |
| Scaling/normalization | Planned | Product and model contract are unverified |
| Chip generation | Planned | Input dimensions are unverified |
| Dataset splitting | Planned | No manifest or geographic groups exist |

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

