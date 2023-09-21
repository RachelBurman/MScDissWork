from py2neo import Graph, Node
from gensim.models import Word2Vec
import pandas as pd
import numpy as np  # Import NumPy for array operations

# Replace these values with your database configuration
host = "localhost"  # or the IP address where your Neo4j server is running
port = 7687  # the default Bolt port
username = "neo4j"
password = "password"

# Create a Py2neo Graph object to connect to your database
graph = Graph(host, auth=(username, password), port=port)

model = Word2Vec.load('ingredient_word2vec.model')
unique_ingredients = pd.read_csv('onetoone_mapping_90.csv', header=None, names=['Ingredient'])

# Assuming unique_ingredients is a DataFrame containing your unique ingredients
for ingredient in unique_ingredients['Ingredient']:
    # Check if the ingredient exists in the model
    if ingredient in model.wv:
        # Convert the NumPy array to a Python list
        embedding_list = model.wv[ingredient].tolist()
        
        # Create a Neo4j node for the ingredient and add the embedding as a property (as a list)
        node = Node("Ingredient", name=ingredient, embedding=embedding_list)
        graph.create(node)
