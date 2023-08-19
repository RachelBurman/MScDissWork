import pandas as pd
from unicodedata import*
import re

# Read the CSV file into a DataFrame
df = pd.read_csv('CurrentDF.csv', encoding='ansi')

# Function to process the ingredient text
def process_ingredient(ingredient):
    if isinstance(ingredient, str):
        # Split the ingredient by space and look for numeric values
        parts = ingredient.split()
        amount = ""
        unit = ""
        name = ""
        info = ""
        for part in parts:
            if any(c.isdigit() for c in part) or part in ['½', '¼', '¾', '⅓', '⅔']:
                amount += part + " "
            elif any(c.isalpha() for c in part):
                unit += part + " "
            else:
                name += part + " "
        return [amount.strip(), unit.strip(), name.strip(), info.strip()]
    else:
        return ['', '', '', '']

# Apply the function to each "Ingredient" column
for col in df.columns:
    if col.startswith("Ingredient "):
        df[col] = df[col].astype(str)  # Convert the column to strings
        df[[f"{col}_Amount", f"{col}_Unit", f"{col}_Name", f"{col}_Info"]] = df[col].apply(process_ingredient).apply(pd.Series)

# Drop the original "Ingredient" columns
#df.drop(columns=[col for col in df.columns if col.startswith("Ingredient")], inplace=True)

   
# Save the updated DataFrame to a new CSV file
df.to_csv('updated_dataframe.csv', index=False)

# Iterate over the ingredient columns
    #for column in ingredient_columns:
    # Split the column into separate columns for measurement and ingredient
    #df[[f'{column}_Amount', f'{column}_Ingredient']] = df[column].str.split(' ', 1, expand=True)
