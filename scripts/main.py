import os
from typing import List
from time import time
from src.arg_parser import create_arg_parser
import src.utils as utils
import src.filtering as filtering
import src.memory as memory
import src.unprocessed_doc_handling as unprocessed_doc_handling
from path_helper import add_parent_dir_to_path

add_parent_dir_to_path()

utils.init_unmark()

def process_single_doc(doc: str, keywords: List[str]) -> str:
    cleaned_doc = utils.remove_images(doc)
    cleaned_doc = utils.remove_links(cleaned_doc)
    
    if utils.contains_keywords(cleaned_doc, keywords):
        # remove headers from markdown
        cleaned_doc = utils.remove_headers(cleaned_doc)
        # convert markdown to plain text
        cleaned_doc = utils.unmark(cleaned_doc)
        # remove non-ascii chars
        cleaned_doc = utils.remove_nonprintable_chars(cleaned_doc)
        # filter out irrelevant phrases
        cleaned_doc = utils.remove_irrelevant_text(cleaned_doc)

        return cleaned_doc
    else:
        return None

def process_docs(input_dir: str, output_dir: str, keywords: List[str], verbose: bool = False):
    start_time = time()

    print("Processing Docs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # clean all the documents and store them in memory
    cleaned_docs = {}
    for doc in os.listdir(input_dir):
        with open(os.path.join(input_dir, doc), 'r', encoding='utf-8') as file:
            content = file.read()

        if content:
            if verbose:
                print(f"Processing document: {doc}")

            cleaned_doc = process_single_doc(content, keywords)
            if cleaned_doc:
                cleaned_docs[doc] = cleaned_doc

    # apply a filtering step to the entire cleaned corpus
    # filtered_docs = filtering.filter_relevant_docs(cleaned_docs, keywords)
    filtered_docs = cleaned_docs

    # write filtered documents to disk
    for doc, content in filtered_docs.items():
        split_docs = memory.check_memory_reqs(content)

        try:
            for i, part in enumerate(split_docs):
                part_suffix = f'_part_{i}' if len(split_docs) > 1 else ""
                output_filename = os.path.join(output_dir, f'{doc}{part_suffix}.txt')

                with open(output_filename, 'w', encoding='utf-8') as file:
                    file.write(part)
        except:
            unprocessed_doc_handling.doc_not_processed(doc)

    unprocessed_doc_handling.export_unprocessed_docs(unprocessed_doc_handling.unprocessed_doc_ids)

    end_time = time()
    print("Documents processed.")
    print(f'Runtime: {end_time - start_time} seconds')

    return None


if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()

    process_docs(args.input_dir, args.output_dir, args.keywords, args.verbose)
