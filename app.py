from flask import Flask, request, jsonify, render_template
import pandas as pd
from logic.recipe_filter import filter_recipes_by_ingredients

app = Flask(__name__)

# Chargement des données de recettes
data = pd.read_csv("data/full_dataset.csv")
data['ingredients'] = data['ingredients'].apply(eval)  # Convertir la chaîne en liste Python

# Liste pour stocker les ingrédients sélectionnés par l'utilisateur
selected_ingredients = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    global selected_ingredients
    ingredient = request.json.get("ingredient")
    if ingredient and ingredient not in selected_ingredients:
        selected_ingredients.append(ingredient)
    return jsonify(selected_ingredients)

@app.route("/get_recipes", methods=["GET"])
def get_recipes():
    global selected_ingredients
    filtered_recipes = filter_recipes_by_ingredients(data, selected_ingredients)
    recipes = filtered_recipes.to_dict(orient="records")  # Convertir le DataFrame en liste de dictionnaires
    return jsonify(recipes)

@app.route("/reset_ingredients", methods=["POST"])
def reset_ingredients():
    global selected_ingredients
    selected_ingredients = []
    return jsonify(selected_ingredients)

if __name__ == "__main__":
    app.run(debug=True)
