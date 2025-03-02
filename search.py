"""
Milestone 2
Goal: Develop a search and retrieval component
At least the following queries should be used to test your retrieval:
1 iftekhar ahmed
2 machine learning
3 ACM
4 master of software engineering
- Developing the Search component
Once you have built the inverted index, you are ready to test document retrieval
with queries. At the very least, the search should be able to deal with boolean
queries: AND only.
If you wish, you can sort the retrieved documents based on tf-idf scoring
(you are not required to do so now, but doing it now may save you time in
the future). This can be done using the cosine similarity method. Feel free to
use a library to compute cosine similarity once you have the term frequencies
and inverse document frequencies (although it should be very easy for you to
write your own implementation). You may also add other weighting/scoring
mechanisms to help refine the search results.
- Deliverables
Submit your code and a report (in pdf) to Canvas with the following content:
• the top 5 URLs for each of the queries above
• a picture of your search interface in action
- Note for the developer option: at this time, you do not need to have the
optimized index, but you may save time if you do.
Evaluation criteria
• Did your report show up on time?
• Are the reported URLs plausible?
"""

"""
TODO (for M2):
Write helper functions for document at a time retrieval function
- Get inverted list given a token
- get_current_document
- go_to_document
- get_score
Update inverted index to work better
- Add a dictionary that maps doc_ids to urls
- (if we have time) Update to add tf/idf scores for more precise retrieval
"""

import heapq
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import ijson

stemmer = PorterStemmer()

# Returns next document that contains the inv_list's term, starting at the given doc (returns doc if doc contains the term)
def go_to_document(inv_list: list, doc: int) -> list:
    while inv_list[1] and inv_list[1][0][0] < doc:
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
                # result.append((term, len(postings)))
                inverted_lists.append((term, postings))
    document = -1

    # The following section of code is the main loop of the conjunctive processing
    # document at a time retrieval process. The helper functions still have to be written.
    # Updates the inverted lists by popping elements off the front
    while inverted_lists:
        doc_score = 0
        for list in inverted_lists:
            if len(list[1]) > 0 and list[1][0][0] > document: # TODO: list[1][0] = get_current_document
                document = list[1][0][0]
        for list in inverted_lists:
            list = go_to_document(list, document) # TODO: Write go_to_document, goes to next document that >= {document}
            if len(list[1]) == 0 or list[1][0][0] != document:
                document = -1
                break
            else:
                # doc_score += get_score(query, document) # TODO: Write get_score
                doc_score += list[1][0][1] # Gets the number of appearances in the given doc
                list[1].pop(0) # Going to next document
        if document > -1:
            results.append((doc_score, document))
        else:
            break

    # The following line was used to test heapq to make sure it properly returns the top elements
    # results = [(5, 'https://uci.edu/'), (3, 'https://uci.edu/academics/index.php'), (6, 'https://ics.uci.edu/facts-figures/ics-mission-history/'), (1, 'https://ics.uci.edu/'), (2, 'https://merage.uci.edu/?utm_source=uciedu&utm_medium=referral'), (4, 'https://ics.uci.edu/2025/02/06/black-history-month-pioneers-in-science-and-technology/')]

    # Update return later to include more results
    # Currently returns the 5 urls with the highest weight
    print(results)
    return [entry[1] for entry in heapq.nlargest(5, results)]


# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: str) -> list:
    urls = document_at_a_time_retrieval(query)
    # urls = ['https://uci.edu/', 'https://uci.edu/academics/index.php', 'https://merage.uci.edu/?utm_source=uciedu&utm_medium=referral', 'https://ics.uci.edu/', 'https://ics.uci.edu/facts-figures/ics-mission-history/']
    return urls


if __name__ == '__main__':
    # Get original query
    query_str = word_tokenize(input("Enter query: ").lower())
    # Get tokens from query
    query = [token for token in query_str if token.isalnum()]
    # Add stems to original query
    stems = [stemmer.stem(token) for token in query if token.isalnum()]
    terms = query + [token for token in stems if token not in query]
    # Main search function
    urls = search_from_query(terms)
    # Print out urls
    count = 0
    for url in urls:
        count += 1
        print(f"{count}. {url}")