from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from scipy.spatial import KDTree


df = pd.read_csv('truncatedRecipeEmbeddings.csv')

# Assuming 'TruncatedEmbedding' is the column with the truncated embeddings
embeddings = df['TruncatedEmbedding'].apply(lambda x: eval(x))

# Convert list of embeddings into a 2D array
X = np.array(embeddings.tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply t-SNE
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200)
tsne_results = tsne.fit_transform(X_scaled)

# Visualization
plt.figure(figsize=(8, 6))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1])
plt.xlabel('t-SNE Feature 1')
plt.ylabel('t-SNE Feature 2')
plt.title('t-SNE Visualization of Embeddings')
plt.show()

tsne_df = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])

# Add the ingredient names to this DataFrame
tsne_df['RecipeName'] = df['RecipeName']

# Create the figure using Plotly Express
fig = px.scatter(tsne_df, x='TSNE1', y='TSNE2', hover_data=['RecipeName'])

# Customize the layout
fig.update_layout(title='t-SNE Visualization of Embeddings', 
                  xaxis_title='t-SNE Feature 1', 
                  yaxis_title='t-SNE Feature 2')

# Show the plot
fig.show()


# Create a KDTree for efficient nearest neighbor searches
tree = KDTree(tsne_results)
num_closest_nodes = 5 
# Prepare a list to collect data for the CSV
data_for_csv = []

for i, name in enumerate(tsne_df['RecipeName']):
    # Query the KDTree for nearest neighbors
    distances, indices = tree.query(tsne_results[i], k=num_closest_nodes + 1)
    
    # Get the names of the closest ingredients, excluding the ingredient itself
    closest_names = [tsne_df['RecipeName'][idx] for idx in indices if idx != i]
    
    # Append the result to the data list
    data_for_csv.append([name] + closest_names)

# Create a DataFrame from the data list


closest_df = pd.DataFrame(data_for_csv, columns=['Recipe'] + [f'Closest Node {i+1}' for i in range(num_closest_nodes + 1)])

closest_df.to_csv('closest_nodes_recipe_tsne.csv', index=False)

print("Closest nodes CSV file has been created.")