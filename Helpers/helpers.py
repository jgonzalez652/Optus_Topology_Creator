# helpers.py
from datetime import datetime

def get_timestamped_filename():
    return datetime.now().strftime('%Y%m%d_%H%M%S')