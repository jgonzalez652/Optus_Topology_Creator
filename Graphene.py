import os
from Helpers.file_handler import read_input_files
from Helpers.cdp_parser import parse_cdp_output
from Helpers.topology_builder import build_topology, find_orphans, remove_syd_nodes
from Helpers.topology_output import save_topology_diagram, save_orphan_report
from Helpers.helpers import get_timestamped_filename
from Helpers.graphml_exporter import export_graphml
from Helpers.add_yed_labels import add_yed_labels
from Helpers.json_exporter import export_json

INPUT_DIR = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input'
OUTPUT_DIR = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output'
OUTPUT_DIR_JSON = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\json'

def main():
    files_data = read_input_files(INPUT_DIR)
    all_connections = []
    for raw in files_data:
        all_connections.extend(parse_cdp_output(raw))
    graph, devices = build_topology(all_connections)
    export_json(devices, all_connections, OUTPUT_DIR_JSON)
    orphan_devices, orphan_connections = find_orphans(graph, devices)
    remove_syd_nodes(graph)
    filename = get_timestamped_filename()
     #save_topology_diagram(graph, OUTPUT_DIR, filename) # this is to save .PNG files - no needed for now
    save_orphan_report(orphan_devices, orphan_connections, OUTPUT_DIR, filename)
    export_graphml(graph, OUTPUT_DIR, filename)  # <-- Save as .graphml
    print(f'Topology diagram, orphan report, and GraphML file saved as {filename} in {OUTPUT_DIR}')
    add_yed_labels(f"{OUTPUT_DIR}\\{filename}.graphml")

if __name__ == '__main__':
    main()