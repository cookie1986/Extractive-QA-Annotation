import psutil
import math

# calculate memory per character for non Parser/NER tasks in SpaCy (requires 1GB per 100,000 character document)
MEMORY_REQS_PER_CHAR = 1000000000 / 100000

MAX_CHARS_DEFAULT = 100000

# get available memory
def get_available_memory():
    mem = psutil.virtual_memory()

    return mem.available

# check memory requiresments and split doc if requirements > current available resources
def check_memory_reqs(doc, memory_factor: int = MEMORY_REQS_PER_CHAR):

    # check for blank (empty) docs
    if type(doc) == None:
        return None  

    # sub list to store document splits
    doc_list = []

    # get length of document (in chars)
    doc_length = len(doc)

    if doc_length > MAX_CHARS_DEFAULT:
        # get current available memory
        current_available = get_available_memory()
    
        # calculate if memory requirements exceed the currently available memory - SpaCy needs 1GB per 100,000 char document
        required_memory = doc_length * memory_factor

        # if required memory is greater than current memory, the document needs to be split
        if required_memory > current_available:
            
            # calculate the number of parts required to split the doc so that its < current available memory
            num_parts = math.ceil(required_memory / current_available)

            # get the length of each part
            part_length = math.ceil(doc_length / num_parts)

            # split the doc into num_parts
            doc_list = [doc[i:i + part_length] for i in range(0, doc_length, part_length)]

            return doc_list
        
        else:
            doc_list.append(doc)
    
    else:
        doc_list.append(doc)
    
        return doc_list
