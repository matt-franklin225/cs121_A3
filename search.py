import heapq
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import time
import os


stemmer = PorterStemmer()


# Returns next document that contains the inv_list's term, starting at the given doc (returns doc if doc contains the term)
def go_to_document(inv_list: list, doc: int) -> list:
    while inv_list[1] and int(inv_list[1][0][0]) < doc:
        inv_list[1].pop(0)
    return inv_list


# Returns the document's score for a given query
def get_score(query: list, doc: int) -> int:
    pass


# def document_at_a_time_retrieval(query: list) -> list:
#     inverted_lists = []  # Stores an inverted list for each term in the query
#     results = []
#     print(query)
#     start_time = time.time()
#     for term in query:
#         # term_line = binary_search_file("merged_index.txt", term)
#         inverted_lists.append((term, binary_search_file("merged_index.txt", term)))
#     end_time = time.time()
#     print(f"Time: {(end_time-start_time)*1000} ms ")
#     if not inverted_lists or any(len(lst[1]) == 0 for lst in inverted_lists):
#         return []
#     # The following section of code is the main loop of the conjunctive processing
#     # document at a time retrieval process. The helper functions still have to be written.
#     # Updates the inverted lists by popping elements off the front
#     while all(len(lst[1]) > 0 for lst in inverted_lists):
#         doc_score = 0
#         document = max(int(lst[1][0][0]) for lst in inverted_lists if
#                        len(lst[1]) > 0)  # lst[1][0][0] is doc_id
#         contains_all = True
#         for i in range(len(inverted_lists)):
#             inverted_lists[i] = go_to_document(inverted_lists[i], document)
#             if len(inverted_lists[i][1]) == 0 or int(inverted_lists[i][1][0][0]) != document:
#                 contains_all = False
#                 break
#             else:
#                 doc_score += float(
#                     inverted_lists[i][1][0][2])  # Gets the tf score for the given doc
#                 inverted_lists[i][1].pop(0)  # Going to next document
#         if contains_all:
#             results.append((doc_score, document))
#             for list in inverted_lists:
#                 if len(list[1]) > 0:
#                     list[1].pop(0)

#     # Update return later to include more results
#     # Currently returns the 10 urls with the highest weight
#     # print(results)
#     return [entry[1] for entry in heapq.nlargest(10, results)]


# def get_urls_from_doc_ids(doc_ids: list) -> list:
#     urls = []
#     with open("url_ids.json", 'r') as file:
#         urls_index = json.load(file)
#         for doc_id in doc_ids:
#             urls.append(urls_index[f"{doc_id+1}"])

#     return urls


def document_at_a_time_retrieval(query: list) -> list:
    inverted_lists = {}  # Stores an inverted list for each term in the query
    doc_freqs = {}  # Map of terms to number of docs it appears in
    results = {}  # Map of docs to scores
    # results = []
    print(query)
    start_time = time.time()
    for term in query:
        term_line = binary_search_file("merged_index.txt", term)
        posting_list, doc_freq = parse_posting_list(term_line)
        inverted_lists[term] = posting_list
        doc_freqs[term] = doc_freq
    doc_freqs = dict(sorted(doc_freqs.items(), key=lambda item: item[1]))
    if not inverted_lists or any(len(lst) == 0 for lst in inverted_lists):
        return []
    # for lst in inverted_lists:
    #     print(lst)
        # print(len(lst.values()))
    
    # Begin by creating a dict of the relevant terms, then go thru each term and process them appropriately
    first_term = True
    for term in doc_freqs.keys():
        for doc in inverted_lists[term]:
            if first_term:
                results[doc[0]] = doc[2]
            elif doc[0] in results:
                results[doc[0]] += doc[2]
        first_term = False
    end_time = time.time()
    print(f"Time: {(end_time-start_time)*1000} ms ")
    # Update return later to include more results
    # Currently returns the 10 urls with the highest weight
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return [entry for entry in results]


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

def parse_posting_list(line: str):
    docs = []
    term, postings = line.strip().split(": ", 1)  # Split term from postings
    freq = 0  # Number of docs for the term

    for posting in postings.split(" | "):  # Iterate through postings
        doc_id, url, tf_score = posting.split(",,")  # Extract components
        docs.append((int(doc_id), url, float(tf_score)))  # Store in dict
        freq += 1

    return docs, freq

if __name__ == '__main__':
    main()
    # Found 2 in 42.97 ms
    # Found 2 in 547.85 ms