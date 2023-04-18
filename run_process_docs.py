import os
from dotenv import load_dotenv
from main import process_docs


load_dotenv()

INPUT_DIR = os.environ['INPUT_DIR']
OUTPUT_DIR = os.environ['OUTPUT_DIR']

asthma_keywords = ["asthma", "lung", "inhaler"]

process_docs(
    input_dir=INPUT_DIR, 
    output_dir=OUTPUT_DIR, 
    keywords=asthma_keywords
    )