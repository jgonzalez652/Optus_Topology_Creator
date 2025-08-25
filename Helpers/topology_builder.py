import networkx as nx
import re


def clean_device_name(device):
    if device is None:
        return None
    name = str(device).lower()
    # Only match up to .nx, .sx, .gw, .cr
    match = re.search(r'(.+?\.(?:sx|nx|gw|cr))', name)
    return match.group(1) if match else name

def is_valid_device(device):
    cleaned = clean_device_name(device)
    if cleaned is None:
        return False
    # Exclude devices ending with .syd
    if cleaned.endswith('.syd'):
        return False
    return any(cleaned.endswith(x) for x in ['.nx', '.sx', '.gw', '.cr'])

def build_topology(connections):
    G = nx.Graph()
    devices = set()
    for conn in connections:
        local = clean_device_name(conn['local_device'])
        neighbor = clean_device_name(conn['neighbor_device'])
        valid_local = is_valid_device(local)
        valid_neighbor = is_valid_device(neighbor)
        if valid_local and not G.has_node(local):
            G.add_node(local, label=local, name=local)
            devices.add(local)
        if valid_neighbor and not G.has_node(neighbor):
            G.add_node(neighbor, label=neighbor, name=neighbor)
            devices.add(neighbor)
        if (valid_local or valid_neighbor) and local and neighbor:
            G.add_edge(local, neighbor)
    return G, devices

def remove_syd_nodes(graph):
    nodes_to_remove = []
    for n, data in graph.nodes(data=True):
        if '.syd' in str(n) or '.syd' in str(data.get('label', '')):
            nodes_to_remove.append(n)
        elif '.lvh' in str(n) or '.lvh' in str(data.get('label', '')):
            nodes_to_remove.append(n)
    graph.remove_nodes_from(nodes_to_remove)

def find_orphans(graph, devices):
    """
    Find orphan devices (no connections) and orphan connections (one-way).
    Returns a list of orphan devices and a list of orphan connections.
    """
    orphan_devices = [d for d in devices if not list(graph.neighbors(d))]
    orphan_connections = []
    for d in graph.nodes:
        for n in graph.neighbors(d):
            if not graph.has_edge(n, d):
                orphan_connections.append((d, n))
    return orphan_devices, orphan_connections
