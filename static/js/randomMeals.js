//let meals = {{ meals | tojson }};
            
function removeItem(element) {
    element.style.transition = "opacity 0.5s ease-out";
    element.style.opacity = 0;
    setTimeout(function() {
    element.style.display = "none";
    }, 500);
}

function rerollMeal(element, index) {
    fetch('/randommeals/reroll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ index: index })
    })
    .then(response => response.json())
    .then(data => {
        meals[index] = data;
        // element.innerHTML = `
        //     <td>${data.meal}</td>
        //     <td>${formatIngredients(data.ingredients)}</td>
        //     <td>${data.instructions}</td>
        // `;
        element.innerHTML = `
            <td>${ data.meal }</td>
            <td><img src="${ data.mealThumb }" alt="${ data.meal }" width="100"></td>
        `;
        updateGroceryList();
    });
}

function formatIngredients(ingredients) {
    return ingredients.map(ingredient => ingredient.ingredient + ': ' + ingredient.measure).join(', ');
}

// Shared function for rendering grocery list from data (object or array)
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

function updateGroceryList() {
    // Rebuild grocery list from meals
    const groceryItems = {};
    meals.forEach(meal => {
        meal.ingredients.forEach(ingredient => {
            if (groceryItems[ingredient.ingredient]) {
                groceryItems[ingredient.ingredient] += ' & ' + ingredient.measure;
            } else {
                groceryItems[ingredient.ingredient] = ingredient.measure;
            }
        });
    });
    updateGroceryListFromData(groceryItems);
}

// Add Save As dialog for naming meal group
function saveMeals() {
    let groupName = prompt('Enter a name for this meal group:');
    if (!groupName) return;
    const now = new Date();
    const creationDate = now.toISOString().split('T')[0];
    const data = {
        groupName: groupName,
        creationDate: creationDate,
        meals: meals,
        groceryList: Array.from(document.querySelectorAll('#grocery-list li')).map(li => li.textContent)
    };
    fetch('/randommeals/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert('Meals and grocery list saved successfully!');
        } else {
            alert('Failed to save meals.');
        }
    });
}

function toggleGroceryList() {
    const groceryList = document.getElementById('grocery-list');
    const arrow = document.getElementById('grocery-list-arrow');
    groceryList.classList.toggle('collapsed');
    if (groceryList.classList.contains('collapsed')) {
        arrow.style.transform = 'rotate(-90deg)'; // Rotate arrow to point left
    } else {
        arrow.style.transform = 'rotate(0deg)'; // Reset arrow to point down
    }
}