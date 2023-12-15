import umap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast

df = pd.read_csv('TESTINGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert list of embeddings into a 2D array
X = np.array(embedding.tolist())

# Apply UMAP
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(X)

# Visualization
from sklearn.cluster import KMeans

# Cluster the data
kmeans = KMeans(n_clusters=10, random_state=42) 
cluster_labels = kmeans.fit_predict(X)

# Apply UMAP
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(X)

# Visualization with cluster color
plt.figure(figsize=(12, 8))
plt.scatter(X_umap[:, 0], X_umap[:, 1], c=cluster_labels, cmap='viridis', alpha=0.5)
plt.colorbar(label='Cluster Label')
plt.xlabel('UMAP Feature 1')
plt.ylabel('UMAP Feature 2')
plt.title('Testing UMAP Visualization of Ingredient Embeddings')
plt.show()

import plotly.express as px


df['UMAP_1'] = X_umap[:, 0]
df['UMAP_2'] = X_umap[:, 1]

# Create a Plotly scatter plot
fig = px.scatter(df, x='UMAP_1', y='UMAP_2', color=cluster_labels, hover_data=['IngredientName'])

# Customize the layout
fig.update_layout(title='Testing UMAP Visualization with Tooltips', xaxis_title='UMAP 1', yaxis_title='UMAP 2')

# Show the plot
fig.show()