
# Data Cleaning

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from food_modules import feature_engg

# Load Data
df = pd.read_csv(r'data/IndianFoodDatasetCSV.csv')

# Drop Null values from the dataset
df.dropna(axis=0, inplace=True)

# Translation
## Ingredients
df['TranslatedIngredients'] = df['TranslatedIngredients'].str.lower() # Convert to lower case

df['TranslatedIngredients'] = df['TranslatedIngredients'].apply(feature_engg.find_hi) # Translate the ingredients

df['TranslatedIngredients'] = [x[0].split(",") for x in df['TranslatedIngredients']] # Split the ingredients in each row (list)

## Instructions
df['TranslatedInstructions'] = df['TranslatedInstructions'].str.lower() # Convert to lower case

df['TranslatedInstructions'] = df['TranslatedInstructions'].apply(feature_engg.find_hi) # Translate the instructions

## Recipe Name
df['RecipeName'] = df['RecipeName'].str.lower() # Convert to lower case

df['RecipeName'] = df['RecipeName'].apply(feature_engg.find_hi) # Translate the Recipe Name

# All masalas used in the dish
df['masalas_used'] = df['TranslatedIngredients'].apply(lambda x: feature_engg.trim_masala(x))

# Number of Masalsa used in the dish
df['masala#'] = df['masala_used'].apply(lambda x: len(x))

# All vegetables used in the dish
df['veggies_used'] = df['TranslatedIngredients'].apply(lambda x: feature_engg.trim_veggies(x))

# Number of vegetables used in the dish
df['veggie#'] = df['masala_used'].apply(lambda x: len(x))

# Ingredient numbers
df['ingredients#'] = df.TranslatedIngredients.apply(lambda x: [feature_engg.value_ing(i) for i in x[1:-2].split(',')])

# Convert to proper list
df['TranslatedIngredients'] = df['TranslatedIngredients'].apply(feature_engg.clean_list) # Ingredients

df['RecipeName'] = df['RecipeName'].apply(lambda x: x[2:-2]) # Recipe Name

## Save the file
df.to_csv("data/cleaned.csv", index=False)
