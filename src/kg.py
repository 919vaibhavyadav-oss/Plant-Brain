"""Knowledge graph construction.

Nodes: equipment, areas, documents (WOs collapsed per equipment to keep the
graph readable), incidents, SOPs, regulatory clauses.
Edges carry relationship labels so the graph answers "what is connected to
this asset" — the question fragmented systems cannot answer.
"""
import networkx as nx


def build_graph(chunks, tables):
    g = nx.Graph()
    eq = tables["equipment"]
    for _, r in eq.iterrows():
        g.add_node(r["tag"], kind="equipment", label=f"{r['tag']}\n{r['name']}",
                   criticality=r["criticality"], area=r["area"])
        g.add_node(r["area"], kind="area", label=r["area"])
        g.add_edge(r["tag"], r["area"], rel="located_in")

    known_tags = set(eq["tag"])

    # regulations -> equipment types
    regs = tables["regulations"]
    type_map = eq.groupby("equipment_type")["tag"].apply(list).to_dict()
    for _, r in regs.iterrows():
        g.add_node(r["clause_id"], kind="regulation", label=r["clause_id"])
        for t in r["applies_to_types"].split("|"):
            for tag in type_map.get(t, []):
                g.add_edge(r["clause_id"], tag, rel="applies_to")

    # incident / sop documents -> equipment and clauses
    seen_docs = set()
    for c in chunks:
        if c.doc_type not in ("incident", "sop"):
            continue
        doc = c.source.split("/")[-1].replace(".md", "")
        if doc not in seen_docs:
            g.add_node(doc, kind=c.doc_type, label=doc)
            seen_docs.add(doc)
        for tag in c.equipment_tags:
            if tag in known_tags:
                g.add_edge(doc, tag, rel="references")
        for cl in c.clause_refs:
            if g.has_node(cl):
                g.add_edge(doc, cl, rel="cites")

    # work-order history collapsed to one summary node per equipment
    wo = tables["work_orders"]
    for tag, grp in wo.groupby("equipment_tag"):
        node = f"WO-history:{tag}"
        corr = int((grp["wo_type"] != "Preventive").sum())
        g.add_node(node, kind="wo_history",
                   label=f"{len(grp)} WOs\n({corr} corrective)")
        g.add_edge(node, tag, rel="maintains")
    return g


def neighbourhood(g, node, hops=1):
    if node not in g:
        return g.subgraph([])
    nodes = {node}
    frontier = {node}
    for _ in range(hops):
        nxt = set()
        for n in frontier:
            nxt.update(g.neighbors(n))
        nodes |= nxt
        frontier = nxt
    return g.subgraph(nodes)
