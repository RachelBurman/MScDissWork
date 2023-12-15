import pandas as pd
import ast
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('TRAININGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert lists to a proper format for KMeans (list of lists to 2D array)
embedding_array = np.array(embedding.tolist())

kmeans = KMeans(n_clusters=5, n_init=10)  # Set n_init explicitly
cluster_labels = kmeans.fit_predict(embedding_array)

silhouette_avg = silhouette_score(embedding_array, cluster_labels)
print("For n_clusters =", 5, "The average silhouette_score is :", silhouette_avg)

silhouette_scores = []
for i in range(2, 11):  # Example range
    kmeans = KMeans(n_clusters=i)
    cluster_labels = kmeans.fit_predict(embedding_array)
    score = silhouette_score(embedding_array, cluster_labels)
    silhouette_scores.append(score)

plt.plot(range(2, 11), silhouette_scores)
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()
