import os
from typing import List
from time import time
from arg_parser import create_arg_parser
import utils
import filtering
import memory
import unprocessed_doc_handling

utils.init_unmark()

def process_single_doc(doc: str, keywords: List[str]) -> str:
    cleaned_doc = utils.remove_images(doc)
    cleaned_doc = utils.remove_links(cleaned_doc)
    
    if utils.contains_keywords(cleaned_doc, keywords):
        cleaned_doc = utils.remove_headers(cleaned_doc)
        cleaned_doc = utils.unmark(cleaned_doc)
        cleaned_doc = utils.remove_nonprintable_chars(cleaned_doc)
        return cleaned_doc
    else:
        return None

def process_docs(input_dir: str, output_dir: str, keywords: List[str], verbose: bool = False):
    start_time = time()

    print("Processing Docs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for doc in os.listdir(input_dir):
        with open(os.path.join(input_dir, doc), 'r', encoding='utf-8') as file:
            content = file.read()

        if content:
            if verbose:
                print(f"Processing document: {doc}")

            processed_doc = process_single_doc(content, keywords)

            if processed_doc:
                split_docs = memory.check_memory_reqs(processed_doc)

                try:
                    for i, part in enumerate(split_docs):
                        part_filtered = filtering.filter_irrelevant_text(part)

                        part_suffix = f'_part_{i}' if len(split_docs) > 1 else ""
                        output_filename = os.path.join(output_dir, f'{doc}{part_suffix}.txt')

                        with open(output_filename, 'w', encoding='utf-8') as file:
                            file.write(part_filtered)
                except:
                    unprocessed_doc_handling.doc_not_processed(doc)
    
    unprocessed_doc_handling.export_unprocessed_docs(unprocessed_doc_handling.unprocessed_doc_ids)
        
    end_time = time()
    print(f'Runtime: {end_time - start_time} seconds')

    return None

if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()

    process_docs(args.input_dir, args.output_dir, args.keywords, args.verbose)

    print("Documents processed.")
