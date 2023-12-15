import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('TRAININGDATA.csv')
df2 = pd.read_csv('TESTINGDATA.csv')

#'TruncatedEmbedding' is the column with the truncated embeddings
embeddings = df['embedding'].apply(lambda x: eval(x))
embeddings2 = df2['embedding'].apply(lambda x: eval(x))

# Convert list of embeddings into a 2D array
X = np.array(embeddings.tolist())
X2 = np.array(embeddings2.tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled2 = scaler.fit_transform(X2)

# Applying PCA
pca = PCA(n_components=2)  # Adjust n_components as needed
principal_components = pca.fit_transform(X_scaled)
principal_components2 = pca.fit_transform(X_scaled2)
# Explained variance
explained_variance = pca.explained_variance_ratio_
explained_variance2 = pca.explained_variance_ratio_
# Cumulative explained variance
cumulative_variance = np.cumsum(explained_variance)
cumulative_variance2 = np.cumsum(explained_variance2)

fig, axs = plt.subplots(ncols=2, figsize=(20, 5))

# Plotting Cumulative Explained Variance for the first set
axs[0].bar(range(1, len(cumulative_variance) + 1), cumulative_variance, alpha=0.5, align='center', label='Training Data: Individual explained variance')
axs[0].step(range(1, len(cumulative_variance) + 1), cumulative_variance, where='mid', label='Training Data: Cumulative explained variance')
axs[0].set_ylabel('Explained variance ratio')
axs[0].set_xlabel('Principal components')
axs[0].legend(loc='best')

# Plotting Cumulative Explained Variance for the second set
axs[1].bar(range(1, len(cumulative_variance2) + 1), cumulative_variance2, alpha=0.5, align='center', label='Testing Data: Individual explained', color='green')
axs[1].step(range(1, len(cumulative_variance2) + 1), cumulative_variance2, where='mid', label='Testing Data: Cumulative explained', color='red')
axs[1].set_ylabel('Explained variance ratio')
axs[1].set_xlabel('Principal components')
axs[1].legend(loc='best')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
# Plotting Cumulative Explained Variance

plt.bar(range(1, len(cumulative_variance) + 1), cumulative_variance, alpha=0.5, align='center', label='Individual explained variance')
plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance, where='mid', label='Cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')


plt.bar(range(1, len(cumulative_variance2) + 1), cumulative_variance2, alpha=0.5, align='center', label='Individual explained variance')
plt.step(range(1, len(cumulative_variance2) + 1), cumulative_variance2, where='mid', label='Cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# For biplot or scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2D PCA of Embeddings')
plt.show()

from scipy.spatial import KDTree

# Create a DataFrame for PCA results
pca_df = pd.DataFrame(principal_components, columns=['PCA1', 'PCA2'])
pca_df['IngredientName'] = df['IngredientName']

# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(principal_components)
num_closest_nodes = 5 

# Prepare a list to collect data for the CSV
data_for_csv = []

for i, name in enumerate(pca_df['IngredientName']):
    # Query the KDTree for nearest neighbors
    distances, indices = tree.query(principal_components[i], k=num_closest_nodes + 1)
    
    # Get the names of the closest ingredients, excluding the ingredient itself
    closest_names = [pca_df['IngredientName'][idx] for idx in indices if idx != i]
    
    # Append the result to the data list
    data_for_csv.append([name] + closest_names)

# Create a DataFrame from the data list
closest_df = pd.DataFrame(data_for_csv, columns=['Ingredient'] + [f'Closest Node {i+1}' for i in range(num_closest_nodes + 1)])

# Save the DataFrame to a CSV file
#closest_df.to_csv('closest_nodes_pca.csv', index=False)

#print("Closest nodes CSV file for PCA results has been created.")

import plotly.express as px

# Add PCA results to the DataFrame
df['PCA_1'] = principal_components[:, 0]
df['PCA_2'] = principal_components[:, 1]


from sklearn.cluster import KMeans

# Apply clustering
kmeans = KMeans(n_clusters=10)  # Adjust the number of clusters as needed
clusters = kmeans.fit_predict(X_scaled)

# Visualization with cluster color
plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1], c=clusters, cmap='viridis')
plt.xlabel('PCA Feature 1')
plt.ylabel('PCA Feature 2')
plt.title('PCA Visualization of Embeddings with Cluster Coloring')
plt.colorbar(label='Cluster Label')
plt.show()

fig = px.scatter(pca_df, x='PCA1', y='PCA2', color='Cluster', hover_data=['IngredientName'])
fig.update_layout(title='PCA Visualization of Embeddings with Clusters', 
                  xaxis_title='PCA Feature 1', 
                  yaxis_title='PCA Feature 2')
fig.show()
