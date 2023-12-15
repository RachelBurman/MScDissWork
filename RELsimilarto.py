import numpy as np
from py2neo import Graph
import time

# Function to calculate cosine similarity
#def cosine_similarity(vec_a, vec_b):
    #try:
#        result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    #except:
    #    result = 0
    #    print(result, end=" ")
 #       return result

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

# Track processing time
start_time = time.time()
print(start_time)
# Retrieve vector property names
vector_properties_query = "MATCH (emb:Ingredient_Embedding) RETURN keys(emb) LIMIT 1"
vector_properties = graph.evaluate(vector_properties_query)
vector_properties = [prop for prop in vector_properties if prop.startswith('vector_')]

# Batch processing parameters
batch_size = 500  # Number of nodes to process in each batch
total_nodes = 17823  # Total number of nodes
threshold = 0.9  # Similarity threshold

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
    
    # Similarity calculations and relationship creation for each batch
    for emb_a in embeddings_batch:
        vec_a = np.array([emb_a[prop] for prop in vector_properties])
        
        for emb_b in embeddings_batch:
            if emb_a['name'] != emb_b['name']:  # Avoid comparing an embedding with itself
                vec_b = np.array([emb_b[prop] for prop in vector_properties])
                if (vec_b.size != 0):
                    similarity = cosine_similarity(vec_a, vec_b)
                else:
                    break
                if similarity > threshold:
                    # Check if the relationship exists in both directions
                    check_query = """
                    MATCH (a:Ingredient_Embedding {name: $name_a}), (b:Ingredient_Embedding {name: $name_b})
                    RETURN EXISTS((a)-[:ING_SIMILAR_TO]-(b)) as rel_exists
                    """
                    result = graph.evaluate(check_query, name_a=emb_a['name'], name_b=emb_b['name'])
                    
                    if not result:  # If the relationship does not exist in both directions
                        # Create ING_SIMILAR_TO relationship
                        rel_query = "MATCH (a:Ingredient_Embedding {name: $name_a}), (b:Ingredient_Embedding {name: $name_b}) MERGE (a)-[:ING_SIMILAR_TO]->(b)"
                        graph.run(rel_query, name_a=emb_a['name'], name_b=emb_b['name'])

    print(f"Finished processing batch starting at offset {offset}. Total relationships created so far: {relationship_count}")


# Print completion message
print("Similarity relationships created.")
# Record end time
end_time = time.time()

# Output processing time
print(f"Total time taken: {end_time - start_time} seconds")