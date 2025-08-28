import networkx as nx
import re

def extract_device_name(device):
    if device is None:
        return None
    name = str(device).lower().strip()
    # Match base device names with or without domain/suffix
    match = re.search(r'([a-z0-9]+)\.(cr|nx|sx|gw)', name)
    if match:
        #if "mas3" in name:
        #    print(f"Match: {name}")
        return f"{match.group(1)}.{match.group(2)}"
    return name

def is_valid_device(device):
    if device is None:
        return False
    exclude_types = ['.syd', '.lvh']
    for ex in exclude_types:
        if device.endswith(ex):
            return False
    valid_types = ['.nx', '.sx', '.gw', '.cr']
    return any(device.endswith(t) for t in valid_types)

def build_topology(connections):
    G = nx.Graph()
    devices = set()
    for conn in connections:
        local = extract_device_name(conn.get('local_device'))
        neighbor = extract_device_name(conn.get('neighbor_device'))
        valid_local = is_valid_device(local)
        valid_neighbor = is_valid_device(neighbor)
        if valid_local and not G.has_node(local):
            G.add_node(local, label=local, name=local)
            devices.add(local)
        if valid_neighbor and not G.has_node(neighbor):
            G.add_node(neighbor, label=neighbor, name=neighbor)
            devices.add(neighbor)
        if valid_local and valid_neighbor and local and neighbor:
            G.add_edge(local, neighbor)
    return G, devices

def remove_syd_nodes(graph):
    nodes_to_remove = []
    for n, data in graph.nodes(data=True):
        if any(x in str(n) or x in str(data.get('label', '')) for x in ['.syd', '.lvh']):
            nodes_to_remove.append(n)
    graph.remove_nodes_from(nodes_to_remove)

def find_orphans(graph, devices):
    orphan_devices = [d for d in devices if not list(graph.neighbors(d["name"]))]
    orphan_connections = []
    for d in graph.nodes:
        for n in graph.neighbors(d):
            if not graph.has_edge(n, d):
                orphan_connections.append((d, n))
    return orphan_devices, orphan_connections