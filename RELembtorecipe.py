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

# Query to get all Recipe nodes
recipe_query = "MATCH (rec:Recipe) RETURN rec"
recipes = graph.run(recipe_query).data()

# Track the number of relationships created
relationship_count = 0

# Start time for progress tracking
start_time = time.time()

for recipe in recipes:
    recipe_id = recipe['rec']['id']  
    
    # Create relationships from Recipe to its corresponding Recipe_Embedding
    rel_query = """
    MATCH (rec:Recipe), (emb:Recipe_Embedding)
    WHERE rec.id = $recipe_id AND emb.id = $recipe_id
    MERGE (emb)-[r:REPRESENTS_RECIPE]->(rec)
    RETURN count(r) as rel_created
    """
    result = graph.run(rel_query, recipe_id=recipe_id).data()
    relationship_count += result[0]['rel_created']

    # Print progress
    print(f"Processed Recipe ID: {recipe_id}")

# Total time taken
end_time = time.time()
print(f"Total relationships created: {relationship_count}")
print(f"Time taken: {end_time - start_time} seconds")
