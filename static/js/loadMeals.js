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

function loadMealGroup(filename) {
    fetch(`/randommeals/load_save/${filename}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('loaded-meals-container').style.display = 'block';
            document.getElementById('loaded-meals-container').innerHTML = `
                <h3>Loaded Meals: ${data.groupName}</h3>
                <div><b>Created:</b> ${data.creationDate} &nbsp; <b>Last Loaded:</b> ${data.lastLoadDate}</div>
                <div id="meals-list"></div>
                <h3>Grocery List</h3>
                <ul id="grocery-list"></ul>
            `;
            renderMeals(data.meals);
            updateGroceryListFromData(data.groceryList);
        });
}

function renderMeals(meals) {
    const mealsList = document.getElementById('meals-list');
    mealsList.innerHTML = '';
    meals.forEach(meal => {
        const div = document.createElement('div');
        div.className = 'meal-entry';
        div.innerHTML = `
            <strong>${meal.meal}</strong><br>
            <img src="${meal.mealThumb}" alt="${meal.meal}" width="100"><br>
        `;
        mealsList.appendChild(div);
    });
}

// This function is shared with randomMeals.js for consistency
function updateGroceryListFromData(groceryList) {
    const groceryUl = document.getElementById('grocery-list');
    groceryUl.innerHTML = '';
    if (Array.isArray(groceryList)) {
        groceryList.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            groceryUl.appendChild(li);
        });
    } else if (typeof groceryList === 'object') {
        Object.entries(groceryList).forEach(([ingredient, measure]) => {
            const li = document.createElement('li');
            li.textContent = `${ingredient}: ${measure}`;
            groceryUl.appendChild(li);
        });
    }
}
