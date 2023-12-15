import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('truncatedRecipeEmbeddings.csv')

# Assuming 'TruncatedEmbedding' is the column with the truncated embeddings
embeddings = df['TruncatedEmbedding'].apply(lambda x: eval(x))

# Convert list of embeddings into a 2D array
X = np.array(embeddings.tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Applying PCA
pca = PCA(n_components=2)  
principal_components = pca.fit_transform(X_scaled)

# Explained variance
explained_variance = pca.explained_variance_ratio_

# Cumulative explained variance
cumulative_variance = np.cumsum(explained_variance)

# Plotting Cumulative Explained Variance
plt.figure(figsize=(8, 5))
plt.bar(range(1, len(cumulative_variance) + 1), cumulative_variance, alpha=0.5, align='center', label='Individual explained variance')
plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance, where='mid', label='Cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2D PCA of Embeddings')
plt.show()

from scipy.spatial import KDTree

# Create a DataFrame for PCA results
pca_df = pd.DataFrame(principal_components, columns=['PCA1', 'PCA2'])
pca_df['RecipeName'] = df['RecipeName']

# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(principal_components)
num_closest_nodes = 5 

data_for_csv = []

for i, name in enumerate(pca_df['RecipeName']):
    # Query the KDTree for nearest neighbors
    distances, indices = tree.query(principal_components[i], k=num_closest_nodes + 1)
    
    # Get the names of the closest ingredients, excluding the ingredient itself
    closest_names = [pca_df['RecipeName'][idx] for idx in indices if idx != i]
    
    # Append the result to the data list
    data_for_csv.append([name] + closest_names)

# Create a DataFrame from the data list
closest_df = pd.DataFrame(data_for_csv, columns=['RecipeName'] + [f'Closest Node {i+1}' for i in range(num_closest_nodes + 1)])

# Save the DataFrame to a CSV file
closest_df.to_csv('closest_recipes_pca.csv', index=False)

print("Closest nodes CSV file for PCA results has been created.")

