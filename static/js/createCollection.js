document.addEventListener('DOMContentLoaded', function() {

    // Helper to get query param
    function getQueryParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    const collectionId = getQueryParam('collection_id');
    // Hide form button, show correct bottom button
    document.getElementById('formCreateBtn').style.display = 'none';
    if (collectionId) {
        document.getElementById('saveCollectionBtn').style.display = 'inline-block';
        document.getElementById('createCollectionBtn').style.display = 'none';
        // Editing mode: fetch collection and pre-fill form
        fetch(`/collections/get/${collectionId}`)
            .then(res => res.json())
            .then(collection => {
                if (collection.error) return;
                document.getElementById('formTitle').textContent = 'Edit Meal Collection';
                document.getElementById('collectionName').value = collection.name || '';
                document.getElementById('collectionDescription').value = collection.description || '';
                // Meals: convert array to comma-separated IDs if possible
                if (Array.isArray(collection.meals)) {
                    window.currentMeals = collection.meals.map(m => ({
                        mealId: m.mealId || m.idMeal || m.id,
                        meal: m.meal || m.strMeal,
                        mealThumb: m.mealThumb || m.strMealThumb
                    }));
                    renderMealsTable();
                    document.getElementById('collectionMeals').value = window.currentMeals.map(m => m.mealId).join(',');
                }
            });
    } else {
        document.getElementById('saveCollectionBtn').style.display = 'none';
        document.getElementById('createCollectionBtn').style.display = 'inline-block';
        window.currentMeals = [];
    }

    // Render meals table
    function renderMealsTable() {
        const tbody = document.querySelector('#mealsTable tbody');
        tbody.innerHTML = '';
        window.currentMeals.forEach(function(meal, idx) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${meal.meal}</td>
                <td><img src="${meal.mealThumb}" alt="${meal.meal}" style="width:60px; height:auto;"></td>
                <td><button class="removeMealBtn" data-idx="${idx}" style="background:none; border:none; color:red; font-size:20px; cursor:pointer;" title="Remove"><span>&#128465;</span></button></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Remove meal
    document.querySelector('#mealsTable').addEventListener('click', function(e) {
        if (e.target.closest('.removeMealBtn')) {
            const idx = e.target.closest('.removeMealBtn').dataset.idx;
            window.currentMeals.splice(idx, 1);
            renderMealsTable();
            document.getElementById('collectionMeals').value = window.currentMeals.map(function(m) { return m.mealId; }).join(',');
        }
    });

    // Add Meal button opens modal
    document.getElementById('addMealBtn').addEventListener('click', function() {
        document.getElementById('searchModal').style.display = 'block';
        document.getElementById('searchInput').value = '';
        document.querySelector('#searchResultsTable tbody').innerHTML = '';
    });

    // Close modal
    document.getElementById('closeModalBtn').addEventListener('click', function() {
        document.getElementById('searchModal').style.display = 'none';
    });

    // Search meals
    document.getElementById('searchInput').addEventListener('input', function() {
        const query = this.value.trim();
        if (!query) {
            document.querySelector('#searchResultsTable tbody').innerHTML = '';
            return;
        }
        fetch(`/collections/search_meals?query=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(results => {
                const tbody = document.querySelector('#searchResultsTable tbody');
                tbody.innerHTML = '';
                results.forEach(meal => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${meal.meal || meal.strMeal}</td>
                        <td><img src="${meal.mealThumb || meal.strMealThumb}" alt="${meal.meal || meal.strMeal}" style="width:60px; height:auto;"></td>
                        <td><button class="addMealBtn" data-mealid="${meal.mealId || meal.idMeal || meal.id}" data-mealname="${meal.meal || meal.strMeal}" data-mealthumb="${meal.mealThumb || meal.strMealThumb}" style="background:none; border:none; color:green; font-size:20px; cursor:pointer;" title="Add"><span>+</span></button></td>
                    `;
                    tbody.appendChild(tr);
                });
            });
    });

    // Add meal from search
    document.querySelector('#searchResultsTable').addEventListener('click', function(e) {
        if (e.target.closest('.addMealBtn')) {
            const btn = e.target.closest('.addMealBtn');
            const mealId = btn.dataset.mealid;
            const mealName = btn.dataset.mealname;
            const mealThumb = btn.dataset.mealthumb;
            // Prevent duplicates
            if (!window.currentMeals.some(m => m.mealId === mealId)) {
                window.currentMeals.push({ mealId, meal: mealName, mealThumb });
                renderMealsTable();
                document.getElementById('collectionMeals').value = window.currentMeals.map(m => m.mealId).join(',');
            }
        }
    });

    function handleSaveOrCreate(isEdit) {
        const name = document.getElementById('collectionName').value;
        const description = document.getElementById('collectionDescription').value;
        const meals = window.currentMeals.map(m => m.mealId);
        let url = '/collections/create';
        let payload = { name, description, meals };
        if (isEdit) {
            payload.collection_id = collectionId;
        }
        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('creationMessage').textContent = data.message;
            if (!isEdit) {
                document.getElementById('createCollectionForm').reset();
                window.currentMeals = [];
                renderMealsTable();
            }
        });
    }

    document.getElementById('saveCollectionBtn').addEventListener('click', function() {
        handleSaveOrCreate(true);
    });
    document.getElementById('createCollectionBtn').addEventListener('click', function() {
        handleSaveOrCreate(false);
    });
    // Initial render for new collection
    renderMealsTable();
});
