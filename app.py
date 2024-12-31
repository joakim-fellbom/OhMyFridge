from flask import Flask, request, jsonify, render_template
from xata.client import XataClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialisation avec configuration explicite
xata = XataClient(
    api_key=os.getenv("XATA_API_KEY"),
    db_url=os.getenv("XATA_DATABASE_URL")
)

# Test de la connexion au démarrage
try:
    test_query = {
        "page": {
            "size": 1
        }
    }
    test = xata.data().query("full_dataset_with_nutriscore", test_query)
    print("Connexion Xata réussie")
except Exception as e:
    print(f"Erreur de connexion Xata: {str(e)}")

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

@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    global selected_ingredients
    exact_match = request.json.get("exact_match", False)
    print(f"Exact match: {exact_match}")
    
    if not selected_ingredients:
        return jsonify([])
    
    try:
        ingredients_lower = [ing.lower() for ing in selected_ingredients]
        #ingredients_str = str(ingredients_lower).replace("'", "\"")
        ingredients_formatted = [f'\"{ing.lower()}\"' for ing in selected_ingredients]
        ingredients_joined = ", ".join(ingredients_formatted)
        ingredients_str = f"[{ingredients_joined}]"
        
        if exact_match:
            # For exact match using $iContains
            filter_conditions = {
                "NER": {
                    "$iContains": ingredients_str 
                }
            }
        else:
            # Pour la recherche partielle, on utilise $all avec $contains
            filter_conditions = {
                "NER": {
                    "$all": [
                        {"$contains": ing} for ing in ingredients_lower
                    ]
                }
            }
        
        query = {
            "columns": ["title", "ingredients", "directions", "nutriscore", "NER"],
            "filter": filter_conditions,
            "page": {
                "size": 15  # Limited to 15 results as per example
            }
        }
        
        print(f"Query: {query}")
        
        results = xata.data().query("full_dataset_with_nutriscore", query)
        
        if not results.is_success():
            print(f"Erreur Xata: {results}")
            return jsonify({"error": "Erreur de requête"}), 500
        
        records = results.get('records', [])
        
        for record in records:
            try:
                record['ingredients'] = eval(record['ingredients']) if isinstance(record['ingredients'], str) else record['ingredients']
                record['directions'] = eval(record['directions']) if isinstance(record['directions'], str) else record['directions']
                record.pop('NER', None)
            except:
                record['ingredients'] = []
                record['directions'] = []
        
        print(f"Nombre de recettes trouvées : {len(records)}")
        return jsonify(records)
        
    except Exception as e:
        print(f"Erreur lors du filtrage : {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/reset_ingredients", methods=["POST"])
def reset_ingredients():
    global selected_ingredients
    selected_ingredients = []
    return jsonify(selected_ingredients)