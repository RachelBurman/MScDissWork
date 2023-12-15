from py2neo import Graph
import time

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

# Start time for progress tracking
start_time = time.time()
print("Start time:", time.ctime(start_time))

# Construct the list of vector properties up to the maximum index
max_vector_index = 979

# Ingredient Embedding Properties
ing_vector_properties = ', '.join([f'"vector_{i}"' for i in range(max_vector_index + 1)])
with open('ing_vector_properties.txt', 'w') as file:
    file.write(ing_vector_properties)

# Recipe Embedding Properties
rec_vector_properties = ', '.join([f'vector_{i}: "vector_{i}"' for i in range(max_vector_index + 1)])
with open('rec_vector_properties.txt', 'w') as file:
    file.write(rec_vector_properties)

print("Property files generated.")
