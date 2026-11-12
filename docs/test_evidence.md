# Test Evidence Log

**Maintainer:** Venkatesh (Member 7 — Testing & Documentation Coordinator)  
**Policy:** Record only directly observed command outputs, exact environment versions, and verified artifacts. Never extrapolate, edit, or mark unexecuted tests as passing.

---

## 1. Environment Baseline (Observed 2026-11-12)

| Component | Observed Value | Notes |
|---|---|---|
| Python | `3.11.0` | Standard library `unittest` available |
| NumPy | `2.4.0` | Installed |
| `pytest` | Not installed | Use `python -m unittest discover -s tests -v` |
| `rasterio` | Not installed | `validation/check_masks.py` exits with code `2` when invoked for raster inspection |
| Node.js | `v22.22.0` | `npm` CLI failed path lookup in current shell (`Cannot find module 'D:\node_modules\npm\bin\npm-prefix.js'`) |
| Dataset (`data/`) | Empty (`.gitkeep` only) | No GeoTIFF imagery or masks available for end-to-end tests |

---

## 2. Executed & Pending Test Runs

| Run ID | Date | Scope / Command | Status | Observed Output / Notes |
|---|---|---|---|---|
| `RUN-001` | 2026-11-12 | `python -m unittest discover -s tests -v` | **Pending execution** | `tests/test_validation.py` added in PR #6 (`TC-VAL-01` through `TC-VAL-06`); awaiting local/CI run record |
| `RUN-002` | 2026-11-12 | `python validation/metrics.py` | **Pending execution** | Built-in self-check on synthetic `2x2` arrays |
| `RUN-003` | 2026-11-12 | `cd frontend && npm install && npm run build` | **Blocked / Not run** | Local shell `npm` path error (`npm-prefix.js` missing under `D:\node_modules`); requires working `npm` installation to verify build |
| `RUN-004` | — | `python validation/check_masks.py --image ... --mask ...` | **Blocked** | Requires `rasterio` and paired GeoTIFF files in `data/` |

---

## 3. Evidence Retention Rules (For Upcoming PRs)

When adding new test evidence to this file, include:
1. **Run ID & Date**
2. **Git Commit / Branch**
3. **Exact Command Executed**
4. **Pass / Fail Counts & Any Skipped Cases**
5. **Artifact Links** (e.g., evaluation report files, confusion matrices, or screenshots once generated)
