import pandas as pd
import re
from fuzzywuzzy import fuzz

# Load your lemmatized ingredient dataset and FooDB dataset
lemmatized_df = pd.read_csv('lemmated_ingredients.csv', header=None, names=['Ingredient'])
foodb_df = pd.read_csv('FooDBCSV.csv')

similarity_threshold = 70
# Create an empty mapping dictionary
ingredient_mapping = {}

# Preprocess data (convert to lowercase for consistency)
lemmatized_df['Ingredient'] = lemmatized_df['Ingredient'].str.lower()
foodb_df['food'] = foodb_df['name'].str.lower()

foodb_df = foodb_df.head(5)

# Loop through rows of foodb_df
for index, row in foodb_df.iterrows():
    # Get the lowercase 'name' from foodb_df
    foodb_name = row['name'].lower()
    matched_ingredients = []

    # Check if the ingredient from FooDB exists in the extracted dataset
    if foodb_name in lemmatized_df['Ingredient'].values:
        # Map the extracted ingredient to its category or base ingredient
        ingredient_mapping[foodb_name] = foodb_name.lower()

    for _, lemmated_row in lemmatized_df.iterrows():
        lemmated_name = lemmated_row['Ingredient']
        
        # Calculate the similarity score
        similarity_score = fuzz.token_sort_ratio(foodb_name, lemmated_name)
        
        if similarity_score >= similarity_threshold:
            matched_ingredients.append(lemmated_name)

    # Store the matches in the dictionary
    if matched_ingredients:
        ingredient_mapping[foodb_name] = matched_ingredients

# Now, ingredient_mapping contains mappings between extracted ingredients and their categories/base ingredients from FooDB
print(ingredient_mapping)

mapping_df = pd.DataFrame.from_dict(ingredient_mapping, orient='index', columns=['matched_ingredients'])

# Save the DataFrame to a CSV file without column titles
mapping_df.to_csv('mapped_ingredients2.csv', header=False)

# # Convert the dictionary to a DataFrame
# mapping_df = pd.DataFrame.from_dict(ingredient_mapping, orient='index', columns=['name'])

# # Reset the index to make the dictionary keys a regular column
# mapping_df.reset_index(inplace=True)

# # Rename the columns to 'FooDB_Ingredient' and 'Extracted_Ingredient'
# mapping_df.rename(columns={'index': 'FooDB_Ingredient'}, inplace=True)


# # Save the DataFrame to a CSV file without column titles
# mapping_df.to_csv('mapped_ingredients2.csv', index=False, header=False)

# # mapping_df = pd.DataFrame.from_dict(ingredient_mapping.items(), orient='index', columns=['Mapped_Ingredient'])

# # # Save the DataFrame to a CSV file without column titles
# # mapping_df.to_csv('mapped_ingredients2.csv', header=False)

# #ingredient_mapping.to_csv('mapped_ingredients.csv', header=False)