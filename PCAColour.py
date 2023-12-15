import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('TESTINGDATA.csv')

# Convert the string representations of lists into actual lists
df['embedding'] = df['embedding'].apply(lambda x: eval(x))

# Calculate the sum of absolute values for each embedding as a sorting measure
df['EmbeddingSum'] = df['embedding'].apply(lambda x: sum(abs(np.array(x))))

# Sort by 'EmbeddingSum' and select the top 50 items
df_top50 = df.nlargest(50, 'EmbeddingSum')

# Convert list of embeddings into a 2D array for the top 50 items
X_top50 = np.array(df_top50['embedding'].tolist())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_top50)

# Applying PCA
pca = PCA(n_components=2)  # Adjust n_components as needed
principal_components = pca.fit_transform(X_scaled)

# Explained variance
explained_variance = pca.explained_variance_ratio_

# For biplot or scatter plot
plt.figure(figsize=(10, 8))  # Width, Height

# Create a scatter plot and color it by the group labels of the top 50 items
sns.scatterplot(x=principal_components[:, 0], y=principal_components[:, 1], 
                hue=df_top50['IngredientName'], palette='viridis')  

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2D PCA of Top 50 Embeddings')
#plt.legend(title='Ingredient', loc='best', fancybox=True, framealpha=0.5)  
plt.legend(title='Ingredient', loc='upper left', fontsize='small',  bbox_to_anchor=(1,1))
plt.tight_layout()
plt.show()


#plt.legend(title='Ingredient', loc='best', fancybox=True, framealpha=0.5)  

#plt.savefig('pca80.png', bbox_inches='tight')
