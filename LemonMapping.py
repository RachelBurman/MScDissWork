import pandas as pd
from fuzzywuzzy import fuzz

# Load your lemmatized ingredient dataset and FooDB dataset
lemmatized_df = pd.read_csv('lemmated_ingredients.csv', header=None, names=['Ingredient'])
foodb_df = pd.read_csv('FooDBCSV.csv')

similarity_threshold = 90

# Create an empty DataFrame to store the results
mapping_df = pd.DataFrame(columns=['foodb_name', 'Mapped_Ingredient'])

# Preprocess data (convert to lowercase for consistency)
lemmatized_df['Ingredient'] = lemmatized_df['Ingredient'].str.lower()
foodb_df['food'] = foodb_df['name'].str.lower()

#foodb_df = foodb_df.head(10)

# Loop through rows of foodb_df
for index, row in foodb_df.iterrows():
    # Get the lowercase 'name' from foodb_df
    foodb_name = row['food']
    matched_ingredients = []

    # Check if the ingredient from FooDB exists in the extracted dataset
    if foodb_name in lemmatized_df['Ingredient'].values:
        # Map the extracted ingredient to its category or base ingredient
        ingredient_mapping = {'foodb_name': foodb_name, 'Mapped_Ingredient': foodb_name}
        mapping_df = mapping_df.append(ingredient_mapping, ignore_index=True)

    for _, lemmated_row in lemmatized_df.iterrows():
        lemmated_name = lemmated_row['Ingredient']
        
        # Calculate the similarity score
        similarity_score = fuzz.token_sort_ratio(foodb_name, lemmated_name)
        
        if similarity_score >= similarity_threshold:
            matched_ingredients.append(lemmated_name)

    # Store the matches in the DataFrame
    if matched_ingredients:
        for matched_ingredient in matched_ingredients:
            ingredient_mapping = {'foodb_name': foodb_name, 'Mapped_Ingredient': matched_ingredient}
            mapping_df = mapping_df.append(ingredient_mapping, ignore_index=True)

# Save the DataFrame to a CSV file without column titles
mapping_df.to_csv('mapped_ingredients90.csv', header=False)
