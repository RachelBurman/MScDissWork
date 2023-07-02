import pandas as pd

# Load the CSV data into a pandas DataFrame with the correct encoding
df = pd.read_csv('CurrentDF.csv', encoding='latin1')

# Iterate over the ingredient columns
for column in df.columns:
    if column.startswith('Ingredient'):
        # Split the ingredient column into amount and name
        split_values = df[column].str.split(' ', n=1)
        df[f'{column}_Amount'] = split_values.str[0].str.strip()
        df[f'{column}_Ingredient'] = split_values.str[1].str.strip()

# Save the modified DataFrame back to a new CSV file
df.to_csv('modified_data.csv', index=False)
