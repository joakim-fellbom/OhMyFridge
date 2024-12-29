import pandas as pd
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.nutriscore_calculator import calculate_nutriscore

# Load the CSV data
data = pd.read_csv("full_dataset.csv")
data['ingredients'] = data['ingredients'].apply(eval)  # Convert string to Python list

# Add nutriscore to the dataset
data['nutriscore'] = data['ingredients'].apply(calculate_nutriscore)

# Keep only the desired columns
data = data[['title', 'ingredients', 'directions', 'nutriscore']]

# Save the updated dataset to a new CSV file
data.to_csv("full_dataset_with_nutriscore.csv", index=False)