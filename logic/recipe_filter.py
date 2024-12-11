import pandas as pd

def filter_recipes_by_ingredients_and_allergies(data, input_ingredients, allergies):
    """
    Filtre les recettes pour ne retourner que celles qui contiennent les ingrédients donnés
    et qui ne contiennent aucune des allergies spécifiées.

    :param data: DataFrame contenant les recettes avec les colonnes 'title', 'ingredients', 'directions'.
    :param input_ingredients: Liste des ingrédients à rechercher dans les recettes.
    :param allergies: Liste des allergies à éviter dans les recettes.
    :return: DataFrame contenant les recettes qui correspondent.
    """
    # Affiche et nettoie les noms de colonnes
    print("Colonnes du DataFrame :", data.columns.tolist())
    data.columns = data.columns.str.strip()  # Nettoie les espaces autour des noms de colonnes

    # Vérifie que les colonnes nécessaires sont présentes
    required_columns = ['title', 'ingredients', 'directions']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"La colonne {col} est absente du DataFrame.")

    # Supprime les lignes avec des valeurs manquantes dans 'ingredients'
    data = data[data['ingredients'].notna()]

    # Définitions des fonctions de filtrage
    def contains_all_ingredients(recipe_ingredients):
        return all(ingredient in recipe_ingredients for ingredient in input_ingredients)
    
    def contains_allergies(recipe_ingredients):
        return any(allergy in recipe_ingredients for allergy in allergies)

    # Applique les filtres
    filtered_data = data[data['ingredients'].apply(contains_all_ingredients)]
    filtered_data = filtered_data[~filtered_data['ingredients'].apply(contains_allergies)]

    # Retourne uniquement les colonnes nécessaires
    return filtered_data[['title', 'ingredients', 'directions']]
