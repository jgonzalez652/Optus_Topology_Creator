import json
from collections import Counter

json_path = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output\json\20250828_145649.json'

with open(json_path, 'r') as f:
    data = json.load(f)

devices = data.get('devices', [])
device_models = data.get('device_models', {})

model_list = [device_models.get(name, 'Unknown') for name in devices]
model_counts = Counter(model_list)
total_devices = len(devices)

print("Devices per model:")
for model, count in model_counts.items():
    print(f"{model}: {count}")
print(f"\nTotal devices: {total_devices}")