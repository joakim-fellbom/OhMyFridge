const ingredientInput = document.getElementById("ingredient-input");
const ingredientList = document.getElementById("ingredient-list");
const selectedIngredientsContainer = document.getElementById("selected-ingredients-container");
const showRecipesBtn = document.getElementById("show-recipes-btn");
const loader = document.getElementById("loader");
const recipesContainer = document.getElementById("recipes-container");
const recipesTitleContainer = document.getElementById("recipes-title-container");

let allowedIngredients = [];

async function addIngredient() {
    const ingredient = ingredientInput.value.trim().toLowerCase();
    const errorMessageDiv = document.getElementById("error-message");
    
    if (ingredient && allowedIngredients.includes(ingredient)) {
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
        errorMessageDiv.textContent = "";
    } else {
        errorMessageDiv.textContent = "Ingredient not allowed. Please enter a valid ingredient.";
        errorMessageDiv.style.color = "red";
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
    updateIngredientList(ingredients);
}

async function fetchAllowedIngredients() {
    try {
        const response = await fetch("/static/unique_ingredients.json");
        allowedIngredients = await response.json();
    } catch (error) {
        console.error("Error fetching allowed ingredients:", error);
    }
}

async function fetchRecipes() {
    const exactMatch = document.getElementById("exact-match-checkbox").checked;

    // Show loader and hide containers
    loader.style.display = "flex";
    recipesContainer.style.display = "none";
    recipesTitleContainer.style.display = "none";

    try {
        const response = await fetch("/get_recipes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ exact_match: exactMatch })
        });

        const data = await response.json();
        recipesContainer.innerHTML = "";

        // Parse and prepare recipes
        const recipes = Object.values(data).map(recipe => ({
            ...recipe,
            ingredients: typeof recipe.ingredients === 'string' ? 
                JSON.parse(recipe.ingredients.replace(/'/g, '"')) : recipe.ingredients,
            directions: typeof recipe.directions === 'string' ? 
                JSON.parse(recipe.directions) : recipe.directions
        }));

        // Hide loader and show recipes container
        loader.style.display = "none";
        recipesContainer.style.display = "block";

        if (recipes.length > 0) {
            recipesTitleContainer.style.display = "block";
            
            recipes.forEach((recipe) => {
                const recipeDiv = document.createElement("div");
                recipeDiv.className = "recipe";

                const headerDiv = document.createElement("div");
                headerDiv.className = "recipe-header";

                const title = document.createElement("h3");
                title.textContent = recipe.title;

                const nutriscoreContainer = document.createElement("div");
                nutriscoreContainer.className = "nutriscore-container";
                
                const nutriscoreDiv = document.createElement("div");
                nutriscoreDiv.className = `nutriscore nutriscore-${recipe.nutriscore.toLowerCase()}`;
                nutriscoreDiv.textContent = recipe.nutriscore;
                
                const tooltip = document.createElement("div");
                tooltip.className = "nutriscore-tooltip";
                tooltip.textContent = getNutriscoreDescription(recipe.nutriscore);
                
                nutriscoreContainer.appendChild(nutriscoreDiv);
                nutriscoreContainer.appendChild(tooltip);

                headerDiv.appendChild(title);
                headerDiv.appendChild(nutriscoreContainer);

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
                directionsText.textContent = recipe.directions.join(" ");
                directionsDiv.appendChild(directionsTitle);
                directionsDiv.appendChild(directionsText);

                recipeDiv.appendChild(headerDiv);
                recipeDiv.appendChild(ingredientsDiv);
                recipeDiv.appendChild(directionsDiv);

                recipesContainer.appendChild(recipeDiv);
            });
        } else {
            recipesContainer.innerHTML = "<p>No recipes found with these ingredients.</p>";
        }
    } catch (error) {
        console.error("Error fetching recipes:", error);
        // Hide loader and show error message
        loader.style.display = "none";
        recipesContainer.style.display = "block";
        recipesContainer.innerHTML = "<p>Error loading recipes. Please try again.</p>";
    }
}

function updateIngredientList(ingredients) {
    ingredientList.innerHTML = "";
    ingredients.forEach((ingredient) => {
        const li = document.createElement("li");
        li.textContent = ingredient;
        ingredientList.appendChild(li);
    });
    if (ingredients.length > 0) {
        selectedIngredientsContainer.style.display = "block";
        showRecipesBtn.style.display = "inline-block";
    } else {
        selectedIngredientsContainer.style.display = "none";
        showRecipesBtn.style.display = "none";
    }
}

function getNutriscoreDescription(score) {
    const descriptions = {
        'A': 'Excellent nutritional quality',
        'B': 'Good nutritional quality',
        'C': 'Average nutritional quality',
        'D': 'Poor nutritional quality',
        'E': 'Very poor nutritional quality'
    };
    return descriptions[score] || 'Nutritional information not available';
}

// Initialize
fetchAllowedIngredients();
fetchIngredients();