from py2neo import Graph
import csv

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "ingredients"))

# Read the CSV file
with open('NERMapped.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Start processing from the 8570th row
    for i, row in enumerate(reader):
        if i >= 8570:  # Skip rows until the 8570th
            ingredient_name = row['Ingredient']  # Assuming 'Ingredient' is the header for ingredient names
            embeddings = [float(row[key]) for key in row if key != 'Ingredient' and row[key].replace('.', '', 1).isdigit()]

            properties = {f'vector_{i}': embedding for i, embedding in enumerate(embeddings)}

            query = """
            MERGE (ingredient:Ingredient_Embedding {name: $name})
            SET ingredient += $properties
            """
            graph.run(query, name=ingredient_name, properties=properties)
