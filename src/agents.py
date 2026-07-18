"""Intelligence agents on top of the unified corpus.

  * ExpertCopilot      — RAG answers with citations + confidence
  * maintenance_intel  — failure patterns, MTBF, RCA triggers per asset
  * compliance_gaps    — statutory requirement vs inspection evidence
  * risk_echoes        — lessons-learned engine: flags when the conditions
                         that preceded a past incident are present again
"""
import os
import re
from collections import Counter
from datetime import date, timedelta

import pandas as pd

TODAY = date(2026, 7, 16)


# ------------------------------------------------------------------ copilot
class ExpertCopilot:
    def __init__(self, index, graph):
        self.index = index
        self.graph = graph
        self._llm = self._init_llm()
        # doc-node name -> representative chunk, for GraphRAG-lite expansion
        self._doc_chunks = {}
        # source -> ordered section chunks, so the LLM sees whole narrative docs
        self._doc_sections = {}
        for c in index.chunks:
            if c.doc_type in ("incident", "sop"):
                node = c.source.split("/")[-1].replace(".md", "")
                self._doc_chunks.setdefault(node, c)
                self._doc_sections.setdefault(c.source, []).append(c)
            elif c.doc_type == "regulation":
                self._doc_chunks.setdefault(c.title, c)

    def _graph_expand(self, hits, limit=2):
        """Document-GraphRAG-style expansion: pull 1-hop knowledge-graph
        neighbours of the equipment mentioned in the top hits, so structurally
        related documents surface even when they share no query terms."""
        have = {c.chunk_id for c, _ in hits}
        tags = []
        for c, _ in hits[:3]:
            tags.extend(t for t in c.equipment_tags if t in self.graph)
        extra = []
        for tag in dict.fromkeys(tags):
            for nb in self.graph.neighbors(tag):
                cc = self._doc_chunks.get(nb)
                if cc is not None and cc.chunk_id not in have:
                    extra.append(cc)
                    have.add(cc.chunk_id)
                if len(extra) >= limit:
                    return extra
        return extra

    @staticmethod
    def _init_llm():
        """Pick an LLM provider from the environment. Order: Anthropic, Groq.
        Returns {provider, model, client} or None (pure offline mode)."""
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                return {"provider": "anthropic", "client": anthropic.Anthropic(),
                        "model": os.environ.get("PLANTBRAIN_LLM_MODEL", "claude-sonnet-5")}
            except Exception:
                pass
        if os.environ.get("GROQ_API_KEY"):
            return {"provider": "groq", "client": None,
                    "model": os.environ.get("PLANTBRAIN_LLM_MODEL",
                                            "llama-3.3-70b-versatile")}
        return None

    def _generate(self, prompt):
        info = self._llm
        if info["provider"] == "anthropic":
            msg = info["client"].messages.create(
                model=info["model"], max_tokens=700,
                messages=[{"role": "user", "content": prompt}])
            return msg.content[0].text
        import requests
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
            json={"model": info["model"], "max_tokens": 700, "temperature": 0.2,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def answer(self, query, k=6):
        hits = self.index.search(query, k=k)
        if not hits:
            return {"answer": "No relevant records found in the corpus for this query.",
                    "citations": [], "confidence": 0.0, "related_equipment": [], "llm": False}
        top = hits[0][1]
        confidence = min(0.97, round(0.35 + top * 1.4, 2))
        expanded = [(c, None) for c in self._graph_expand(hits)]

        # merge hits: a narrative document (incident/SOP) appears once, and the
        # LLM gets its FULL text — a matched summary section alone can miss the
        # root cause two headings below it
        merged, seen_narrative = [], set()
        for c, s in hits + expanded:
            if c.doc_type in ("incident", "sop"):
                if c.source in seen_narrative:
                    continue
                seen_narrative.add(c.source)
                full = "\n\n".join(sec.text for sec in self._doc_sections[c.source])
                merged.append((c, s, full))
            else:
                merged.append((c, s, c.text))

        citations = [{"source": c.source, "title": c.title, "doc_type": c.doc_type,
                      "date": c.date, "score": round(s, 3) if s is not None else None,
                      "via": "vector" if s is not None else "knowledge-graph",
                      "snippet": c.text[:420] + ("…" if len(c.text) > 420 else "")}
                     for c, s, _ in merged]
        tags = Counter(t for c, _ in hits for t in c.equipment_tags)
        related = [t for t, _ in tags.most_common(5)]

        if self._llm:
            context = "\n\n---\n\n".join(
                f"[{i+1}] ({c.source}) {text}"
                for i, (c, _, text) in enumerate(merged))
            prompt = (f"You are an industrial operations copilot for a heavy-industry plant. "
                      f"Answer strictly from the numbered context, citing sources as [n]. "
                      f"Be precise and practical; if the context is insufficient, say so.\n\n"
                      f"Context:\n{context}\n\nQuestion: {query}")
            try:
                text = self._generate(prompt)
                label = f"{self._llm['provider']} · {self._llm['model']}"
                return {"answer": text, "citations": citations, "confidence": confidence,
                        "related_equipment": related, "llm": True, "llm_label": label}
            except Exception:
                pass  # fall through to extractive mode — the demo must never break

        # extractive composition (offline mode)
        lines = [f"Based on {len(hits)} matching records across "
                 f"{len({c.doc_type for c, _ in hits})} source systems:"]
        for i, (c, _) in enumerate(hits[:4], 1):
            snippet = re.sub(r"\s+", " ", c.text)[:300]
            lines.append(f"**[{i}] {c.title}** ({c.doc_type}, {c.date or 'undated'}) — {snippet}…")
        return {"answer": "\n\n".join(lines), "citations": citations,
                "confidence": confidence, "related_equipment": related, "llm": False}


# ------------------------------------------------- maintenance intelligence
FAILURE_KEYWORDS = {
    "seal": "Mechanical seal failure", "bearing": "Bearing degradation",
    "vibration": "High vibration", "leak": "Leakage", "tracking": "Belt tracking fault",
    "interlock": "Guard/interlock fault", "valve": "Valve failure",
    "refractory": "Refractory damage", "calibration": "Calibration issue",
    "oil": "Oil system issue", "brake": "Brake wear", "limit switch": "Limit switch failure",
}


def _classify(desc):
    d = desc.lower()
    for kw, label in FAILURE_KEYWORDS.items():
        if kw in d:
            return label
    return "Other"


def maintenance_intel(tag, tables):
    wo = tables["work_orders"]
    mine = wo[wo["equipment_tag"] == tag].copy()
    mine["date"] = pd.to_datetime(mine["date"])
    corr = mine[mine["wo_type"] != "Preventive"].sort_values("date")
    out = {"tag": tag, "total_wos": len(mine), "corrective": len(corr),
           "downtime_h": round(float(corr["downtime_hours"].sum()), 1),
           "mtbf_days": None, "modes": [], "rca_flags": [], "timeline": corr}
    if len(corr) >= 2:
        gaps = corr["date"].diff().dt.days.dropna()
        out["mtbf_days"] = round(float(gaps.mean()), 1)
    corr = corr.assign(mode=corr["description"].map(_classify))
    out["timeline"] = corr
    counts = corr["mode"].value_counts()
    out["modes"] = list(counts.items())
    cutoff = pd.Timestamp(TODAY) - pd.Timedelta(days=365)
    recent = corr[corr["date"] >= cutoff]
    for mode, n in recent["mode"].value_counts().items():
        if n >= 3 and mode != "Other":
            out["rca_flags"].append(
                f"'{mode}' occurred {n}× in the last 12 months — formal RCA required "
                f"per SOP-ME-002 (repeat-failure rule).")
    return out


# ---------------------------------------------------------- compliance gaps
def compliance_gaps(tables):
    eq = tables["equipment"]
    regs = tables["regulations"]
    insp = tables["inspections"].copy()
    insp["date"] = pd.to_datetime(insp["date"])
    rows = []
    for _, reg in regs.iterrows():
        types = reg["applies_to_types"].split("|")
        for _, e in eq[eq["equipment_type"].isin(types)].iterrows():
            evid = insp[(insp["equipment_tag"] == e["tag"]) &
                        (insp["inspection_type"].str.contains(
                            reg["evidence_inspection_type"].split("(")[0].strip()[:15],
                            case=False, regex=False))]
            if evid.empty:
                rows.append([e["tag"], e["name"], reg["clause_id"], "No evidence on record",
                             None, None, "MISSING", 10_000])
                continue
            last = evid["date"].max().date()
            due = last + timedelta(days=int(reg["frequency_days"]))
            overdue_days = (TODAY - due).days
            status = ("OVERDUE" if overdue_days > 0
                      else "DUE SOON" if overdue_days > -30 else "OK")
            rows.append([e["tag"], e["name"], reg["clause_id"], reg["evidence_inspection_type"],
                         last.isoformat(), due.isoformat(), status, overdue_days])
    df = pd.DataFrame(rows, columns=["tag", "equipment", "clause", "evidence",
                                     "last_done", "due_date", "status", "overdue_days"])
    order = {"MISSING": 0, "OVERDUE": 1, "DUE SOON": 2, "OK": 3}
    return df.sort_values(["status", "overdue_days"],
                          key=lambda s: s.map(order) if s.name == "status" else -s)


# -------------------------------------------------------------- risk echoes
def risk_echoes(chunks, tables, gaps):
    """Match past incidents against *currently active* risk conditions."""
    intel_cache = {}
    echoes = []
    incident_docs = {}
    for c in chunks:
        if c.doc_type == "incident":
            incident_docs.setdefault(c.source, {"title": c.title, "date": c.date, "tags": set()})
            incident_docs[c.source]["tags"].update(c.equipment_tags)

    bad = gaps[gaps["status"].isin(["OVERDUE", "MISSING"])]
    for src, info in incident_docs.items():
        for tag in sorted(info["tags"]):
            g = bad[bad["tag"] == tag]
            for _, row in g.iterrows():
                echoes.append({
                    "severity": "HIGH",
                    "equipment": tag,
                    "headline": f"{tag}: compliance lapse matching a past incident precursor",
                    "detail": (f"**{info['title'].split('—')[0].strip()}** "
                               f"({info['date']}) involved {tag}. Right now, clause "
                               f"**{row['clause']}** evidence is **{row['status']}** "
                               f"(last done {row['last_done'] or 'never'}). The condition that "
                               f"contributed to that incident is present again."),
                    "evidence": [src, f"Compliance radar: {row['clause']}"]})
            if tag not in intel_cache:
                intel_cache[tag] = maintenance_intel(tag, tables)
            for flag in intel_cache[tag]["rca_flags"]:
                echoes.append({
                    "severity": "MEDIUM",
                    "equipment": tag,
                    "headline": f"{tag}: repeat failure pattern echoes {info['title'].split('—')[0].strip()}",
                    "detail": (f"{flag} This asset also appears in past incident record "
                               f"**{info['title'].split('—')[0].strip()}** ({info['date']})."),
                    "evidence": [src, "CMMS work-order history"]})
    # dedupe
    seen, unique = set(), []
    for e in echoes:
        key = (e["equipment"], e["headline"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    unique.sort(key=lambda e: 0 if e["severity"] == "HIGH" else 1)
    return unique
