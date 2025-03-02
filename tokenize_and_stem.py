from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from collections import defaultdict

stemmer = PorterStemmer()
# Ex: "The cats were chasing mice quickly" -> "The cat were chase mice quickli"

""" 
    Given a Soup object, parse through and tokenize each alphanumeric word.
    Then, using Porter Stemmer Algorithm, stem each token (get rid of suffix) and
    keep its root form.
    Returns a list of the stemmed tokens.
"""
def tokenize_and_stem(soup: BeautifulSoup) -> list:
    tokens = word_tokenize(soup.get_text().lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalnum()]
    return stems


"""
    Given a list of tokens, calculate their frequency
    Returns a dictionary of { token: freq }
"""
def calculate_tf(tokens: list) -> dict:
    tf = defaultdict(int)
    for token in tokens:
        tf[token] += 1
    return tf