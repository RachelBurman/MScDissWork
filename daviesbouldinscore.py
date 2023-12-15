from sklearn.metrics import davies_bouldin_score
import pandas as pd
import ast
from sklearn.cluster import KMeans
import numpy as np

df = pd.read_csv('TESTINGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert lists to a proper format for KMeans 
embedding_array = np.array(embedding.tolist())

kmeans = KMeans(n_clusters=12, n_init=10)  # Set n_init explicitly
cluster_labels = kmeans.fit_predict(embedding_array)

score = davies_bouldin_score(embedding_array, cluster_labels)
print("Davies-Bouldin Score: ", score)






