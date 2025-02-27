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
import heapq

def document_at_a_time_retrieval(query):
    inverted_lists = [] # Stores an inverted list for each term in the query
    results = []
    for term in query:
        # term_indexes.append(inverted_list(term, inverted_index))
        # Final implementation: add the inverted list 
        # for each term in the query into this array
        inverted_lists.append({}) # Placeholder
    document = -1

    # The following section of code is the main loop of the conjunctive processing
    # document at a time retrieval process. The helper functions still have to be written.
    # while inverted_lists:
    #     doc_score = 0
    #     for list in inverted_lists:
    #         if get_current_document(list) > document: # TODO: write get_next(list)
    #             document = get_current_document(list)
    #     for list in inverted_lists:
    #         list.go_to_document(document) # TODO: Write go_to_document, goes to next document that >= {document}
    #         if get_current_document(list) == document:
    #             doc_score += get_score(query, document) # TODO: Write get_score
    #             list.go_to_next_document() # TODO: Set list to the next document
    #         else:
    #             document = -1
    #             break
    #     if document > -1:
    #         results.append(doc_score, document)

    # The following line (commented out) was used to test heapq to make sure it properly returns the top elements
    results = [(5, 'https://uci.edu/'), (3, 'https://uci.edu/academics/index.php'), (6, 'https://ics.uci.edu/facts-figures/ics-mission-history/'), (1, 'https://ics.uci.edu/'), (2, 'https://merage.uci.edu/?utm_source=uciedu&utm_medium=referral'), (4, 'https://ics.uci.edu/2025/02/06/black-history-month-pioneers-in-science-and-technology/')]

    # Update return later to include more results
    # Currently returns the 5 urls with the highest weight
    return [entry[1] for entry in heapq.nlargest(5, results)]


# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: str) -> list:
    urls = document_at_a_time_retrieval(query)
    # urls = ['https://uci.edu/', 'https://uci.edu/academics/index.php', 'https://merage.uci.edu/?utm_source=uciedu&utm_medium=referral', 'https://ics.uci.edu/', 'https://ics.uci.edu/facts-figures/ics-mission-history/']
    return urls


if __name__ == '__main__':
    query = input("Enter query: ")
    urls = search_from_query(query)
    count = 0
    for url in urls:
        count += 1
        print(f"{count}. {url}")