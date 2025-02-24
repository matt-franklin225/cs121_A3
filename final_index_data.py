import json

# Simply used to calculate number of tokens
if __name__ == '__main__':
    with open('merged_index.json', 'r') as index:
        data = json.load(index)
    print(len(data))