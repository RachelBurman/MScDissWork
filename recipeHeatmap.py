import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from graphdatascience import GraphDataScience

keys = {}
with open('keys.txt', 'r') as f:
    for line in f:
        key, value = line.strip().split(' = ')
        keys[key] = value

# Now you can access the keys and values like this:
api_key = keys['API KEY']
auth_details = eval(keys['AUTHDETAILS'])
bolt = keys['BOLT']

gds = GraphDataScience(bolt, auth_details)

plt.rcParams['figure.figsize'] = [10, 6]

# Adjust the Cypher query to get a matrix-like data structure suitable for a heatmap
cypher_query = gds.run_cypher("""
MATCH (i:Recipe_Embedding)-[r:REC_SIMILAR_TO]->(i2:Recipe_Embedding)
WHERE i.title CONTAINS 'salad' OR i2.title CONTAINS 'salad'
RETURN i.title AS Recipe1, i2.title AS Recipe2, COUNT(r) AS Similarity
LIMIT 35
""")

# Transforming the query result into a pivot table for heatmap
#pivot_table = cypher_query.pivot(index="Recipe1", columns="Recipe2", values="Similarity")
pivot_table = cypher_query.pivot(index="Recipe1", columns="Ingredient1", values="Similarity")
pivot_table.fillna(0, inplace=True)  # Replace NaN with 0


plt.rcParams['figure.figsize'] = [12, 8] 

sns.set(style="whitegrid")
plt.figure()
ax = sns.heatmap(pivot_table, annot=True, cmap="YlGnBu")

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')


plt.subplots_adjust(bottom=0.2)  

ax.set_title("Salad Recipe Similarity Heatmap", fontsize=16)
plt.show()