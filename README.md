# MSc Dissertation: Recipe & Ingredient Embedding with Graph-Based Similarity

This repository contains the experimental code written for an MSc dissertation exploring **semantic similarity between recipes and ingredients** using word embeddings, graph databases, and dimensionality reduction techniques. The goal is to surface meaningful ingredient substitutions and novel recipe ideas.

## Overview

The pipeline broadly works in four stages:

1. **Data preparation** — clean and parse raw recipe data, splitting ingredient strings into structured amount/unit/name fields
2. **Embedding generation** — produce vector representations for both ingredients (Word2Vec) and recipes (OpenAI embeddings)
3. **Graph construction** — load embeddings and relationships into a Neo4j graph database
4. **Analysis & visualisation** — project embeddings with PCA/UMAP/t-SNE, cluster them, and query for similar ingredients/recipes; use GPT-3.5 to suggest substitutions and novel recipes

## Data

| File | Description |
|---|---|
| `FooDBCSV.csv` | Raw ingredient data from FooDB |
| `Food.json` | Raw food/recipe data in JSON format |
| `merged.json` | Merged recipe dataset |
| `CurrentDF.csv` | Working recipe DataFrame |
| `mergedAllRecipes.csv` | All recipes merged into a single CSV |
| `lemmated_ingredients.csv` | Lemmatised ingredient tokens |
| `unique_ingredients.csv` | Deduplicated ingredient list |
| `mapped_ingredients*.csv` | Ingredient name mappings at various similarity thresholds (80%, 85%, 90%) |
| `onetoone_mapping*.csv` | One-to-one canonical ingredient mappings |
| `tokenized_ingredients.csv` | Tokenised ingredient strings |

## Scripts

### Data Preparation

| Script | Purpose |
|---|---|
| `SplitOnAmount.py` / `SplitOnAmount copy*.py` | Parse ingredient strings into amount, unit, and name using regex |
| `SplittingDirections.py` | Separate cooking directions from ingredient lists |
| `splitingingredients.py` / `splitingingredientsAmounts.py` | Further ingredient splitting utilities |
| `ingredientDataSplit.py` | Split ingredient data for processing |
| `tokenize_ingredients.py` | Tokenise ingredient names |
| `MergeJson2.py` / `MergeJsonOLD.py` | Merge raw JSON recipe sources |
| `jsontocsv.py` | Convert JSON recipe data to CSV |
| `truncate.py` | Truncate data files |
| `id.py` | Assign/manage IDs for records |

### Embedding Generation

| Script | Purpose |
|---|---|
| `WordEmbeddings.py` | Train a Word2Vec model on lemmatised ingredients |
| `MapIng2WordVec.py` | Map canonical ingredients to their Word2Vec vectors |
| `MappedLemons2.py` / `LemonMapping.py` / `mappingLemons.py` | Experiments mapping specific ingredients (used "lemons" as a test case) |
| `recipeEmbeddings.py` / `recipeEmbeddings8-11.py` | Load recipe OpenAI embeddings into Neo4j (`Recipe_Embedding` nodes) |
| `LoadEmbeddings.py` | General embedding loader |
| `QuerysEmbeddings.py` | Query stored embeddings |
| `word2vec_attempt.py` | Early Word2Vec experiments |

### Graph Construction (Neo4j)

| Script | Purpose |
|---|---|
| `neo4jattempt.py` | Initial Neo4j connection and Cypher query test |
| `NativeProjection.py` / `NativeProjectionTwo.py` / `NativeProjectionThree.py` / `nativeprojectionfour.py` | Build GDS graph projections over the full schema (Ingredient, Recipe, and their embeddings) |
| `RELembecipes.py` / `RELembtorecipe.py` / `RELingedienttorecipe.py` / `RELrecipetoemb.py` / `RELrecipetoingredient.py` / `RELsimilarrecipes.py` / `RELsimilarto.py` / `RELtest.py` | Create and test relationships between nodes (CONTAINS, ING\_SIMILAR\_TO, REC\_SIMILAR\_TO, etc.) |
| `traversingrelationships.py` | Traverse and inspect graph relationships |

Graph schema includes nodes: `Recipe`, `Recipe_Embedding`, `Ingredient`, `Ingredient_Embedding`
and relationships: `CONTAINS`, `USED_IN`, `ING_HAS_EMBEDDING`, `REC_HAS_EMBEDDING`, `ING_SIMILAR_TO`, `REC_SIMILAR_TO`, `REPESENTS_ING`, `REPRESENTS_RECIPE`.

### Dimensionality Reduction & Clustering

| Script | Purpose |
|---|---|
| `PCAattempt.py` / `PCAagain.py` / `PCAColour.py` | PCA projections of ingredient/recipe embeddings with KMeans clustering |
| `UMAP.py` / `umapexport.py` | UMAP projections with KMeans clustering and interactive Plotly output |
| `TSNEAttempt.py` / `tsneRecipes.py` | t-SNE projections |
| `numberofClusters.py` | Determine optimal cluster count |
| `CalinskiHarabaszScore.py` | Evaluate clustering quality with Calinski-Harabasz score |
| `daviesbouldinscore.py` | Evaluate clustering quality with Davies-Bouldin score |
| `Silhouette Score.py` | Evaluate clustering quality with Silhouette score |
| `nearestneighbours.py` / `nearestneighbours_recipes.py` | Find nearest neighbours in embedding space |
| `ingredientHeatmap.py` / `recipeHeatmap.py` / `Heatmap2.py` | Similarity heatmaps |

### Exploration & Visualisation

| Script | Purpose |
|---|---|
| `explorationIngredients.py` | Bar chart of most-connected ingredient embedding nodes |
| `explorationRecipes.py` | Bar chart of most-connected recipe embedding nodes |
| `GraphAttempt.py` | Graph visualisation attempt |

### LLM Integration (OpenAI)

| Script | Purpose |
|---|---|
| `SubstitutionsOpenAI.py` | Query GPT-3.5-turbo for vegan ingredient substitutions given nearest neighbours |
| `OpenAIRecipeGeneration.py` | Query GPT-3.5-turbo to suggest novel recipes from similar ingredients |
| `OpenAIattempt2.py` / `openaiattempt.py` / `openAIIngredients.py` | Earlier OpenAI API experiments |

### Miscellaneous

| Script | Purpose |
|---|---|
| `butterChecker.py` | Spot-check butter-related ingredient mappings |
| `explorationIngredients.py` | Exploratory ingredient queries |
| `attempt.py` | Early general-purpose experiment |
| `pdaRecipes.py` | Miscellaneous recipe processing |
| `RELembecipes.py` | Relationship loading utilities |

## Setup

### Prerequisites

- Python 3.8+
- A running **Neo4j** instance with the **Graph Data Science (GDS)** plugin installed
- An **OpenAI API key** (for substitution/recipe generation scripts)

### Install dependencies

```bash
pip install py2neo graphdatascience gensim pandas numpy scikit-learn umap-learn matplotlib seaborn plotly openai scipy
```

### Configuration

Scripts read credentials from a `keys.txt` file (not committed). Create it in the repo root:

```
API KEY = sk-...
AUTHDETAILS = ('neo4j', 'your-password')
BOLT = bolt://localhost:7687
```

## Key Models & Saved Files

- `ingredient_word2vec.model` — trained Word2Vec model for ingredient tokens

## Notes

- This is research/dissertation code; scripts are largely standalone experiments rather than a unified pipeline.
- Several scripts reference intermediate CSV files (e.g. `TESTINGDATA.csv`, `TRAININGDATA.csv`, `closest_nodes_*.csv`) that are generated by earlier steps or not included in the repository.
- `keys.txt` is excluded from version control — never commit API keys or database credentials.
