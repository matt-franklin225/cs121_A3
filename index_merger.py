import json
import os
import heapq
from collections import defaultdict


def merge_partial_indexes(partial_index_files, output_file_path):
    merged_index = defaultdict(list)

    for file_path in partial_index_files:
        with open(file_path, 'r') as file:
            for line in file:
                term, postings = line.split(': ', 1)
                postings = postings.strip().split('|')
                merged_index[term].extend(postings)

    with open(output_file_path, 'w') as f:
        for term, postings in sorted(merged_index.items()):
            f.write(f"{term}: {' | '.join(postings)}\n")


def merge(root_dir, output_file):
    partial_files = []
    for dir, subdirs, files in os.walk(root_dir):
        for file in files:
            partial_files.append(os.path.join(dir, file))
    merge_partial_indexes(partial_files, output_file)

if __name__ == '__main__':
    merge('partial_index', 'merged_index.txt')