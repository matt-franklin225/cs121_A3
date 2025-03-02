import json

class DocIDs:

    def __init__(self):
        self.map_of_IDs = {}


    def add(self, doc_id: str, url: str) -> None:
        self.map_of_IDs[doc_id] = url

    def get_map(self) -> dict:
        return self.map_of_IDs

    def write_to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            json.dump(self.map_of_IDs, file, ensure_ascii = False, indent = 4)