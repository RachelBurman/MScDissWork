import pandas as pd
import json

# Create an empty list to store JSON objects
data = []

# Open the JSON file and read each line
with open('Food.json', 'r', encoding='utf-8') as json_file:
    for line in json_file:
        try:
            # Parse each line as a JSON object
            json_data = json.loads(line)
            data.append(json_data)
        except json.JSONDecodeError:
            print(f"Skipping line: {line.strip()}")

# Convert the list of JSON objects to a DataFrame
df = pd.json_normalize(data)

# Save the DataFrame to a CSV file
df.to_csv('FooDBCSV.csv', index=False)
