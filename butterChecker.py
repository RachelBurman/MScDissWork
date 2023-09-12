from gensim.models import Word2Vec

# Load the Word2Vec model
model = Word2Vec.load('ingredient_word2vec.model')

# Check if 'butter' is in the vocabulary
word_to_check = 'oil'
if word_to_check in model.wv.key_to_index:
    vector = model.wv[word_to_check]
    print(f"Vector for '{word_to_check}': {vector}")
else:
    print(f"'{word_to_check}' not found in the vocabulary.")


# Get the vector for a specific ingredient
vector = model.wv[word_to_check]

# Find similar ingredients based on vector similarity
similar_ingredients = model.wv.most_similar(word_to_check, topn=5)

print("Vector for 'oil':", vector)
print("Similar ingredients to 'oil':", similar_ingredients)
