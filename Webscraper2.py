from allrecipes import AllRecipes

# Search:
search_string = "Almonds"  # Query
query_result = AllRecipes.search(search_string)

# Get:
main_recipe_url = query_result[18]['url']
detailed_recipe = AllRecipes.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

# Display result:
print(main_recipe_url)
print("## %s:" % detailed_recipe['name'])  # Title of the recipe
print("### For %s servings:" % detailed_recipe['nb_servings'])
for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)