import numpy as np
from py2neo import Graph
import time

def cosine_similarity(vec_a, vec_b):
    if any(x is None for x in vec_a) or any(x is None for x in vec_b):
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


start_time = time.time()

# Retrieve vector property titles
vector_properties_query = "MATCH (emb:Recipe_Embedding) RETURN keys(emb) LIMIT 1"
vector_properties = graph.evaluate(vector_properties_query)
vector_properties = [prop for prop in vector_properties if prop.startswith('vector_')]

# Batch processing parameters
batch_size = 500
total_nodes = 530953
threshold = 0.5

# Function to get a batch of embeddings
def get_embeddings(offset, limit):
    query = """
    MATCH (emb:Recipe_Embedding) 
    RETURN emb.title as title, 
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
            if emb_a['title'] != emb_b['title']:
                vec_b = np.array([emb_b[prop] for prop in vector_properties])

                similarity = cosine_similarity(vec_a, vec_b)
                if similarity > threshold:
                    try:
                        # Check if the relationship exists in both directions
                        check_query = """
                        MATCH (a:Recipe_Embedding {title: $title_a}), (b:Recipe_Embedding {title: $title_b})
                        RETURN EXISTS((a)-[:RECIPE_SIMILAR_TO]-(b)) as rel_exists
                        """
                        result = graph.evaluate(check_query, title_a=emb_a['title'], title_b=emb_b['title'])
                        
                        if not result:
                            # Create RECIPE_SIMILAR_TO relationship
                            rel_query = "MATCH (a:Recipe_Embedding {title: $title_a}), (b:Recipe_Embedding {title: $title_b}) MERGE (a)-[:RECIPE_SIMILAR_TO]->(b)"
                            graph.run(rel_query, title_a=emb_a['title'], title_b=emb_b['title'])
                            relationship_count += 1
                    except Exception as e:
                        print(f"Error at relationship {relationship_count}: {e}")
                        
# Record end time
end_time = time.time()

# Output processing time and completion status
print(f"Total relationships created: {relationship_count}")
print(f"Total time taken: {end_time - start_time} seconds")
print("Similarity relationships creation process completed.")
