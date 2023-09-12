import pandas as pd
import re

# Read the original CSV
original_df = pd.read_csv('Ingredient_Split.csv', encoding='ansi')

# Create a set to store unique ingredient names (case-insensitive and order-insensitive)
unique_ingredients = set()

# Get the maximum value of x
max_x = original_df.columns.str.extract(r'new_Ingredient (\d+)_Name', expand=False).dropna().astype(int).max()

# Define a function to normalize ingredient names
def normalize_ingredient(ingredient):
    # Convert to lowercase
    ingredient = ingredient.lower()
    
    # Remove non-alphabetic characters and extra spaces
    ingredient = re.sub(r'[^a-zA-Z\s]', '', ingredient)
    
    # Split the ingredient into words
    words = ingredient.split()
    
    # Remove "and" from the list of words
    cleaned_words = [word for word in words if word != "and"]
    
    # Sort and join the cleaned words
    return ' '.join(sorted(cleaned_words))

# Loop through each x and extract ingredient names
for x in range(1, max_x + 1):
    col_name = f'new_Ingredient {x}_Name'
    ingredients = original_df[col_name].dropna().apply(normalize_ingredient).tolist()
    unique_ingredients.update(ingredients)

# Convert the set back to a list
unique_ingredients_list = list(unique_ingredients)

# Create a DataFrame with unique ingredients
unique_df = pd.DataFrame({'Ingredient': unique_ingredients_list})

# Save the DataFrame to a new CSV without column titles
unique_df.to_csv('unique_ingredients.csv')
