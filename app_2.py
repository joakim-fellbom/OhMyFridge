import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity

# Fonction pour charger les objets depuis un fichier pickle
def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Interface Streamlit
st.title('Recipe Matcher, Trouves ta recette')

# Saisie de la liste d'ingrédients par l'utilisateur randommmmmmmmmmmmmm
ingredient_input = st.text_input("Entrez vos ingrédients (séparés par des virgules), Ex: brown sugar, milk, vanilla")

# Case à cocher pour activer le match exact des ingrédients
exact_match = st.checkbox("Uniquement les ingredients cités")

# Chemin pour les fichiers pickle
tfidf_matrix_file = "tfidf_matrix.pkl"
tfidf_vectorizer_file = "tfidf_vectorizer.pkl"
recipe_info_file = "recipe_info.pkl"  # Fichier contenant les informations essentielles des recettes

# Si les fichiers pickle existent, on charge les données
if 'tfidf_matrix' not in st.session_state or 'tfidf_vectorizer' not in st.session_state or 'recipe_info' not in st.session_state:
    if os.path.exists(tfidf_matrix_file) and os.path.exists(tfidf_vectorizer_file) and os.path.exists(recipe_info_file):
        # Charger les vecteurs, le vectorizer et les informations des recettes depuis les fichiers pickle
        st.session_state.tfidf_matrix = load_from_pickle(tfidf_matrix_file)
        st.session_state.tfidf_vectorizer = load_from_pickle(tfidf_vectorizer_file)
        st.session_state.recipe_info = load_from_pickle(recipe_info_file)
    else:
        st.write("Les fichiers de modèle ou les informations sur les recettes n'existent pas. Veuillez d'abord entraîner le modèle.")
        st.stop()  # Pour arrêter l'application si les fichiers pickle sont manquants, parce que c'est chiant que ca plante pour ca 

# Fonction de matching avec la similarité cosinus 
def match_recipe_cosine(_tfidf_matrix, _tfidf_vectorizer, _recipe_info, ingredient_input, threshold=0.8, exact_match=False, max_recipes=10):
    # Transformons l'entrée de l'utilisateur en vecteur TF-IDF
    input_tfidf = _tfidf_vectorizer.transform([ingredient_input])

    # Calcul de la similarité cosinus entre l'entrée et les ingrédients dans le df
    cosine_sim = cosine_similarity(input_tfidf, _tfidf_matrix).flatten()

    if exact_match:
        # On veut un match exact (similarité = 1) 
        similar_recipes_idx = [i for i, score in enumerate(cosine_sim) if score == 1.0]
    else:
        # On ne veut que les recettes ayant une similarité >= 0.8
        similar_recipes_idx = [i for i, score in enumerate(cosine_sim) if score >= threshold]

    # Si aucune recette ne dépasse le seuil, renvoyer un message
    if len(similar_recipes_idx) == 0:
        return {"message": "Oups vas falloir rajouter d'autres ingredients :)"}

    # Assurez-vous que similar_recipes_idx est un tableau unidimensionnel d'entiers
    similar_recipes_idx = np.array(similar_recipes_idx)

    # Trier les indices par similarité décroissante
    sorted_indices = similar_recipes_idx[np.argsort(cosine_sim[similar_recipes_idx])[::-1]]

    # Limiter à un maximum de "max_recipes" recettes
    sorted_indices = sorted_indices[:max_recipes]

    # Extraire les info des recettes correspondantes
    recipes = []
    for idx in sorted_indices:
        recipe = _recipe_info.iloc[idx]
        recipes.append({
            "recette": recipe['title'],
            "ingredients": recipe['NER'],
            "directions": recipe['directions']
        })
    
    return recipes

# Si l'user a saisi des ingrédients
if ingredient_input:
    # Appel de la fonction pour trouver les recettes correspondantes en fonction de la similarité cosinus
    result = match_recipe_cosine(st.session_state.tfidf_matrix, st.session_state.tfidf_vectorizer, st.session_state.recipe_info, ingredient_input, threshold=0.8, exact_match=exact_match, max_recipes=10)
    
    if 'message' in result:
        st.write(result['message'])  # Si aucune recette ne dépasse le seuil
    else:
        # On affiche les résultats sous forme de tableau
        st.subheader('Recettes Correspondantes')

        # Convertir les résultats en DataFrame pour une meilleure présentation
        result_df = pd.DataFrame(result)
        st.table(result_df)