import pandas as pd
import ast

file_path = 'POOLRELU.csv'
df = pd.read_csv(file_path)

# Convert the string representations of lists into actual lists
df['embedding'] = df['embedding'].apply(ast.literal_eval)

# Find the minimum length of embeddings
min_length = min(len(embedding) for embedding in df['embedding'])

# Truncate each embedding to the minimum length
df['TruncatedEmbedding'] = df['embedding'].apply(lambda x: x[:min_length])

# Save the modified dataframe back to CSV
df.to_csv('truncatedPOOLRELU.csv', index=False)
