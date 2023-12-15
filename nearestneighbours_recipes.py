from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import ast
import csv


df = pd.read_csv('truncatedRecipeEmbeddings.csv')

# 'TruncatedEmbedding' is the column with the truncated embeddings
embeddings = df['TruncatedEmbedding'].apply(lambda x: eval(x))

# Convert list of embeddings into a 2D array
X = np.array(embeddings.tolist())

nbrs = NearestNeighbors(n_neighbors=6, metric='cosine').fit(X)  # 5 neighbors plus the ingredient itself
distances, indices = nbrs.kneighbors(X)


# Open a file to write the nearest neighbors into
with open('nearest_neighbors_recipes.csv', 'w', newline='', encoding='utf-8') as file:

    recipe_names = df['RecipeName'].tolist()  
    for i, name in enumerate(recipe_names):
        nearest_indices = indices[i][1:]  # Skip the first one because it will be the ingredient itself
        nearest_names = [recipe_names[j] for j in nearest_indices]
    
    print(f"Nearest neighbors for {name}: {nearest_names}")
    writer = csv.writer(file)
    writer.writerow(["Recipe", "Nearest Neighbors"])  # Writing the header

    for i, name in enumerate(recipe_names):
        nearest_indices = indices[i][1:]  # Skip the first one because it will be the ingredient itself
        nearest_names = [recipe_names[j] for j in nearest_indices]
        writer.writerow([name, ", ".join(nearest_names)])

print("Nearest neighbors have been written to nearest_neighbors_recipes.csv")

