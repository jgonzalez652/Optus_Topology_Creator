import xml.etree.ElementTree as ET

def add_yed_labels(graphml_path):
    tree = ET.parse(graphml_path)
    root = tree.getroot()
    ns = {
        'graphml': 'http://graphml.graphdrawing.org/xmlns',
        'y': 'http://www.yworks.com/xml/yfiles-common/3.0',
        'x': 'http://www.yworks.com/xml/yfiles-common/markup/3.0'
    }

    # Find or create the yEd label key
    key_id = 'd4'
    keys = root.findall('graphml:key', ns)
    if not any(k.attrib.get('id') == key_id for k in keys):
        key = ET.SubElement(root, '{http://graphml.graphdrawing.org/xmlns}key', {
            'id': key_id,
            'for': 'node',
            'attr.name': 'NodeLabels'
        })

    # Add yEd label markup to each node
    for node in root.findall('.//graphml:node', ns):
        label_text = node.attrib['id']
        data = ET.SubElement(node, '{http://graphml.graphdrawing.org/xmlns}data', {'key': key_id})
        xlist = ET.SubElement(data, '{http://www.yworks.com/xml/yfiles-common/markup/3.0}List')
        ylabel = ET.SubElement(xlist, '{http://www.yworks.com/xml/yfiles-common/3.0}Label', {'Text': label_text})

    tree.write(graphml_path, encoding='utf-8', xml_declaration=True)

# Usage:
# add_yed_labels('path_to_exported_graphml_file')