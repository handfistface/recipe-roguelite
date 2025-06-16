// Shared JS for meals and grocery list functionality

function removeItem(element) {
    element.style.transition = "opacity 0.5s ease-out";
    element.style.opacity = 0;
    setTimeout(function() {
        element.style.display = "none";
    }, 500);
}

function formatIngredients(ingredients) {
    return ingredients.map(ingredient => ingredient.ingredient + ': ' + ingredient.measure).join(', ');
}

function updateGroceryListFromData(groceryList) {
    const groceryUl = document.getElementById('grocery-list');
    groceryUl.innerHTML = '';
    if (Array.isArray(groceryList)) {
        groceryList.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            li.onclick = () => removeItem(li);
            groceryUl.appendChild(li);
        });
    } else if (typeof groceryList === 'object') {
        Object.entries(groceryList).forEach(([ingredient, measure]) => {
            const li = document.createElement('li');
            li.textContent = `${ingredient}: ${measure}`;
            li.onclick = () => removeItem(li);
            groceryUl.appendChild(li);
        });
    }
}
