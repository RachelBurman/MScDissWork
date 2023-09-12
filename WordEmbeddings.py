from gensim.models import Word2Vec
import pandas as pd

# Load your tokenized and lemmatized dataset
lemmatized_df = pd.read_csv('lemmated_ingredients.csv', header=None, names=['Ingredient'])

# Tokenized ingredients should be in a list of lists format
sentences = [ingredient.split(',') for ingredient in lemmatized_df['Ingredient']]

# Train Word2Vec model
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, sg=0)

# Save the trained model
model.save('ingredient_word2vec.model')
