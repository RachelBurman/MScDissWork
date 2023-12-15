# import csv

# input_file_path = 'recipe_embeddings_batch_2.csv'  
# output_file_path = 'your_modified_2.csv'  

# with open(input_file_path, mode='r', encoding='utf-8') as infile, \
#      open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:

#     # Create CSV reader and writer
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)

#     # Read the header and write it to the new file with an added 'ID' column
#     headers = next(reader)
#     writer.writerow(['ID'] + headers) 

#     # Iterate over the rows, adding an ID to each, and write to the new file
#     for id, row in enumerate(reader, start=1):  # Start counting IDs from 1
#         writer.writerow([id] + row)

import csv

input_file_path = 'recipe_embeddings_batch_11.csv'  
output_file_path = 'your_modified_11.csv' 


with open(input_file_path, mode='r', encoding='utf-8') as infile, \
     open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:

    # Create CSV reader and writer
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the header and write it to the new file with an added 'ID' column
    headers = next(reader)
    writer.writerow(['ID'] + headers)  

    
    for id, row in enumerate(reader, start=550001):  # Start counting IDs from 50001
        writer.writerow([id] + row)
