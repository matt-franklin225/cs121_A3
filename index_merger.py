import json
import os
import heapq


def merge_partial_indexes(partial_index_files, output_file):
    file_contents = []
    for file in partial_index_files: # Open all partial index files and put their contents into file
        with open(file, 'r') as fh:
            file_contents.append(json.load(fh)) #Stores as dict

    min_heap = [] # To keep track of the smallest termID (key/token) across all files
    for i, content in enumerate(file_contents): #Go through each file's contents
        if content:
            termID = min(content.keys())
            heapq.heappush(min_heap, (termID, i)) #Push to heapq (a priority queue)
    #min_heap now contains smallest token from each file (token, file_index)
    print(len(min_heap), "\n\n") #DELETE ME

    output_buffer = {}
    with open(output_file, 'w') as output_handle:
        while min_heap:
            smallest_token, file_index = heapq.heappop(min_heap)
            content_dict = file_contents[file_index]
            term_data = content_dict.pop(smallest_token)

            # Merge the postings lists for the smallest token
            if smallest_token in output_buffer:
                output_buffer[smallest_token].extend(term_data)
            else:
                output_buffer[smallest_token] = term_data

            if not content_dict:
                continue

            # Push the next smallest token from current file into the heap
                #heapq places it to where it should go
            next_token = min(content_dict.keys())
            heapq.heappush(min_heap, (next_token, file_index))

        json.dump(output_buffer, output_handle, indent=4)


if __name__ == '__main__':
    root_dir = 'partial_index'
    partial_files = []
    for dir, subdirs, files in os.walk(root_dir):
        for file in files:
            partial_files.append(os.path.join(dir, file))
    output = "merged_index.json"
    merge_partial_indexes(partial_files, output)