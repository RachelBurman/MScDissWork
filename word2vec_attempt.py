from gensim.models import Word2Vec

# Load the Word2Vec model
model = Word2Vec.load('ingredient_word2vec.model')

# Get the list of words in the vocabulary
vocabulary_words = list(model.wv.key_to_index.keys())

# Print the first few words in the vocabulary
print("Words in the vocabulary:")
for word in vocabulary_words[:10]:  # Print the first 10 words as an example
    print(word)
