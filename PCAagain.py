import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
import ast
from scipy.spatial import KDTree

df = pd.read_csv('TESTINGDATA.csv')

embeddings = df['embedding'].apply(lambda x: ast.literal_eval(x))

# Convert list of embeddings into a 2D array
X = np.array(embeddings.tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Applying PCA
pca = PCA(n_components=2)  # Adjust n_components as needed
principal_components = pca.fit_transform(X_scaled)

# Add PCA results to the DataFrame
df['PCA_1'] = principal_components[:, 0]
df['PCA_2'] = principal_components[:, 1]

# Apply clustering
kmeans = KMeans(n_clusters=10, random_state=42)  # Adjust the number of clusters as needed
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualization with cluster color using Matplotlib
plt.figure(figsize=(8, 6))
plt.scatter(df['PCA_1'], df['PCA_2'], c=df['Cluster'], cmap='viridis')
plt.xlabel('PCA Feature 1')
plt.ylabel('PCA Feature 2')
plt.title('PCA Visualization of Embeddings with Cluster Coloring')
plt.colorbar(label='Cluster Label')
plt.show()

# Visualization with cluster color using Plotly Express
fig = px.scatter(df, x='PCA_1', y='PCA_2', color='Cluster', hover_data=['IngredientName'])
fig.update_layout(title='PCA Visualization of Embeddings with Clusters', 
                  xaxis_title='PCA Feature 1', 
                  yaxis_title='PCA Feature 2')
fig.show()

# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(principal_components)
num_closest_nodes = 5  # Define the number of closest nodes 

# Prepare a list to collect data for the CSV
data_for_csv = []

for i, embedding in enumerate(principal_components):
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
closest_df.to_csv('closest_nodes_PCA_2.csv', index=False)

print("Closest nodes CSV file for PCA results has been created.")
