import openai
import pandas as pd

openai.api_key = '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'

recipe_df = pd.read_csv('closest_recipes_pca.csv')
ingredient_df = pd.read_csv('closest_nodes_umap_2.csv')

# Loop through each row in the DataFrame
for index, row in recipe_df.iterrows():
    recipe = row['RecipeName']
    for index, row in ingredient_df.iterrows():
        ingredient = row['IngredientName']

        closest_nodes = [row[f'Closest_Node_{i}'] for i in range(1, 6)]  # get all closest nodes
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Could you suggest a novel recipe utilizing {ingredient} and {closest_nodes} based upon {recipe}?"}
                ]
            )
            # Extracting the response text
            answer = response['choices'][0]['message']['content'] if response['choices'] else "No response"
            print(f"Novel recipe using {ingredient} and {closest_nodes} based upon {recipe}: {answer}")
        except Exception as e:
            print(f"Error with ingredient {ingredient}: {e}")