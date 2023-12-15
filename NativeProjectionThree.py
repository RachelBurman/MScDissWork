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

# Fetch vector property keys for Ingredient_Embedding nodes
ing_vector_query = """
MATCH (n:Ingredient_Embedding) 
UNWIND keys(n) AS key
WITH key
WHERE key STARTS WITH 'vector_'
RETURN COLLECT(DISTINCT key) AS ing_vectors
"""
ing_vector_properties = graph.evaluate(ing_vector_query)

# Fetch vector property keys for Recipe_Embedding nodes
rec_vector_query = """
MATCH (n:Recipe_Embedding) 
UNWIND keys(n) AS key
WITH key
WHERE key STARTS WITH 'vector_'
RETURN COLLECT(DISTINCT key) AS rec_vectors
"""
rec_vector_properties = graph.evaluate(rec_vector_query)

# Start time for progress tracking
start_time = time.time()
print("Start time:", time.ctime(start_time))

# Construct node projection strings
ing_vector_properties_str = ', '.join([f"'{prop}'" for prop in ing_vector_properties])
rec_vector_properties_str = ', '.join([f"'{prop}'" for prop in rec_vector_properties])

# Construct the entire graph projection query
projection_query = f"""
CALL gds.graph.project(
    'TESTGRAPH',
    {{
        'Ingredient': {{'label': 'Ingredient', 'properties': ['name']}},
        'Ingredient_Embedding': {{'label': 'Ingredient_Embedding', 'properties': ['name', {ing_vector_properties_str}]}},
        'Recipe': {{'label': 'Recipe', 'properties': ['title', 'id', 'NER']}},
        'Recipe_Embedding': {{'label': 'Recipe_Embedding', 'properties': ['title', 'id', {rec_vector_properties_str}]}}
    }},
    {{
        'CONTAINS': {{'type': 'CONTAINS', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'ING_HAS_EMBEDDING': {{'type': 'ING_HAS_EMBEDDING', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'ING_SIMILAR_TO': {{'type': 'ING_SIMILAR_TO', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'REC_HAS_EMBEDDING': {{'type': 'REC_HAS_EMBEDDING', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'REC_SIMILAR_TO': {{'type': 'REC_SIMILAR_TO', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'REPESENTS_ING': {{'type': 'REPESENTS_ING', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'REPRESENTS_RECIPE': {{'type': 'REPRESENTS_RECIPE', 'orientation': 'NATURAL', 'aggregation': 'NONE'}},
        'USED_IN': {{'type': 'USED_IN', 'orientation': 'NATURAL', 'aggregation': 'NONE'}}
    }}
)
YIELD graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount
"""

# Execute the graph projection query
result = graph.run(projection_query).data()

# Output the result
print(result)

# Record end time
end_time = time.time()
print("End time:", time.ctime(end_time))
print(f"Total time taken: {end_time - start_time} seconds")

