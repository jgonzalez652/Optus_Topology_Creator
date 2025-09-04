import os
import json
import pandas as pd
from datetime import datetime

output_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\stp'
excel_output_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\excel_output'

def get_latest_json_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    files.sort(reverse=True)
    return os.path.join(directory, files[0]) if files else None

def flatten_devices(data):
    rows = []
    for device_name, info in data.get('device', {}).items():
        base = {k: v for k, v in info.items() if k != 'vlan_data' and k != 'mst_instances'}
        base['device_name'] = device_name
        vlan_data = info.get('vlan_data')
        if vlan_data:
            for vlan_id, vlan_info in vlan_data.items():
                row = base.copy()
                row['vlan_id'] = vlan_id
                row['vlan_priority'] = vlan_info.get('vlan_priority')
                row['root_bridge'] = vlan_info.get('root_bridge')
                row['adjusted_vlan_priority'] = vlan_info.get('adjusted_vlan_priority')
                rows.append(row)
        else:
            mst_instances = info.get('mst_instances')
            if mst_instances:
                for inst, inst_info in mst_instances.items():
                    row = base.copy()
                    row['mst_instance'] = inst
                    for k, v in inst_info.items():
                        row[k] = v
                    rows.append(row)
            else:
                rows.append(base)
    return rows

def export_to_excel():
    json_file = get_latest_json_file(output_dir)
    if not json_file:
        print("No JSON file found.")
        return

    with open(json_file, 'r') as f:
        data = json.load(f)

    rows = flatten_devices(data)
    df = pd.DataFrame(rows)
    df = df.fillna("n/a")
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_filename = f'stp_mst_status_{now}.xlsx'
    excel_path = os.path.join(excel_output_dir, excel_filename)
    df.to_excel(excel_path, index=False)
    print(f"Excel file created: {excel_path}")

if __name__ == "__main__":
    export_to_excel()