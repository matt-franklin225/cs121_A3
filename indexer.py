import os
import json
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import tokenize_and_stem as tokenizer
from posting import Posting, PostingEncoder, PostingDecoder
from doc_ids import DocIDs
import index_merger

doc_ids = DocIDs()

def calculate_frequencies(tokens: list) -> dict:
    tf = defaultdict(int)
    for token in tokens:
        tf[token] += 1
    return tf

def build_partial_index(file_paths: list, index_file_name: str) -> None:
    inverted_index = defaultdict(list)

    # Iterate through the files, tokenizing and getting frequencies for each
    for file_path in file_paths:
        with open(file_path[1], 'r') as file:
            print(file_path[0])
            content = json.load(file)
            doc_ids.add(file_path[0], content['url'])

            soup = BS(content['content'], 'html.parser')
            tokens = tokenizer.tokenize_and_stem(soup)
            tf = calculate_frequencies(tokens)
            tokens_unique = set(tokens)
            
            for token in tokens_unique:
                posting = Posting(file_path[0], content['url'])
                posting.set_tf(tf[token])
                posting.calculate_tf_score(len(tokens), tf[token])
                inverted_index[token].append(posting)

    # Write partial index to file
    with open(index_file_name, 'w') as file:
        for term, postings in inverted_index.items():
            postings_str = ' | '.join(f'{p.id},{p.url},{p.tf_score}' for p in postings)
            file.write(f'{term}: {postings_str}\n')

    inverted_index.clear()


def build_inverted_index(root_folder: str, target_folder: str):
    documents = []
    current_doc_id = -1
    # Can manually adjust starting point, this is done in case
    # we suffer a crash or other issue midway through a run
    starting_doc = 0
    current_p_index = starting_doc // 1000
    DOCUS_PER_PARTIAL_INDEX = 1000
    for dir, subdirs, files in os.walk(root_folder):
        for file in files:
            if file == '.DS_Store':
                continue
            current_doc_id += 1
            # Skip over documents before the starting point (if necessary)
            if current_doc_id < starting_doc:
                continue
            documents.append([current_doc_id, os.path.join(dir, file)])
            # Every 1k documents, build out a new partial index
            if (current_doc_id+1) % DOCUS_PER_PARTIAL_INDEX == 0:
                build_partial_index(documents, f'{target_folder}/p-index{current_p_index}.txt')
                current_p_index += 1
                documents.clear()
    build_partial_index(documents, f'{target_folder}/p-index{current_p_index}.txt')
    current_p_index += 1
    documents.clear()

if __name__ == '__main__':
    root_folder = 'DEV'
    target_folder = 'partial_index'
    output_file = 'merged_index.txt'
    doc_ids_file = 'url_ids.json'

    build_inverted_index(root_folder, target_folder)
    doc_ids.write_to_file(doc_ids_file)
    index_merger.merge(target_folder, output_file)
