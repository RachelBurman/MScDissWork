from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from scipy.spatial import KDTree
import ast
from sklearn.cluster import KMeans

df = pd.read_csv('TRAININGDATA.csv')

# Convert the embedding strings to lists of floats
embedding = df['embedding'].apply(ast.literal_eval)

# Convert list of embeddings into a 2D array
X = np.array(embedding.tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply t-SNE
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200)
tsne_results = tsne.fit_transform(X_scaled)




# Apply clustering
kmeans = KMeans(n_clusters=10) 
clusters = kmeans.fit_predict(X_scaled)

# Visualization with cluster color
plt.figure(figsize=(8, 6))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=clusters, cmap='viridis')
plt.xlabel('t-SNE Feature 1')
plt.ylabel('t-SNE Feature 2')
plt.title('t-SNE Visualization of Embeddings with Cluster Coloring')
plt.colorbar(label='Cluster Label')
plt.show()



# Visualization
plt.figure(figsize=(8, 6))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1])
plt.xlabel('t-SNE Feature 1')
plt.ylabel('t-SNE Feature 2')
plt.title('t-SNE Visualization of Embeddings')
plt.show()

tsne_df = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])


tsne_df['IngredientName'] = df['IngredientName']

# Create the figure using Plotly Express
fig = px.scatter(tsne_df, x='TSNE1', y='TSNE2', hover_data=['IngredientName'])

# Customize the layout
fig.update_layout(title='t-SNE Visualization of Embeddings', 
                  xaxis_title='t-SNE Feature 1', 
                  yaxis_title='t-SNE Feature 2')

# Show the plot
fig.show()


# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(tsne_results)
num_closest_nodes = 5  #

# Prepare a list to collect data for the CSV
data_for_csv = []

for i, name in enumerate(tsne_df['IngredientName']):
    # Query the KDTree for nearest neighbors
    distances, indices = tree.query(tsne_results[i], k=num_closest_nodes + 1)
    
    # Get the names of the closest ingredients, excluding the ingredient itself
    closest_names = [tsne_df['IngredientName'][idx] for idx in indices if idx != i]
    
    # Append the result to the data list
    data_for_csv.append([name] + closest_names)

# Create a DataFrame from the data list


closest_df = pd.DataFrame(data_for_csv, columns=['Ingredient'] + [f'Closest Node {i+1}' for i in range(num_closest_nodes + 1)])

closest_df.to_csv('closest_nodesTEST.csv', index=False)

print("Closest nodes CSV file has been created.")

# Add cluster labels to the DataFrame
tsne_df['Cluster'] = clusters

# Interactive plot with Plotly
fig = px.scatter(tsne_df, x='TSNE1', y='TSNE2', color='Cluster', hover_data=['IngredientName'])
fig.update_layout(title='t-SNE Visualization of Embeddings with Clusters', 
                  xaxis_title='t-SNE Feature 1', 
                  yaxis_title='t-SNE Feature 2')
fig.show()