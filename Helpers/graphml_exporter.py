import os
import networkx as nx

def export_graphml(graph, output_dir, filename):
    """
    Export the NetworkX graph to a GraphML file.
    """
    path = os.path.join(output_dir, f"{filename}.graphml")
    nx.write_graphml(graph, path, encoding='utf-8')