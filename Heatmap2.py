import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from graphdatascience import GraphDataScience


host = "bolt://localhost:7687"  
username = "neo4j"
password = "ingredients"

gds = GraphDataScience(host, auth=(username, password))

plt.rcParams['figure.figsize'] = [10, 6]



cypher_query = gds.run_cypher("""
    MATCH (i:Recipe_Embedding)-[r:REC_SIMILAR_TO]->(i2:Recipe_Embedding)
    MATCH (in:Ingredient_Embedding)-[b:ING_SIMILAR_TO]->(in2:Ingredient_Embedding)
    WHERE (i.title CONTAINS 'salad') AND 
        (in.name CONTAINS 'water') 
    RETURN i.title AS Recipe1, in.name AS Ingredient1, COUNT(r) AS Similarity
    LIMIT 20
""")

cypher_query2 = gds.run_cypher("""
    MATCH (i:Recipe_Embedding)-[r:REC_SIMILAR_TO]->(i2:Recipe_Embedding)
    MATCH (in:Ingredient_Embedding)-[b:ING_SIMILAR_TO]->(in2:Ingredient_Embedding)
    WHERE (i.title CONTAINS 'salad') AND 
        (in.name CONTAINS 'salt') 
    RETURN i.title AS Recipe1, in.name AS Ingredient2, COUNT(r) AS Similarity
    LIMIT 20
""")

# Transforming the query result into a pivot table for heatmap
#pivot_table = cypher_query.pivot(index="Recipe1", columns="Recipe2", values="Similarity")
pivot_table = cypher_query.pivot(index="Recipe1", columns="Ingredient1", values="Similarity")
pivot_table2 = cypher_query2.pivot(index="Recipe1", columns="Ingredient2", values="Similarity")
pivot_table.fillna(0, inplace=True)  
pivot_table2.fillna(0, inplace=True)  

plt.rcParams['figure.figsize'] = [12, 8]  

sns.set(style="whitegrid")
plt.figure()
ax = sns.heatmap(pivot_table, annot=True, cmap="YlGnBu")


plt.xticks(rotation=45, ha='right')  


plt.subplots_adjust(bottom=0.2)  

ax.set_title("Water-Salad Recipe Similarity Heatmap", fontsize=16)
ax.set_xlabel('Ingredient')  
ax.set_ylabel('Recipe')  
plt.show()

fig, axs = plt.subplots(ncols=2, figsize=(24, 8))  # Create a figure with two subplots

# First heatmap
sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", ax=axs[0])
axs[0].set_title("Water-Salad Recipe Similarity Heatmap", fontsize=16)
axs[0].set_xlabel('Ingredient')
axs[0].set_ylabel('Recipe')
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, horizontalalignment='right')

# Second heatmap
sns.heatmap(pivot_table2, annot=True, cmap="YlGnBu", ax=axs[1])
axs[1].set_title("Salt-Salad Recipe Similarity Heatmap", fontsize=16)
axs[1].set_xlabel('Ingredient')
axs[1].set_ylabel('Recipe')
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, horizontalalignment='right')

plt.tight_layout()  # Ensure the subplots do not overlap
plt.show()