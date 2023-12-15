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
MATCH (i:Ingredient_Embedding)-[r:ING_SIMILAR_TO]->(i2:Ingredient_Embedding)
RETURN i.name AS name, COUNT(r) AS num_relationships
ORDER BY num_relationships DESC
LIMIT 10
""")

sns.set(style="whitegrid")
plt.figure()
ax = sns.barplot(x="name", y="num_relationships", data=cypher_query)

# Increase font size for title and axis labels
ax.set(xlabel="Tokenised Word", ylabel="Number of Similar Words")
ax.set_title("Ingredient Word Similarity Distribution", fontsize=16) 

plt.xticks(rotation=45)
plt.tight_layout()  

plt.show()


