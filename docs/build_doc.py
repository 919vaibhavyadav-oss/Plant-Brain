"""Build the detailed submission PDF for the ET AI Hackathon portal.

Output: docs/PlantBrain_Submission.pdf
Regenerate after edits with:  python docs/build_doc.py
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (HRFlowable, Image, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "PlantBrain_Submission.pdf")

INK = colors.HexColor("#16191D")
STEEL = colors.HexColor("#44586C")
MUTED = colors.HexColor("#6B7885")
AMBER = colors.HexColor("#B87407")   # darker amber for print contrast
PALE = colors.HexColor("#F2F4F6")
AMBER_TINT = colors.HexColor("#FDF3E0")

TEAM = "Team: __________________"   # filled before submission

S = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, leading=25,
                         textColor=INK, spaceAfter=10, spaceBefore=6),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                         textColor=STEEL, spaceBefore=14, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15,
                           textColor=INK, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10.5, leading=15,
                             textColor=INK, leftIndent=14, bulletIndent=4, spaceAfter=4),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8.5, leading=11.5,
                          textColor=MUTED, spaceAfter=8),
    "stat": ParagraphStyle("stat", fontName="Helvetica-Bold", fontSize=26, leading=30,
                           textColor=AMBER),
}


def deco(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.1 * cm, "PlantBrain - ET AI Hackathon 2026 - Problem Statement 8")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


story = []

# ------------------------------------------------------------------ cover
story.append(Spacer(1, 4.2 * cm))
story.append(Paragraph(
    '<font color="#B87407"><b>ET AI HACKATHON 2026 &nbsp;·&nbsp; PROBLEM STATEMENT 8</b></font>',
    ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=11, alignment=TA_CENTER,
                   spaceAfter=16)))
story.append(Paragraph("PlantBrain",
    ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=42, leading=48,
                   textColor=INK, alignment=TA_CENTER, spaceAfter=10)))
story.append(Paragraph("The Unified Asset &amp; Operations Brain",
    ParagraphStyle("st", fontName="Helvetica", fontSize=17, textColor=STEEL,
                   alignment=TA_CENTER, spaceAfter=22)))
story.append(Paragraph(
    "AI for Industrial Knowledge Intelligence — one intelligence layer over every plant "
    "document, validated on 8,076 real maintenance work orders and official Indian regulatory "
    "standards.",
    ParagraphStyle("tag", fontName="Helvetica", fontSize=11.5, leading=16, textColor=MUTED,
                   alignment=TA_CENTER, spaceAfter=30)))
story.append(Paragraph(TEAM,
    ParagraphStyle("team", fontName="Helvetica-Bold", fontSize=12, textColor=INK,
                   alignment=TA_CENTER, spaceAfter=6)))
story.append(Paragraph("July 2026",
    ParagraphStyle("date", fontName="Helvetica", fontSize=10, textColor=MUTED,
                   alignment=TA_CENTER)))
story.append(PageBreak())

# ------------------------------------------------------- 1 exec summary
story.append(Paragraph("1. Executive Summary", S["h1"]))
story.append(Paragraph(
    "Indian heavy industry does not have a data problem — it has a memory problem. "
    "Professionals in asset-intensive industries spend 35% of working hours searching for "
    "information that already exists (McKinsey, 2024); the average large Indian plant runs "
    "7–12 disconnected document systems (NASSCOM-EY); fragmented equipment history "
    "contributes to 18–22% of unplanned downtime (BIS Research); and 25% of India's "
    "experienced industrial engineers retire within the decade, taking undocumented knowledge "
    "with them.", S["body"]))
story.append(Paragraph(
    "<b>PlantBrain</b> is an AI platform that ingests every operational document a plant has "
    "— CMMS work orders, inspection registers, incident reports, SOPs, and regulatory "
    "standards — into one queryable, continuously watching intelligence layer. Four agents "
    "operate on that layer: an Expert Copilot that answers any operational question with "
    "citations; a Compliance Radar that continuously joins statutory requirements against "
    "inspection evidence; Maintenance Intelligence that detects repeat-failure patterns; and a "
    "Risk Echo engine — our core innovation — that raises an alert when the conditions "
    "that preceded a past incident become active again.", S["body"]))
story.append(Paragraph(
    "Unlike typical document chatbots, every claim is measured: entity extraction scores "
    "<b>94.8% token accuracy (0.909 macro-F1)</b> on held-out, expert double-annotated real "
    "work orders from the published MaintIE benchmark, and the working prototype ingests 8,076 "
    "real field work orders plus the official OISD-STD-116 standard and the Factories Act 1948.",
    S["body"]))

# ------------------------------------------------------- 2 problem
story.append(Paragraph("2. The Problem", S["h1"]))
t = Table([
    ["35%", "7–12", "18–22%", "25%"],
    ["of engineer hours spent\nhunting for information\n(McKinsey 2024)",
     "disconnected document\nsystems per large plant\n(NASSCOM-EY)",
     "of unplanned downtime tied\nto fragmented history\n(BIS Research)",
     "of experienced engineers\nretiring this decade\n(Problem Statement 8)"],
], colWidths=[4.2 * cm] * 4, rowHeights=[1.5 * cm, 2.1 * cm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 22),
    ("LEADING", (0, 0), (-1, 0), 24),
    ("TEXTCOLOR", (0, 0), (-1, 0), AMBER),
    ("FONTSIZE", (0, 1), (-1, 1), 8.5),
    ("LEADING", (0, 1), (-1, 1), 11),
    ("TEXTCOLOR", (0, 1), (-1, 1), INK),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("INNERGRID", (0, 0), (-1, -1), 1.2, colors.white),
]))
story.append(t)
story.append(Spacer(1, 0.35 * cm))
story.append(Paragraph(
    "Knowledge fragmentation is not a file-management inconvenience. The incident record of "
    "Indian heavy industry shows the same pattern repeatedly: the information needed to prevent "
    "a failure existed — in a maintenance log, a lab spreadsheet, a contractor PDF — "
    "but nobody could see it at the moment of decision. It is a safety problem, a statutory "
    "compliance problem, and an operational efficiency problem, and it compounds every year.",
    S["body"]))

# ------------------------------------------------------- 3 solution
story.append(Paragraph("3. The Solution: Four Agents on One Knowledge Layer", S["h1"]))
story.extend(bullets([
    "<b>Expert Copilot</b> — ask the plant anything. GraphRAG-lite retrieval over 8,540 "
    "unified records; answers synthesized by an LLM (Groq, llama-3.3-70b) strictly constrained "
    "to retrieved context, with an automatic extractive fallback if the API is unavailable. "
    "Every claim cites an openable source record; knowledge-graph-sourced citations are "
    "visibly badged.",
    "<b>Risk Echo Engine</b> — cross-references every historical incident's assets against "
    "currently live risk signals (overdue statutory evidence, repeat-failure patterns) and "
    "raises cited warnings <i>before the repeat</i>. This is the layer that turns an incident "
    "archive into a prevention system.",
    "<b>Compliance Radar</b> — a continuous join of the regulatory library (OISD, "
    "Factories Act, IBR, PESO, CEA) against the inspection register: applicability × "
    "required frequency × evidence. Found 8 live statutory gaps in the demo plant.",
    "<b>Maintenance Intelligence</b> — per-asset MTBF, failure-mode patterns, downtime "
    "and automatic repeat-failure RCA triggers: nine identical seal failures on one pump is a "
    "process failure, not bad luck.",
]))
story.append(Paragraph(
    "The flagship scenario: transformer TR-501 had a Buchholz-alarm near-miss in December 2025 "
    "because the dissolved-gas analysis on file was three months stale. In July 2026 the same "
    "180-day statutory test is overdue again — it lives in the electrical lab's "
    "spreadsheet, and nobody has noticed. PlantBrain raises the Risk Echo automatically, citing "
    "both the incident report and the live compliance state. A prevented transformer failure is "
    "worth Rs 8–15 crore before counting the outage.", S["body"]))

# ------------------------------------------------------- 4 architecture
story.append(Paragraph("4. Architecture", S["h1"]))
arch_png = os.path.join(ROOT, "deck", "qa", "slide-07.png")
if os.path.exists(arch_png):
    story.append(Image(arch_png, width=16.4 * cm, height=9.22 * cm))
    story.append(Paragraph("Figure 1 — end-to-end architecture of the working prototype.",
                           S["cap"]))
story.extend(bullets([
    "<b>Universal ingestion:</b> every record from every source — a CMMS row, a real "
    "MaintIE field work order, a page of the official OISD-STD-116 PDF, a section of an "
    "incident report — becomes one chunk schema with extracted entities (equipment tags, "
    "regulatory clause references, dates). Downstream agents never care where a fact came from.",
    "<b>Auto-derived knowledge graph:</b> every edge (equipment–document, clause–asset, "
    "incident–SOP) comes from entity extraction at ingest time — no manual curation, "
    "which is the property that makes adoption realistic.",
    "<b>GraphRAG-lite retrieval</b> (after Document GraphRAG, <i>Electronics</i> 2025; "
    "FDRKG-LLM, <i>Int'l J. Production Research</i> 2025): vector hits are expanded with 1-hop "
    "graph neighbours of the assets they mention, so structurally related documents surface "
    "with zero term overlap. Entity-aware ranking boosts records of any asset named in the "
    "query; narrative documents reach the LLM in full so a root cause is never lost below a "
    "matched summary section.",
    "<b>Offline-first:</b> retrieval, citations, and all four agents work with no API at all; "
    "an available LLM upgrades synthesis quality. A failed API call falls back silently. The "
    "demo cannot be broken by connectivity.",
]))

# ------------------------------------------------------- 5 validation
story.append(Paragraph("5. Measured on Real Industrial Data", S["h1"]))
story.append(Paragraph(
    "The Problem Statement 8 evaluation focus asks for entity-extraction accuracy across "
    "document types, ideally validated with real industrial document samples. We validate "
    "against <b>MaintIE</b> (Bikaun et al., LREC-COLING 2024, MIT licence): 1,076 expert "
    "double-annotated real maintenance work orders from mining, rail and heavy industry. Our "
    "extractor trains on 860 records and is scored on a held-out 216 (1,222 tokens):", S["body"]))
bt = Table([
    ["Entity class", "Precision", "Recall", "F1", "Support (tokens)"],
    ["PhysicalObject", "0.94", "0.98", "0.96", "475"],
    ["Activity", "0.95", "0.94", "0.95", "187"],
    ["Process", "0.96", "0.85", "0.90", "26"],
    ["State", "0.93", "0.80", "0.86", "98"],
    ["Property", "1.00", "0.71", "0.83", "7"],
    ["Overall", "token accuracy 94.8%", "", "macro-F1 0.909", "1,222"],
], colWidths=[4.2 * cm, 3.2 * cm, 2.6 * cm, 3.4 * cm, 3.4 * cm])
bt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("BACKGROUND", (0, 0), (-1, 0), STEEL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("BACKGROUND", (0, -1), (-1, -1), AMBER_TINT),
    ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, PALE]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4DAE0")),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(bt)
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "The classifier is deliberately simple (windowed lexical features → logistic "
    "regression) so the result is reproducible with one command and no API dependency; the "
    "production path swaps in a fine-tuned transformer on the same schema. Beyond the "
    "benchmark, the prototype ingests all 8,076 real MaintIE work orders and 142 pages of "
    "official regulatory documents (OISD-STD-116, OISD-STD-117 amendment, Factories Act 1948), "
    "so copilot answers about fire-protection requirements cite actual standard pages with "
    "actual design values.", S["body"]))
story.append(PageBreak())

# ------------------------------------------------------- 6 innovation
story.append(Paragraph("6. Innovation and Differentiation", S["h1"]))
story.extend(bullets([
    "<b>Risk echoes are the innovation.</b> Document chatbots answer questions someone thinks "
    "to ask. PlantBrain connects records nobody reads together — an incident report from "
    "December and an inspection register row from today — and speaks up unprompted.",
    "<b>Peer-reviewed architecture:</b> knowledge-graph-enhanced RAG outperforms plain RAG on "
    "industrial fault reasoning (Document GraphRAG, <i>Electronics</i> 2025; FDRKG-LLM, "
    "<i>IJPR</i> 2025). PlantBrain implements exactly this pattern, lightweight.",
    "<b>Category validated at billion-dollar scale:</b> Schneider Electric is acquiring "
    "Cognite (~$170M ARR industrial knowledge graphs); Siemens ships an Industrial Copilot "
    "reporting ~25% reactive-maintenance savings in pilots.",
    "<b>The open wedge:</b> those platforms are multi-year deployments priced for global "
    "majors, and none ships an Indian regulatory brain. PlantBrain is document-native — "
    "it deploys on the file shares and registers a plant already has — and "
    "compliance-first, with OISD / Factories Act / IBR / PESO / CEA built in. Land with the "
    "Compliance Radar's auditable ROI, expand to the full knowledge layer.",
]))

# ------------------------------------------------------- 7 scalability
story.append(Paragraph("7. Scalability and Roadmap", S["h1"]))
rt = Table([
    ["Prototype (today)", "Production path"],
    ["TF-IDF + type/entity boosts", "Embedding model + vector DB, hybrid BM25+dense"],
    ["NetworkX in-memory graph", "Neo4j with industrial ontology (ISO 14224)"],
    ["Logistic-regression NER (benchmarked)", "Transformer NER fine-tuned on the same MaintIE schema"],
    ["CSV / Markdown / PDF loaders", "SAP PM / Maximo connectors, OCR, email archives"],
    ["Page-level PDF chunks", "Layout-aware parsing + P&ID vision (cf. TCS Digitize-PID)"],
    ["Streamlit console", "Role-based web + mobile for field technicians"],
], colWidths=[7.6 * cm, 9.2 * cm])
rt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("BACKGROUND", (0, 0), (-1, 0), STEEL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4DAE0")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(rt)
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "Every layer sits behind an interface chosen for swappability: the engines upgrade, the "
    "system design does not change. One deployment pattern serves steel, refining, power, "
    "cement and mining.", S["body"]))

# ------------------------------------------------------- 8 tech + eval map
story.append(Paragraph("8. Technology Stack and How to Run", S["h1"]))
story.append(Paragraph(
    "Python 3.13 · Streamlit · scikit-learn · NetworkX · Plotly · "
    "pdfplumber · Groq LLM API (llama-3.3-70b-versatile) with automatic offline fallback. "
    "Setup and run instructions are in the repository README; the benchmark regenerates with "
    "<font face=\"Courier\">python -m src.benchmark</font>.", S["body"]))
story.append(Paragraph("Mapping to the stated evaluation focus", S["h2"]))
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=12, textColor=INK)
hcell = ParagraphStyle("hcell", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
                       textColor=colors.white)
et_rows = [
    ["Evaluation focus item", "Where PlantBrain delivers it"],
    ["Entity extraction accuracy across document types",
     "94.8% / 0.909 macro-F1 on MaintIE gold; per-class table in-app"],
    ["Query answer quality on domain benchmark questions",
     "Copilot with cited, context-constrained answers over 8,540 records"],
    ["Knowledge graph linkage completeness",
     "54-node auto-derived graph; graph-sourced citations badged in every answer"],
    ["Time-to-answer versus traditional search",
     "Seconds versus the 35%-of-hours baseline; live in the demo"],
    ["Compliance gap detection accuracy",
     "8 planted statutory gaps found (OISD/CEA/Factories Act), zero false compliant"],
    ["Validation with real industrial document samples",
     "8,076 real MWOs + official OISD-STD-116 + Factories Act 1948 ingested"],
]
et = Table([[Paragraph(a, hcell if i == 0 else cell),
             Paragraph(b, hcell if i == 0 else cell)]
            for i, (a, b) in enumerate(et_rows)],
           colWidths=[7.6 * cm, 9.2 * cm])
et.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("BACKGROUND", (0, 0), (-1, 0), STEEL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4DAE0")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(et)
story.append(Spacer(1, 0.5 * cm))
story.append(HRFlowable(width="100%", color=colors.HexColor("#D4DAE0"), thickness=0.7))
story.append(Spacer(1, 0.25 * cm))
story.append(Paragraph(
    "Data notes: the demo plant (Bharat Ispat & Energy Ltd, Unit 2) is fictional and generated; "
    "the MaintIE corpus is MIT-licensed; OISD documents were obtained from oisd.gov.in and are "
    "used for local demonstration only, not redistributed. All third-party sources are credited "
    "in the repository.", S["cap"]))

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=1.9 * cm, bottomMargin=1.9 * cm,
                        leftMargin=2 * cm, rightMargin=2 * cm,
                        title="PlantBrain - ET AI Hackathon 2026 Submission",
                        author="PlantBrain team")
doc.build(story, onFirstPage=deco, onLaterPages=deco)
print("written:", OUT)
