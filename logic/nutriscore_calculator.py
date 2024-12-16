import pandas as pd
import re

def calculate_nutriscore(ingredients_list):
    """
    Calculate a simplified nutriscore (A to E) based on ingredients.
    
    This is a simplified version that:
    - Promotes fruits, vegetables, lean proteins, whole grains
    - Penalizes added sugars, saturated fats, processed ingredients
    
    :param ingredients_list: List of ingredients
    :return: Nutriscore letter (A, B, C, D, or E)
    """
    # Convert ingredients list to lowercase string for easier searching
    ingredients_str = ' '.join(ingredients_list).lower()
    
    # Initialize scores
    positive_points = 0
    negative_points = 0
    
    # Positive ingredients patterns
    positive_ingredients = {
        'fruits': ['apple', 'banana', 'berry', 'berries', 'orange', 'fruit'],
        'vegetables': ['carrot', 'spinach', 'lettuce', 'broccoli', 'vegetable', 'tomato'],
        'lean_proteins': ['chicken breast', 'fish', 'turkey', 'tofu', 'lentils'],
        'whole_grains': ['whole grain', 'brown rice', 'quinoa', 'oats'],
        'healthy_fats': ['olive oil', 'avocado', 'nuts', 'seeds']
    }
    
    # Negative ingredients patterns
    negative_ingredients = {
        'added_sugars': ['sugar', 'syrup', 'honey'],
        'processed_foods': ['processed', 'artificial', 'preservative'],
        'saturated_fats': ['butter', 'cream', 'lard'],
        'refined_grains': ['white flour', 'refined'],
        'high_sodium': ['salt', 'sodium']
    }
    
    # Calculate positive points
    for category, ingredients in positive_ingredients.items():
        for ingredient in ingredients:
            if ingredient in ingredients_str:
                positive_points += 2
                
    # Calculate negative points
    for category, ingredients in negative_ingredients.items():
        for ingredient in ingredients:
            if ingredient in ingredients_str:
                negative_points += 2
    
    # Calculate final score
    final_score = positive_points - negative_points
    
    # Convert score to nutriscore letter
    if final_score >= 8:
        return 'A'
    elif final_score >= 4:
        return 'B'
    elif final_score >= 0:
        return 'C'
    elif final_score >= -4:
        return 'D'
    else:
        return 'E'

def add_nutriscore_to_dataset(df):
    """
    Add nutriscore column to the dataset
    
    :param df: DataFrame containing recipes with 'ingredients' column
    :return: DataFrame with added 'nutriscore' column
    """
    # Create a copy of the dataframe
    df_with_nutriscore = df.copy()
    
    # Add nutriscore column
    df_with_nutriscore['nutriscore'] = df_with_nutriscore['ingredients'].apply(calculate_nutriscore)
    
    return df_with_nutriscore