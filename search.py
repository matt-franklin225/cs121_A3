import heapq
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import ijson
import os # Remove later???

stemmer = PorterStemmer()

# Returns next document that contains the inv_list's term, starting at the given doc (returns doc if doc contains the term)
def go_to_document(inv_list: list, doc: int) -> list:
    while inv_list[1] and inv_list[1][0]["id"] < doc:
        inv_list[1].pop(0)
    return inv_list

# Returns the document's score for a given query
def get_score(query: list, doc: int) -> int:
    pass

def document_at_a_time_retrieval(query: list) -> list:
    inverted_lists = [] # Stores an inverted list for each term in the query
    results = []
    print(query)
    with open("merged_index.json", "r") as file:
        for term, postings in ijson.kvitems(file, ""):
            if term in query:
                inverted_lists.append((term, postings))
    document = -1

    if not inverted_lists or any(len(lst[1]) == 0 for lst in inverted_lists):
        return []

    # The following section of code is the main loop of the conjunctive processing
    # document at a time retrieval process. The helper functions still have to be written.
    # Updates the inverted lists by popping elements off the front
    while all(len(lst[1]) > 0 for lst in inverted_lists):
        doc_score = 0
        document = max(lst[1][0]["id"] for lst in inverted_lists if len(lst[1]) > 0)
        contains_all = True
        for i in range(len(inverted_lists)):
            inverted_lists[i] = go_to_document(inverted_lists[i], document)
            if len(inverted_lists[i][1]) == 0 or inverted_lists[i][1][0]["id"] != document:
                contains_all = False
                break
            else:
                doc_score += inverted_lists[i][1][0]["tf_score"] # Gets the tf score for the given doc
                inverted_lists[i][1].pop(0) # Going to next document
        if contains_all:
            results.append((doc_score, document))
            for list in inverted_lists:
                if len(list[1]) > 0:
                    list[1].pop(0)

    # Update return later to include more results
    # Currently returns the 5 urls with the highest weight
    # print(results)
    return [entry[1] for entry in heapq.nlargest(5, results)]

def get_urls_from_doc_ids(doc_ids: list) -> list:
    # This is deeply inefficient but it technically works
    urls = []
    count = 0
    for root_dir, subdirs, files in os.walk("DEV"):
        for file in files:
            count += 1
            if count in doc_ids:
                with open(f"{root_dir}/{file}", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    url = data.get("url")
                    urls.append(url)
    return urls

# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: str) -> list:
    doc_ids = document_at_a_time_retrieval(query)
    urls = get_urls_from_doc_ids(doc_ids)
    return urls


if __name__ == '__main__':
    # Get original query
    query_str = word_tokenize(input("Enter query: ").lower())
    # Get tokens from query
    query = [token for token in query_str if token.isalnum()]
    # Add stems to original query
    stems = [stemmer.stem(token) for token in query if token.isalnum()]
    terms = query + [token for token in stems if token not in query]
    # terms = query
    # Main search function
    # urls = search_from_query(terms)
    urls = search_from_query(stems)
    # Print out urls
    count = 0
    for url in urls:
        count += 1
        print(f"{count}. {url}")