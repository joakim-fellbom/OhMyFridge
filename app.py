from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
from logic.recipe_filter import filter_recipes_by_ingredients  # Import de la fonction de filtrage

app = Flask(__name__)

# Chargement des données de recettes
data = pd.read_csv("data/full_dataset.csv")
data['ingredients'] = data['ingredients'].apply(eval)  # Convertir la chaîne en liste Python

# Liste pour stocker les ingrédients sélectionnés par l'utilisateur
selected_ingredients = []

# Route pour obtenir des recettes aléatoires
@app.route("/get_random_recipes")
def get_random_recipes():
    # Sélectionner 10 recettes aléatoires
    random_recipes = data.sample(n=10)  # Prendre 10 recettes au hasard
    recipes_list = random_recipes.to_dict(orient="records")  # Convertir les recettes en format JSON
    return jsonify(recipes_list)

# Route pour ajouter un ingrédient
@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    global selected_ingredients
    ingredient = request.json.get("ingredient")
    if ingredient and ingredient not in selected_ingredients:
        selected_ingredients.append(ingredient)
    return jsonify(selected_ingredients)

# Route pour obtenir les recettes correspondant aux ingrédients
@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    global selected_ingredients
    exact_match = request.json.get("exact_match", False)  # Récupérer l'état de la case à cocher

    # Filtrage des recettes selon la correspondance exacte ou partielle
    filtered_recipes = filter_recipes_by_ingredients(data, selected_ingredients, exact_match=exact_match)
    
    recipes = filtered_recipes.to_dict(orient="records")  # Convertir le DataFrame en liste de dictionnaires
    return jsonify(recipes)

# Route pour réinitialiser les ingrédients
@app.route("/reset_ingredients", methods=["POST"])
def reset_ingredients():
    global selected_ingredients
    selected_ingredients = []
    return jsonify(selected_ingredients)

if __name__ == "__main__":
    app.run(debug=True)