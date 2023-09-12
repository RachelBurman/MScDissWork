from gensim.models import Word2Vec
import pandas as pd

# Load the Word2Vec model
model = Word2Vec.load('ingredient_word2vec.model')
unique_ingredients = pd.read_csv('onetoone_mapping_90.csv', header=None, names=['Ingredient'])


ingredient_vectors = {}
for ingredient in unique_ingredients['Ingredient']:
    if ingredient in model.wv:
        ingredient_vectors[ingredient] = model.wv[ingredient]

# Print the first few entries of the ingredient_vectors dictionary
for ingredient, vector in list(ingredient_vectors.items())[:5]:
    print(f"Ingredient: {ingredient}, Vector: {vector}")