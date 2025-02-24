# import os
# import json

# def intersect(index1, index2):
#     try:
#         iterator = iter(index2)
#         index2_curr = next(iterator)
#         for key in index1:
#             while index2_curr < key:
#                 index2_curr = next(iterator)
#             if key == index2_curr:
#                 index1[key].extend(index2[key])
#             else:
#                 index1[index2_curr] = index2[index2_curr]

#     except StopIteration:
#         return index1
#     for key in index2:
#         index1[key] = index2[key]
#     return index1

# def merge_partial_indexes(root_folder, file_write_name):
#     inverted_index = {}
#     count = 0
#     for dir, subdirs, file_paths in os.walk(root_folder):
#         for file_path in file_paths:
#             index_path = os.path.join(dir, file_path)
#             file = open(index_path, 'r')
#             new_partial_index = dict(sorted(json.load(file).items()))
#             file.close()
#             inverted_index = intersect(inverted_index, new_partial_index)

#             count += 1
#             print(count)
#             if(count > 2):
#                 break

#     with open(file_write_name, 'w') as file:
#         print("we here")
#         print(len(inverted_index))
#         json.dump(inverted_index, file, indent=4)
#     return inverted_index


# if __name__ == '__main__':
#     root_folder = 'partial_index'
#     merge_partial_indexes(root_folder, 'inverted_index.json')

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