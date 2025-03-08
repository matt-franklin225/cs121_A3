import math
import json

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
        return f"(ID: {self.id}, Score: {self.tfidf})"

    def __lt__(self, other) -> bool:
        return self.tfidf < other.tfidf

    def __gt__(self, other) -> bool:
        return self.tfidf > other.tfidf

    def __eq__(self, other) -> bool:
        return self.tfidf == other.tfidf

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "url": self.url,
            "tf_score": self.tf_score,
            "tf": self.tf,
            "tfidf": self.tfidf
        }

class PostingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Posting):
            return obj.to_dict()
        return super().default(obj)

class PostingDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "id" in obj and "url" in obj:  # Check if the object matches a Posting structure
            posting = Posting(obj["id"], obj["url"])
            posting.tf_score = obj["tf_score"]
            posting.tf = obj["tf"]
            posting.tfidf = obj["tfidf"]
            return posting
        return obj  # Otherwise, return as-is (e.g., for normal dicts)