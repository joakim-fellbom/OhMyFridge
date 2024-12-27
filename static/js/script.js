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


document.getElementById("show-recipes-btn").addEventListener("click", () => {
    fetchAllergies(); // Récupère les allergies avant
    fetchRecipes(allergies); // Passe les allergies récupérées
});

async function fetchRecipes(allergies) {
    const response = await fetch("/get_recipes");
    const recipes = await response.json();
    console.log("Recipes fetched:", recipes);

    const recipesContainer = document.getElementById("recipes-container");
    const recipesTitleContainer = document.getElementById("recipes-title-container");

    recipesContainer.innerHTML = ""; // Efface les résultats précédents

    if (recipes.length > 0) {
        recipesTitleContainer.style.display = "block";

        recipes.forEach((recipe) => {
            const hasAllergy = recipe.ingredients.some(ingredient => 
                allergies.includes(ingredient)
            );

            if (!hasAllergy) {
                const recipeDiv = document.createElement("div");
                recipeDiv.className = "recipe";

                const title = document.createElement("h3");
                title.textContent = recipe.title;

                const ingredientsDiv = document.createElement("div");
                ingredientsDiv.className = "ingredients";
                const ingredientsTitle = document.createElement("h4");
                ingredientsTitle.textContent = "Ingredients:";
                const ingredientsList = document.createElement("p");
                ingredientsList.textContent = recipe.ingredients.join(", ");
                ingredientsDiv.appendChild(ingredientsTitle);
                ingredientsDiv.appendChild(ingredientsList);

                const directionsDiv = document.createElement("div");
                directionsDiv.className = "directions";
                const directionsTitle = document.createElement("h4");
                directionsTitle.textContent = "Directions:";
                const directionsText = document.createElement("p");
                directionsText.textContent = recipe.directions;
                directionsDiv.appendChild(directionsTitle);
                directionsDiv.appendChild(directionsText);

                recipeDiv.appendChild(title);
                recipeDiv.appendChild(ingredientsDiv);
                recipeDiv.appendChild(directionsDiv);

                recipesContainer.appendChild(recipeDiv);
            }
        });
    } else {
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

async function addAllergy() {
    const allergyInput = document.getElementById("allergy-input");
    const allergyList = document.getElementById("allergy-list");
    const selectedAllergiesContainer = document.getElementById("selected-allergies-container");

    if (allergyInput.value.trim() !== "") {
        const allergy = allergyInput.value.trim();
        const listItem = document.createElement("li");
        listItem.textContent = allergy;
        allergyList.appendChild(listItem);
        allergyInput.value = "";

        // Ajout de l'allergie au backend
        const response = await fetch("/add_allergy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ allergy: allergy }),
        });

        selectedAllergiesContainer.style.display = "block";
    }
}

async function fetchAllergies() {
    const response = await fetch("/get_allergies");
    const ingredients = await response.json();
    recipesTitleContainer.style.display = "block";
    console.log("Allergies fetched:", allergies); // Vérification dans la console

    updateAllergiesList(allergies);
}

function resetAllergies() {
    const allergyList = document.getElementById("allergy-list");
    const selectedAllergiesContainer = document.getElementById("selected-allergies-container");

    allergyList.innerHTML = ""; // Efface toutes les allergies
    selectedAllergiesContainer.style.display = "none";
}

// Initialize the list on page load
fetchIngredients();
fetchAllergies();
