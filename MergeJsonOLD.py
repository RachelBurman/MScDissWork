import json
import glob

json_files_path = r"C:\Users\rache\OneDrive\Documents\MScDissWork\Data\*.json"
output_file_path = r"C:\Users\rache\OneDrive\Documents\MScDissWork\merged.json"

merged_data = []

# Open each JSON file and load its contents
for filename in glob.glob(json_files_path):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        merged_data.extend(data)

# Write the merged data to a new JSON file with indentation
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, indent=4)
