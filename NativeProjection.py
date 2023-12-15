#Dont know if this code worked
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
ing_vector_properties = ', '.join([f'vector_{i}: "vector_{i}"' for i in range(max_vector_index + 1)])
rec_vector_properties = ', '.join([f'vector_{i}: "vector_{i}"' for i in range(max_vector_index + 1)])


# Construct the node projection part as a string
node_projection_str = """
'Ingredient': {
    'label': 'Ingredient',
    'properties': ['name']
},
'Ingredient_Embedding': {
    'label': 'Ingredient_Embedding',
    'properties': ['name', %s]
},
'Recipe': {
    'label': 'Recipe',
    'properties': ['title', 'id', 'NER']
},
'Recipe_Embedding': {
    'label': 'Recipe_Embedding',
    'properties': ['title', 'id', %s]
}
""" % (ing_vector_properties, rec_vector_properties)

# Construct the relationship projection part
relationship_projection = """
  	'CONTAINS': {
		'type': 'CONTAINS',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'ING_HAS_EMBEDDING': {
		'type': 'ING_HAS_EMBEDDING',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'ING_SIMILAR_TO': {
		'type': 'ING_SIMILAR_TO',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'REC_HAS_EMBEDDING': {
		'type': 'REC_HAS_EMBEDDING',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'REC_SIMILAR_TO': {
		'type': 'REC_SIMILAR_TO',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'REPESENTS_ING': {
		'type': 'REPESENTS_ING',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'REPRESENTS_RECIPE': {
		'type': 'REPRESENTS_RECIPE',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',

	},
	'USED_IN': {
		'type': 'USED_IN',
		'orientation': 'NATURAL',
		'aggregation': 'NONE',
	}
"""

# Construct the entire graph projection query
projection_query = f"""
CALL gds.graph.project(
    'TEST_GRAPH',
    {{{node_projection_str}}},
    {{{relationship_projection}}}
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

