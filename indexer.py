import os
import json
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import tokenize_and_stem as tokenizer

def calculate_tf(tokens: list) -> dict:
    tf = defaultdict(int)
    for token in tokens:
        tf[token] += 1
    return tf


def build_partial_index(file_paths: list, index_file_name: str) -> None:
    inverted_index = defaultdict(list)
    tokens_unique = list(set())

    for file_path in file_paths: # doc[0] is the ID, doc[1] is the file path
        with open(file_path[1], 'r') as file:
            print(file_path[0]) # REMOVE THIS LATER
            content = json.dumps(json.load(file))
            soup = BS(content, "html.parser")
            tokens = tokenizer.tokenize_and_stem(soup)
            tf = calculate_tf(tokens)
            tokens_unique = list(set(tokens))
            for token in tokens_unique:
                inverted_index[token].append((file_path[0], tf[token]))

    with open(index_file_name, 'w') as file:
        json.dump(inverted_index, file, indent=4)
    inverted_index.clear()


# def build_inverted_index(root_folder):
#     documents = []
#     current_doc_id = 0
#     current_p_index = 0
#     DOCUS_PER_PARTIAL_INDEX = 1000
#     for dir, subdirs, files in os.walk(root_folder):
#         for file in files:
#             current_doc_id += 1
#             documents.append([current_doc_id, os.path.join(dir, file)])
#             if current_doc_id % DOCUS_PER_PARTIAL_INDEX == 0:
#                 build_partial_index(documents, f"partial_index/p-index{current_p_index}.json")
#                 current_p_index += 1
#                 documents.clear()

def build_inverted_index(root_folder):
    documents = []
    current_doc_id = 0
    starting_doc = 55001
    current_p_index = starting_doc // 1000
    DOCUS_PER_PARTIAL_INDEX = 1000
    for dir, subdirs, files in os.walk(root_folder):
        for file in files:
            current_doc_id += 1
            if current_doc_id < starting_doc:
                continue
            documents.append([current_doc_id, os.path.join(dir, file)])
            if current_doc_id % DOCUS_PER_PARTIAL_INDEX == 0:
                build_partial_index(documents, f"partial_index/p-index{current_p_index}.json")
                current_p_index += 1
                documents.clear()
    build_partial_index(documents, f"partial_index/p-index{current_p_index}.json")
    current_p_index += 1
    documents.clear()

if __name__ == "__main__":
    root_folder = "DEV"
    # inverted_index = build_inverted_index(root_folder)
    build_inverted_index(root_folder)