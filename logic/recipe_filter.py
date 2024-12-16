import pandas as pd

def filter_recipes_by_ingredients(data, input_ingredients):
    """
    Filtre les recettes pour ne retourner que celles qui contiennent les ingrédients donnés.

    :param data: DataFrame contenant les recettes avec les colonnes 'title', 'ingredients', 'directions', 'nutriscore'.
    :param input_ingredients: Liste des ingrédients à rechercher dans les recettes.
    :return: DataFrame contenant les recettes qui correspondent.
    """
    def contains_all_ingredients(recipe_ingredients):
        # Vérifie si tous les ingrédients donnés sont dans la liste des ingrédients de la recette
        return all(ingredient in recipe_ingredients for ingredient in input_ingredients)
    
    # Filtre les recettes en appliquant la condition sur la colonne 'ingredients'
    filtered_data = data[data['ingredients'].apply(contains_all_ingredients)]
    return filtered_data[['title', 'ingredients', 'directions', 'nutriscore']]