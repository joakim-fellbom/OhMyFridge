import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Importation du dataset
df = pd.read_csv('RecipeNLG_dataset.csv')

# Fonction pour enregistrer les objets dans un fichier pickle
def save_to_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

# Sauvegardons uniquement les informations essentielles pour nous(title, NER, dir)
def save_recipe_info(df):
    recipe_info = df[['title', 'NER', 'directions']].copy()
    
    # On les Sauvegarde sous forme de pickle
    save_to_pickle(recipe_info, "recipe_info.pkl")
    print("Informations sur les recettes sauvegardées en bienn.")

# Petite fonction pour calculer les vecteurs TF-IDF :)
def compute_tfidf(df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Faut s'assurer que chaque élément de NER est une liste et qu'on la convertit en texte
    df['NER'] = df['NER'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

    # On Calcule les vecteurs TF-IDF pour la colonne 'NER'
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['NER'].tolist())

    # Sauvegarde des objets dans des fichiers pickle
    save_to_pickle(tfidf_matrix, "tfidf_matrix.pkl")
    save_to_pickle(tfidf_vectorizer, "tfidf_vectorizer.pkl")

    # sauvegarde des info essentielles
    save_recipe_info(df)

    print("Vecteurs TF-IDF et informations sauvegardées avec succès.")

if __name__ == "__main__":
    # Calcul des vecteurs TF-IDF et sauvegarde des fichiers pickle
    compute_tfidf(df)