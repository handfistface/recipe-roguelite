// loadMeals.js: Handles loading and displaying saved meal groups

document.addEventListener('DOMContentLoaded', function() {
    fetch('/randommeals/list_saves')
        .then(res => res.json())
        .then(data => populateSavesTable(data));
});

function populateSavesTable(saves) {
    const tbody = document.querySelector('#saved-meals-table tbody');
    tbody.innerHTML = '';
    saves.forEach(save => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${save.groupName}</td>
            <td>${save.creationDate}</td>
            <td>${save.lastLoadDate || ''}</td>
            <td><button onclick="loadMealGroup('${save.filename}')">Load</button></td>
        `;
        tbody.appendChild(tr);
    });
}

let meals = [];
let loadedFilename = null;

function loadMealGroup(filename) {
    loadedFilename = filename;
    fetch(`/randommeals/load_save/${filename}`)
        .then(res => res.json())
        .then(data => {
            meals = data.meals;
            document.getElementById('loaded-meals-container').style.display = 'block';
            document.getElementById('loaded-meals-container').innerHTML = `
                <h3>Loaded Meals: ${data.groupName}</h3>
                <div><b>Created:</b> ${data.creationDate} &nbsp; <b>Last Loaded:</b> ${data.lastLoadDate}</div>
                <button id="save-loaded-meals-btn">Save As</button>
                <table id="meals-table" border="1" style="width:100%;margin-top:20px;">
                    <tr>
                        <th>Name</th>
                        <th>Ingredients</th>
                    </tr>
                </table>
                <h3>Grocery List</h3>
                <ul id="grocery-list"></ul>
            `;
            renderMealsTable(meals);
            updateGroceryListFromMeals(meals);
            document.getElementById('save-loaded-meals-btn').onclick = saveLoadedMealsAsNewCollection;
        });
}

function renderMealsTable(meals) {
    const table = document.getElementById('meals-table');
    // Remove all rows except header
    while (table.rows.length > 1) table.deleteRow(1);
    meals.forEach((meal, idx) => {
        const tr = document.createElement('tr');
        tr.onclick = () => rerollMealInLoad(tr, idx);
        tr.innerHTML = `
            <td>${meal.meal}</td>
            <td><img src="${meal.mealThumb}" alt="${meal.meal}" width="100"></td>
        `;
        table.appendChild(tr);
    });
}

function rerollMealInLoad(rowElement, index) {
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
        rowElement.innerHTML = `
            <td>${data.meal}</td>
            <td><img src="${data.mealThumb}" alt="${data.meal}" width="100"></td>
        `;
        updateGroceryListFromMeals(meals);
    });
}

function updateGroceryListFromMeals(mealsArr) {
    // Build grocery list from meals array
    const groceryItems = {};
    mealsArr.forEach(meal => {
        meal.ingredients.forEach(ingredient => {
            if (groceryItems[ingredient.ingredient]) {
                groceryItems[ingredient.ingredient] += ' & ' + ingredient.measure;
            } else {
                groceryItems[ingredient.ingredient] = ingredient.measure;
            }
        });
    });
    updateGroceryListFromData(groceryItems);
    // Attach removeItem to all li
    document.querySelectorAll('#grocery-list li').forEach(li => {
        li.onclick = () => removeItem(li);
    });
}

function saveLoadedMealsAsNewCollection() {
    let groupName = prompt('Enter a name for this meal group:');
    if (!groupName) return;
    const now = new Date();
    const creationDate = now.toISOString().split('T')[0];
    // Get grocery list from current meals
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
    const data = {
        groupName: groupName,
        creationDate: creationDate,
        meals: meals,
        groceryList: Object.entries(groceryItems).map(([ingredient, measure]) => `${ingredient}: ${measure}`)
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
