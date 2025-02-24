import json

if __name__ == '__main__':
    with open('merged_index.json', 'r') as index:
        data = json.load(index)
    print(len(data))