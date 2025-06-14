import json

# Load singleMeal.json
with open("scraping/output/meals.json", "r") as f:
    allMeals = json.load(f)

convertedMeals = []
for single_meal in allMeals:
    # Convert to targetOutput.json structure
    target_output = {
        "mealId": single_meal["idMeal"],
        "meal": single_meal["strMeal"],
        "drinkAlternate": single_meal["strDrinkAlternate"],
        "category": single_meal["strCategory"],
        "area": single_meal["strArea"],
        "instructions": single_meal["strInstructions"].split("\r\n"),
        "mealThumb": single_meal["strMealThumb"],
        "tags": single_meal["strTags"],
        "youtube": single_meal["strYoutube"],
        "ingredients": [
            {
                "ingredient": single_meal[f"strIngredient{i}"],
                "measure": single_meal[f"strMeasure{i}"],
            }
            for i in range(1, 21)
            if single_meal[f"strIngredient{i}"]
        ],
        "source": single_meal["strSource"],
        "imageSource": single_meal["strImageSource"],
        "creativeCommonsConfirmed": single_meal["strCreativeCommonsConfirmed"],
        "dateModified": single_meal["dateModified"],
    }
    convertedMeals.append(target_output)

# Save to convertedMealDb.json
with open("scraping/output/convertedMeals.json", "w") as f:
    json.dump(convertedMeals, f, indent=4)
