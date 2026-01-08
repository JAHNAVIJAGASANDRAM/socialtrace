import networkx as nx

def analyze_graph(graph):
    """
    Basic graph analytics to find important nodes
    """

    centrality = nx.degree_centrality(graph)

    ranked = sorted(
        centrality.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"node": node, "score": score}
        for node, score in ranked[:10]
    ]
