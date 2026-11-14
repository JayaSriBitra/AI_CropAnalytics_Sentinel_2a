# Sentinel-2 band information

## Evidence from this repository

Inspection date: **2026-11-14**  
Dataset root inspected: [`../data/`](../data/)

The repository currently contains only `data/.gitkeep`. No Sentinel-2 image,
archive, raster, label, or mask file was found. Consequently, the following
project facts are **not verified**:

| Property | Verified project value |
|---|---|
| Available bands | None available in this checkout |
| File format | No image files found |
| Dimensions | Not available |
| Resolution | Not available |
| CRS or transform | Not available |
| Acquisition dates | Not available |
| Ground-truth masks | None found |

The Sentinel-2 band specifications below are general MSI product reference
information. They are **not evidence that these bands are present in this
project**. Confirm the product level, file metadata, band descriptions and
channel order when imagery is supplied.

## Sentinel-2 MSI reference bands

| Band | Common description | Native resolution | Project availability |
|---|---|---:|---|
| B01 | Coastal aerosol | 60 m | Not verified |
| B02 | Blue | 10 m | Not verified |
| B03 | Green | 10 m | Not verified |
| B04 | Red | 10 m | Not verified |
| B05 | Red edge 1 | 20 m | Not verified |
| B06 | Red edge 2 | 20 m | Not verified |
| B07 | Red edge 3 | 20 m | Not verified |
| B08 | Near-infrared (NIR) | 10 m | Not verified |
| B8A | Narrow NIR | 20 m | Not verified |
| B09 | Water vapour | 60 m | Not verified |
| B10 | Cirrus | 60 m | Not verified |
| B11 | Short-wave infrared 1 (SWIR) | 20 m | Not verified |
| B12 | Short-wave infrared 2 (SWIR) | 20 m | Not verified |

Native resolution is a property of the Sentinel-2 MSI product. It does not
mean that all bands in a model input have the same pixel grid. Any
multi-resolution input must use an explicitly documented target grid and
resampling method after the source metadata is inspected.

## Required checks when data is supplied

Run the repository inspection utility before selecting channels:

```powershell
python preprocessing\inspect_dataset.py --root data
```

For every image, record the relative path, format/driver, width, height, band
count and descriptions, CRS, transform, bounds, resolution, data types and
NoData values. Also record acquisition dates from authoritative product
metadata; do not infer dates or band order from a filename alone. If a
multi-file product is supplied, confirm that all files belong to the same
scene and grid.

### Requested band availability checks

| Requested group | Result in this checkout |
|---|---|
| B02, B03, B04 | No files are present, so availability is unverified |
| B08 | No files are present, so availability is unverified |
| Red edge: B05, B06, B07, B8A | No files are present, so availability is unverified |
| SWIR: B11, B12 | No files are present, so availability is unverified |

## Band combinations

The following are **proposals only**. None has been implemented or tested
against this repository's data:

| Purpose | Proposed bands | Notes |
|---|---|---|
| Natural-colour visualisation | B04, B03, B02 | Requires all three 10 m bands |
| NIR false colour | B08, B04, B03 | Requires all three 10 m bands |
| Vegetation red-edge features | B05, B06, B07, B8A | Requires 20 m red-edge bands and a chosen target grid |
| Vegetation/SWIR features | B08, B11, B12 | Requires resampling the 20 m SWIR bands to the selected grid |
| NDVI | B08 and B04 | Formula below; requires both bands on the same grid |

There is currently no implemented band-selection, resampling, cloud masking,
normalization, chip-generation, or NDVI pipeline in this repository. Do not
describe any proposal above as an implemented model input until code and tests
confirm it.

## NDVI specification

For Sentinel-2, the proposed NDVI calculation is:

```text
NDVI = (B08 - B04) / (B08 + B04)
```

Use NIR **B08** and red **B04**. Before calculating, confirm that both bands
have matching dimensions, CRS, transform and pixel alignment, and apply the
product's documented scale factor consistently if values are stored as
integers. Pixels with invalid values or a zero denominator must be handled by
an explicitly documented policy. No NDVI helper is currently present in this
checkout, so this specification is not an implementation claim.

## Ground-truth data

No ground-truth mask or label is present. Mask dimensions, CRS, transform,
class IDs, class names and NoData policy remain **to be confirmed** before
segmentation training or evaluation.
