from flask import Flask, request, jsonify, render_template
import pandas as pd
from logic.recipe_filter import filter_recipes_by_ingredients
#from logic.nutriscore_calculator import add_nutriscore_to_dataset

app = Flask(__name__)

# Load recipe data
data = pd.read_csv("data/full_dataset_with_nutriscore.csv")
data['ingredients'] = data['ingredients'].apply(eval)  # Convert string to Python list

# Add nutriscore to the dataset
#data = add_nutriscore_to_dataset(data)

# List to store selected ingredients
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
    recipes = filtered_recipes.to_dict(orient="records")
    return jsonify(recipes)

@app.route("/reset_ingredients", methods=["POST"])
def reset_ingredients():
    global selected_ingredients
    selected_ingredients = []
    return jsonify(selected_ingredients)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)