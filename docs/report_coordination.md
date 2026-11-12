# Final Report & Submission Coordination

**Coordinator:** Venkatesh (Member 7 — Testing & Documentation Coordinator)  
**Project Period:** November 2026 – April 2027  
**Reference Abstract:** [`CSM_A01_MajorProject_ABSTRACT.pdf`](../CSM_A01_MajorProject_ABSTRACT.pdf)

---

## 1. Purpose

This document coordinates the structure, ownership, and verification rules for the final major-project report and demonstration package so that every claim in the final report traces back to committed code, datasets, and recorded test evidence.

---

## 2. Final Report Section Ownership

| Report Section | Primary Owner(s) | Required Supporting Evidence in Repo |
|---|---|---|
| 1. Introduction, Problem Statement & Literature Survey | JayaSri, Venkatesh | `CSM_A01_MajorProject_ABSTRACT.pdf`, `Base_Paper.pdf`, `Reference_Paper_01`–`05.pdf` |
| 2. System Architecture & Database Design | Bhavani | `docs/system_architecture.md`, `docs/database_design.md`, implemented `backend/` & migrations |
| 3. Sentinel-2A Dataset & Preprocessing | Meghana | Verified `dataset/README.md`, completed `docs/dataset_inventory_template.md`, `preprocessing/` & `src/indices/` |
| 4. U-Net Segmentation & Baseline Models | JayaSri | `src/segmentation/`, training configs, saved model metadata, loss/metric curves |
| 5. Ground-Truth Validation & Error Analysis | Ajay Surya | `validation/` split manifest, per-class metrics (`Accuracy`, `Precision`, `Recall`, `F1`, `IoU`, `Dice`), error analysis |
| 6. Qwen + RAG Analytical Layer | Dheeraj | `llm_rag/` implementation, knowledge-base sources, faithfulness/citation/abstention results |
| 7. Web Dashboard & Integration | Rajasekar, Bhavani | `frontend/` build + screenshots of live connected dashboard & end-to-end demo |
| 8. Testing Summary, Contributions & Conclusion | Venkatesh | `docs/testing_plan.md`, `docs/test_evidence.md`, `docs/contribution_tracker.md` |

---

## 3. Pre-Submission Quality Checklist

- [ ] Root `README.md` accurately matches final repository files, setup steps, and commands.
- [ ] `requirements.txt` and `frontend/package.json` install cleanly on a fresh environment.
- [ ] All unit, integration, and frontend tests pass and are logged in [`docs/test_evidence.md`](test_evidence.md).
- [ ] No real credentials, `.env` files, or API keys are committed to Git.
- [ ] Every metric table and figure in the final report cites the exact commit/script that produced it.
- [ ] Contribution summary in [`docs/contribution_tracker.md`](contribution_tracker.md) matches Git commit/PR history.
