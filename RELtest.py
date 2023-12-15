import numpy as np
from py2neo import Graph
import time

# Function to calculate cosine similarity
def cosine_similarity(vec_a, vec_b):
    if None in vec_a or None in vec_b:
        print(f"Invalid vector encountered. Skipping similarity calculation.")
        return 0
    try:
        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    except Exception as e:
        print(f"Error in cosine similarity calculation: {e}")
        return 0


graph = Graph("bolt://localhost:7687", auth=("neo4j", "ingredients"))

# Track processing time
start_time = time.time()

# Retrieve vector property names
vector_properties_query = "MATCH (emb:Ingredient_Embedding) RETURN keys(emb) LIMIT 1"
vector_properties = graph.evaluate(vector_properties_query)
vector_properties = [prop for prop in vector_properties if prop.startswith('vector_')]

# Batch processing parameters
batch_size = 500
total_nodes = 17823
threshold = 0.9

# Function to get a batch of embeddings
def get_embeddings(offset, limit):
    query = """
    MATCH (emb:Ingredient_Embedding) 
    RETURN emb.name as name, 
    """ + ', '.join([f'emb.{prop} as {prop}' for prop in vector_properties]) + """
    SKIP $offset LIMIT $limit
    """
    return graph.run(query, offset=offset, limit=limit).data()

# Initialize relationship count
relationship_count = 0

# Process batches of embeddings
for offset in range(0, total_nodes, batch_size):
    embeddings_batch = get_embeddings(offset, batch_size)
    
    for emb_a in embeddings_batch:
        vec_a = np.array([emb_a[prop] for prop in vector_properties])

        for emb_b in embeddings_batch:
            if emb_a['name'] != emb_b['name']:
                vec_b = np.array([emb_b[prop] for prop in vector_properties])

                similarity = cosine_similarity(vec_a, vec_b)
                if similarity > threshold:
                    try:
                        # Check if the relationship exists in both directions
                        check_query = """
                        MATCH (a:Ingredient_Embedding {name: $name_a}), (b:Ingredient_Embedding {name: $name_b})
                        RETURN EXISTS((a)-[:TEST]-(b)) as rel_exists
                        """
                        result = graph.evaluate(check_query, name_a=emb_a['name'], name_b=emb_b['name'])
                        
                        if not result:
                            # Create ING_SIMILAR_TO relationship
                            rel_query = "MATCH (a:Ingredient_Embedding {name: $name_a}), (b:Ingredient_Embedding {name: $name_b}) MERGE (a)-[:TEST]->(b)"
                            graph.run(rel_query, name_a=emb_a['name'], name_b=emb_b['name'])
                            relationship_count += 1
                    except Exception as e:
                        print(f"Error at relationship {relationship_count}: {e}")

    print(f"Finished processing batch starting at offset {offset}. Total relationships created so far: {relationship_count}")

# Record end time
end_time = time.time()

# Output processing time and completion status
print(f"Total relationships created: {relationship_count}")
print(f"Total time taken: {end_time - start_time} seconds")
print("Similarity relationships creation process completed.")
