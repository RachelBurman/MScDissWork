import pandas as pd
import ast
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import numpy as np

df = pd.read_csv('TRAININGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert lists to a proper format for KMeans 
embedding_array = np.array(embedding.tolist())

kmeans = KMeans(n_clusters=22, n_init=10)  # Set n_init explicitly
cluster_labels = kmeans.fit_predict(embedding_array)

silhouette_avg = silhouette_score(embedding_array, cluster_labels)
print("For n_clusters =", 26, "The average silhouette_score is :", silhouette_avg)
