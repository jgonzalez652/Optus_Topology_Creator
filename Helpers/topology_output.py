import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from adjustText import adjust_text

def get_device_type(device, platform=None):
    name = device.lower()
    platform = platform.lower() if platform else ""
    if '.gw' in name or 'CISCO7609' in platform or '7206VXR' in name or '7206VXR' in platform:
        return 'router'
    elif '.sx' in name or 'ws-c3750' in platform or 'catalyst' in name or 'catalyst' in platform or 'c3560' in name or 'WS-C3750G' in platform:
        return 'catalyst_switch'
    elif 'N5K' in name or 'N5K' in platform or '.nx' in name or 'nexus' in platform:
        return 'nexus_switch'
    elif 'fw' in name or 'firewall' in name or 'fw' in platform or 'firewall' in platform:
        return 'firewall'
    elif 'server' in name or 'server' in platform:
        return 'server'
    else:
        return 'other'

DEVICE_STYLES = {
    'router':         {'node_shape': 's', 'color': '#1f77b4'},  # square, blue
    'catalyst_switch':{'node_shape': 'o', 'color': '#2ca02c'},  # circle, green
    'nexus_switch':   {'node_shape': '^', 'color': '#ff7f0e'},  # triangle, orange
    'server':         {'node_shape': 'D', 'color': '#9467bd'},  # diamond, purple
    'firewall':       {'node_shape': 'p', 'color': '#d62728'},  # pentagon, red
    'other':          {'node_shape': 'h', 'color': '#8c564b'},  # hexagon, brown
}


def group_devices_by_prefix(devices, prefix_len=5):
    groups = defaultdict(list)
    for d in devices:
        key = d[:prefix_len]
        groups[key].append(d)
    return groups

def save_topology_diagram(graph, output_dir, filename, device_platforms=None):
    num_devices = len(graph.nodes)
    plt.figure(figsize=(max(22, num_devices // 1.5), max(16, num_devices // 2)))
    pos = nx.spring_layout(graph, k=3.5, seed=42)
    # Draw nodes by type
    for device_type, style in DEVICE_STYLES.items():
        nodes_of_type = [
            n for n in graph.nodes
            if get_device_type(n, device_platforms[n] if device_platforms and n in device_platforms else None) == device_type
        ]
        if nodes_of_type:
            nx.draw_networkx_nodes(
                graph, pos,
                nodelist=nodes_of_type,
                node_shape=style['node_shape'],
                node_color=style['color'],
                node_size=1200,
                label=device_type
            )
    # Draw labels above nodes
    label_offset = 0.1
    label_pos = {k: (v[0], v[1] + label_offset) for k, v in pos.items()}
    nx.draw_networkx_labels(
        graph, label_pos,
        font_size=16,
        font_color='black',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
        verticalalignment='bottom',
        horizontalalignment='center'
    )
    # Draw edges last, underneath nodes/labels
    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5)
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{filename}.png'))
    plt.close()


def save_orphan_report(orphan_devices, orphan_connections, output_dir, filename):
    out_path = os.path.join(output_dir, filename + '_orphans.txt')
    with open(out_path, 'w') as f:
        f.write('Orphan Devices:\n')
        for d in orphan_devices:
            f.write(f'{d}\n')
        f.write('\nOrphan Connections:\n')
        for c in orphan_connections:
            f.write(f'{c[0]} -> {c[1]}\n')