import pandas as pd

# Assuming you have a DataFrame with the column 'recipe'
df = pd.read_csv('recipes_updated.csv')  # Replace 'recipes.csv' with your actual CSV file name

# Split the recipe column based on the numbering pattern
df['directions'] = df['directions'].str.split('\d+\.\s')

# Get the maximum number of steps in any recipe
max_num_steps = df['directions'].apply(len).max()

# Create the new column names for steps
new_columns = [f'Step {i+1}' for i in range(max_num_steps)]

# Create new DataFrame with split recipe steps
steps_df = pd.DataFrame(df['directions'].tolist(), columns=new_columns)

# Concatenate the original DataFrame and the split steps DataFrame
df = pd.concat([df, steps_df], axis=1)

# Drop the original recipe column
df.drop('directions', axis=1, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('recipes_updated_2.csv', index=False)  # Replace 'recipes_updated.csv' with your desired output file name
