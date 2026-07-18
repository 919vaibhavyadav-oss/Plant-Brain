# 🏭 PlantBrain — Unified Asset & Operations Brain

**ET AI Hackathon 2026 · Problem Statement #8: AI for Industrial Knowledge Intelligence**

Industrial plants run on 7–12 disconnected document systems. PlantBrain ingests them all —
CMMS work orders, inspection registers, incident reports, SOPs, and regulatory documents —
into one intelligence layer that answers questions with citations, detects compliance gaps
continuously, and warns when the conditions that preceded a past incident are active again.

**Validated on real industrial data:** 8,076 real maintenance work orders (MaintIE corpus),
the official OISD-STD-116 fire-protection standard, and the Factories Act 1948 — with a
published-benchmark entity-extraction score of **94.8% token accuracy / 0.909 macro-F1**.

## Quick start

```bash
pip install streamlit pandas scikit-learn networkx plotly requests
python generate_data.py            # synthetic demo plant (BIEL-2)
git clone --depth 1 https://github.com/nlp-tlp/maintie external/maintie   # real MWOs
python -m src.benchmark            # trains + scores the entity extractor
streamlit run app.py
```

**LLM synthesis (optional):** copy `.env.example` to `.env` and add a `GROQ_API_KEY`
(free at console.groq.com). The copilot then synthesizes answers with
`llama-3.3-70b-versatile`, constrained to retrieved context with citations. Without a key —
or if the API fails mid-demo — it falls back automatically to extractive answers.
Everything else runs fully offline.

## What's inside

| Path | Role |
|---|---|
| `generate_data.py` | Synthetic plant corpus with engineered cross-system patterns |
| `src/ingest.py` | Universal ingestion + entity extraction (tags, clauses, dates) — CSV, Markdown, PDF |
| `src/maintie.py` | Loader for the MaintIE real work-order corpus (gold + silver) |
| `src/benchmark.py` | Entity-extraction benchmark vs expert gold labels → `data/benchmark_results.json` |
| `src/kg.py` | Auto-derived knowledge graph (NetworkX) |
| `src/retrieval.py` | TF-IDF index + doc-type boosts + entity-aware asset boosting |
| `src/agents.py` | Copilot (GraphRAG-lite + LLM/extractive), maintenance intel, compliance radar, risk echoes |
| `app.py` | Streamlit console — 7 views |

## Data sources

- **MaintIE** (Bikaun et al., LREC-COLING 2024, MIT licence) — 1,076 expert double-annotated +
  7,000 reviewed real maintenance work orders from mining, rail and heavy industry.
- **OISD-STD-116 / OISD-STD-117** — official Oil Industry Safety Directorate documents
  (downloaded from oisd.gov.in; **do not redistribute** — local demo use only).
- **Factories Act 1948** — official text from India Code (public domain).
- **BIEL-2 synthetic plant** — fictional; generated to demonstrate cross-system reasoning.

## The demo stories

1. **TR-501 transformer** — a 2025 Buchholz near-miss caused by a stale oil test; the Risk Echo
   engine flags that the same statutory test is overdue *again* today.
2. **C-201 compressor** — ask *"Why did compressor C-201 fail in March 2026?"* → the copilot
   reconstructs the two months of ignored vibration warnings, with citations, and the
   knowledge graph pulls in the vibration SOP and OISD-RP-124 automatically.
3. **Fire water** — ask about storage tank protection → answers cite actual pages of the real
   OISD-STD-116 standard, including design flow rates.
4. **Benchmark page** — entity extraction scored against expert annotations on real work
   orders, per-class precision/recall/F1 on screen.
