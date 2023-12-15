import umap
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import ast
import plotly.express as px


df = pd.read_csv('TESTINGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert list of embeddings into a 2D array
X = np.array(embedding.tolist())

# Apply UMAP
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(X)

# Apply clustering
kmeans = KMeans(n_clusters=10, random_state=42)  
cluster_labels = kmeans.fit_predict(X_umap)

# Visualization with cluster color
plt.figure(figsize=(12, 8))
plt.scatter(X_umap[:, 0], X_umap[:, 1], c=cluster_labels, cmap='viridis', alpha=0.5)
plt.colorbar(label='Cluster Label')
plt.xlabel('UMAP Feature 1')
plt.ylabel('UMAP Feature 2')
plt.title('Testing UMAP Visualization of Ingredient Embeddings')
plt.show()




df['UMAP_1'] = X_umap[:, 0]
df['UMAP_2'] = X_umap[:, 1]

# Create a Plotly scatter plot
fig = px.scatter(df, x='UMAP_1', y='UMAP_2', color=cluster_labels, hover_data=['IngredientName'])

# Customize the layout
fig.update_layout(title='Testing UMAP Visualization with Tooltips', xaxis_title='UMAP 1', yaxis_title='UMAP 2')

# Show the plot
fig.show()

# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(X_umap)
num_closest_nodes = 5  

# Prepare a list to collect data for the CSV
data_for_csv = []

for i, embedding in enumerate(X_umap):
    # Query the KDTree for nearest neighbors
    distances, indices = tree.query(embedding, k=num_closest_nodes + 1)
    
    # Get the indices of the closest nodes, excluding the node itself
    closest_indices = indices[1:]  # Exclude the first result (the node itself)
    
    # Get the names of the closest ingredients using the indices
    closest_names = df.iloc[closest_indices]['IngredientName'].values
    
    # Append the result to the data list, using df.iloc[i]['IngredientName'] for the current node's name
    data_for_csv.append([df.iloc[i]['IngredientName']] + list(closest_names))

# Create a DataFrame from the data list
columns = ['IngredientName'] + [f'Closest_Node_{i+1}' for i in range(num_closest_nodes)]
closest_df = pd.DataFrame(data_for_csv, columns=columns)

# Save the DataFrame to a CSV file
closest_df.to_csv('closest_nodes_umap_2.csv', index=False)

print("Closest nodes CSV file for UMAP results has been created.")
