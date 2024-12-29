import pandas as pd

def filter_recipes_by_ingredients(data, input_ingredients, exact_match=False):
    """
    Filtre les recettes pour ne retourner que celles qui contiennent les ingrédients donnés.

    :param data: DataFrame contenant les recettes avec les colonnes 'title', 'ingredients', 'directions'.
    :param input_ingredients: Liste des ingrédients à rechercher dans les recettes.
    :param exact_match: Booléen pour activer le filtrage exact.
    :return: DataFrame contenant les recettes qui correspondent.
    """
    def contains_all_ingredients(recipe_ingredients):
        # Si exact_match est True, on vérifie si la recette contient exactement les ingrédients donnés
        if exact_match:
            return set(input_ingredients) == set(recipe_ingredients)  # Comparaison exacte des ensembles d'ingrédients
        else:
            # Si exact_match est False, on vérifie si tous les ingrédients sont présents dans la recette
            return all(ingredient in recipe_ingredients for ingredient in input_ingredients)
    
    # Filtre les recettes en appliquant la condition sur la colonne 'ingredients'
    filtered_data = data[data['ingredients'].apply(contains_all_ingredients)]
    return filtered_data[['title', 'ingredients', 'directions', 'nutriscore']]