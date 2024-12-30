import pandas as pd
import json
import os
import re

try:
    # Load the dataset
    data_path = "data/full_dataset_with_nutriscore.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    data = pd.read_csv(data_path)
    print(f"Dataset loaded successfully from {data_path}")

    # Function to clean ingredient strings
    def clean_ingredient(ingredient):
        # Remove special characters and extra whitespace
        cleaned = re.sub(r'[^\w\s]', '', ingredient)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    # Extract unique ingredients from the NER field
    unique_ingredients = set()
    for ner_list in data['NER']:
        ingredients = eval(ner_list) if isinstance(ner_list, str) else ner_list
        cleaned_ingredients = [clean_ingredient(ing) for ing in ingredients]
        unique_ingredients.update(cleaned_ingredients)

    # Convert the set to a list and sort it
    unique_ingredients = sorted(list(unique_ingredients))

    # Save the unique ingredients to a JSON file
    with open("unique_ingredients.json", "w") as f:
        json.dump(unique_ingredients, f, indent=4)

    print(f"Unique ingredients saved to unique_ingredients.json")

except Exception as e:
    print(f"An error occurred: {e}")