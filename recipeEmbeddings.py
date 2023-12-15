from py2neo import Graph
import csv
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
t1 = datetime.strptime(current_time, "%H:%M:%S")
print('start time:', t1.time())

keys = {}
with open('keys.txt', 'r') as f:
    for line in f:
        key, value = line.strip().split(' = ')
        keys[key] = value

# Now you can access the keys and values like this:
api_key = keys['API KEY']
auth_details = eval(keys['AUTHDETAILS'])
bolt = keys['BOLT']

graph = Graph(bolt, auth_details)  

# Read the second CSV file
with open('your_modified_7.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Extract the ID and title from the row
        recipe_id = row['ID']  
        recipe_title = row['title']  
        
        # Prepare the properties, including all the vector columns
        properties = {key: float(value) for key, value in row.items() if key not in ['ID', 'title'] and value.replace('.', '', 1).isdigit()}

        # Merge the Recipe_Embedding node with ID and vector properties
        query = """
        MERGE (recipe:Recipe_Embedding {id: $id})
        ON CREATE SET recipe += $properties, recipe.title = $title
        ON MATCH SET recipe += $properties
        """
        graph.run(query, id=recipe_id, title=recipe_title, properties=properties)
        print(recipe_id, recipe_title)

now2 = datetime.now()
new_time = now2.strftime("%H:%M:%S")
t2 = datetime.strptime(new_time, "%H:%M:%S")

print('End Time: ', t2.time())

delta = t2-t1

print(f"Time difference is {delta.total_seconds()} seconds")

ms = delta.total_seconds() * 1000
print(f"Time difference is {ms} milliseconds")