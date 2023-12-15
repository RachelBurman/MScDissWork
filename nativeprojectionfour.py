from py2neo import Graph
import time
import json

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

# Fetch vector property keys for Ingredient_Embedding nodes
vector_properties_query = """
MATCH (n:Ingredient_Embedding) 
RETURN keys(n)
"""
keys = graph.evaluate(vector_properties_query)
ing_vector_properties = [k for k in keys if k.startswith('vector_')]

# Fetch vector property keys for Recipe_Embedding nodes
rec_vector_properties_query = """
MATCH (n:Recipe_Embedding) 
RETURN keys(n)
"""
keys_2 = graph.evaluate(rec_vector_properties_query)
rec_vector_properties = [k for k in keys_2 if k.startswith('vector_')]

# Construct the node projection part dynamically
node_projection = {
    "Ingredient": {                       
        "label": "Ingredient",                        
        "properties": ["name"]                     
    },
    "Ingredient_Embedding": {
        "label": "Ingredient_Embedding",
        "properties": ["name"] + ing_vector_properties    
    },
    "Recipe": {
        "label": "Recipe",
        "properties": ["title", "id", "NER"]
    },
    "Recipe_Embedding": {
        "label": "Recipe_Embedding",
        "properties": ["title", "id"] + rec_vector_properties
    }
}

# Construct the relationship projection part
relationship_projection = {
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
	},
}

# Convert the dictionaries to JSON-like strings
node_projection_string = json.dumps(node_projection).replace("'", '"')
relationship_projection_string = json.dumps(relationship_projection).replace("'", '"')


# Use the converted strings in the Cypher query
projection_query = f"""
CALL gds.graph.project(
    'RecipeGraph',
    {node_projection_string},
    {relationship_projection_string}
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
