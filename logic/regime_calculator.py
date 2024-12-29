import pandas as pd
import re

def vege(ingredients_list):
    # Convert ingredients list to lowercase string for easier searching
    ingredients_str = ' '.join(ingredients_list).lower()
    
    # Initialize scores
    veget = True
    
    # Meat ingredients
    meat_ingredients = ["chicken", "beef", "pork", "lamb", "veal", "duck", "turkey", "goose", "rabbit", 
    "quail", "venison", "bacon", "ham", "salami", "sausage", "pepperoni", 
    "prosciutto", "pastrami", "mutton", "goat", "buffalo", "boar", "kangaroo", "camel", "horse", "alligator",
    "crocodile", "emu", "ostrich", "pheasant", "partridge", "guinea fowl", "elk", "moose", "bear", "squirrel", 
    "porcupine", "seal", "walrus", "whale", "dolphin", "chorizo", "pancetta", "mortadella", "bresaola", "capicola", 
    "lardo", "guanciale", "soppressata", "coppa", "liverwurst", "blood sausage", "head cheese", "black pudding", 
    "spam", "corned beef", "beef jerky", "hot dogs", "kielbasa", "andouille", "bratwurst", "frankfurter", "bologna", 
    "biltong", "jerky", "smoked turkey", "smoked salmon", "smoked duck", 
    "beef brisket", "salt pork", "liver", "kidney", "heart", "tongue", "tripe", "sweetbreads", 
    "gizzards", "oxtail", "marrow", "fish", "salmon", "tuna", "mackerel", "sardine", "herring", 
    "anchovy", "cod", "trout", "catfish", "halibut", "bass", "shellfish", 
    "shrimp", "prawn", "lobster", "crab", "clam", "scallop", 
    "oyster", "mussel", "squid", "octopus", "cuttlefish", "eel"]

    # Calculate vege
    for ingredient in ingredients_str:
        if ingredient in meat_ingredients:
            veget = False

    return veget


def gluten_free(ingredients_list):
    # Convert ingredients list to lowercase string for easier searching
    ingredients_str = ' '.join(ingredients_list).lower()
    
    # Initialize scores
    gluten_free = True   
    
    gluten_ingredients = ["wheat", "barley", "rye", "triticale", "spelt", "kamut", "farro", 
    "einkorn", "durum", "semolina", "bulgur", "emmer", "wheat flour", "all-purpose flour",
    "self-rising flour", "whole wheat flour", "bread flour", "cake flour", "pasta flour",
    "rye flour", "barley flour", "graham flour", "semolina flour", "bread", "baguette", "sourdough",
    "rye bread", "whole wheat bread", "ciabatta", "focaccia", "naan", "pita", "croissant", "brioche", 
    "muffin", "scone", "bagel", "roll", "donut", "cake", "cupcake", "brownie", "cookie", "biscuit", "waffle", "pancake", 
    "pasta", "spaghetti", "macaroni", "fettuccine", "lasagna", "penne", "tagliatelle", "ravioli", "tortellini", "udon", "ramen", "soba", 
    "granola", "muesli", "bran flakes", "wheat flakes", "shredded wheat", 
    "crackers", "pretzels", "breadcrumbs", "croutons", "tortilla chips", "pita chips", "graham crackers", 
    "soy sauce", "teriyaki sauce", "malt vinegar", "beer", "malt extract", "malt flavoring", "modified wheat starch", "barley malt", 
    "breaded chicken", "breaded fish", "breaded shrimp", "tempura", "fish sticks", "chicken nuggets",
    "cream of mushroom soup", "gravy", "roux", "seitan", "gluten flour", "vital wheat gluten", "wheat gluten"]

    # Calculate gluten
    for ingredient in ingredients_str:
        if ingredient in gluten_ingredients:
            gluten_free = False

    return gluten_free


def add_regime_to_dataset(df):
    """
    Add nutriscore column to the dataset
    
    :param df: DataFrame containing recipes with 'ingredients' column
    :return: DataFrame with added 'nutriscore' column
    """
    # Create a copy of the dataframe
    df_with_regime = df.copy()
    
    # Add nutriscore column
    df_with_regime['vege'] = df_with_regime['ingredients'].apply(vege)
    df_with_regime['gluten_free'] = df_with_regime['ingredients'].apply(gluten_free)

    return df_with_regime