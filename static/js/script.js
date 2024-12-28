const ingredientInput = document.getElementById("ingredient-input");
const ingredientList = document.getElementById("ingredient-list");
const selectedIngredientsContainer = document.getElementById("selected-ingredients-container");
const showRecipesBtn = document.getElementById("show-recipes-btn");


async function addIngredient() {
    const ingredient = ingredientInput.value.trim();
    if (ingredient) {
        const response = await fetch("/add_ingredient", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ingredient: ingredient }),
        });
        const updatedList = await response.json();
        updateIngredientList(updatedList);
        ingredientInput.value = "";
    }
}

async function resetIngredients() {
    const response = await fetch("/reset_ingredients", {
        method: "POST",
    });
    const updatedList = await response.json();
    updateIngredientList(updatedList);
}

async function fetchIngredients() {
    const response = await fetch("/get_ingredients");
    const ingredients = await response.json();
    recipesTitleContainer.style.display = "block";
    updateIngredientList(ingredients);
}

async function fetchRecipes() {
    // Récupérer l'état de la case à cocher "exact match"
    const exactMatch = document.getElementById("exact-match-checkbox").checked;

    // Envoyer l'état du checkbox au backend avec la requête
    const response = await fetch("/get_recipes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ exact_match: exactMatch })  // Ajout de la donnée exact_match
    });

    const recipes = await response.json();
    const recipesContainer = document.getElementById("recipes-container");
    const recipesTitleContainer = document.getElementById("recipes-title-container");

    recipesContainer.innerHTML = ""; // Effacer les résultats précédents

    if (recipes.length > 0) {
        // Affiche le titre "Recipes:"
        recipesTitleContainer.style.display = "block";

        // Ajoute les recettes au conteneur
        recipes.forEach((recipe) => {
            // Création d'un conteneur pour chaque recette
            const recipeDiv = document.createElement("div");
            recipeDiv.className = "recipe";

            // Titre de la recette
            const title = document.createElement("h3");
            title.textContent = recipe.title;

            // Section Ingrédients
            const ingredientsDiv = document.createElement("div");
            ingredientsDiv.className = "ingredients";
            const ingredientsTitle = document.createElement("h4");
            ingredientsTitle.textContent = "Ingredients:";
            const ingredientsList = document.createElement("p");
            ingredientsList.textContent = recipe.ingredients.join(", ");
            ingredientsDiv.appendChild(ingredientsTitle);
            ingredientsDiv.appendChild(ingredientsList);

            // Section Directions
            const directionsDiv = document.createElement("div");
            directionsDiv.className = "directions";
            const directionsTitle = document.createElement("h4");
            directionsTitle.textContent = "Directions:";
            const directionsText = document.createElement("p");
            directionsText.textContent = recipe.directions;
            directionsDiv.appendChild(directionsTitle);
            directionsDiv.appendChild(directionsText);

            // Ajout des sections au conteneur de la recette
            recipeDiv.appendChild(title);
            recipeDiv.appendChild(ingredientsDiv);
            recipeDiv.appendChild(directionsDiv);

            // Ajout de la recette au conteneur principal
            recipesContainer.appendChild(recipeDiv);
        });
    } else {
        // Masque le titre si aucune recette n'est disponible
        recipesTitleContainer.style.display = "none";
    }
}


function updateIngredientList(ingredients) {
    ingredientList.innerHTML = "";
    ingredients.forEach((ingredient) => {
        const li = document.createElement("li");
        li.textContent = ingredient;
        ingredientList.appendChild(li);
    });
    // Show or hide the "Selected Ingredients" and "Show Recipes" sections
    if (ingredients.length > 0) {
        selectedIngredientsContainer.style.display = "block";
        showRecipesBtn.style.display = "inline-block";
    } else {
        selectedIngredientsContainer.style.display = "none";
        showRecipesBtn.style.display = "none";
    }
}



// Initialize the list on page load
fetchIngredients();
