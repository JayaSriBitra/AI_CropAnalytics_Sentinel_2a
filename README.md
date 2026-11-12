# AI Crop Analytics Using Sentinel-2A Satellite Data (`AI_CropAnalytics_Sentinel_2a`)

**Project Title:** Implementation of LLMs in Agriculture: Crop Analytics Using Sentinel-2A Satellite Data  
**Repository:** `JayaSriBitra/AI_CropAnalytics_Sentinel_2a`  
**Project Period:** November 2026 – April 2027  

> **Repository Status:** Active planning, documentation, validation-starter, and frontend-scaffold phase. Do not treat proposed architecture, database schemas, or Qwen/RAG workflows as already implemented backend services.

---

## Table of Contents

- [Overview](#overview)
- [Team Role Allocation](#team-role-allocation)
- [Implemented vs. Planned Status](#implemented-vs-planned-status)
- [Repository Structure](#repository-structure)
- [Frontend Setup (`frontend/`)](#frontend-setup-frontend)
- [Validation Utilities (`validation/`)](#validation-utilities-validation)
- [Testing (`tests/`)](#testing-tests)
- [Documentation Index (`docs/`)](#documentation-index-docs)
- [Known Documentation & Setup Gaps](#known-documentation--setup-gaps)
- [License](#license)

---

## Overview

This project aims to build an end-to-end agricultural analytics platform combining:

1. **Sentinel-2A Data Preparation & Spectral Indices** (`preprocessing/`, `src/preprocessing/`, `src/indices/`): Band selection, quality filtering, NDVI/NDWI/EVI calculation, and area analysis.
2. **Semantic Segmentation** (`src/segmentation/`, `models/`): U-Net crop/land-cover segmentation with baseline comparisons (Random Forest, SVM, Naïve Bayes as planned in validation).
3. **Ground-Truth & Validation** (`validation/`): Spatial alignment checks, group-leakage-free dataset splitting, and segmentation metrics (Accuracy, Precision, Recall, F1, IoU, Dice).
4. **LLM + RAG Analytical Layer** (`llm_rag/`): Qwen-based evidence-grounded interpretation of structured analysis JSON, retrieved agronomy/index references, and citation checks.
5. **Backend & Spatial Database** (`backend/`): FastAPI services with PostgreSQL + PostGIS metadata persistence.
6. **Web Dashboard** (`frontend/`): React + Vite dashboard (`FieldSight`) for imagery upload, NDVI trends, crop health breakdown, and report export.

---

## Team Role Allocation

| Team Member | Assigned Role | Main Responsibility |
|---|---|---|
| **JayaSri** | ML Lead | Own the U-Net workflow: architecture, training, inference, evaluation, and model improvements |
| **Bhavani** | Backend & Integration Lead | Lead FastAPI, PostgreSQL/PostGIS, backend architecture, API development, and module integration |
| **Meghana** | Remote Sensing Developer | Handle Sentinel-2A data preparation, band selection, preprocessing, NDVI/NDWI/EVI calculations, and area analysis |
| **Dheeraj** | Qwen / RAG Developer | Build Qwen-based explanations, agricultural knowledge collection, embeddings, retrieval, prompts, and grounding evaluation |
| **Ajay Surya** | Ground Truth & Validation Developer | Prepare reference data and validation methodology; implement metrics, independent validation, error analysis, and reporting |
| **Rajasekar** | Frontend Developer | Build React dashboard components and pages, improve UI, display maps/charts, and connect frontend views to APIs |
| **Venkatesh** | Testing & Documentation Coordinator | Maintain README and documentation, track genuine contributions, prepare test cases, record test evidence, and coordinate final reports |

---

## Implemented vs. Planned Status

| Area | Current State in Checkout | Key Files |
|---|---|---|
| **System & Database Design** | Proposed architecture & logical ERD documented | [`docs/system_architecture.md`](docs/system_architecture.md), [`docs/database_design.md`](docs/database_design.md) |
| **Qwen + RAG Design** | Proposed pipeline, JSON contract & grounding rules documented; no code yet | [`docs/qwen_integration_plan.md`](docs/qwen_integration_plan.md), [`llm_rag/README.md`](llm_rag/README.md) |
| **Validation Methodology & Utilities** | Starter Python scripts & methodology implemented (`metrics.py`, `create_split.py`, `check_masks.py`) | [`docs/validation_plan.md`](docs/validation_plan.md), [`validation/README.md`](validation/README.md) |
| **Frontend Dashboard (`FieldSight`)** | Vite + React scaffold with demo-data fallback & API client | [`frontend/src/App.jsx`](frontend/src/App.jsx), [`frontend/src/services/api.js`](frontend/src/services/api.js) |
| **Dataset & Preprocessing** | Dataset inventory & workflow documented; `data/` contains only `.gitkeep` | [`dataset/README.md`](dataset/README.md), [`preprocessing/README.md`](preprocessing/README.md), [`docs/dataset_inventory_template.md`](docs/dataset_inventory_template.md) |
| **Testing & Documentation Coordination** | Contribution tracker, test plan, unit tests (`tests/`), test evidence log & report plan | [`docs/contribution_tracker.md`](docs/contribution_tracker.md), [`docs/testing_plan.md`](docs/testing_plan.md), [`docs/test_evidence.md`](docs/test_evidence.md), [`docs/report_coordination.md`](docs/report_coordination.md) |
| **Backend API (`backend/`)** | Skeleton `.gitkeep` only; not yet implemented | [`backend/.gitkeep`](backend/.gitkeep) |
| **ML / Indices (`src/`, `models/`)** | Skeleton `.gitkeep` directories only; not yet implemented | [`src/segmentation/.gitkeep`](src/segmentation/.gitkeep), [`models/.gitkeep`](models/.gitkeep) |

---

## Repository Structure

```text
AI_CropAnalytics_Sentinel_2a/
├── backend/                     # Planned FastAPI backend (currently .gitkeep)
├── data/                        # Dataset root (currently .gitkeep; no imagery committed)
├── dataset/
│   └── README.md                # Verified dataset inventory
├── docs/
│   ├── contribution_tracker.md  # Verified team PR & contribution log
│   ├── database_design.md       # Proposed PostgreSQL + PostGIS schema
│   ├── dataset_inventory_template.md
│   ├── qwen_integration_plan.md # Proposed Qwen + RAG analytical design
│   ├── report_coordination.md   # Final report structure & sign-off checklist
│   ├── system_architecture.md   # Proposed production architecture
│   ├── test_evidence.md         # Recorded verification & test execution log
│   ├── testing_plan.md          # Test cases & release gates
│   └── validation_plan.md       # Ground-truth & evaluation methodology
├── frontend/                    # React + Vite dashboard ("FieldSight")
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── styles.css
│       └── services/api.js
├── llm_rag/
│   └── README.md                # Qwen + RAG module overview (planning stage)
├── models/                      # Planned model artifacts (currently .gitkeep)
├── notebooks/                   # Experiment notebooks (currently .gitkeep)
├── preprocessing/
│   └── README.md                # Sentinel-2A preprocessing plan & status
├── src/
│   ├── evaluation/              # Planned evaluation scripts (.gitkeep)
│   ├── indices/                 # Planned NDVI/NDWI/EVI scripts (.gitkeep)
│   ├── preprocessing/           # Planned preprocessing modules (.gitkeep)
│   └── segmentation/            # Planned U-Net modules (.gitkeep)
├── tests/
│   └── test_validation.py       # Unit & CLI tests for validation utilities
├── validation/
│   ├── README.md
│   ├── check_masks.py           # Raster alignment & label value checker
│   ├── create_split.py          # Geographic-grouped train/val/test splitter
│   ├── metrics.py               # Pixel accuracy, P/R/F1, IoU, Dice metrics
│   └── sample_manifest.csv      # Sample manifest header template
├── Base_Paper.pdf
├── CSM_A01_MajorProject_ABSTRACT.pdf
├── Reference_Paper_01.pdf .. 05.pdf
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Frontend Setup (`frontend/`)

The dashboard is built with **React** and **Vite** (configured on port `5173` in [`frontend/vite.config.js`](frontend/vite.config.js)). When the FastAPI backend at `VITE_API_URL` (default `http://localhost:8000`) is offline, [`frontend/src/services/api.js`](frontend/src/services/api.js) falls back to local demo data.

```bash
cd frontend
npm install

# Optional: configure backend URL
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS

# Start Vite dev server (http://localhost:5173)
npm run dev

# Build production bundle
npm run build
```

---

## Validation Utilities (`validation/`)

1. **Mask & Grid Inspection** (requires `rasterio` and `numpy`):
   ```bash
   python validation/check_masks.py --image path/to/image.tif --mask path/to/mask.tif
   ```
2. **Geographic-Grouped Split**:
   ```bash
   python validation/create_split.py --input validation/sample_manifest.csv --output validation/split_manifest.csv --seed 42
   ```
3. **Segmentation Metrics**:
   ```bash
   python validation/metrics.py
   ```

---

## Testing (`tests/`)

Run the automated Python `unittest` suite from the repository root (requires Python 3.11+ and `numpy`):

```bash
python -m unittest discover -s tests -v
```

See [`docs/testing_plan.md`](docs/testing_plan.md) for test case definitions and [`docs/test_evidence.md`](docs/test_evidence.md) for recorded execution logs.

---

## Documentation Index (`docs/`)

- [`docs/system_architecture.md`](docs/system_architecture.md) — Target full-stack architecture & release gates
- [`docs/database_design.md`](docs/database_design.md) — Logical PostgreSQL + PostGIS schema
- [`docs/qwen_integration_plan.md`](docs/qwen_integration_plan.md) — Qwen + RAG grounding and JSON contract
- [`docs/validation_plan.md`](docs/validation_plan.md) — Ground-truth review, split rules, and metrics
- [`docs/dataset_inventory_template.md`](docs/dataset_inventory_template.md) — Dataset metadata capture template
- [`docs/contribution_tracker.md`](docs/contribution_tracker.md) — Genuine PR & commit tracking across all members
- [`docs/testing_plan.md`](docs/testing_plan.md) — Unit, integration, frontend, and RAG test cases
- [`docs/test_evidence.md`](docs/test_evidence.md) — Recorded test evidence and verification gaps
- [`docs/report_coordination.md`](docs/report_coordination.md) — Final report structure and submission checklist

---

## Known Documentation & Setup Gaps

- `dataset/README.md`, `preprocessing/README.md`, and `docs/dataset_inventory_template.md` reference `preprocessing/inspect_dataset.py`, which has not yet been committed to `preprocessing/`.
- Root `requirements.txt` is currently empty (`0` bytes) and should be populated as backend, ML, and geospatial dependencies are finalized.
- `backend/`, `models/`, `notebooks/`, and `src/` currently contain only `.gitkeep` placeholders.

---

## License

For educational and academic research purposes (`CSM_A01_MajorProject_ABSTRACT.pdf`).
