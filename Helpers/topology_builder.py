import networkx as nx

def build_topology(connections):
    """
    Build a NetworkX graph from a list of connection dicts.
    Each connection dict should have 'local_device' and 'neighbor_device' keys.
    Returns the graph and a set of all devices.
    """
    G = nx.Graph()
    devices = set()
    for conn in connections:
        for device in [conn['local_device'], conn['neighbor_device']]:
            if not G.has_node(device):
                G.add_node(device, label=device, name=device)
            devices.add(device)
        G.add_edge(conn['local_device'], conn['neighbor_device'])
    return G, devices

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