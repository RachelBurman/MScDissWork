import pandas as pd

# Assuming you have a DataFrame with the column 'ingredients'
df = pd.read_csv('mergedAllRecipes.csv', encoding='latin1')  # Replace 'mergedAllRecipes.csv' with your actual CSV file name and specify the appropriate encoding

# Split the ingredients column on the comma
df['ingredients'] = df['ingredients'].str.split(';')

# Get the maximum number of ingredients in any recipe
max_num_ingredients = df['ingredients'].apply(len).max()

# Create the new column names for the amount and ingredient
amount_columns = [f'Amount {i+1}' for i in range(max_num_ingredients)]
ingredient_columns = [f'Ingredient {i+1}' for i in range(max_num_ingredients)]

# Create new DataFrames for the amounts and ingredients
amounts_df = pd.DataFrame(columns=amount_columns)
ingredients_df = pd.DataFrame(columns=ingredient_columns)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    ingredients = row['ingredients']
    amounts = []
    ingredient_names = []
    
    # Split each ingredient into amount and ingredient name
    for ingredient in ingredients:
        split_ingredient = ingredient.split(' ', 1)
        if len(split_ingredient) == 2:
            amount, ingredient_name = split_ingredient
            amounts.append(amount.strip())
            ingredient_names.append(ingredient_name.strip())
        else:
            amounts.append('')
            ingredient_names.append(ingredient.strip())
    
    # Pad the amounts list with empty strings to match the number of columns
    amounts += [''] * (max_num_ingredients - len(amounts))
    
    # Add the amounts and ingredient names to the respective DataFrames
    amounts_df.loc[index] = amounts
    ingredients_df.loc[index] = ingredient_names

# Concatenate the original DataFrame with the amounts and ingredients DataFrames
df = pd.concat([df, amounts_df, ingredients_df], axis=1)

# Drop the original ingredients column
df.drop('ingredients', axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('recipes_updated.csv', index=False)  # Replace 'recipes_updated.csv' with your desired output file name
