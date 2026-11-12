# Team Contribution Tracker

**Coordinator:** Venkatesh (Member 7 — Testing & Documentation Coordinator)  
**Repository:** `JayaSriBitra/AI_CropAnalytics_Sentinel_2a`  
**Tracking Rule:** Only contributions verified via committed files and Git pull request history are marked as completed. Planned work and placeholders (`.gitkeep`) are tracked separately without inflating status.

---

## 1. Team Overview & Current Status

| Member | Assigned Role | First PR / Branch | Primary Deliverables Verified in Git | Current Status |
|---|---|---|---|---|
| **JayaSri** | ML Lead | Repo owner & PR reviews (`#1`, `#2`, `#3`, `#5`) | Base & reference papers (`Base_Paper.pdf`, `Reference_Paper_01`–`05.pdf`), PR merges | Papers & repo management complete; U-Net code (`src/segmentation/`) pending |
| **Bhavani** | Backend & Integration Lead | PR `#1` (`bhavani/system-database-design`) | Initial skeleton, [`docs/system_architecture.md`](system_architecture.md), [`docs/database_design.md`](database_design.md) | Architecture & DB design complete; FastAPI code (`backend/`) pending |
| **Dheeraj** | Qwen / RAG Developer | PR `#2` (`dheerajchowdary65/dheeraj/qwen-rag-plan`) | [`docs/qwen_integration_plan.md`](qwen_integration_plan.md), [`llm_rag/README.md`](../llm_rag/README.md) | Design & JSON contract complete; RAG/Qwen implementation pending |
| **Ajay Surya** | Ground Truth & Validation Developer | PR `#3` (`ajay-validation`) | [`docs/validation_plan.md`](validation_plan.md), [`validation/README.md`](../validation/README.md), `check_masks.py`, `create_split.py`, `metrics.py`, `sample_manifest.csv` | Validation starter scripts & methodology complete; real dataset evaluation pending |
| **Rajasekar** | Frontend Developer | PR `#4` (`rajasekhar2005/UI-feature`) | [`frontend/`](../frontend/package.json) Vite + React dashboard (`App.jsx`, `api.js`, `styles.css`, `vite.config.js`) | Dashboard UI scaffold with demo-data fallback complete; live API wiring pending backend |
| **Meghana** | Remote Sensing Developer | PR `#5` (`feature/meghana-dataset-preprocessing`) | [`dataset/README.md`](../dataset/README.md), [`preprocessing/README.md`](../preprocessing/README.md), [`docs/dataset_inventory_template.md`](dataset_inventory_template.md) | Dataset audit & workflow plan complete; `inspect_dataset.py` & preprocessing code pending |
| **Venkatesh** | Testing & Documentation Coordinator | Pending PR (`venkatesh/testing-docs-coordination`) | Updated [`README.md`](../README.md), [`tests/test_validation.py`](../tests/test_validation.py), contribution tracker, testing plan, test evidence log, report coordination | PR #6 ready for review |

---

## 2. Verified Git Pull Request & Commit Ledger

| PR # | Commit Hash | Date | Author (Git) | Summary & Files Verified |
|---|---|---|---|---|
| Initial | `8cb0ccb`..`0f66e5f` | 2026-09-19 | `Bhuvanagiri Bhavani`, `JayaSriBitra` | Uploaded project abstract, base/reference papers, initial `README.md`, and directory skeleton |
| **PR #1** | `13905ae` (merged `0b2ca9a`) | 2026-11-07 | `Bhuvanagiri Bhavani` (merged by `JayaSriBitra`) | Added `docs/system_architecture.md` and `docs/database_design.md` |
| **PR #2** | `6b33b86` (merged `c72c193`) | 2026-11-07 / 2026-11-09 | `dheerajchowdary65` (merged by `JayaSriBitra`) | Added `docs/qwen_integration_plan.md` and `llm_rag/README.md` |
| **PR #3** | `c2c54bf` (merged `3e2cde7`) | 2026-11-07 / 2026-11-09 | `ajaysurya1812` (merged by `JayaSriBitra`) | Added `docs/validation_plan.md`, `validation/README.md`, `validation/check_masks.py`, `validation/create_split.py`, `validation/metrics.py`, `validation/sample_manifest.csv` |
| **PR #4** | `154883e` (merged `667d3b2`) | 2026-11-08 | `Raja Sekhar Bonam` | Added `frontend/` React + Vite dashboard scaffold and updated `README.md` |
| **PR #5** | `1190e23` (merged `c8c1aa2`) | 2026-11-11 / 2026-11-12 | `megha2710005` (merged by `JayaSriBitra`) | Added `dataset/README.md`, `docs/dataset_inventory_template.md`, `preprocessing/README.md` |

---

## 3. Open Action Items & Cross-Team Dependencies

1. **Dataset Supply (`data/`)**: Required by Remote Sensing (Meghana), ML (JayaSri), and Validation (Ajay Surya) before any real training, preprocessing, or metric reporting can occur.
2. **Missing Referenced Script**: `preprocessing/inspect_dataset.py` is referenced in PR #5 docs but not yet present in `preprocessing/`.
3. **Dependencies Manifest**: Root `requirements.txt` is currently empty and needs coordinated updates from Backend, ML, Remote Sensing, Validation, and Qwen/RAG owners.
4. **API Contract Alignment**: `frontend/src/services/api.js` expects `/api/v1/health`, `/api/v1/statistics`, `/api/v1/predictions`, and `/api/v1/reports` on `VITE_API_URL` (`http://localhost:8000`); Backend (Bhavani) and Frontend (Rajasekar) must keep these routes aligned with `docs/system_architecture.md`.
