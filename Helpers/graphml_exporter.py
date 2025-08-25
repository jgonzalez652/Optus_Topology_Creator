import os
import networkx as nx

def infer_device_type(node_name):
    name = str(node_name).lower()
    if name.endswith('.nx'):
        return 'nexus_switch'
    elif name.endswith('.sx'):
        return 'catalyst_switch'
    elif name.endswith('.gw'):
        return 'router'
    else:
        return 'unknown'

def export_graphml(graph, output_dir, filename):
    for node in graph.nodes:
        graph.nodes[node]['label'] = str(node)
        graph.nodes[node]['device_type'] = infer_device_type(str(node))
    for u, v, data in graph.edges(data=True):
        label = f"{data.get('local_interface', '')} ↔ {data.get('neighbor_interface', '')}"
        graph.edges[u, v]['label'] = label
    path = os.path.join(output_dir, f"{filename}.graphml")
    nx.write_graphml(graph, path)