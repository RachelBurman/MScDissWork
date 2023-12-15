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
max_vector_index = 960
ing_vector_properties = [f'vector_{i}' for i in range(max_vector_index + 1)]
rec_vector_properties = [f'vector_{i}' for i in range(max_vector_index + 1)]

# Construct the node projection part as a string
node_projection_str = "{"
node_projection_str += "'Ingredient': {'label': 'Ingredient', 'properties': ['name']}, "
node_projection_str += "'Ingredient_Embedding': {'label': 'Ingredient_Embedding', 'properties': ['name'] + " + str(ing_vector_properties) + "}, "
node_projection_str += "'Recipe': {'label': 'Recipe', 'properties': ['title', 'id', 'NER']}, "
node_projection_str += "'Recipe_Embedding': {'label': 'Recipe_Embedding', 'properties': ['title', 'id'] + " + str(rec_vector_properties) + "}"
node_projection_str += "}"

# Similarly, construct the relationship projection part as a string
relationship_projection_str = "{"
# Construct the relationship projection part
relationship_projection_str += "'CONTAINS': { type: 'CONTAINS', 'orientation': 'NATURAL', 'aggregation': 'NONE',},"
relationship_projection_str += "'ING_HAS_EMBEDDING': { type: 'ING_HAS_EMBEDDING', 'orientation': 'NATURAL','aggregation': 'NONE',},"
relationship_projection_str += "'ING_SIMILAR_TO': { type: 'ING_SIMILAR_TO', 'orientation': 'NATURAL', 'aggregation': 'NONE',},"
relationship_projection_str += "'REC_HAS_EMBEDDING': {type: 'REC_HAS_EMBEDDING','orientation': 'NATURAL','aggregation': 'NONE',},"
relationship_projection_str += "'REC_SIMILAR_TO': {type: 'REC_SIMILAR_TO','orientation': 'NATURAL','aggregation': 'NONE',},"
relationship_projection_str += "'REPESENTS_ING': {type: 'REPESENTS_ING','orientation': 'NATURAL','aggregation': 'NONE',},"
relationship_projection_str += "'REPRESENTS_RECIPE': {type: 'REPRESENTS_RECIPE','orientation': 'NATURAL','aggregation': 'NONE',},"
relationship_projection_str += "'USED_IN': {type: 'USED_IN','orientation': 'NATURAL','aggregation': 'NONE',},  }"
relationship_projection_str += "}"

# Construct the entire graph projection query
projection_query = f"""
CALL gds.graph.project(
    'RecipeGraph',
    {node_projection_str},
    {relationship_projection_str}
)
YIELD graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount
"""

# Execute the graph projection query
result = graph.run(projection_query).data()

# Output the result
print(result)

# Record end time
end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")
