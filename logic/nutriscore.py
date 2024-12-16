import pandas as pd
import re
from collections import Counter
from typing import List, Set
import os

class IngredientParser:
    def __init__(self):
        self.quantity_patterns = [
            r'\d+(/\d+)?',  # Matches fractions like 1/2
            r'\d*\.?\d+',   # Matches decimal numbers
            r'one|two|three|four|five|six|seven|eight|nine|ten',  # Written numbers
            r'dozen|half|quarter'  # Common quantity words
        ]
        
        self.measurement_units = [
            r'\bc\b|\bcup(s)?\b',  # cups
            r'\btsp\.?|\bteaspoon(s)?\b',  # teaspoons
            r'\btbsp\.?|\btablespoon(s)?\b',  # tablespoons
            r'\boz\.?|\bounce(s)?\b',  # ounces
            r'\blb\.?|\bpound(s)?\b',  # pounds
            r'\bpkg\.?|\bpackage(s)?\b',  # packages
            r'\bcan(s)?\b',  # cans
            r'\bjar(s)?\b',  # jars
            r'\bbunch(es)?\b',  # bunches
            r'\bhead(s)?\b',  # heads
            r'\bclove(s)?\b',  # cloves
            r'\bpiece(s)?\b',  # pieces
            r'\bslice(s)?\b',  # slices
            r'\bcontainer(s)?\b',  # containers
            r'\bcarton(s)?\b'  # cartons
        ]
        
        self.descriptive_terms = [
            r'\bfresh\b',
            r'\bdried\b',
            r'\bchopped\b',
            r'\bsliced\b',
            r'\bdiced\b',
            r'\bminced\b',
            r'\bground\b',
            r'\bpeeled\b',
            r'\bgrated\b',
            r'\bcrushed\b',
            r'\bmelted\b',
            r'\bsoftened\b',
            r'\bbeaten\b',
            r'\bcooked\b',
            r'\bboiled\b',
            r'\bfrozen\b',
            r'\bcanned\b',
            r'\bpacked\b',
            r'\bfirmly\b',
            r'\boptional\b'
        ]

    def clean_ingredient(self, ingredient: str) -> str:
        """Clean and normalize an ingredient string."""
        # Convert to lowercase
        ingredient = ingredient.lower()
        
        # Remove parenthetical notes
        ingredient = re.sub(r'\([^)]*\)', '', ingredient)
        
        # Remove quantities
        for pattern in self.quantity_patterns:
            ingredient = re.sub(pattern, '', ingredient)
            
        # Remove measurement units
        for unit in self.measurement_units:
            ingredient = re.sub(unit, '', ingredient)
            
        # Remove descriptive terms
        for term in self.descriptive_terms:
            ingredient = re.sub(term, '', ingredient)
            
        # Remove punctuation and extra whitespace
        ingredient = re.sub(r'[,.]', '', ingredient)
        ingredient = re.sub(r'\s+', ' ', ingredient)
        
        return ingredient.strip()

    def parse_dataset(self, filepath: str) -> dict:
        """
        Parse the dataset and return unique ingredients with their frequencies.
        """
        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file not found at: {filepath}\nCurrent working directory: {os.getcwd()}")
            
        # Read the dataset
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
        
        # Convert string representation of lists to actual lists
        df['ingredients'] = df['ingredients'].apply(eval)
        
        # Flatten list of ingredients and clean each one
        all_ingredients = []
        original_to_cleaned = {}  # Dictionary to map original to cleaned ingredients
        
        for recipe_ingredients in df['ingredients']:
            for ing in recipe_ingredients:
                cleaned = self.clean_ingredient(ing)
                if cleaned:  # Only add non-empty strings
                    all_ingredients.append(cleaned)
                    original_to_cleaned[ing] = cleaned
        
        # Count frequencies
        ingredient_frequencies = Counter(all_ingredients)
        
        # Create ingredient analysis
        analysis = {
            'unique_ingredients': len(ingredient_frequencies),
            'total_occurrences': sum(ingredient_frequencies.values()),
            'frequency_distribution': dict(ingredient_frequencies.most_common()),
            'original_to_cleaned': original_to_cleaned
        }
        
        return analysis

def print_ingredient_analysis(analysis: dict):
    """Print a formatted analysis of the ingredients."""
    print("=== Ingredient Analysis ===")
    print(f"Total unique ingredients: {analysis['unique_ingredients']}")
    print(f"Total ingredient occurrences: {analysis['total_occurrences']}\n")
    
    print("Top 50 most common ingredients:")
    for i, (ingredient, count) in enumerate(list(analysis['frequency_distribution'].items())[:50], 1):
        print(f"{i:2d}. {ingredient:<30} ({count} occurrences)")
    
    print("\nSample of original to cleaned mappings:")
    sample_mappings = list(analysis['original_to_cleaned'].items())[:20]
    for original, cleaned in sample_mappings:
        print(f"Original: {original:<40} -> Cleaned: {cleaned}")

if __name__ == "__main__":
    # Try different possible paths
    possible_paths = [
        "data/full_dataset.csv",
        "../data/full_dataset.csv",
        "./data/full_dataset.csv",
        "full_dataset.csv"
    ]
    
    parser = IngredientParser()
    
    # Try each path until we find the file
    for path in possible_paths:
        try:
            print(f"Trying path: {path}")
            analysis = parser.parse_dataset(path)
            print(f"Success! Found file at: {path}")
            print_ingredient_analysis(analysis)
            break
        except FileNotFoundError:
            print(f"File not found at: {path}")
            continue
        except Exception as e:
            print(f"Error with path {path}: {str(e)}")
            continue
    else:
        print("\nCould not find the dataset file. Please ensure the file exists and provide the correct path.")
        print(f"Current working directory: {os.getcwd()}")