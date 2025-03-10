import json
import math
import re


def calculate_tf_idf(tf_score: str, dft: float, N: int) -> float:
    tf = float(tf_score)
    tf_idf = tf * (math.log(N / dft))
    return tf_idf

def parse_text_file(content: str) -> dict:
    token_maps = {}
    lines = content.split("\n")
    for line in lines:
        if not line.strip():
            continue

        token, postings = line.split(": ", 1)
        token_maps[token.strip()] = []

        doc_entries = postings.split(" | ")

        for entry in doc_entries:
            doc_id, tf_score = map(str.strip, entry.split(", "))
            tf_score = float(tf_score)
            token_maps[token].append((doc_id, tf_score))
    return token_maps

def update_content(content: str, N: int):
    updated_lines = []
    tokens_dict = parse_text_file(content)


    for token, postings_list in tokens_dict.items():
        updated_postings = []
        for posting in postings_list:
            dft = len(postings_list)
            tf_idf_score = calculate_tf_idf(posting[1], dft, N)
            updated_postings.append(f"{posting[0]}, {tf_idf_score}")
        updated_lines.append(f"{token}: {' | '.join(updated_postings)}")
    return "\n".join(updated_lines)


def main(file_path: str, N: int) -> None:
    with open(file_path, "r") as file:
        content = file.read()

    updated_content = update_content(content, N)

    with open(file_path, "w") as file:
        file.write(updated_content)


if __name__ == "__main__":
    file_path = "merged_index.txt"
    url_id_file = 'url_ids.json'
    # file_path = "merged_example.txt"
    # url_id_file = 'url_ids_example.json'
    with open(url_id_file, 'r') as file:
        content = json.load(file)
        N = len(content.keys())

    main(file_path, N)