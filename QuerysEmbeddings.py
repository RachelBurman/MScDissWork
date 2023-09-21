from neo4j import GraphDatabase

# Define the Cypher query

# cypher_query = """
# MATCH (i1:Ingredient {name: 'butter'}), (i2:Ingredient)
# WHERE i1 <> i2
# WITH i1, i2, i1.embedding AS embedding1, i2.embedding AS embedding2
# WITH i1, i2, embedding1, embedding2, gds.similarity.cosine(embedding1, embedding2) AS similarity
# WHERE similarity > 0.7
# RETURN i2.name AS similar_ingredient, similarity
# """

# cypher_query = """
# MATCH (i1:Ingredient)
# MATCH (i2:Ingredient)
# WHERE i1 <> i2
# WITH i1, i2, gds.similarity.cosine(i1.embedding, i2.embedding) AS similarity
# WHERE similarity > 0.6
# MERGE (i1)-[r:SIMILAR_TO]->(i2)
# SET r.score = similarity

# """

cypher_query = """
MATCH (i1:Ingredient)
MATCH (i2:Ingredient)
WHERE i1 <> i2
WITH i1, i2, gds.similarity.cosine(i1.embedding, i2.embedding) AS similarity
WHERE similarity > 0.25
CREATE (i1)-[:SIMILAR_TO {score: similarity}]->(i2)
"""
#instead of cosine can use euclidean 
#highest cosine similarity i can go to is 0.42
#highest eulidean similarity i can go is 0.94
#highest pearsons similarity i can go is 0.43

#to look at specific ingredient:
#MATCH (i1:Ingredient {name: 'dill'})-[:SIMILAR_TO]->(i2:Ingredient)
#RETURN i2.name AS recommended_ingredient
#LIMIT 5


# Execute the query
def find_similar_ingredients(driver, query):
    with driver.session() as session:
        results = session.run(query)
        for record in results:
            print(f"Ingredient: {record['similar_ingredient']}, Similarity: {record['similarity']}")

# Connect to the Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Call the function to execute the query
find_similar_ingredients(driver, cypher_query)

# Close the Neo4j driver when done
driver.close()
