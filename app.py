from flask import Flask, request, jsonify, render_template
import pandas as pd
from logic.recipe_filter import filter_recipes_by_ingredients_and_allergies
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

# Chargement des données de recettes
data = pd.read_csv("data/full_dataset.csv", sep=',', nrows=1000)
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
    global allergies
    filtered_recipes = filter_recipes_by_ingredients_and_allergies(data, selected_ingredients, allergies)
    recipes = filtered_recipes.to_dict(orient="records")  # Convertir le DataFrame en liste de dictionnaires
    return jsonify(recipes)

@app.route("/reset_ingredients", methods=["POST"])
def reset_ingredients():
    global selected_ingredients
    selected_ingredients = []
    return jsonify(selected_ingredients)

allergies = []

@app.route('/add_allergy', methods=['POST'])
def add_allergy():
    global allergies
    allergy = request.json.get('allergy')
    if allergy and allergy not in allergies:
        allergies.append(allergy)
    return jsonify(allergies)

@app.route('/reset_allergies', methods=['POST'])
def reset_allergies():
    global allergies
    allergies.clear()
    return jsonify(allergies)

if __name__ == "__main__":
    app.run(debug=True)
