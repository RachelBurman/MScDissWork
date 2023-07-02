import pandas as pd

# Assuming you have a DataFrame with the column 'ingredients'
df = pd.read_csv('mergedAllRecipes.csv')  # Replace 'recipes.csv' with your actual CSV file name

# Split the ingredients column on the comma
df['ingredients'] = df['ingredients'].str.split(';')

# Get the maximum number of ingredients in any recipe
max_num_ingredients = df['ingredients'].apply(len).max()

# Create the new column names
new_columns = [f'Ingredient {i+1}' for i in range(max_num_ingredients)]

# Create new DataFrame with split ingredients
ingredients_df = pd.DataFrame(df['ingredients'].tolist(), columns=new_columns)

# Concatenate the original DataFrame and the split ingredients DataFrame
df = pd.concat([df, ingredients_df], axis=1)

# Drop the original ingredients column
df.drop('ingredients', axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('recipes_updated.csv', index=False)  # Replace 'recipes_updated.csv' with your desired output file name
