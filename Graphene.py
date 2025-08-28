import os
import json
from Helpers.file_handler import read_input_files
from Helpers.cdp_parser import parse_cdp_output
from Helpers.topology_builder import build_topology, find_orphans, remove_syd_nodes
from Helpers.topology_output import save_topology_diagram, save_orphan_report
from Helpers.helpers import get_timestamped_filename
from Helpers.graphml_exporter import export_graphml
from Helpers.add_yed_labels import add_yed_labels
from Helpers.json_exporter import export_json

INPUT_DIR = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input\sh_cdp_neigh'
OUTPUT_DIR = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output'
OUTPUT_DIR_JSON = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\json'

def main():
    files_data = read_input_files(INPUT_DIR)
    all_connections = []
    print(f"\nINFO: Parsing cdp neighbors...")
    for raw in files_data:
        all_connections.extend(parse_cdp_output(raw))
    graph, devices = build_topology(all_connections)
    print(f"\nINFO: Exporting JSON file...")
    export_json(devices, all_connections, OUTPUT_DIR_JSON)

    # --- Enrich devices with type/model from latest JSON ---
    json_files = [f for f in os.listdir(OUTPUT_DIR_JSON) if f.endswith('.json')]
    json_files.sort(reverse=True)
    latest_json = os.path.join(OUTPUT_DIR_JSON, json_files[0])
    with open(latest_json, 'r') as f:
        json_data = json.load(f)
    device_models = json_data.get("device_models", {})
    device_types = json_data.get("device_types", {})
    enriched_devices = []
    for name in devices:
        enriched_devices.append({
            "name": name,
            "device_model": device_models.get(name),
            "device_type": device_types.get(name)
        })
    # ------------------------------------------------------

    print(f"\nINFO: Finding any orphan connections...")
    orphan_devices, orphan_connections = find_orphans(graph, enriched_devices)
    print(f"\nINFO: Cleaning up a bit...")
    remove_syd_nodes(graph)
    filename = get_timestamped_filename()
    #save_topology_diagram(graph, OUTPUT_DIR, filename) # this is to save .PNG files - no needed for now
    save_orphan_report(orphan_devices, orphan_connections, OUTPUT_DIR, filename)
    export_graphml(graph, OUTPUT_DIR, filename, device_types)  # <-- Save as .graphml
    print(f'Topology diagram, orphan report, and GraphML file saved as {filename} in {OUTPUT_DIR}')
    add_yed_labels(f"{OUTPUT_DIR}\\{filename}.graphml")

if __name__ == '__main__':
    main()