import pandas as pd
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.nutriscore_calculator import calculate_nutriscore
from logic.regime_calculator import vege, gluten_free

# Load the CSV data
data = pd.read_csv("data/full_dataset.csv")
data['ingredients'] = data['ingredients'].apply(eval)  # Convert string to Python list

# Add nutriscore to the dataset
data['nutriscore'] = data['ingredients'].apply(calculate_nutriscore)
data['vege'] = data['ingredients'].apply(vege)
data['gluten_free'] = data['ingredients'].apply(gluten_free)

# Keep only the desired columns
data = data[['title', 'ingredients', 'directions', 'nutriscore', 'vege', 'gluten_free']]

# Save the updated dataset to a new CSV file
data.to_csv("full_dataset_with_nutriscore.csv", index=False)