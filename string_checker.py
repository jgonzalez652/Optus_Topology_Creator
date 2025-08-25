import os

INPUT_DIR = r'C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input'
search_string = 'mas11dc1.nx.optusnet.com.au'  # Replace with the string you want to find

def find_files_with_string(directory, target):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if target in content:
                    print(f'Found in: {filename}')

def remove_lines_starting_with_string(directory, target):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            new_lines = [line for line in lines if not line.startswith(target)]
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.writelines(new_lines)

if __name__ == '__main__':
    find_files_with_string(INPUT_DIR, search_string)
    #remove_lines_starting_with_string(INPUT_DIR, search_string)