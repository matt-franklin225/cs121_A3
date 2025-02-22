from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer = PorterStemmer()
# Ex: "The cats were chasing mice quickly" -> "The cat were chase mice quickli"

""" 
    Given a string, parse through and tokenize each alphanumeric word.
    Then, using Porter Stemmer Algorithm, stem each token (get rid of suffix) and
    keep its root form.
"""
def tokenize_and_stem(text: str) -> list :
    tokens = word_tokenize(text)
    stems = [ stemmer.stem(token) for token in tokens if token.isalnum() ]
    return stems