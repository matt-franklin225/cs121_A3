# import math
# import os
# import json
# from bs4 import BeautifulSoup as BS
# from collections import defaultdict
# from tokenize_and_stem import tokenize_and_stem as tokenizer
# from posting import Posting, PostingEncoder, PostingDecoder
# from doc_ids import DocIDs
# import index_merger
# # import tfdif
# # from duplicate_detector import hash_content

# doc_ids = DocIDs()
# root_folder = 'DEV' #Change to DEV
# target_folder = 'partial_index_test'
# output_file = 'merged_index_test.txt'
# doc_ids_file = 'url_ids.json'
# # root_folder = 'ANALYST' #For shorter folder
# # target_folder = 'partial_index_test'
# # output_file = 'merged_example.txt'
# # doc_ids_file = 'url_ids_example.json'

# def calculate_frequencies(tokens: list) -> dict:
#     tf = defaultdict(int)
#     for token in tokens:
#         tf[token] += 1
#     return tf

# def parse_json_file(file_path: str) -> dict and str:
#     with open(file_path, 'r', encoding = 'utf-8') as file:
#         data = json.load(file)
#         url = data.get('url', '')
#         content = data.get('content', '')
#         soup = BS(content, "html.parser")
#         tokens = tokenizer(soup)
#         token_freq = calculate_frequencies(tokens)

#         # clean_url = defragment_url(url) #Do we need to defragment urls?

#     return token_freq, url, content

# def build_partial_index(file_paths: list, index_file_name: str) -> None:
#     inverted_index = defaultdict(list)
#     # content_hashes = {} To store hashed version of the content

#     # Iterate through the files, tokenizing and getting frequencies for each
#     for file_path in file_paths: # doc[0] is the document ID, doc[1] is the file path
#         doc_id = file_path[0]
#         token_freq, url, content = parse_json_file(file_path[1])
#         # content_hash = hash_content(content)

#         # if content_hash in content_hashes:    #Add this section later
#         #     continue
#         # content_hashes[content_hash] = doc_id
#         # doc_ids.add(file_path[0], url)

#         tokens = token_freq.keys()
#         for token in tokens:
#             posting = Posting(file_path[0], url)
#             posting.set_tf(token_freq[token])
#             posting.calculate_tf_score(sum(token_freq.values()), token_freq[token])
#             inverted_index[token].append(posting)


#     # Write inverted index to file
#     with open(index_file_name, 'w') as file:
#         for term, postings in inverted_index.items():
#             # TODO: Perhaps find a better way to separate traits
#             postings_str = ' | '.join(f'{p.id},,{p.url},,{p.tf_score}' for p in postings)
#             file.write(f'{term}: {postings_str}\n')
#     inverted_index.clear()


# def build_inverted_index(root_folder: str, target_folder: str):
#     documents = []
#     current_doc_id = 0
#     # Can manually adjust starting point, this is done in case
#     # we suffer a crash or other issue midway through a run
#     starting_doc = 0
#     current_p_index = starting_doc // 1000
#     DOCUS_PER_PARTIAL_INDEX = 1000
#     for dir, subdirs, files in os.walk(root_folder):
#         for file in files:
#             if file == ".DS_Store":
#                 continue
#             current_doc_id += 1
#             # Skip over documents before the starting point (if necessary)
#             if current_doc_id < starting_doc:
#                 continue
#             documents.append([current_doc_id, os.path.join(dir, file)])
#             # Every 1k documents, build out a new partial index
#             if (current_doc_id + 1) % DOCUS_PER_PARTIAL_INDEX == 0:
#                 build_partial_index(documents, f'{target_folder}/p-index{current_p_index}.txt')
#                 current_p_index += 1
#                 documents.clear()
#     build_partial_index(documents, f'{target_folder}/p-index{current_p_index}.txt')
#     current_p_index += 1
#     documents.clear()

# def main(root: str, target: str, output: str, doc_id_file: str) -> None:
#     build_inverted_index(root, target)
#     doc_ids.write_to_file(doc_id_file)
#     index_merger.merge(target_folder, output)
#     # N = int(len(doc_ids.map_of_IDs.keys()))  #To Rewrite the file and swap for tf-idf score
#     # tfdif.main(output, N)


# if __name__ == "__main__":
#     main(root_folder, target_folder, output_file, doc_ids_file)

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
            # TODO: Perhaps find a better way to separate traits
            postings_str = ' | '.join(f'{p.id},,{p.url},,{p.tf_score}' for p in postings)
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

    # build_inverted_index(root_folder, target_folder)
    # doc_ids.write_to_file(doc_ids_file)
    index_merger.merge(target_folder, output_file)