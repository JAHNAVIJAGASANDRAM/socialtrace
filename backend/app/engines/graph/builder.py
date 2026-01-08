import networkx as nx

def build_investigation_graph(evidence_store: dict):
    """
    Builds a graph of Account -> Content -> Case
    """

    G = nx.DiGraph()

    for case_id, evidences in evidence_store.items():
        # Case node
        G.add_node(case_id, type="case")

        for ev in evidences:
            content_node = ev["sha256"]
            G.add_node(content_node, type="content")

            # Content belongs to case
            G.add_edge(content_node, case_id, relation="PART_OF")

            # Account node (if exists)
            if ev.get("username"):
                account_node = f"{ev.get('platform')}::{ev.get('username')}"
                G.add_node(account_node, type="account")

                G.add_edge(account_node, content_node, relation="POSTED")

    return G
