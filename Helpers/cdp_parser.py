# cdp_parser.py
import re

def clean_device_name(name):
    name = name.replace('ï»¿', '').strip()
    # Only remove known domains, not valid device names
    name = re.sub(
        r'\.(optusnet\.com\.au|iplab\.au\.singtelgroup\.net|ipnet\.optus\.com\.au|ipdev\.iplab\.au\.singtelgroup\.n)(\(.*\))?$',
        '',
        name
    )
    # Extract base device name if it matches the pattern
    match = re.search(r'([a-z0-9]+)\.(cr|nx|sx|gw)', name)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return name

def parse_cdp_output(raw_data):
    connections = []
    device_name = None

    first_line = raw_data.splitlines()[0]
    device_name_match = re.match(r'([^\s#]+)', first_line)
    if device_name_match:
        device_name = clean_device_name(device_name_match.group(1))

    lines = raw_data.splitlines()
    table_start = None
    for i, line in enumerate(lines):
        if re.search(r'Device[\s-]*ID', line, re.IGNORECASE):
            table_start = i + 1
            break
    if table_start is None:
        return connections

    entry = []
    for line in lines[table_start:]:
        if line.strip() == '':
            continue
        if not line.startswith(' '):
            if entry:
                conn = _parse_cdp_entry(entry, device_name)
                if conn:
                    connections.append(conn)
                entry = []
        entry.append(line)
    if entry:
        conn = _parse_cdp_entry(entry, device_name)
        if conn:
            connections.append(conn)
    return connections

def _parse_cdp_entry(entry_lines, local_device):
    entry = ' '.join(line.strip() for line in entry_lines)
    parts = entry.split()
    if len(parts) < 5:
        return None
    neighbor_device = clean_device_name(parts[0])
    local_intf = parts[1] + ' ' + parts[2] if parts[2][0].isdigit() else parts[1]
    neighbor_intf = parts[-2] + ' ' + parts[-1] if parts[-2][0].isalpha() else parts[-1]
    #if "mas3cr1.nx" in local_device:
    #    print(f"Entry lines: {entry_lines}")
    #print(f"local_device: {local_device}, local_intf: {local_intf}, neighbor_device: {neighbor_device}, neighbor_intf: {neighbor_intf}")
    return {
        'local_device': local_device,
        'local_intf': local_intf,
        'neighbor_device': neighbor_device,
        'neighbor_intf': neighbor_intf
    }