import os
import json
import re
from datetime import datetime

def clean_interface_name(intf):
    pattern = r'\b(?:Gig|Ten|Eth|mgmt)\s*\d+(?:/\d+)*\b'
    match = re.search(pattern, str(intf))
    return match.group(0) if match else None

def export_json(devices, connections, output_dir, filename=None):
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean interface names in connections
    for conn in connections:
        if "local_intf" in conn:
            conn["local_intf"] = clean_interface_name(conn["local_intf"])
        if "neighbor_intf" in conn:
            conn["neighbor_intf"] = clean_interface_name(conn["neighbor_intf"])
    data = {
        "devices": list(devices),
        "connections": connections
    }
    json_path = os.path.join(output_dir, f"{filename}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON file saved as {json_path}")