import sys
import os

def add_parent_dir_to_path():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)