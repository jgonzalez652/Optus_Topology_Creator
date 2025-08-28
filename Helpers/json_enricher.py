import os
import json
import re
from datetime import datetime

def find_latest_json(json_dir):
    files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    files.sort(reverse=True)
    return os.path.join(json_dir, files[0]) if files else None

def find_sh_version_file(device, sh_version_dir):
    for fname in os.listdir(sh_version_dir):
        if fname.startswith(device):
            return os.path.join(sh_version_dir, fname)
    return None

def parse_device_model(sh_version_path):
    # Try multiple patterns to extract the model, including models with spaces
    model_patterns = [
        r'Model\s+number\s*[:\-]\s*(\S+)',
        r'cisco\s+([A-Za-z0-9\s\-]+)\s+Chassis',
        r'cisco\s+(\S+)\s*\(',
    ]
    try:
        with open(sh_version_path, 'r') as f:
            for line in f:
                for pattern in model_patterns:
                    match = re.search(pattern, line)
                    if match:
                        return match.group(1).strip()
    except Exception:
        pass
    return None

def get_device_type(device_name, device_model):
    if device_name.endswith('.gw') or device_name.endswith('.cr'):
        return "router"
    if device_model:
        if "Nexus" in device_model:
            return "nexus_switch"
        if device_model.startswith("WS"):
            return "catalyst_switch"
    return None

def enrich_json():
    json_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\json'
    sh_version_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input\sh_version'
    latest_json = find_latest_json(json_dir)
    if not latest_json:
        print("No JSON file found.")
        return

    with open(latest_json, 'r') as f:
        data = json.load(f)

    device_models = {}
    device_types = {}
    for device in data.get("devices", []):
        sh_version_file = find_sh_version_file(device, sh_version_dir)
        model = parse_device_model(sh_version_file) if sh_version_file else None
        device_models[device] = model
        device_types[device] = get_device_type(device, model)

    data["device_models"] = device_models
    data["device_types"] = device_types

    with open(latest_json, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Updated JSON file: {latest_json}")

if __name__ == "__main__":
    enrich_json()