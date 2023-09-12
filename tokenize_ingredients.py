import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize
import pandas as pd
from nltk.stem import WordNetLemmatizer

#nltk.download('punkt')
#nltk.download('wordnet')

unique_ingredients = pd.read_csv('unique_ingredients.csv', encoding='ansi')

# Create an empty list to store tokenized ingredients
tokenized_ingredients = []
lemmatizer = WordNetLemmatizer()


for index, row in unique_ingredients.iterrows():
    ingredient_description = row['Ingredient']
    words = word_tokenize(ingredient_description)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in words]
    tokenized_ingredients.extend(lemmatized_tokens)

# Create a DataFrame with unique ingredients
lemmatized_ingredient_df = pd.DataFrame({'Ingredient': tokenized_ingredients})

# Save the DataFrame to a new CSV without column titles
lemmatized_ingredient_df.to_csv('lemmated_ingredients.csv', header=False)