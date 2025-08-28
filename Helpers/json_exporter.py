import os
import json
from datetime import datetime

def export_json(devices, connections, output_dir, filename=None):
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    data = {
        "devices": list(devices),
        "connections": connections
    }
    json_path = os.path.join(output_dir, f"{filename}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON file saved as {json_path}")