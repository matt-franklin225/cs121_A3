import math

class Posting:
    def __init__(self, doc_id: str, url: str):
        self.id = doc_id
        self.url = url
        self.tf = 0
        self.tfidf = 0

    def calculate_idtf(self, total_docs: int, docs_with_token: int) -> None:
        self.tfidf = self.tf * math.log(total_docs / docs_with_token)

    def calculate_tf(self, total_words: int, token_frequency: int) -> None:
        self.tf = token_frequency / total_words

    def get_tfidf_score(self) -> int:
        return self.tfidf

    def get_tf(self) -> int:
        return self.tf

    def __str__(self) -> str:
        return f"({self.id}, {self.tfidf})"