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
MATCH (i:Ingredient_Embedding)-[r:ING_SIMILAR_TO]->(i2:Ingredient_Embedding)
WHERE i.name CONTAINS 'crepe' OR i2.name CONTAINS 'crepe'
RETURN i.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS Similarity
LIMIT 50
""")

# Transforming the query result into a pivot table for heatmap
pivot_table = cypher_query.pivot(index="Ingredient1", columns="Ingredient2", values="Similarity")
pivot_table.fillna(0, inplace=True)  


plt.rcParams['figure.figsize'] = [12, 8]  

sns.set(style="whitegrid")
plt.figure()
ax = sns.heatmap(pivot_table, annot=True, cmap="YlGnBu")


plt.xticks(rotation=45, ha='right') 

# Adjust the bottom margin
plt.subplots_adjust(bottom=0.2)  

ax.set_title("Crepe Ingredient Similarity Heatmap", fontsize=16)
plt.show()