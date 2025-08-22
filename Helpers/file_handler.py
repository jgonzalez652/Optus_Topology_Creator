# file_handler.py
import os

def read_input_files(input_dir):
    files_data = []
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                files_data.append(f.read())
    return files_data