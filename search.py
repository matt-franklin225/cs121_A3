import heapq
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import time
import os
from itertools import islice
import re


output_file = 'merged_index.txt'
doc_ids_file = 'url_ids.json'

stemmer = PorterStemmer()
stop_phrases_regex = re.compile(r'^(how to|what is|why is|who is|where is|when does|can you|can i|when will) ')


# Adjusts query to remove duplicates and stop phrases (how to, what is, etc.)
def fix_query(query_str: list) -> list:
    query = re.sub(stop_phrases_regex, '', ' '.join(query_str)).split(' ')
    query = [stemmer.stem(token) for token in query if token.isalnum()]
    return list(set(query))


# Returns next document that contains the inv_list's term, starting at the given doc (returns doc if doc contains the term)
def go_to_document(inv_list: list, doc: int) -> list:
    while inv_list[1] and int(inv_list[1][0][0]) < doc:
        inv_list[1].pop(0)
    return inv_list


# Upon being given an inverted index line for a term, will return the relevant document data along with term's doc frequency
def parse_posting_list(line: str):
    docs = []
    term, postings = line.strip().split(": ", 1)  # Split term from postings
    freq = 0  # Number of docs for the term
    for posting in postings.split(" | "):  # Iterate through postings
        doc_id, tf_score = posting.split(", ")  # Extract components
        docs.append((int(doc_id), float(tf_score)))  # Store in dict
        freq += 1

    return docs, freq


# Main function to get relevant documents
def get_results(query: list) -> list:
    inverted_lists = {}  # Stores an inverted list for each term in the query
    doc_freqs = {}  # Map of terms to number of docs it appears in
    results = {}  # Map of docs to scores
    print(query)
    start_time = time.time()
    for term in query:
        term_line = binary_search_file(output_file, term)  # Main thing slowing us down
        if term_line:
            posting_list, doc_freq = parse_posting_list(term_line)  # Secondary thing slowing us down
            inverted_lists[term] = posting_list
            doc_freqs[term] = doc_freq
        else:
            return []
    doc_freqs = dict(sorted(doc_freqs.items(), key=lambda item: item[1]))
    if not inverted_lists or any(len(lst) == 0 for lst in inverted_lists):
        return []
    end_time = time.time()
    print(f'Time for creating inverted lists: {(end_time-start_time)*1000} ms')

    print(doc_freqs)

    # Get the set of doc_ids for each term
    doc_id_sets = [set(doc_id for doc_id, score in postings) for postings in inverted_lists.values()]

    # Find the intersection of all sets (docs containing all terms)
    valid_doc_ids = set.intersection(*doc_id_sets) if doc_id_sets else set()

    for term, postings in inverted_lists.items():
        for doc_id, score in postings:
            if doc_id in valid_doc_ids:
                results[doc_id] = results.get(doc_id, 0) + score
    # Currently returns the 10 urls with the highest weight
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return [entry for entry in results][:10]


def get_urls_from_doc_ids(doc_ids: list) -> list:
    urls = []
    with open(doc_ids_file, 'r', encoding='utf-8') as file:
        urls_index = json.load(file)
        for doc_id in doc_ids:
            urls.append(urls_index[f"{doc_id}"])

    return urls


# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: list) -> list:
    doc_ids = get_results(query)
    urls = get_urls_from_doc_ids(doc_ids)
    return urls


def binary_search_file(file_path, query_term):
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(0, 2)
        size = file.tell()  # endpoint
        left, right = 0, size

        while left < right:
            mid = (left + right) // 2  # midpoint
            file.seek(mid)  # Go to midpoint
            file.readline()  # Get line from midpoint
            
            pos = file.tell()  # Current position
            if pos >= size:  # Break if outside range
                break
            # Read the next line
            line = file.readline().strip()
            if not line:
                break
            
            term, postings = line.split(": ", 1)
            if term == query_term:
                return line
            elif term < query_term:
                left = pos  # Check right half
            else:
                right = mid  # Check left half

    return ''  # Return empty if term not found


def main():
    # Get query and tokenize it
    query_str = word_tokenize(input("Enter query: ").lower())

    start_time = time.time()

    # Adjust query to remove duplicates and stop phrases (how to, what is, etc.)
    query = fix_query(query_str)
    urls = search_from_query(query)

    end_time = time.time()

    # Print out urls
    if urls:
        print(f"Found {len(urls)} in {(end_time - start_time) * 1000:.2f} ms")
        for rank, url in enumerate(urls, start = 1):
            print(f"{rank}. {url}")
    else:
        print("No results found--please try a different query.")
        print(f"Terminated query in {(end_time - start_time) * 1000:.2f} ms")


if __name__ == '__main__':
    main()
