import openai
import pandas as pd

keys = {}
with open('keys.txt', 'r') as f:
    for line in f:
        key, value = line.strip().split(' = ')
        keys[key] = value

# Now you can access the keys and values like this:
api_key = keys['API KEY']
auth_details = eval(keys['AUTHDETAILS'])
bolt = keys['BOLT']

openai.api_key = api_key

df = pd.read_csv('closest_nodes_PCA_2.csv')

# Loop through each ingredient in the 'Ingredient' column
for ingredient in df['IngredientName']:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"What are some good ingredient pairings for {ingredient}?"}
            ]
        )
        # Extracting the response text
        answer = response['choices'][0]['message']['content'] if response['choices'] else "No response"
        print(f"Pairings for {ingredient}: {answer}")
    except Exception as e:
        print(f"Error with ingredient {ingredient}: {e}")