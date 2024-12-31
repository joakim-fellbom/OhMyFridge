# FoodLy

FoodLy est une application web qui aide les utilisateurs à trouver des recettes en fonction des ingrédients qu'ils ont à la maison. L'application utilise la base de données Xata pour stocker et interroger les données des recettes, et elle calcule le Nutri-Score pour chaque recette afin de fournir des informations nutritionnelles.

## Fonctionnalités

- Ajouter des ingrédients à votre liste
- Rechercher des recettes en fonction des ingrédients sélectionnés
- Option pour rechercher des correspondances exactes ou partielles
- Afficher les détails des recettes, y compris les ingrédients, les instructions et le Nutri-Score
- Réinitialiser la liste des ingrédients

## Technologies Utilisées

- Python
- Flask
- XataClient
- Pandas
- Docker
- Vercel

## Prise en Main

### Prérequis

- Python 3.9 ou supérieur
- Docker
- Vercel CLI

### Installation

1. Cloner le dépôt :
    ```bash
    git clone https://github.com/votre-nom-utilisateur/OhMyFridge.git
    cd OhMyFridge
    ```

2. Créer un environnement virtuel et l'activer :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
    ```

3. Installer les packages requis :
    ```bash
    pip install -r requirements.txt
    ```

4. Créer un fichier `.env` et ajouter votre clé API Xata et l'URL de la base de données :
    ```plaintext
    XATA_API_KEY=votre_cle_api_xata
    XATA_DATABASE_URL=votre_url_base_de_donnees_xata
    ```

### Exécution de l'Application

1. Exécuter l'application Flask :
    ```bash
    python app.py
    ```

2. Ouvrir votre navigateur et naviguer à `http://localhost:5000`.

### Utilisation de Docker

1. Construire l'image Docker :
    ```bash
    docker-compose build
    ```

2. Exécuter le conteneur Docker :
    ```bash
    docker-compose up
    ```

3. Ouvrir votre navigateur et naviguer à `http://localhost:5000`.

### Déploiement sur Vercel

1. Installer le Vercel CLI :
    ```bash
    npm install -g vercel
    ```

2. Se connecter à Vercel :
    ```bash
    vercel login
    ```

3. Déployer l'application :
    ```bash
    vercel
    ```

### Lancer les Tests

1. Exécuter les tests avec `unittest` :
    ```bash
    python -m unittest tests/test_app.py
    ```

## Structure du Projet

```
OhMyFridge/
├── data/
│   ├── data_processing.py
│   └── full_dataset_with_nutriscore.csv
├── logic/
│   ├── nutriscore_calculator.py
│   └── recipe_filter.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── .dockerignore
├── .env.example
├── .gitignore
├── app.py
├── docker-compose.yml
├── package.json
├── requirements.txt
└── vercel.json
```

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request pour toute amélioration ou correction de bug.

