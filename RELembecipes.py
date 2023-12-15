import numpy as np
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

# Function to calculate cosine similarity
def cosine_similarity(vec_a, vec_b):
    vec_a = [0 if v is None else v for v in vec_a]
    vec_b = [0 if v is None else v for v in vec_b]
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


graph = Graph(bolt, auth_details)  

# Extract vector property names
vector_properties_query = "MATCH (emb:Recipe_Embedding) RETURN keys(emb) LIMIT 1"
vector_properties = graph.evaluate(vector_properties_query)
vector_properties = [prop for prop in vector_properties if prop.startswith('vector_')]

# Set batch parameters
batch_size = 500  
total_nodes = 530953  # Total number of Recipe_Embedding nodes
threshold = 0.9  # Similarity threshold

# Function to get a batch of embeddings
def get_embeddings(offset, limit):
    query = """
    MATCH (emb:Recipe_Embedding) 
    RETURN emb.id as id, 
    """ + ', '.join([f'emb.{prop} as {prop}' for prop in vector_properties]) + """
    SKIP $offset LIMIT $limit
    """
    return graph.run(query, offset=offset, limit=limit).data()

# Track processing time
start_time = time.time()

# Process in batches
for offset in range(0, total_nodes, batch_size):
    embeddings_batch = get_embeddings(offset, batch_size)
    
    # Calculate similarities and create relationships for each batch
    for i, emb_a in enumerate(embeddings_batch):
        vec_a = np.array([emb_a.get(prop, 0) for prop in vector_properties])
        for j, emb_b in enumerate(embeddings_batch):
            if i != j:
                vec_b = np.array([emb_b.get(prop, 0) for prop in vector_properties])
                similarity = cosine_similarity(vec_a, vec_b)
                if similarity > threshold:
                    rel_query = "MATCH (a:Recipe_Embedding {id: $id_a}), (b:Recipe_Embedding {id: $id_b}) MERGE (a)-[:REC_SIMILAR_TO]->(b)"
                    graph.run(rel_query, id_a=emb_a['id'], id_b=emb_b['id'])

    print(f"Processed batch starting at offset {offset}")

# Record end time
end_time = time.time()

# Output processing time
print(f"Total time taken: {end_time - start_time} seconds")
