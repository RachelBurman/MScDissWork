from py2neo import Graph, Node

# Replace these values with your database configuration
host = "localhost"  # or the IP address where your Neo4j server is running
port = 7687  # the default Bolt port
username = "neo4j"
password = "password"

# Create a Py2neo Graph object to connect to your database
graph = Graph(host, auth=(username, password), port=port)

# Define and run a Cypher query to retrieve the first 25 recipe nodes
query = """
MATCH p=()-[r:CONTAINS_COMMON]->()
RETURN r
LIMIT 25
"""

result = graph.run(query)

# Print the results
for record in result:
    print(record)