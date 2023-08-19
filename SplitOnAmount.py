import pandas as pd
from unicodedata import*
import re

# Read the CSV file into a DataFrame
df = pd.read_csv('CurrentDF.csv', encoding='ansi')

#Function to extract amount, unit, and ingredient name
def process_ingredient(ingredient):
    pattern = r'(?P<Amount>[\d\s/½¼¾⅓¾]+)?\s?(?P<Unit>(?!(?:egg\s*(?:whites?|yolks?|s)?))[a-zA-Z]+)?\s?(?P<Name>.*)'
    match = re.match(pattern, ingredient)
    amount = match.group('Amount').strip() if match.group('Amount') else ''
    unit = match.group('Unit').strip() if match.group('Unit') else ''
    name = match.group('Name').strip() if match.group('Name') else ''

    return [amount, unit, name]

#Apply function to each "Ingredient" Coumn
for col in df.columns: 
    if col.startswith("Ingredient"):
        df[col] = df[col].astype(str)
        processed_data = df[col].apply(process_ingredient)
        df[[f"new_{col}_Amount", f"new_{col}_Unit", f"new_{col}_Name"]] = processed_data.apply(pd.Series)
        #df[[f"new_{col}_Amount", f"new_{col}_Unit", f"new_{col}_Name"]]  = df[col].apply(process_ingredient).apply(pd.Series)

#Drop the original "Ingredient" columns
df.drop(columns=[col for col in df.columns if col.startswith("Ingredient")], inplace=True)

   
# Save the updated DataFrame to a new CSV file
df.to_csv('Ingredient_Split.csv', index=False)

# Iterate over the ingredient columns
    #for column in ingredient_columns:
    # Split the column into separate columns for measurement and ingredient
    #df[[f'{column}_Amount', f'{column}_Ingredient']] = df[column].str.split(' ', 1, expand=True)
