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
        'fruits': ['apple', 'apples', 'banana', 'bananas', 'orange', 'oranges',
            'strawberries', 'blueberries', 'raspberries', 'blackberries',
            'cranberries', 'pineapple', 'peaches', 'fruit cocktail',
            'mandarin oranges', 'orange juice', 'apple juice', 'mango',
            'apricots', 'cherries', 'rhubarb', 'fruit', 'pineapple juice',
            'pineapple chunks', 'mandarin oranges drained', 'orange juice concentrate',
            'orange zest', 'orange peel', 'orange rind', 'lemon', 'lime',
            'citrus fruits', 'dried fruit', 'fresh fruit', 'fruit puree',
            'cranberry juice', 'grape juice', 'fruit nectar'],    
        'vegetables': ['carrot', 'carrots', 'spinach', 'lettuce', 'romaine lettuce',
            'broccoli', 'vegetable', 'vegetables', 'tomato', 'tomatoes',
            'bell pepper', 'green pepper', 'red pepper', 'celery',
            'zucchini', 'cucumber', 'asparagus', 'green beans',
            'peas', 'cauliflower', 'green onions', 'baby spinach',
            'arugula', 'squash', 'yellow squash', 'artichoke hearts',
            'leeks', 'radishes', 'okra', 'tomato sauce', 'tomato paste',
            'tomato puree', 'stewed tomatoes', 'cherry tomatoes',
            'plum tomatoes', 'roma tomatoes', 'vegetable broth',
            'vegetable stock', 'mixed vegetables', 'green chilies',
            'jalapeno', 'jalapenos', 'bell peppers', 'sweet peppers',
            'red bell pepper', 'green bell pepper', 'yellow bell pepper',
            'pepper flakes', 'hot peppers', 'sweet potato', 'sweet potatoes',
            'potato', 'potatoes', 'garlic', 'onion', 'shallots',
            'baby carrots', 'celery ribs', 'celery stalks', 'water chestnuts',
            'bamboo shoots', 'bean sprouts', 'cabbage', 'brussels sprouts',
            'eggplant', 'mushrooms', 'button mushrooms', 'portobello mushrooms'],        
        'lean_proteins': ['chicken breast', 'skinless chicken breast', 'turkey',
            'fish', 'salmon', 'tuna', 'shrimp', 'lean beef',
            'tofu', 'lentils', 'chickpeas', 'quinoa',
            'black beans', 'kidney beans', 'pinto beans',
            'chicken breasts', 'turkey breast', 'ground turkey',
            'salmon fillet', 'cod', 'tilapia', 'halibut',
            'mahi mahi', 'sea bass', 'trout', 'catfish',
            'crab meat', 'crabmeat', 'lobster', 'scallops',
            'clams', 'mussels', 'oysters', 'lean pork',
            'pork tenderloin', 'lean ground beef', 'sirloin',
            'top round', 'flank steak', 'chicken thighs skinless',
            'egg whites', 'tempeh', 'seitan', 'edamame',
            'greek yogurt', 'low-fat yogurt', 'plain yogurt'],
        'whole_grains': ['whole grain', 'brown rice', 'whole wheat flour',
            'quinoa', 'oats', 'rolled oats', 'quick oats',
            'wild rice', 'whole wheat pastry flour', 'steel cut oats',
            'whole wheat bread', 'whole grain pasta', 'whole wheat pasta',
            'bulgur', 'buckwheat', 'millet', 'barley', 'whole rye',
            'whole grain cereal', 'whole wheat couscous', 'amaranth',
            'sprouted grain', 'whole grain crackers', 'whole wheat tortillas',
            'whole grain breadcrumbs', 'wheat berries', 'whole wheat pita',
            'whole grain rice', 'whole oats', 'old fashioned oats'],
        'healthy_fats': ['olive oil', 'extra virgin olive oil', 'extra-virgin olive oil',
            'avocado', 'avocados', 'nuts', 'walnuts', 'almonds',
            'pecans', 'pine nuts', 'cashews', 'hazelnuts',
            'sunflower seeds', 'sesame seeds', 'pumpkin seeds',
            'flaxseed', 'coconut oil', 'chia seeds', 'hemp seeds',
            'macadamia nuts', 'pistachios', 'brazil nuts',
            'almond butter', 'natural peanut butter', 'tahini',
            'ground flaxseed', 'avocado oil', 'grapeseed oil',
            'walnut oil', 'canola oil', 'safflower oil',
            'peanuts', 'natural almond butter', 'sunflower oil']
    }

    # Negative ingredients patterns
    negative_ingredients = {
        'added_sugars': ['sugar', 'brown sugar', 'white sugar', 'granulated sugar',
            'powdered sugar', 'confectioners sugar', 'light brown sugar',
            'dark brown sugar', 'corn syrup', 'light corn syrup',
            'dark corn syrup', 'maple syrup', 'honey', 'molasses',
            'agave nectar', 'karo syrup', 'simple syrup', 'cane sugar',
            'demerara sugar', 'turbinado sugar', 'raw sugar',
            'palm sugar', 'date sugar', 'golden syrup', 'malt syrup',
            'rice syrup', 'barley malt', 'corn sweetener',
            'high fructose corn syrup', 'invert sugar', 'caramel',
            'caster sugar', 'icing sugar', 'superfine sugar'],        
        'processed_foods': ['processed', 'artificial', 'preservative', 'velveeta cheese',
            'cheez whiz', 'cool whip', 'marshmallow cream',
            'marshmallow creme', 'instant', 'cake mix', 'food coloring',
            'artificial sweetener', 'processed cheese', 'instant coffee',
            'instant pudding', 'cake mix', 'brownie mix', 'biscuit mix',
            'pancake mix', 'cookie mix', 'frosting mix', 'pie filling',
            'prepared frosting', 'flavoring syrup', 'fruit flavoring',
            'artificial flavor', 'food dye', 'red food coloring',
            'blue food coloring', 'yellow food coloring',
            'artificial vanilla', 'imitation vanilla', 'margarine spread',
            'processed meat', 'lunch meat', 'hot dogs', 'spam'],
        'saturated_fats': ['butter', 'cream', 'lard', 'margarine', 'shortening',
            'sour cream', 'heavy cream', 'whipping cream',
            'cream cheese', 'buttermilk', 'crisco', 'bacon drippings',
            'oleo', 'stick butter', 'stick margarine',
            'heavy whipping cream', 'creme fraiche', 'butter sofed',
            'salted butter', 'unsalted butter', 'clarified butter',
            'ghee', 'bacon fat', 'chicken fat', 'duck fat',
            'beef tallow', 'palm oil', 'coconut cream',
            'half and half', 'light cream', 'double cream',
            'clotted cream', 'butter powder', 'butter flavoring'],
        'refined_grains': ['white flour', 'refined', 'all-purpose flour', 'cake flour',
            'bleached flour', 'plain flour', 'white bread',
            'bread flour', 'sifted flour', 'cornflour', 'enriched flour',
            'self-rising flour', 'pastry flour', 'white rice',
            'instant rice', 'minute rice', 'white pasta',
            'white breadcrumbs', 'cracker crumbs', 'graham cracker crumbs',
            'cookie crumbs', 'bread crumbs', 'panko breadcrumbs',
            'rice flour', 'tapioca flour', 'potato flour'],
        'high_sodium': ['salt', 'kosher salt', 'sea salt', 'garlic salt',
            'celery salt', 'onion salt', 'table salt',
            'seasoning salt', 'salt and pepper', 'salt to taste',
            'sodium', 'msg', 'accent', 'bouillon', 'bouillon cubes',
            'chicken bouillon', 'beef bouillon', 'vegetable bouillon',
            'soy sauce', 'fish sauce', 'oyster sauce', 'teriyaki sauce',
            'worcestershire sauce', 'steak sauce', 'barbecue sauce',
            'seasoned salt', 'adobo seasoning', 'season-all',
            'marinade mix', 'gravy mix', 'sauce mix', 'taco seasoning',
            'chili seasoning', 'fajita seasoning', 'poultry seasoning']
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