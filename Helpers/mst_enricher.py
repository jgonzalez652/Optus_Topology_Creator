import os
import json
import re

output_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\stp'
mst_status_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input\mst_status'

def get_latest_json_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    files.sort(reverse=True)
    return os.path.join(directory, files[0]) if files else None

def extract_vlans_mapped(file_path):
    mst_vlans = {}
    with open(file_path, 'r') as f:
        content = f.read()
    for match in re.finditer(r'##### (MST\d+)\s+vlans mapped:\s+([^\n]+)', content):
        instance = match.group(1)  # e.g., MST0
        vlans = match.group(2).strip()
        num = instance[3:]
        json_instance = f"MST{int(num):04d}"
        mst_vlans[json_instance] = vlans
    return mst_vlans

def enrich_json():
    json_file = get_latest_json_file(output_dir)
    if not json_file:
        print("No JSON file found.")
        return

    with open(json_file, 'r') as f:
        data = json.load(f)

    devices = data.get('device', {})
    for device_name, info in devices.items():
        if info.get('stp_mode') == 'mstp':
            for fname in os.listdir(mst_status_dir):
                if fname.startswith(device_name):
                    mst_file = os.path.join(mst_status_dir, fname)
                    mst_vlans = extract_vlans_mapped(mst_file)
                    for instance, vlans in mst_vlans.items():
                        if "mst_instances" in info and instance in info["mst_instances"]:
                            info["mst_instances"][instance]["vlans_mapped"] = vlans
                    break

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Enriched JSON file updated: {json_file}")

if __name__ == "__main__":
    enrich_json()