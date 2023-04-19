from argparse import ArgumentParser

def create_arg_parser():
    parser = ArgumentParser(description="Process a dictionary of documents for QA annotation.")
    parser.add_argument("input_dir", type=str, help="Path to the directory of documents to be processed.")
    parser.add_argument("output_dir", type=str, help="Path to the location where processed documents are to be stored.")
    parser.add_argument("--keywords", nargs="+", default=["asthma","lung","inhaler"], help="List of keywords to filter documents.")
    parser.add_argument("--verbose", action="store_true", default=False, help="If True, prints the ID of each document being processed.")
    return parser
