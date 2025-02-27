# Primary search function, returns a list of URLs sorted by relevance
def search_from_query(query: str) -> list:
    urls = ['https://uci.edu/', 'https://uci.edu/academics/index.php', 'https://merage.uci.edu/?utm_source=uciedu&utm_medium=referral', 'https://ics.uci.edu/', 'https://ics.uci.edu/facts-figures/ics-mission-history/']
    return urls


if __name__ == '__main__':
    query = input("Enter query: ")
    urls = search_from_query(query)
    for i in range(5):
        if urls[i]:
            print(f"{i+1}. {urls[i]}")