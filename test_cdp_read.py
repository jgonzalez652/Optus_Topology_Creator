
# Python
import os

input_dir = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input'

for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    if os.path.isfile(filepath):
        print(f'--- {filename} ---')
        with open(filepath, 'r') as f:
            print(f.read())
        print('\n')