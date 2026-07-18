/* PlantBrain pitch deck — ET AI Hackathon 2026, Problem #8 */
const pptxgen = require("pptxgenjs");

const DARK = "1F262E";      // gunmetal — title & close
const CARD_DARK = "2B3440"; // card on dark
const STEEL = "44586C";     // supporting steel blue
const INK = "16191D";       // body text on light
const MUTED = "6B7885";     // captions
const PALE = "F2F4F6";      // card fill on light
const WHITE = "FFFFFF";
const AMBER = "E8960C";     // hard-hat amber accent
const AMBER_TINT = "FDF3E0";
const RED = "C0392B";
const GREEN = "2E7D32";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
const W = 13.333;

const F = "Arial";

function footer(s, n) {
  s.addText("PlantBrain · ET AI Hackathon 2026", {
    x: 0.55, y: 7.08, w: 4, h: 0.3, fontFace: F, fontSize: 9, color: MUTED, margin: 0,
  });
  s.addText(String(n), {
    x: W - 1.0, y: 7.08, w: 0.5, h: 0.3, fontFace: F, fontSize: 9, color: MUTED,
    align: "right", margin: 0,
  });
}

function title(s, text, opts = {}) {
  s.addText(text, {
    x: 0.55, y: 0.42, w: W - 1.1, h: 0.85, fontFace: F, fontSize: 31, bold: true,
    color: opts.color || INK, margin: 0,
  });
}

function chip(s, x, y, label, fill) {
  s.addShape("ellipse", { x, y, w: 0.52, h: 0.52, fill: { color: fill || AMBER } });
  s.addText(label, {
    x, y, w: 0.52, h: 0.52, fontFace: F, fontSize: 15, bold: true, color: WHITE,
    align: "center", valign: "middle", margin: 0,
  });
}

/* ---------------------------------------------------------- 1 · title */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("ET AI HACKATHON 2026  ·  PROBLEM #8  ·  INDUSTRIAL KNOWLEDGE INTELLIGENCE", {
    x: 0, y: 1.35, w: W, h: 0.4, fontFace: F, fontSize: 13, color: AMBER, bold: true,
    align: "center", charSpacing: 2, margin: 0,
  });
  s.addText("PlantBrain", {
    x: 0, y: 2.15, w: W, h: 1.3, fontFace: F, fontSize: 66, bold: true, color: WHITE,
    align: "center", margin: 0,
  });
  s.addText("The Unified Asset & Operations Brain", {
    x: 0, y: 3.5, w: W, h: 0.6, fontFace: F, fontSize: 24, color: "C9D4DE",
    align: "center", margin: 0,
  });
  s.addText(
    "One intelligence layer over every plant document — validated on 8,076 real work orders and official Indian standards",
    { x: 1.8, y: 4.35, w: W - 3.6, h: 0.7, fontFace: F, fontSize: 15, color: "8FA0B0",
      align: "center", margin: 0 });
  s.addShape("roundRect", { x: 4.87, y: 5.35, w: 3.6, h: 0.62, rectRadius: 0.31,
    fill: { color: CARD_DARK }, line: { color: AMBER, width: 1 } });
  s.addText("Live working prototype inside", {
    x: 4.87, y: 5.35, w: 3.6, h: 0.62, fontFace: F, fontSize: 13.5, bold: true,
    color: AMBER, align: "center", valign: "middle", margin: 0 });
  s.addText("Team Aero Flash  —  Vaibhav  ·  Subham Kumar", {
    x: 0, y: 6.35, w: W, h: 0.4, fontFace: F, fontSize: 14, bold: true,
    color: "C9D4DE", align: "center", margin: 0 });
  s.addNotes("Open with the hook: Indian heavy industry doesn't have a data problem — it has a memory problem. We built the layer that ends it, and we validated it on real industrial data.");
}

/* ------------------------------------------------------- 2 · problem */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Plants don't have a data problem. They have a memory problem.");
  const stats = [
    ["35%", "of engineers' working hours spent hunting for information that already exists", "McKinsey global survey, 2024"],
    ["7–12", "disconnected document systems inside a single large Indian plant", "NASSCOM-EY manufacturing study"],
    ["18–22%", "of unplanned downtime events tied to decisions made without complete equipment history", "BIS Research"],
    ["25%", "of India's experienced industrial engineers retire within a decade — knowledge goes with them", "Problem statement #8"],
  ];
  stats.forEach((st, i) => {
    const x = 0.55 + i * 3.11;
    s.addShape("roundRect", { x, y: 1.75, w: 2.86, h: 3.6, rectRadius: 0.09,
      fill: { color: PALE } });
    s.addText(st[0], { x: x + 0.22, y: 2.0, w: 2.42, h: 0.95, fontFace: F, fontSize: 40,
      bold: true, color: AMBER, margin: 0 });
    s.addText(st[1], { x: x + 0.22, y: 3.0, w: 2.42, h: 1.7, fontFace: F, fontSize: 12.5,
      color: INK, margin: 0 });
    s.addText(st[2], { x: x + 0.22, y: 4.85, w: 2.42, h: 0.4, fontFace: F, fontSize: 9.5,
      italic: true, color: MUTED, margin: 0 });
  });
  s.addText(
    "Fragmented knowledge is not a filing problem. It is a safety problem, a compliance problem, and a downtime problem — and it compounds every year.",
    { x: 0.55, y: 5.75, w: W - 1.1, h: 0.8, fontFace: F, fontSize: 16, italic: true,
      color: STEEL, margin: 0 });
  footer(s, 2);
  s.addNotes("Each number is from the hackathon problem statement's own sources — judges recognise them. Land the last line: it compounds.");
}

/* ------------------------------------------------------- 3 · insight */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "The insight: connect what nobody reads together");
  // left flow
  s.addShape("roundRect", { x: 0.55, y: 1.7, w: 5.4, h: 1.25, rectRadius: 0.09,
    fill: { color: PALE }, line: { color: RED, width: 1.25 } });
  s.addText([
    { text: "PAST INCIDENT — Dec 2025", options: { bold: true, color: RED, fontSize: 12.5, breakLine: true } },
    { text: "TR-501 transformer Buchholz near-miss: the oil test needed for the call was 3 months stale", options: { color: INK, fontSize: 12.5 } },
  ], { x: 0.8, y: 1.85, w: 4.95, h: 1.0, fontFace: F, margin: 0 });
  s.addShape("roundRect", { x: 0.55, y: 3.15, w: 5.4, h: 1.25, rectRadius: 0.09,
    fill: { color: PALE }, line: { color: AMBER, width: 1.25 } });
  s.addText([
    { text: "LIVE CONDITION — today", options: { bold: true, color: AMBER, fontSize: 12.5, breakLine: true } },
    { text: "The same statutory DGA test is overdue again — 140 days past due in the inspection register", options: { color: INK, fontSize: 12.5 } },
  ], { x: 0.8, y: 3.3, w: 4.95, h: 1.0, fontFace: F, margin: 0 });
  s.addShape("downArrow", { x: 2.95, y: 4.5, w: 0.6, h: 0.55, fill: { color: STEEL } });
  s.addShape("roundRect", { x: 0.55, y: 5.15, w: 5.4, h: 1.35, rectRadius: 0.09,
    fill: { color: AMBER } });
  s.addText([
    { text: "RISK ECHO — raised automatically", options: { bold: true, color: WHITE, fontSize: 13.5, breakLine: true } },
    { text: "The condition that caused the last incident is active again — with both records cited", options: { color: WHITE, fontSize: 12.5 } },
  ], { x: 0.8, y: 5.32, w: 4.95, h: 1.05, fontFace: F, margin: 0 });
  // right text
  s.addText([
    { text: "Everyone builds chatbots over documents.", options: { fontSize: 17, bold: true, color: INK, breakLine: true, paraSpaceAfter: 10 } },
    { text: "The value isn't answering questions — it's connecting records nobody reads together. A near-miss report from December and an inspection register row from today live in different systems, owned by different teams. Only a machine reads both.", options: { fontSize: 14.5, color: INK, breakLine: true, paraSpaceAfter: 14 } },
    { text: "Peer-reviewed backing", options: { fontSize: 13, bold: true, color: STEEL, breakLine: true, paraSpaceAfter: 6 } },
    { text: "Knowledge-graph-enhanced RAG outperforms plain RAG on industrial fault reasoning — Document GraphRAG (Electronics, 2025); FDRKG-LLM (Int'l J. Production Research, 2025). PlantBrain implements exactly this architecture.", options: { fontSize: 12, italic: true, color: MUTED } },
  ], { x: 6.55, y: 1.75, w: 6.2, h: 4.8, fontFace: F, margin: 0 });
  footer(s, 3);
  s.addNotes("This is the innovation claim: risk echoes. Chatbots answer; we connect. Cite the two 2025 papers verbally only if asked.");
}

/* ---------------------------------------------- 4 · real data numbers */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Measured on real industrial data — not adjectives");
  s.addChart("bar", [{
    name: "F1",
    labels: ["PhysicalObject", "Activity", "Process", "State", "Property"],
    values: [0.96, 0.95, 0.90, 0.86, 0.83],
  }], {
    x: 0.55, y: 1.8, w: 6.6, h: 4.4,
    barDir: "col",
    chartColors: [AMBER],
    showTitle: true, title: "Entity extraction F1 by class — held-out expert test set",
    titleFontSize: 13, titleColor: INK, titleFontFace: F,
    showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 11,
    dataLabelColor: INK, dataLabelFontFace: F, dataLabelFormatCode: "0.00",
    valAxisMaxVal: 1, valAxisMinVal: 0,
    catAxisLabelColor: MUTED, catAxisLabelFontSize: 10.5, catAxisLabelFontFace: F,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10, valAxisLabelFontFace: F,
    valGridLine: { color: "E3E6EA", size: 0.75 }, catGridLine: { style: "none" },
  });
  const facts = [
    ["94.8%", "token accuracy on 1,222 held-out tokens (macro-F1 0.909)"],
    ["8,076", "real maintenance work orders ingested — mining, rail, heavy industry (MaintIE corpus)"],
    ["142", "pages of official regulatory documents ingested: OISD-STD-116 and the Factories Act 1948"],
  ];
  facts.forEach((f0, i) => {
    const y = 1.8 + i * 1.5;
    s.addShape("roundRect", { x: 7.55, y, w: 5.2, h: 1.32, rectRadius: 0.09,
      fill: { color: i === 0 ? AMBER_TINT : PALE } });
    s.addText(f0[0], { x: 7.8, y: y + 0.14, w: 1.7, h: 1.0, fontFace: F, fontSize: 30,
      bold: true, color: AMBER, valign: "middle", margin: 0 });
    s.addText(f0[1], { x: 9.55, y: y + 0.12, w: 3.05, h: 1.1, fontFace: F, fontSize: 11.5,
      color: INK, valign: "middle", margin: 0 });
  });
  s.addText("Benchmark: MaintIE — 1,076 expert double-annotated work orders (Bikaun et al., LREC-COLING 2024, MIT licence). Trained on 860, scored on 216. Reproducible with one command.",
    { x: 0.55, y: 6.35, w: W - 1.1, h: 0.55, fontFace: F, fontSize: 10.5, italic: true,
      color: MUTED, margin: 0 });
  footer(s, 4);
  s.addNotes("Key line: 'We don't say high accuracy. We say 94.8% on held-out expert-annotated real work orders, per class, reproducible.' The evaluation focus for this problem asks for exactly this validation.");
}

/* -------------------------------------------------------- 5 · product */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Four agents on one knowledge layer");
  const cards = [
    ["EC", "Expert Copilot", "Ask the plant anything. GraphRAG-lite retrieval over 8,540 records; answers synthesized by LLM (Groq) strictly from retrieved context — with automatic offline fallback. Every claim cites an openable record."],
    ["RE", "Risk Echo Engine", "Cross-references every historical incident's assets against live conditions — overdue statutory evidence, repeat-failure patterns — and raises cited warnings before the repeat."],
    ["CR", "Compliance Radar", "Continuous join of the regulatory library (OISD · Factories Act · IBR · PESO · CEA) against inspection evidence. 8 live statutory gaps found in the demo plant."],
    ["MI", "Maintenance Intelligence", "Per-asset MTBF, failure-mode patterns and downtime. Repeat-failure RCA triggers fire automatically — nine identical seal failures on one pump is a process failure, not bad luck."],
  ];
  cards.forEach((c, i) => {
    const x = 0.55 + (i % 2) * 6.24, y = 1.7 + Math.floor(i / 2) * 2.42;
    s.addShape("roundRect", { x, y, w: 5.98, h: 2.2, rectRadius: 0.09, fill: { color: PALE } });
    chip(s, x + 0.28, y + 0.28, c[0]);
    s.addText(c[1], { x: x + 1.0, y: y + 0.26, w: 4.7, h: 0.55, fontFace: F, fontSize: 16.5,
      bold: true, color: INK, valign: "middle", margin: 0 });
    s.addText(c[2], { x: x + 0.3, y: y + 0.95, w: 5.4, h: 1.15, fontFace: F, fontSize: 11.5,
      color: INK, margin: 0 });
  });
  s.addText("Auditability by construction: no answer without a source the user can open. Graph-sourced citations are visibly badged.",
    { x: 0.55, y: 6.35, w: W - 1.1, h: 0.5, fontFace: F, fontSize: 12.5, italic: true,
      color: STEEL, margin: 0 });
  footer(s, 5);
  s.addNotes("Point at the screen for each agent, then segue to the live demo. The four agents share one ingestion layer and one knowledge graph — that's the architecture story.");
}

/* ---------------------------------------------------- 6 · demo moment */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "One alert pays for the product");
  const nodes = [
    [RED, "DEC 2025", "TR-501 Buchholz alarm. Decision needed — but the oil test on file is 3 months stale. Precautionary shutdown, load restriction."],
    [AMBER, "JUL 2026", "The same 180-day DGA test is overdue again. Nobody has noticed — it lives in the electrical lab's spreadsheet."],
    [GREEN, "PLANTBRAIN", "Risk Echo raised automatically: incident record + live compliance state, both cited. Test ordered before the next alarm."],
  ];
  nodes.forEach((n, i) => {
    const x = 0.55 + i * 4.36;
    s.addShape("ellipse", { x: x + 1.62, y: 1.75, w: 0.85, h: 0.85, fill: { color: n[0] } });
    s.addText(String(i + 1), { x: x + 1.62, y: 1.75, w: 0.85, h: 0.85, fontFace: F,
      fontSize: 22, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    if (i < 2) s.addShape("rightArrow", { x: x + 3.3, y: 2.02, w: 1.35, h: 0.32,
      fill: { color: "D4DAE0" } });
    s.addText(n[1], { x, y: 2.8, w: 4.1, h: 0.4, fontFace: F, fontSize: 14, bold: true,
      color: n[0], align: "center", margin: 0 });
    s.addText(n[2], { x: x + 0.15, y: 3.25, w: 3.8, h: 1.5, fontFace: F, fontSize: 12,
      color: INK, align: "center", margin: 0 });
  });
  s.addShape("roundRect", { x: 0.55, y: 5.0, w: 7.35, h: 1.7, rectRadius: 0.09,
    fill: { color: AMBER_TINT } });
  s.addText([
    { text: "₹8–15 crore", options: { fontSize: 34, bold: true, color: AMBER, breakLine: true } },
    { text: "typical cost of one failed power transformer — before counting the outage", options: { fontSize: 12.5, color: INK } },
  ], { x: 0.85, y: 5.2, w: 6.8, h: 1.3, fontFace: F, margin: 0 });
  s.addText([
    { text: "Benchmark for the category:", options: { fontSize: 12, bold: true, color: STEEL, breakLine: true, paraSpaceAfter: 4 } },
    { text: "Siemens' comparable maintenance copilot reports ~25% reactive-maintenance time savings in pilots — and it doesn't watch for incident recurrence at all.", options: { fontSize: 11.5, color: MUTED } },
  ], { x: 8.25, y: 5.05, w: 4.5, h: 1.6, fontFace: F, margin: 0 });
  footer(s, 6);
  s.addNotes("This is the Business Impact slide (25% of score). One prevented transformer failure pays for years of the product. Then show it live in the app.");
}

/* --------------------------------------------------- 7 · architecture */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "Architecture: document-native by design");
  const boxes = [
    ["7 source types", "CMMS · inspections · incidents · SOPs · clause library · real OISD / Factories Act PDFs · 8,076 real field MWOs"],
    ["Universal ingestion", "One chunk schema for every record. Entity extraction benchmarked at 94.8% on MaintIE gold"],
    ["Knowledge layer", "Auto-derived knowledge graph + vector index with entity-aware, doc-type-boosted ranking"],
    ["Four agents", "GraphRAG-lite retrieval · LLM synthesis (Groq) constrained to context · automatic offline fallback"],
    ["Operations console", "7 views: overview, risk echoes, copilot, graph, maintenance, compliance, benchmark"],
  ];
  boxes.forEach((b, i) => {
    const x = 0.45 + i * 2.56;
    s.addShape("roundRect", { x, y: 2.1, w: 2.32, h: 2.9, rectRadius: 0.09,
      fill: { color: i === 3 ? AMBER_TINT : PALE },
      line: i === 3 ? { color: AMBER, width: 1.25 } : undefined });
    s.addText(b[0], { x: x + 0.16, y: 2.3, w: 2.0, h: 0.75, fontFace: F, fontSize: 13.5,
      bold: true, color: INK, margin: 0 });
    s.addText(b[1], { x: x + 0.16, y: 3.05, w: 2.0, h: 1.8, fontFace: F, fontSize: 10.5,
      color: i === 3 ? INK : MUTED, margin: 0 });
    if (i < 4) s.addShape("rightArrow", { x: x + 2.3, y: 3.38, w: 0.28, h: 0.26,
      fill: { color: STEEL } });
  });
  const chips = [
    "Offline-first — the demo cannot die on stage",
    "Every answer cites an openable record",
    "Production-swappable: Neo4j · embeddings · transformer NER",
  ];
  chips.forEach((c, i) => {
    const x = 0.55 + i * 4.28;
    s.addShape("roundRect", { x, y: 5.65, w: 4.0, h: 0.75, rectRadius: 0.37,
      fill: { color: WHITE }, line: { color: STEEL, width: 1 } });
    s.addText(c, { x: x + 0.18, y: 5.65, w: 3.64, h: 0.75, fontFace: F, fontSize: 11,
      color: STEEL, align: "center", valign: "middle", margin: 0 });
  });
  footer(s, 7);
  s.addNotes("30 seconds max. The one technical claim to land: everything downstream of ingestion is source-agnostic — point it at a real plant's exports and nothing changes.");
}

/* --------------------------------------------------------- 8 · market */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "A validated category — and an open wedge");
  s.addShape("roundRect", { x: 0.55, y: 1.75, w: 6.0, h: 4.35, rectRadius: 0.09,
    fill: { color: PALE } });
  s.addText([
    { text: "The majors prove the market", options: { fontSize: 17, bold: true, color: INK, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Schneider Electric is acquiring Cognite — the industrial knowledge-graph company, ~$170M ARR.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Siemens ships an Industrial Copilot for maintenance — ~25% reactive-time savings in pilots.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Both are multi-year platform deployments priced for global majors.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 14 } },
    { text: "The NASSCOM-EY plants running on 7–12 disconnected systems cannot buy either.", options: { fontSize: 13.5, italic: true, color: STEEL } },
  ], { x: 0.9, y: 2.0, w: 5.3, h: 3.9, fontFace: F, margin: 0 });
  s.addShape("roundRect", { x: 6.85, y: 1.75, w: 5.95, h: 4.35, rectRadius: 0.09,
    fill: { color: AMBER_TINT }, line: { color: AMBER, width: 1.25 } });
  s.addText([
    { text: "PlantBrain's wedge", options: { fontSize: 17, bold: true, color: INK, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Document-native: deploys on the file shares and registers a plant already has — no DataOps programme first.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Compliance-first: an Indian regulatory brain — OISD, Factories Act, IBR, PESO, CEA — that no global platform ships.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Risk echoes: incident history × live compliance state. Neither incumbent leads with it.", options: { fontSize: 13, color: INK, bullet: true, breakLine: true, paraSpaceAfter: 14 } },
    { text: "Land with the Compliance Radar — auditable ROI — then expand to the full knowledge layer.", options: { fontSize: 13.5, bold: true, color: AMBER } },
  ], { x: 7.2, y: 2.0, w: 5.25, h: 3.9, fontFace: F, margin: 0 });
  footer(s, 8);
  s.addNotes("Anticipate 'doesn't Cognite do this?' head-on: they validate the category and serve a different buyer. Our wedge is the mid-market Indian plant and the regulatory brain.");
}

/* -------------------------------------------------------- 9 · roadmap */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, "From prototype to plant floor");
  const steps = [
    ["1", "Connectors", "SAP PM / Maximo work-order sync; OCR pipeline for scanned registers and email archives"],
    ["2", "Transformer NER", "Fine-tuned on the MaintIE schema we already benchmark against — the training path is proven"],
    ["3", "P&ID vision", "Drawing digitisation into the knowledge graph, building on published methods (Digitize-PID — TCS Research)"],
    ["4", "Scale stack", "Neo4j + vector DB behind the same interfaces; role-based web and mobile for field technicians"],
  ];
  steps.forEach((st, i) => {
    const x = 0.55 + i * 3.11;
    s.addShape("roundRect", { x, y: 1.9, w: 2.86, h: 3.5, rectRadius: 0.09,
      fill: { color: PALE } });
    chip(s, x + 0.24, y = 2.14, st[0]);
    s.addText(st[1], { x: x + 0.92, y: 2.14, w: 1.85, h: 0.52, fontFace: F, fontSize: 15.5,
      bold: true, color: INK, valign: "middle", margin: 0 });
    s.addText(st[2], { x: x + 0.26, y: 2.85, w: 2.36, h: 2.4, fontFace: F, fontSize: 12,
      color: INK, margin: 0 });
  });
  s.addText("Every layer of the prototype was chosen to be swappable — the interfaces stay, the engines upgrade.",
    { x: 0.55, y: 5.75, w: W - 1.1, h: 0.5, fontFace: F, fontSize: 13, italic: true,
      color: STEEL, margin: 0 });
  footer(s, 9);
  s.addNotes("Scalability is 15% of score. The message: nothing here is a rewrite — each upgrade slots behind an existing interface.");
}

/* --------------------------------------------------------- 10 · close */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText(
    "\"Every plant already paid for this knowledge — in downtime, in audits, sometimes in lives.\"",
    { x: 1.3, y: 2.0, w: W - 2.6, h: 1.6, fontFace: F, fontSize: 30, bold: true,
      color: WHITE, align: "center", margin: 0 });
  s.addText("PlantBrain makes it impossible to lose.", {
    x: 1.3, y: 3.75, w: W - 2.6, h: 0.7, fontFace: F, fontSize: 22, color: AMBER,
    align: "center", margin: 0 });
  s.addText("Team Aero Flash  —  Vaibhav  ·  Subham Kumar", {
    x: 0, y: 5.35, w: W, h: 0.4, fontFace: F, fontSize: 15, bold: true, color: "C9D4DE",
    align: "center", margin: 0 });
  s.addText("PlantBrain  ·  live demo available  ·  built for ET AI Hackathon 2026", {
    x: 0, y: 5.85, w: W, h: 0.4, fontFace: F, fontSize: 12.5, color: "8FA0B0",
    align: "center", margin: 0 });
  s.addNotes("Close on the quote, invite questions, offer the live demo again.");
}

pres.writeFile({ fileName: "PlantBrain_Pitch.pptx" }).then(() => console.log("written"));
