import os
import networkx as nx

def export_graphml(graph, output_dir, filename):
    # Set node labels
    for node in graph.nodes:
        graph.nodes[node]['label'] = str(node)
    # Set edge labels
    for u, v, data in graph.edges(data=True):
        label = f"{data.get('local_interface', '')} ↔ {data.get('neighbor_interface', '')}"
        graph.edges[u, v]['label'] = label
    # Export to GraphML
    path = os.path.join(output_dir, f"{filename}.graphml")
    nx.write_graphml(graph, path)