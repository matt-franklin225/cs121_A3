import heapq
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import time
import os
from itertools import islice


stemmer = PorterStemmer()


# Returns next document that contains the inv_list's term, starting at the given doc (returns doc if doc contains the term)
def go_to_document(inv_list: list, doc: int) -> list:
    while inv_list[1] and int(inv_list[1][0][0]) < doc:
        inv_list[1].pop(0)
    return inv_list


def parse_posting_list(line: str):
    docs = []
    term, postings = line.strip().split(": ", 1)  # Split term from postings
    freq = 0  # Number of docs for the term

    for posting in postings.split(" | "):  # Iterate through postings
        doc_id, url, tf_score = posting.split(",,")  # Extract components
        docs.append((int(doc_id), url, float(tf_score)))  # Store in dict
        freq += 1

    return docs, freq


def document_at_a_time_retrieval(query: list) -> list:
    inverted_lists = {}  # Stores an inverted list for each term in the query
    doc_freqs = {}  # Map of terms to number of docs it appears in
    results = {}  # Map of docs to scores
    print(query)
    start_time = time.time()
    for term in query:
        start_time = time.time()
        term_line = binary_search_file("merged_index.txt", term)  # Main thing slowing us down
        end_time = time.time()
        print(f'Binary search time: {(end_time-start_time)*1000} ms')
        start_time = time.time()
        posting_list, doc_freq = parse_posting_list(term_line)  # Secondary thing slowing us down
        end_time = time.time()
        print(f'Parse posting list time: {(end_time-start_time)*1000} ms')
        inverted_lists[term] = posting_list
        doc_freqs[term] = doc_freq
    doc_freqs = dict(sorted(doc_freqs.items(), key=lambda item: item[1]))
    if not inverted_lists or any(len(lst) == 0 for lst in inverted_lists):
        return []
    end_time = time.time()
    print(f'Time for creating inverted lists: {(end_time-start_time)*1000} ms')

    print(doc_freqs)

    # Get the set of doc_ids for each term
    doc_id_sets = [set(doc_id for doc_id, url, score in postings) for postings in inverted_lists.values()]

    # Find the intersection of all sets (docs containing all terms)
    valid_doc_ids = set.intersection(*doc_id_sets) if doc_id_sets else set()

    for term, postings in inverted_lists.items():
        for doc_id, url, score in postings:
            if doc_id in valid_doc_ids:
                results[doc_id] = results.get(doc_id, 0) + score
    # Update return later to include more results
    # Currently returns the 10 urls with the highest weight
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return [entry for entry in results][:10]


def get_urls_from_doc_ids(doc_ids: list) -> list:
    urls = []
    with open("url_ids.json", 'r') as file:
        urls_index = json.load(file)
        for doc_id in doc_ids:
            urls.append(urls_index[f"{doc_id+1}"])

    return urls


# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: list) -> list:
    doc_ids = document_at_a_time_retrieval(query)
    urls = get_urls_from_doc_ids(doc_ids)
    return urls


def binary_search_file(file_path, query_term):
    with open(file_path, 'r') as file:
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
                # return [posting.split(',,') for posting in
                #         postings.split(" | ")]  # Found the term, return postings
            elif term < query_term:
                left = pos  # Check right half
            else:
                right = mid  # Check left half

    return ''  # Return empty if term not found


def main():
    query_str = word_tokenize(input("Enter query: ").lower())

    start_time = time.time()
    stems = [stemmer.stem(token) for token in query_str if token.isalnum()]
    urls = search_from_query(list(set(stems)))
    end_time = time.time()

    # Print out urls
    if urls:
        print(f"Found {len(urls)} in {(end_time - start_time) * 1000:.2f} ms")
        for rank, url in enumerate(urls, start = 1):
            print(f"{rank}. {url}")
    else:
        print("No results found--please try a different query.")


if __name__ == '__main__':
    main()
    # Found 2 in 42.97 ms
    # Found 2 in 547.85 ms