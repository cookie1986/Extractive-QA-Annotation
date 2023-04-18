import os
from typing import List
from argparse import ArgumentParser
from time import time
from memory import check_memory_reqs
import utils



    #         # # check if document length is within SpaCy max_length 
    #         # if len(cleaned_doc_ascii) >= 100000:
    #         #     cleaned_doc_ascii = check_memory_reqs(cleaned_doc_ascii)

    #         # filter out irrelevant phrases
    #         filtered_doc = filter_irrelevant_text(cleaned_doc_ascii)


utils.init_unmark()

def process_docs(input_dir: str, output_dir: str, keywords: List[str]):

    # start timer
    start_time = time()
    
    # check whether output_dir exists, and create one if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # loop through each doc in input_dir
    for doc in os.listdir(input_dir):
        # read file
        with open(os.path.join(input_dir, doc), 'r', encoding='utf-8') as file:
            content = file.read()
        
        #  skip empty docs
        if type(content) == None:
            break
        
        # remove images
        cleaned_doc = utils.remove_images(content)
        # remove URL links
        cleaned_doc = utils.remove_links(cleaned_doc)

        # maintain document only if a keyword appears in tokenized word list
        doc_tokens = list(set(cleaned_doc.split()))
        for k in keywords:
            if k in doc_tokens:
                # delete headers
                cleaned_doc = utils.remove_headers(cleaned_doc)
                # convert markdown file to plain text
                cleaned_doc = utils.unmark(cleaned_doc)
                # remove non-ascii characters
                cleaned_doc = utils.remove_nonprintable_chars(cleaned_doc)
                
                # check memory requirements and split doc if doc is too long
                split_docs = check_memory_reqs(cleaned_doc)
                
                try:
                    print(len(split_docs))
                except: 
                    print(doc)

                # # process each split in split_docs
                # for i, part in enumerate(split_docs):
                #     # ADD SPACY CODE

                #     # write to new file, add "part_i" if the number of sub-parts within split_docs > 1
                #     part_suffix = f'_part_{i}' if len(split_docs) > 1 else ""
                #     # set output_filename
                #     output_filename = os.path.join(output_dir, f'{doc}{part_suffix}.txt')
                #     # write to file
                #     with open(output_filename, 'w', encoding='utf-8') as file:
                #         file.write(cleaned_doc)

                # break after finding the first keyword
                break
        
    # print runtime
    end_time = time()
    print(f'Runtime: {end_time - start_time} seconds')

    return None


if __name__ == "__main__":
    parser = ArgumentParser(description="Process a dictionary of documents for QA annotation.")
    parser.add_argument("input_dir", type=str, help="Path to the directory of documents to be processed.")
    parser.add_argument("output_dir", type=str, help="Path to the location where processed documents are to be stored.")
    parser.add_argument("--keywords", nargs="+", default=["asthma","lung","inhaler"], help="List of keywords to filter documents.")
    args = parser.parse_args()

    process_docs(args.input_dir, args.output_dir, args.keywords)

    print("Documents processed.")