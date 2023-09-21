from neo4j import GraphDatabase

cypher_query = """
MATCH (butter:Ingredient {name: 'butter'})-[:SIMILAR_TO]->(similar:Ingredient)<-[:CONTAINS]-(ingredients:Ingredients)-[:CONTAINS_COMMON]-(recipe:Recipe)
WHERE butter <> similar
WITH recipe, COUNT(similar) AS similarityScore
RETURN recipe, similarityScore
ORDER BY similarityScore DESC
LIMIT 5;
"""

def find_similar_ingredients(driver, query):
    with driver.session() as session:
        results = session.run(query)
        for record in results:
            recipe_name = record['recipe']['name']  # Replace 'name' with the property containing the recipe name
            similarity_score = record['similarityScore']
            print(f"Recipe: {recipe_name}, Similarity Score: {similarity_score}")

# Connect to the Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Call the function to execute the query
find_similar_ingredients(driver, cypher_query)

# Close the Neo4j driver when done
driver.close()
