import os
import json
from datetime import datetime
from collections import defaultdict

input_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input\sh_spanning_tree'
output_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\stp'

def parse_stp_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    stp_mode = None
    for line in lines:
        if 'Spanning tree enabled protocol' in line:
            stp_mode = line.strip().split()[-1]
            break

    vlan_data = {}
    mst_instances = {}
    current_instance = None
    instance_priority = None
    root_bridge = False
    current_vlan = None
    vlan_priority = None

    for line in lines:
        if stp_mode == 'mstp':
            if line.strip().startswith('MST') and line.strip()[3:].isdigit():
                current_instance = line.strip()
                instance_priority = None
                root_bridge = False
            elif 'This bridge is the root' in line and current_instance:
                root_bridge = True
            elif line.strip().startswith('Bridge ID  Priority') and current_instance:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        instance_priority = int(parts[3])
                    except ValueError:
                        instance_priority = None
                mst_instances[current_instance] = {
                    'priority': instance_priority,
                    'root_bridge': root_bridge
                }
                current_instance = None
                instance_priority = None
                root_bridge = False
        else:
            if line.strip().startswith('VLAN'):
                current_vlan = line.strip().replace('VLAN', '').lstrip('0')
                vlan_priority = None
                root_bridge = False
            elif 'This bridge is the root' in line and current_vlan:
                root_bridge = True
            elif line.strip().startswith('Bridge ID  Priority') and current_vlan:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        vlan_priority = int(parts[3])
                    except ValueError:
                        vlan_priority = None
                vlan_id = int(current_vlan)
                adjusted_vlan_priority = vlan_priority - vlan_id if vlan_priority is not None else None
                vlan_data[current_vlan] = {
                    'vlan_priority': vlan_priority,
                    'root_bridge': root_bridge,
                    'adjusted_vlan_priority': adjusted_vlan_priority
                }
                current_vlan = None
                vlan_priority = None
                root_bridge = False

    device_info = {'stp_mode': stp_mode}
    if stp_mode == 'mstp':
        device_info['mst_instances'] = mst_instances
    else:
        device_info['vlan_data'] = vlan_data
    return device_info

def collect_devices(input_dir):
    devices = {}
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            device_name = filename.split('_')[0]
            filepath = os.path.join(input_dir, filename)
            devices[device_name] = parse_stp_file(filepath)
    return devices

def write_json(devices, output_dir):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'stp_{now}.json')
    with open(output_file, 'w') as f:
        json.dump({'device': devices}, f, indent=2)
    return output_file

def summarize_stp_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    devices = data.get('device', {})
    print(f"Total switches: {len(devices)}\n")

    for device, info in devices.items():
        print(f"Switch: {device}")
        stp_mode = info.get('stp_mode')
        print(f"  STP Mode: {stp_mode}")

        if stp_mode == 'mstp':
            instances = info.get('mst_instances', {})
            print(f"  MST Instances: {len(instances)}")
            priority_groups = defaultdict(list)
            for inst, inst_data in instances.items():
                priority = inst_data['priority']
                root = inst_data['root_bridge']
                priority_groups[priority].append((inst, root))
            for priority, inst_list in priority_groups.items():
                roots = [inst for inst, root in inst_list if root]
                print(f"    Priority {priority}: Instances {', '.join([i for i, _ in inst_list])} | Root: {', '.join(roots) if roots else 'No'}")
        else:
            vlans = info.get('vlan_data', {})
            print(f"  VLANs: {len(vlans)}")
            adjusted_priority_groups = defaultdict(list)
            for vlan, vlan_data in vlans.items():
                adjusted_priority = vlan_data['adjusted_vlan_priority']
                root = vlan_data['root_bridge']
                adjusted_priority_groups[adjusted_priority].append((vlan, root))
            for priority, vlan_list in adjusted_priority_groups.items():
                roots = [vlan for vlan, root in vlan_list if root]
                print(f"    Adjusted Priority {priority}: VLANs {', '.join([v for v, _ in vlan_list])} | Root: {', '.join(roots) if roots else 'No'}")
        print()

def main():
    devices = collect_devices(input_dir)
    output_file = write_json(devices, output_dir)
    print(f"STP data written to {output_file}")
    summarize_stp_json(output_file)

if __name__ == "__main__":
    main()