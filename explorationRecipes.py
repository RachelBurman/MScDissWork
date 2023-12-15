import matplotlib.pyplot as plt
import seaborn as sns
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

#print(gds.version())

plt.rcParams['figure.figsize'] = [10, 6]

cypher_query = gds.run_cypher("""
MATCH (i:Recipe_Embedding)-[r:REC_SIMILAR_TO]->(i2:Recipe_Embedding)
RETURN i.title AS title, COUNT(r) AS num_relationships
ORDER BY num_relationships DESC
LIMIT 5
""")

sns.set(style="whitegrid")
plt.figure()
ax = sns.barplot(x="title", y="num_relationships", data=cypher_query)
ax.set(xlabel="Recipe Name", ylabel="Number of Similar Recipes")
ax.set_title("Recipe Similarity Distribution", fontsize=16)
plt.show()


plt.show()