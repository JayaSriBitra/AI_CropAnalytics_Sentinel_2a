# Qwen Prompt Templates

**Owner:** Dheeraj (Member 4) | **PR:** Add Qwen Prompt Templates
**Code:** [`prompts.py`](prompts.py) | **Design:** [`../docs/qwen_integration_plan.md`](../docs/qwen_integration_plan.md)

> **Status:** Templates drafted and format-checked with `python llm_rag/prompts.py`. They have **not** yet been run against a Qwen model, so output quality is untested.

## 1. How the prompts work

Qwen does not see satellite pixels. Each prompt has two parts:

| Part | Content |
|---|---|
| **System prompt** | Fixed rules: use only the given JSON and evidence, copy numbers exactly, cite sources, answer "Insufficient data" when evidence is missing |
| **User prompt** | Task template filled with the analysis JSON section(s) and numbered evidence passages `[S1]`, `[S2]`, ... |

`prompts.py` only builds the messages (`[{"role": "system", ...}, {"role": "user", ...}]`). Calling Qwen is a separate, planned step.

## 2. System prompt rules

1. Use only the analysis JSON and evidence. No outside facts or numbers.
2. Copy numbers exactly. Do not compute new statistics.
3. Cite every claim: `[JSON:<field>]` or `[S<number>]`.
4. Missing or `null` values: write `Insufficient data: <what is missing>`.
5. Exact yield only when `yield_reference_available` is `true`; otherwise qualitative yield-related patterns only.
6. Mention data-quality issues and model-reliability limits.
7. Simple, concise language for farmers, planners and researchers.

## 3. Templates

| Template | Builder function | JSON sections used | Output |
|---|---|---|---|
| Crop segmentation explanation | `build_segmentation_prompt` | `segmentation`, `model_metrics`, `data_quality` | Summary, crop pattern, reliability, limitations |
| Vegetation-index explanation | `build_vegetation_index_prompt` | `vegetation_indices`, `data_quality` | Index values, crop health, water condition, caveats |
| Combined insight | `build_combined_prompt` | full analysis JSON | Crop pattern, crop health, yield-related analysis, reliability, sources |
| User question | `build_question_prompt` | full analysis JSON + question | Evidence-based answer or "Insufficient data" |

All builders take `evidence` as an optional list of `{"source": ..., "text": ...}` chunks, which will come from the RAG retriever. With no evidence the prompt states that none was retrieved, so the model must abstain from unsupported interpretation.

## 4. Usage

```python
from llm_rag.prompts import build_combined_prompt

messages = build_combined_prompt(analysis_json, evidence_chunks)
# messages -> chat template of the Qwen model (planned)
```

## 5. Design decisions

- **No index thresholds inside the prompts.** NDVI/NDWI/EVI interpretation ranges must come from retrieved reference documents, so they stay traceable and correctable.
- **Numbers come only from the JSON**, which keeps the LLM from altering code-computed results.
- **Separate templates per task** keep prompts short and easier to evaluate.

## 6. Status

| Item | Status |
|---|---|
| System prompt and four templates | Completed (draft) |
| Prompt builder functions in `prompts.py` | Completed (format-checked only) |
| Testing against Qwen outputs | Planned |
| Faithfulness / citation evaluation | Planned |
| Prompt refinement from evaluation | Planned |
| Connection to retriever and backend | Planned |
