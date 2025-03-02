import math

class Posting:
    def __init__(self, doc_id: str, url: str):
        self.id = doc_id
        self.url = url
        self.tf_score = 0
        self.tf = 0
        self.tfidf = 0

    def calculate_idtf(self, total_docs: int, docs_with_token: int) -> None:
        self.tfidf = self.tf_score * math.log(total_docs / docs_with_token)

    def calculate_tf_score(self, total_words: int, token_frequency: int) -> None:
        self.tf_score = token_frequency / total_words

    def get_tfidf_score(self) -> int:
        return self.tfidf

    def get_tf_score(self) -> int:
        return self.tf_score

    def get_url(self) -> str:
        return self.url

    def set_tf(self, tf: int) -> None:
        self.tf = tf

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"({self.id}, {self.tfidf})"