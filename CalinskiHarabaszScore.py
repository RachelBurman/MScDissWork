from sklearn.metrics import calinski_harabasz_score
import pandas as pd
import ast
from sklearn.cluster import KMeans
import numpy as np

df = pd.read_csv('TRAININGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert lists to a proper format for KMeans (list of lists to 2D array)
embedding_array = np.array(embedding.tolist())

kmeans = KMeans(n_clusters=18, n_init=10)  
# Set n_init explicitly
cluster_labels = kmeans.fit_predict(embedding_array)

score = calinski_harabasz_score(embedding_array, cluster_labels)  
# Use embedding_array instead of embedding
print("Calinski-Harabasz Score: ", score)