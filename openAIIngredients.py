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

df = pd.read_csv('closest_nodesTEST.csv')

print(df['Ingredient'].tolist())

for ingredient in df['Ingredient']:
    clean_ingredient = ingredient.strip().lower()
    if clean_ingredient == 'salt':
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"What are some good ingredient pairings for {ingredient}?"}
                ]
            )
            # Extracting the response text
            if response['choices']:
                answer = response['choices'][0]['message']['content']
                print(f"Pairings for {ingredient}: {answer}")
            else:
                print(f"No response for {ingredient}.")
            break  # If 'salt' is found and processed, exit the loop
        except Exception as e:
            print(f"Error with ingredient {ingredient}: {e}")
            break  # Exit the loop if there's an error
