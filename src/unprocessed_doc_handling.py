unprocessed_doc_ids = []

def doc_not_processed(doc_name: str):
    print(f'Document {doc_name} has not been processed')
    unprocessed_doc_ids.append(doc_name)

    return None

def export_unprocessed_docs(doc_id_list):
    with open('data/unprocessed_docs.txt', 'w') as file:
        for doc_id in doc_id_list:
            file.write(f'{doc_id}\n')
    
    return None