"""PlantBrain — Unified Asset & Operations Brain (ET AI Hackathon 2026, Problem #8)."""
import os

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def _load_env():
    """Load KEY=VALUE lines from plantbrain/.env into the environment (API keys
    live there, never in code). Existing environment variables win."""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()

from src.agents import ExpertCopilot, compliance_gaps, maintenance_intel, risk_echoes
from src.benchmark import load_results
from src.ingest import load_corpus
from src.kg import build_graph, neighbourhood
from src.retrieval import Index

st.set_page_config(page_title="PlantBrain — Unified Asset & Operations Brain",
                   page_icon="🏭", layout="wide")

# dark-mode dataviz palette on the PlantBrain brand surface (gunmetal + amber)
INK = "#E8ECF1"; INK2 = "#C9D4DE"; MUTED = "#8FA0B0"; GRID = "#2C3540"; AXIS = "#3D4854"
SURFACE = "#151A20"; CARD = "#212934"; BORDER = "#2E3947"; AMBER = "#F0A028"
S1 = "#3987E5"; S2 = "#199E70"; S3 = "#C98500"; S4 = "#008300"; S5 = "#9085E9"; S6 = "#E66767"
STATUS = {"MISSING": "#D03B3B", "OVERDUE": "#EC835A", "DUE SOON": "#FAB219", "OK": "#0CA30C"}
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'

CSS = f"""
<style>
/* ---- chrome ---- */
#MainMenu, footer {{visibility: hidden;}}
.block-container {{padding-top: 1.2rem; max-width: 1250px;}}

/* ---- hero ---- */
.pb-hero {{
  background: linear-gradient(135deg, #1B222B 0%, #232E3B 55%, #26313F 100%);
  border: 1px solid {BORDER}; border-radius: 16px;
  padding: 26px 32px 22px 32px; margin-bottom: 14px;
}}
.pb-kicker {{
  color: {AMBER}; font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.18em; margin-bottom: 6px;
}}
.pb-title {{
  color: #FFFFFF; font-size: 2.1rem; font-weight: 800;
  line-height: 1.15; margin: 0 0 4px 0;
}}
.pb-sub {{color: {MUTED}; font-size: 0.95rem; margin-bottom: 14px;}}
.pb-chips span {{
  display: inline-block; background: rgba(240,160,40,0.12); color: {AMBER};
  border: 1px solid rgba(240,160,40,0.35); border-radius: 999px;
  padding: 3px 12px; margin-right: 8px; font-size: 0.78rem; font-weight: 600;
}}

/* ---- nav radio as segmented pills ---- */
div[role="radiogroup"] {{gap: 8px; flex-wrap: wrap;}}
div[role="radiogroup"] label {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 999px;
  padding: 7px 16px; transition: border-color .15s;
}}
div[role="radiogroup"] label:hover {{border-color: {AMBER};}}
div[role="radiogroup"] label:has(input:checked) {{
  background: rgba(240,160,40,0.15); border-color: {AMBER};
}}
div[role="radiogroup"] label > div:first-child {{display: none;}}
div[role="radiogroup"] p {{font-size: 0.88rem; font-weight: 600;}}

/* ---- metric cards ---- */
[data-testid="stMetric"] {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
  padding: 16px 18px 12px 18px;
}}
[data-testid="stMetricValue"] {{color: {AMBER}; font-weight: 700;}}
[data-testid="stMetricLabel"] p {{color: {MUTED}; font-size: 0.8rem;}}

/* ---- buttons ---- */
.stButton button {{
  background: {CARD}; border: 1px solid {BORDER}; color: {INK2};
  border-radius: 10px; font-size: 0.82rem;
}}
.stButton button:hover {{border-color: {AMBER}; color: {AMBER};}}

/* ---- echo cards ---- */
.pb-echo {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
  padding: 16px 20px; margin-bottom: 12px;
}}
.pb-badge {{
  display: inline-block; border-radius: 6px; padding: 2px 10px;
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; color: #151A20;
}}
.pb-echo h4 {{color: {INK}; margin: 8px 0 6px 0; font-size: 1.02rem;}}
.pb-echo p {{color: {INK2}; font-size: 0.9rem; margin: 0 0 6px 0;}}
.pb-echo .ev {{color: {MUTED}; font-size: 0.78rem;}}

/* ---- expanders / containers ---- */
[data-testid="stExpander"] {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
}}
</style>
"""


def style(fig, h=380):
    fig.update_layout(
        height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=INK2, size=13),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hoverlabel=dict(font_family=FONT))
    fig.update_xaxes(gridcolor=GRID, linecolor=AXIS, tickfont=dict(color=MUTED), zeroline=False)
    fig.update_yaxes(gridcolor=GRID, linecolor=AXIS, tickfont=dict(color=MUTED), zeroline=False)
    return fig


@st.cache_resource(show_spinner="Ingesting corpus and building the intelligence layer…")
def boot():
    chunks, tables = load_corpus()
    graph = build_graph(chunks, tables)
    index = Index(chunks)
    copilot = ExpertCopilot(index, graph)
    gaps = compliance_gaps(tables)
    echoes = risk_echoes(chunks, tables, gaps)
    return chunks, tables, graph, index, copilot, gaps, echoes


chunks, tables, graph, index, copilot, gaps, echoes = boot()
wo = tables["work_orders"].copy()
wo["date"] = pd.to_datetime(wo["date"])

st.markdown(CSS, unsafe_allow_html=True)
n_real_hdr = sum(1 for c in chunks if c.doc_type in ("field_wo", "standard"))
st.markdown(f"""
<div class="pb-hero">
  <div class="pb-kicker">ET AI HACKATHON 2026 · PROBLEM STATEMENT 8</div>
  <div class="pb-title">🏭 PlantBrain — Unified Asset &amp; Operations Brain</div>
  <div class="pb-sub">Bharat Ispat &amp; Energy Ltd · Unit 2 (fictional demo plant) — one
  intelligence layer over CMMS, inspection registers, incident reports, SOPs and the
  regulatory library.</div>
  <div class="pb-chips">
    <span>{len(chunks):,} records unified</span>
    <span>{n_real_hdr:,} real-world documents</span>
    <span>94.8% benchmarked extraction</span>
    <span>Answers with citations</span>
  </div>
</div>
""", unsafe_allow_html=True)

PAGES = ["Overview", f"🚨 Risk Echoes ({len(echoes)})", "💬 Expert Copilot",
         "🕸️ Knowledge Graph", "🔧 Maintenance Intelligence", "⚖️ Compliance Radar",
         "📊 Real-Data Benchmark"]
nav = st.radio("Navigation", PAGES, horizontal=True, label_visibility="collapsed")

# ------------------------------------------------------------------ overview
if nav == PAGES[0]:
    n_over = int((gaps["status"].isin(["OVERDUE", "MISSING"])).sum())
    n_real = sum(1 for c in chunks if c.doc_type in ("field_wo", "standard"))
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Records unified", f"{len(chunks):,}")
    c2.metric("Real-world records", f"{n_real:,}",
              help="MaintIE work orders + official OISD / Factories Act pages")
    c3.metric("Assets covered", len(tables["equipment"]))
    c4.metric("Active risk echoes", len(echoes))
    c5.metric("Compliance gaps", n_over)

    left, right = st.columns(2)
    with left:
        corr = wo[wo["wo_type"] != "Preventive"]
        dt = (corr.groupby("equipment_tag")["downtime_hours"].sum()
              .sort_values(ascending=True).tail(10))
        fig = go.Figure(go.Bar(
            x=dt.values, y=dt.index, orientation="h", marker_color=AMBER,
            marker=dict(cornerradius=4),
            hovertemplate="%{y}: %{x:.0f} h downtime<extra></extra>"))
        fig.update_layout(title=dict(text="Corrective downtime by asset (hours, 24 months)",
                                     font=dict(color=INK, size=15)))
        st.plotly_chart(style(fig), use_container_width=True)
    with right:
        monthly = (wo.assign(month=wo["date"].dt.to_period("M").dt.to_timestamp(),
                             kind=wo["wo_type"].map(lambda t: "Preventive" if t == "Preventive"
                                                    else "Corrective / Emergency"))
                   .groupby(["month", "kind"]).size().unstack(fill_value=0))
        fig = go.Figure()
        for name, color in [("Corrective / Emergency", S1), ("Preventive", S2)]:
            if name in monthly:
                fig.add_trace(go.Scatter(x=monthly.index, y=monthly[name], name=name,
                                         mode="lines", line=dict(color=color, width=2),
                                         hovertemplate="%{x|%b %Y}: %{y} WOs<extra>" + name + "</extra>"))
        fig.update_layout(title=dict(text="Work orders per month", font=dict(color=INK, size=15)))
        st.plotly_chart(style(fig), use_container_width=True)

    st.markdown(
        "**The problem this solves:** every chart above required joining records that live in "
        "different systems at this plant — CMMS, paper inspection registers, incident PDFs, "
        "SOP binders. PlantBrain ingests them once and lets agents reason across all of them.")

# --------------------------------------------------------------- risk echoes
elif nav == PAGES[1]:
    st.subheader("Lessons-learned engine — past incidents whose preconditions are active again")
    st.caption("Each alert links a historical incident to a *currently live* condition "
               "(an overdue statutory check or a repeat-failure pattern) on the same asset.")
    if not echoes:
        st.success("No active risk echoes.")
    import re as _re
    for e in echoes:
        badge_color = "#EC835A" if e["severity"] == "HIGH" else "#FAB219"
        detail = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e["detail"])
        st.markdown(f"""
<div class="pb-echo">
  <span class="pb-badge" style="background:{badge_color}">{e['severity']}</span>
  <h4>{e['headline']}</h4>
  <p>{detail}</p>
  <div class="ev">Evidence: {' · '.join(e['evidence'])}</div>
</div>""", unsafe_allow_html=True)

# ------------------------------------------------------------------ copilot
elif nav == PAGES[2]:
    st.subheader("Ask the plant anything — answers with citations")
    examples = [
        "What is the history of seal failures on P-101?",
        "Why did compressor C-201 fail in March 2026?",
        "What must be done when a Buchholz alarm occurs on a transformer?",
        "What are the fire water requirements for storage tank protection?",
        "Has a conveyor guard interlock ever been bypassed?",
    ]
    cols = st.columns(len(examples))
    for col, ex in zip(cols, examples):
        if col.button(ex[:34] + "…", key=ex, help=ex, use_container_width=True):
            st.session_state["q"] = ex
    q = st.text_input("Question", value=st.session_state.get("q", ""),
                      placeholder="e.g. What is the vibration alarm limit for C-201?")
    if q:
        res = copilot.answer(q)
        mode = (f"LLM synthesis ({res.get('llm_label', 'LLM')})" if res["llm"]
                else "extractive (offline mode)")
        st.progress(res["confidence"], text=f"Retrieval confidence {res['confidence']:.0%} · answer mode: {mode}")
        st.markdown(res["answer"])
        if res["related_equipment"]:
            st.caption("Related assets: " + " · ".join(f"`{t}`" for t in res["related_equipment"]))
        with st.expander(f"📎 Sources ({len(res['citations'])})"):
            for c in res["citations"]:
                badge = ("🕸️ knowledge-graph link" if c.get("via") == "knowledge-graph"
                         else f"relevance {c['score']}")
                st.markdown(f"**{c['title']}** — {c['doc_type']} · {c['source']} · "
                            f"{c['date'] or 'undated'} · {badge}")
                st.caption(c["snippet"])

# ------------------------------------------------------------ knowledge graph
elif nav == PAGES[3]:
    st.subheader("Everything connected to everything — the graph fragmented systems can't draw")
    KIND_COLOR = {"equipment": S1, "area": MUTED, "regulation": S5,
                  "incident": S6, "sop": S2, "wo_history": S3}
    KIND_LABEL = {"equipment": "Equipment", "area": "Plant area", "regulation": "Regulatory clause",
                  "incident": "Incident / near-miss", "sop": "SOP", "wo_history": "WO history"}
    focus = st.selectbox("Focus on", ["Whole plant"] + sorted(tables["equipment"]["tag"]),
                         help="Pick an asset to see its 2-hop neighbourhood")
    g = graph if focus == "Whole plant" else neighbourhood(graph, focus, hops=2)
    pos = nx.spring_layout(g, seed=7, k=0.9)
    fig = go.Figure()
    ex, ey = [], []
    for a, b in g.edges():
        ex += [pos[a][0], pos[b][0], None]
        ey += [pos[a][1], pos[b][1], None]
    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", hoverinfo="skip",
                             line=dict(color=GRID, width=1), showlegend=False))
    for kind, color in KIND_COLOR.items():
        nodes = [n for n, d in g.nodes(data=True) if d.get("kind") == kind]
        if not nodes:
            continue
        fig.add_trace(go.Scatter(
            x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes],
            mode="markers+text", name=KIND_LABEL[kind],
            text=[n for n in nodes], textposition="top center",
            textfont=dict(size=9, color=INK2),
            marker=dict(size=14 if kind == "equipment" else 10, color=color,
                        line=dict(color=SURFACE, width=2)),
            hovertemplate="%{text}<extra>" + KIND_LABEL[kind] + "</extra>"))
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False)
    st.plotly_chart(style(fig, h=560), use_container_width=True)
    st.caption(f"{g.number_of_nodes()} nodes · {g.number_of_edges()} relationships — "
               "built automatically from entity extraction over all ingested records.")

# ------------------------------------------------------ maintenance intelligence
elif nav == PAGES[4]:
    st.subheader("Per-asset intelligence: failure patterns, MTBF, RCA triggers")
    tag = st.selectbox("Asset", sorted(tables["equipment"]["tag"]), index=8)
    mi = maintenance_intel(tag, tables)
    erow = tables["equipment"].set_index("tag").loc[tag]
    st.markdown(f"**{erow['name']}** — {erow['equipment_type']}, {erow['area']} · "
                f"criticality **{erow['criticality']}** · OEM {erow['oem']}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Work orders", mi["total_wos"])
    m2.metric("Corrective / emergency", mi["corrective"])
    m3.metric("MTBF (days)", mi["mtbf_days"] or "—")
    m4.metric("Downtime (h)", mi["downtime_h"])
    for f in mi["rca_flags"]:
        st.error("🔁 " + f)
    tl = mi["timeline"]
    if not tl.empty:
        modes = list(tl["mode"].value_counts().index)
        palette = [S1, S2, S3, S4, S5, S6][: len(modes)]
        fig = go.Figure()
        for mode, color in zip(modes, palette):
            sub = tl[tl["mode"] == mode]
            fig.add_trace(go.Scatter(
                x=sub["date"], y=sub["downtime_hours"], mode="markers", name=mode,
                marker=dict(size=11, color=color, line=dict(color=SURFACE, width=2)),
                hovertemplate="%{x|%d %b %Y} · %{y:.1f} h<br>%{customdata}<extra>" + mode + "</extra>",
                customdata=[d[:90] + "…" for d in sub["description"]]))
        fig.update_layout(title=dict(text="Corrective events — downtime hours by failure mode",
                                     font=dict(color=INK, size=15)))
        st.plotly_chart(style(fig), use_container_width=True)
        with st.expander("Full work-order history"):
            st.dataframe(tl[["wo_id", "date", "wo_type", "mode", "description",
                             "downtime_hours", "technician"]], use_container_width=True,
                         hide_index=True)
    else:
        st.info("No corrective history for this asset.")

# ------------------------------------------------------------ compliance radar
elif nav == PAGES[5]:
    st.subheader("Statutory requirements vs inspection evidence — checked continuously")
    counts = gaps["status"].value_counts()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("❌ Missing evidence", int(counts.get("MISSING", 0)))
    c2.metric("🔴 Overdue", int(counts.get("OVERDUE", 0)))
    c3.metric("🟡 Due within 30 days", int(counts.get("DUE SOON", 0)))
    c4.metric("✅ Compliant", int(counts.get("OK", 0)))

    def paint(v):
        return f"color: {STATUS.get(v, INK)}; font-weight: 600" if v in STATUS else ""

    show = gaps.rename(columns={"tag": "Asset", "equipment": "Name", "clause": "Clause",
                                "evidence": "Required evidence", "last_done": "Last done",
                                "due_date": "Due", "status": "Status",
                                "overdue_days": "Days overdue"})
    show["Days overdue"] = show["Days overdue"].map(
        lambda d: "" if d is None or d < 0 or d == 10_000 else str(int(d)))
    st.dataframe(show.style.map(paint, subset=["Status"]),
                 use_container_width=True, hide_index=True, height=520)
    st.caption("Every row is derived live by joining the regulatory library against the "
               "inspection register — the join that NM-2025-021 proved nobody was doing manually.")

# --------------------------------------------------------- real-data benchmark
elif nav == PAGES[6]:
    st.subheader("Measured on real industrial data — not adjectives")
    bench = load_results()
    if bench is None:
        st.warning("Benchmark results not found. Run `python -m src.benchmark` once.")
    else:
        st.markdown(
            f"Entity extraction evaluated on **{bench['corpus']}** — "
            f"{bench['gold_records']:,} expert double-annotated real maintenance work orders "
            f"from mining, rail and heavy industry. Model trained on "
            f"{bench['train_records']:,} records, scored on a held-out "
            f"{bench['test_records']:,} ({bench['test_tokens']:,} tokens).")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Token accuracy", f"{bench['accuracy']:.1%}")
        m2.metric("Macro F1", f"{bench['macro_f1']:.3f}")
        m3.metric("Real MWOs ingested", f"{bench['silver_records'] + bench['gold_records']:,}")
        m4.metric("Real standard pages", sum(1 for c in chunks if c.doc_type == "standard"))

        left, right = st.columns(2)
        with left:
            per = pd.DataFrame(bench["per_class"]).T.reset_index()
            per.columns = ["Entity class", "Precision", "Recall", "F1", "Support (tokens)"]
            st.markdown("**Per-class scores (held-out test set)**")
            st.dataframe(per, hide_index=True, use_container_width=True)
            st.caption("Classifier: windowed lexical features → logistic regression. "
                       "Deliberately simple, fully reproducible, no API dependency — "
                       "the production path swaps in a fine-tuned transformer.")
        with right:
            objs = pd.DataFrame(bench["top_failed_objects"], columns=["object", "mentions"])
            objs = objs.sort_values("mentions").tail(10)
            fig = go.Figure(go.Bar(
                x=objs["mentions"], y=objs["object"], orientation="h", marker_color=AMBER,
                marker=dict(cornerradius=4),
                hovertemplate="%{y}: %{x} mentions<extra></extra>"))
            fig.update_layout(title=dict(
                text="Most-mentioned physical objects across 7,000 real work orders",
                font=dict(color=INK, size=15)))
            st.plotly_chart(style(fig), use_container_width=True)

        st.markdown("**Recurring object–state patterns in the real corpus** — the same "
                    "repeat-failure signal our Risk Echo engine watches for:")
        pairs = pd.DataFrame(bench["top_object_state_pairs"], columns=["Pattern", "Occurrences"])
        st.dataframe(pairs, hide_index=True, use_container_width=True, height=300)
        st.caption("Corpus: MaintIE (Bikaun et al., LREC-COLING 2024), MIT licence, "
                   "github.com/nlp-tlp/maintie · Standards: OISD-STD-116/117 and the "
                   "Factories Act 1948 from official government sources.")
