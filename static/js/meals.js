document.getElementById("meal-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    // Gather all fields
    const meal_id = document.getElementById("meal-id").value;
    const meal = document.getElementById("meal-name").value;
    const category = document.getElementById("category").value;
    const area = document.getElementById("area").value;
    const instructions = document.getElementById("instructions").value
        .split(/\r?\n/)
        .filter(line => line.trim() !== "");
    const mealThumb = document.getElementById("mealThumb").value;
    const tags = document.getElementById("tags").value;
    const youtube = document.getElementById("youtube").value;

    // Gather ingredients
    const ingredientRows = document.querySelectorAll("#ingredients-list .ingredient-row");
    const ingredients = [];
    ingredientRows.forEach(row => {
        const ingredient = row.querySelector('.ingredient-name').value;
        const measure = row.querySelector('.ingredient-measure').value;
        if (ingredient.trim() !== "" || measure.trim() !== "") {
            ingredients.push({ ingredient, measure });
        }
    });

    // Compose meal object
    const mealObj = {
        meal,
        category,
        area,
        instructions,
        mealThumb,
        tags,
        youtube,
        ingredients
        // dateModified will be set server-side
    };
    if (meal_id) mealObj.mealId = meal_id;

    // Determine if create or update
    const url = meal_id ? `/meals/update` : `/meals/add`;

    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mealObj),
    });

    const result = await response.json();
    alert(result.message);
    // Optionally, redirect or update UI
});