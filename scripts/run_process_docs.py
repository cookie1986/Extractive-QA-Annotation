import os
from path_helper import add_parent_dir_to_path
add_parent_dir_to_path()
from dotenv import load_dotenv
from scripts.main import process_docs

load_dotenv()

INPUT_DIR = os.environ['INPUT_DIR']
OUTPUT_DIR = os.environ['OUTPUT_DIR']

with open('data/keywords.txt', 'r') as f:
    keywords_list = f.readlines()
keywords_list = [kw.rstrip() for kw in keywords_list]

process_docs(
    input_dir=INPUT_DIR, 
    output_dir=OUTPUT_DIR, 
    keywords=keywords_list,
    verbose=True
    )