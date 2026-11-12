# Testing Plan and Test Case Catalog

**Coordinator:** Venkatesh (Member 7 — Testing & Documentation Coordinator)  
**Aligned With:** [`docs/system_architecture.md`](system_architecture.md) (Section 10), [`docs/validation_plan.md`](validation_plan.md), and [`docs/qwen_integration_plan.md`](qwen_integration_plan.md) (Section 9)

---

## 1. Testing Strategy

Testing follows a phased gate model matching the repository's implementation progress:

1. **Phase 1 (Current — Starter Code & Frontend Scaffold):** Automated unit and CLI tests for `validation/` scripts, plus manual/build verification of `frontend/`.
2. **Phase 2 (Preprocessing & U-Net Pipeline):** Unit tests for Sentinel-2A band ordering, NoData/cloud masking, NDVI/NDWI/EVI formulas, and U-Net tensor shapes/checkpoints.
3. **Phase 3 (Backend & Database Integration):** FastAPI contract tests (`/api/v1/*`), upload validation, and PostgreSQL/PostGIS migration tests.
4. **Phase 4 (Qwen + RAG Grounding & End-to-End):** Faithfulness, citation validity, abstention (`Insufficient data`), and full upload-to-insight smoke tests.

---

## 2. Test Case Catalog

### 2.1 Validation Module (`validation/`) — Active

| Test ID | Target | Scenario / Input | Expected Result | Automated In |
|---|---|---|---|---|
| `TC-VAL-01` | `validation/metrics.py` | Known `2x2` integer masks (`class_ids=[0,1,2]`) | Pixel accuracy `0.75`; exact per-class precision, recall, F1, IoU, Dice, support, and macro averages | `tests/test_validation.py` |
| `TC-VAL-02` | `validation/metrics.py` | Mask with `ignore_index=255` and absent class `2` | Ignored pixel excluded from `labelled_pixel_count`; absent class returns `None` and is omitted from macro averages | `tests/test_validation.py` |
| `TC-VAL-03` | `validation/metrics.py` | Shape mismatch, empty array, float dtype, duplicate `class_ids`, all-ignored, or unknown class ID | Raises explicit `ValueError` or `TypeError` | `tests/test_validation.py` |
| `TC-VAL-04` | `validation/create_split.py` | 30 chips across 10 `group_id`s with `--seed 42` run twice | Byte-identical output CSVs; every `group_id` appears in strictly one split (`train`/`validation`/`test`) | `tests/test_validation.py` |
| `TC-VAL-05` | `validation/create_split.py` | Empty `group_id` or split ratios not summing to `1.0` | Exits with non-zero status and validation error | `tests/test_validation.py` |
| `TC-VAL-06` | `validation/check_masks.py` | `--help` flag and missing `rasterio` dependency check | `--help` exits `0`; missing `rasterio` exits `2` with install hint on `stderr` | `tests/test_validation.py` |
| `TC-VAL-07` | `validation/check_masks.py` | Real paired GeoTIFF image & mask (mismatched CRS/dimensions vs. aligned) | Returns `1` on mismatch, `0` on aligned single-band mask | Pending GeoTIFF test fixtures |

### 2.2 Preprocessing & Indices (`preprocessing/`, `src/`) — Planned

| Test ID | Target | Scenario / Input | Expected Result | Status |
|---|---|---|---|---|
| `TC-PRE-01` | `preprocessing/inspect_dataset.py` | Run on `data/` (empty vs. sample raster) | Lists files cleanly and reads CRS/transform/bands without modifying inputs | Planned (script pending) |
| `TC-PRE-02` | `src/indices/` | Synthetic Red and NIR arrays including `NIR + Red == 0` and NoData | Output NDVI bounded in `[-1, 1]`, zero denominators handled safely without `inf`/`NaN` | Planned |
| `TC-PRE-03` | `src/segmentation/` | Synthetic input tensor matching documented band count | U-Net forward pass returns expected `(B, num_classes, H, W)` logits | Planned |

### 2.3 Backend & Database (`backend/`) — Planned

| Test ID | Target | Scenario / Input | Expected Result | Status |
|---|---|---|---|---|
| `TC-API-01` | `GET /api/v1/health` | Service running with/without DB or model | Returns structured JSON status and HTTP `200` (or documented readiness error) | Planned |
| `TC-API-02` | `POST /api/v1/predictions` | Valid image vs. oversized/unsupported file | Valid file creates prediction record; invalid MIME/extension/size returns `4xx` | Planned |
| `TC-API-03` | `POST /api/v1/reports` | Valid `analysis_id` and format `PDF` | Creates report metadata and returns safe download reference | Planned |
| `TC-DB-01` | PostgreSQL + PostGIS | Clean DB migration & insert/query `crop_predictions` | Schema applies cleanly with constraints and spatial index | Planned |

### 2.4 Qwen + RAG Grounding (`llm_rag/`) — Planned

| Test ID | Target | Scenario / Input | Expected Result | Status |
|---|---|---|---|---|
| `TC-RAG-01` | Prompt & post-check | Analysis JSON with `yield_reference_available: false` | No numeric yield figure invented; states limitation qualitatively | Planned |
| `TC-RAG-02` | Abstention | Analysis JSON with `null` NDVI or missing cloud cover | Responds with `"Insufficient data: <missing field>"` | Planned |
| `TC-RAG-03` | Citation check | Generated insight with `[JSON:field]` and `[S#]` tags | Every cited source ID exists in retrieved chunks and numbers match input JSON | Planned |

### 2.5 Frontend Dashboard (`frontend/`) — Scaffold Verification

| Test ID | Target | Scenario / Input | Expected Result | Status |
|---|---|---|---|---|
| `TC-FE-01` | Vite production build | `npm install && npm run build` inside `frontend/` | Exits `0` and produces `frontend/dist/` bundle without syntax/import errors | Pending execution |
| `TC-FE-02` | Offline API fallback | Load dashboard when `http://localhost:8000` is unreachable | Displays `Demo data` pill and renders metrics, NDVI chart, field map, and upload modal | Pending manual UI check |
| `TC-FE-03` | Upload error state | Submit file in upload modal with API offline | Displays non-crashing error message (`The API is unavailable...`) | Pending manual UI check |

---

## 3. Release Gate Criteria

Before any milestone demo or final submission:
1. All automated tests in `tests/` must pass on a clean checkout.
2. Frontend production build (`npm run build`) must succeed cleanly.
3. Every reported accuracy/F1/IoU/Dice score in documentation must reference a recorded run in [`docs/test_evidence.md`](test_evidence.md).
