document.addEventListener('DOMContentLoaded', function() {
    let currentCollectionId = null;

    // Show the create collection interface
    document.getElementById('goToCreateCollectionBtn').addEventListener('click', function() {
        document.getElementById('createCollectionInterface').style.display = 'block';
        document.getElementById('goToCreateCollectionBtn').style.display = 'none';
    });

    // Cancel create collection
    document.getElementById('cancelCreateCollectionBtn').addEventListener('click', function() {
        document.getElementById('createCollectionInterface').style.display = 'none';
        document.getElementById('goToCreateCollectionBtn').style.display = 'inline-block';
    });

    document.getElementById('createCollectionBtn').addEventListener('click', function() {
        const name = document.getElementById('collectionName').value;
        fetch('/collections/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        })
        .then(res => res.json())
        .then(data => {
            currentCollectionId = data.collection_id;
            document.getElementById('createCollectionInterface').style.display = 'none';
            document.getElementById('goToCreateCollectionBtn').style.display = 'inline-block';
            document.getElementById('searchSection').style.display = 'block';
            document.getElementById('collectionMealsSection').style.display = 'block';
            updateCollectionMeals();
        });
    });

    document.getElementById('searchMealBtn').addEventListener('click', function() {
        const query = document.getElementById('mealSearchInput').value;
        fetch(`/collections/search_meals?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(meals => {
            const resultsList = document.getElementById('searchResults');
            resultsList.innerHTML = '';
            meals.forEach(meal => {
                const li = document.createElement('li');
                li.textContent = meal.meal;
                const addBtn = document.createElement('button');
                addBtn.textContent = 'Add';
                addBtn.onclick = function() {
                    addMealToCollection(meal.idMeal);
                };
                li.appendChild(addBtn);
                resultsList.appendChild(li);
            });
        });
    });

    function addMealToCollection(mealId) {
        fetch('/collections/add_meal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ collection_id: currentCollectionId, meal_id: mealId })
        })
        .then(res => res.json())
        .then(() => {
            updateCollectionMeals();
        });
    }

    function updateCollectionMeals() {
        fetch(`/collections/get/${currentCollectionId}`)
        .then(res => res.json())
        .then(collection => {
            const mealsList = document.getElementById('collectionMeals');
            mealsList.innerHTML = '';
            if (collection.meals) {
                collection.meals.forEach(meal => {
                    const li = document.createElement('li');
                    li.textContent = meal.meal;
                    mealsList.appendChild(li);
                });
            }
        });
    }
});
