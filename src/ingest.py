"""Universal document ingestion + entity extraction.

Every record from every source system becomes a Chunk with extracted entities
(equipment tags, regulatory clause references, dates), giving downstream layers
one unified representation regardless of the original format.
"""
import os
import re
from dataclasses import dataclass, field

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

TAG_RE = re.compile(r"\b(?:P|C|B|COB|CV|TR|V|F|GD|EOT)-\d{1,3}\b")
CLAUSE_RE = re.compile(
    r"\b(?:OISD-(?:STD|RP)-\d+|IBR-1950-Reg-\d+|FactoriesAct-S\.\d+|PESO-SMPV-Rule-\d+|CEA-Reg-2010-R\.\d+)\b"
)
# textual mentions like "Factories Act 1948, Section 21"
CLAUSE_TEXT_RE = re.compile(r"Factories Act(?: 1948)?,? Section (\d+)")


@dataclass
class Chunk:
    chunk_id: str
    doc_type: str          # work_order | inspection | incident | sop | regulation | equipment
    title: str
    text: str
    source: str            # originating file / system
    date: str = ""
    equipment_tags: list = field(default_factory=list)
    clause_refs: list = field(default_factory=list)


def _extract(text):
    tags = sorted(set(TAG_RE.findall(text)))
    clauses = set(CLAUSE_RE.findall(text))
    for sec in CLAUSE_TEXT_RE.findall(text):
        clauses.add(f"FactoriesAct-S.{sec}")
    return tags, sorted(clauses)


def load_corpus():
    """Return (chunks, tables) where tables holds the raw dataframes."""
    chunks = []
    tables = {}

    eq = pd.read_csv(os.path.join(DATA_DIR, "equipment_master.csv"))
    tables["equipment"] = eq
    for _, r in eq.iterrows():
        text = (f"{r['tag']} {r['name']} — {r['equipment_type']} in {r['area']} area. "
                f"Criticality: {r['criticality']}. OEM: {r['oem']}. Installed {r['installed']}.")
        tags, clauses = _extract(text)
        chunks.append(Chunk(f"EQ::{r['tag']}", "equipment", f"{r['tag']} {r['name']}",
                            text, "equipment_master.csv", str(r["installed"]), tags, clauses))

    wo = pd.read_csv(os.path.join(DATA_DIR, "work_orders.csv"))
    tables["work_orders"] = wo
    for _, r in wo.iterrows():
        text = (f"Work order {r['wo_id']} ({r['wo_type']}) on {r['equipment_tag']} dated {r['date']}: "
                f"{r['description']} Technician: {r['technician']}. Downtime: {r['downtime_hours']} h.")
        tags, clauses = _extract(text)
        if r["equipment_tag"] not in tags:
            tags.append(r["equipment_tag"])
        chunks.append(Chunk(f"WO::{r['wo_id']}", "work_order", f"{r['wo_id']} — {r['equipment_tag']}",
                            text, "CMMS (work_orders.csv)", str(r["date"]), tags, clauses))

    insp = pd.read_csv(os.path.join(DATA_DIR, "inspections.csv"))
    tables["inspections"] = insp
    for _, r in insp.iterrows():
        text = (f"Inspection {r['inspection_id']} on {r['equipment_tag']} dated {r['date']} — "
                f"{r['inspection_type']}. Finding: {r['finding']} Severity: {r['severity']}.")
        tags, clauses = _extract(text)
        if r["equipment_tag"] not in tags:
            tags.append(r["equipment_tag"])
        chunks.append(Chunk(f"INSP::{r['inspection_id']}", "inspection",
                            f"{r['inspection_id']} — {r['equipment_tag']}",
                            text, "Inspection register (inspections.csv)", str(r["date"]), tags, clauses))

    regs = pd.read_csv(os.path.join(DATA_DIR, "regulations.csv"))
    tables["regulations"] = regs
    for _, r in regs.iterrows():
        text = (f"Regulatory clause {r['clause_id']}: {r['requirement']} "
                f"Applies to: {r['applies_to_types'].replace('|', ', ')}. "
                f"Required frequency: every {r['frequency_days']} days. "
                f"Evidence: {r['evidence_inspection_type']}.")
        tags, clauses = _extract(text)
        clauses = sorted(set(clauses + [r["clause_id"]]))
        chunks.append(Chunk(f"REG::{r['clause_id']}", "regulation", r["clause_id"],
                            text, "Regulatory library (regulations.csv)", "", tags, clauses))

    for sub, dtype in [("incidents", "incident"), ("sops", "sop")]:
        folder = os.path.join(DATA_DIR, sub)
        for fname in sorted(os.listdir(folder)):
            with open(os.path.join(folder, fname), encoding="utf-8") as f:
                content = f.read()
            title = content.splitlines()[0].lstrip("# ").strip()
            date_m = re.search(r"\*\*Date:\*\* (\d{4}-\d{2}-\d{2})", content)
            # split on ## headings so retrieval hits stay focused
            sections = re.split(r"\n(?=## )", content)
            for i, sec in enumerate(sections):
                tags, clauses = _extract(sec)
                chunks.append(Chunk(f"{dtype.upper()}::{fname}::{i}", dtype, title,
                                    sec.strip(), f"{sub}/{fname}",
                                    date_m.group(1) if date_m else "", tags, clauses))

    _load_standard_pdfs(chunks)
    _load_maintie(chunks)
    return chunks, tables


def _load_standard_pdfs(chunks):
    """Real regulatory documents (OISD standards, Factories Act) as page chunks.

    Text extraction is cached to _extracted.json so the app never re-parses
    PDFs at boot.
    """
    import json
    pdf_dir = os.path.join(DATA_DIR, "oisd")
    if not os.path.isdir(pdf_dir):
        return
    cache_path = os.path.join(pdf_dir, "_extracted.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
    changed = False
    for fname in sorted(os.listdir(pdf_dir)):
        if not fname.endswith(".pdf") or fname in cache:
            continue
        import pdfplumber
        with pdfplumber.open(os.path.join(pdf_dir, fname)) as pdf:
            cache[fname] = [(p.extract_text() or "") for p in pdf.pages]
        changed = True
    if changed:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    for fname, pages in sorted(cache.items()):
        title = fname.replace(".pdf", "")
        for i, text in enumerate(pages):
            text = text.strip()
            if len(text) < 60:
                continue
            tags, clauses = _extract(text)
            chunks.append(Chunk(f"STD::{title}::p{i+1}", "standard",
                                f"{title} — p.{i+1}", text[:1800],
                                f"{fname} (official document)", "", tags, clauses))


def _load_maintie(chunks):
    """Real maintenance work orders from the MaintIE corpus (7,000 silver +
    1,076 gold records; Bikaun et al. 2024, MIT licence)."""
    from . import maintie
    if not maintie.available():
        return
    for split in ("gold", "silver"):
        for j, rec in enumerate(maintie.load(split)):
            text = maintie.clean_text(rec)
            if len(text) < 8:
                continue
            chunks.append(Chunk(f"MWO::{split}::{j}", "field_wo",
                                f"Real MWO ({split} #{j})",
                                f"Field maintenance work order: {text}",
                                "MaintIE real work-order corpus (UWA)", "", [], []))
