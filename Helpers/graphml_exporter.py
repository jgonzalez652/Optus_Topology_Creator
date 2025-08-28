import os
import networkx as nx

def export_graphml(graph, output_dir, filename, device_types=None):
    for node in graph.nodes:
        graph.nodes[node]['label'] = str(node)
        device_type = device_types.get(node) if device_types else None
        graph.nodes[node]['device_type'] = device_type if device_type is not None else 'unknown'
    for u, v, data in graph.edges(data=True):
        local = data.get('local_interface', '')
        neighbor = data.get('neighbor_interface', '')
        graph.edges[u, v]['label'] = f"{local} ↔ {neighbor}"
    path = os.path.join(output_dir, f"{filename}.graphml")
    nx.write_graphml(graph, path)