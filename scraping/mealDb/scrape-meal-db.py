import json
import os
from lib.mealDbApi import MealDbApi


mealDbApi = MealDbApi()
letters = "abcdefghijklmnopqrstuvwxyz"
# letters = "ab"
meals = []
for letter in letters:
    mealResponse = mealDbApi.listMealsByFirstLetter(letter)
    print(f"Fetched meals for letter {letter}")
    if mealResponse and mealResponse["meals"]:
        meals.extend(mealResponse["meals"])

# output to a file
if not os.path.exists("./scraping/output"):
    os.makedirs("./scraping/output")
filePath = os.path.abspath("./scraping/output/meals.json")
with open(filePath, "w") as file:
    mealsJson = json.dumps(meals)
    file.write(mealsJson)
print(f"Successfully wrote {len(meals)} meals to {filePath}")
