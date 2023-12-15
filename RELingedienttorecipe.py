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
 


recipe_query = "MATCH (rec:Recipe) RETURN rec"
recipes = graph.run(recipe_query).data()

# Track the number of relationships created
relationship_count = 0

# Start time for progress tracking
start_time = time.time()

for recipe in recipes:
    ner_list = recipe['rec']['NER'] 
    
    for ingredient_name in ner_list:
        # Create relationships with Ingredients that exist in the NER list
        rel_query = """
        MATCH (ing:Ingredient {name: $ingredient_name}), (rec:Recipe)
        WHERE ID(rec) = $recipe_id
        MERGE (ing)-[r:USED_IN]->(rec)
        RETURN count(r) as rel_created
        """
        result = graph.run(rel_query, ingredient_name=ingredient_name, recipe_id=recipe['rec'].identity).data()
        relationship_count += result[0]['rel_created']

    # Print progress
    print(f"Processed Recipe: {recipe['rec']['title']} (ID: {recipe['rec']['id']})")

# Total time taken
end_time = time.time()
print(f"Total relationships created: {relationship_count}")
print(f"Time taken: {end_time - start_time} seconds")
