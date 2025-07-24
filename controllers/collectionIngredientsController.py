import re
from flask import Blueprint, render_template, request
from lib.mealCollectionDatabase import MealCollectionDatabase
from lib.mealDatabase import MealDatabase

collection_ingredients_bp = Blueprint('collection_ingredients', __name__)

class IngredientDTO:
    def __init__(self, name, total_measure):
        self.name = name
        self.total_measure = total_measure

def sum_measurements(measures):
    # Supported metrics: g, kg, ml, l, oz, tsp, tbsp
    metric_patterns = [
        (r"([\d\.]+)\s?g", "g"),
        (r"([\d\.]+)\s?kg", "kg"),
        (r"([\d\.]+)\s?ml", "ml"),
        (r"([\d\.]+)\s?l", "l"),
        (r"([\d\.]+)\s?oz", "oz"),
        (r"([\d\.]+)\s?tsp", "tsp"),
        (r"([\d\.]+)\s?tbsp", "tbsp"),
    ]
    sums = {}
    leftovers = []
    for measure in measures:
        matched = False
        for pattern, metric in metric_patterns:
            m = re.match(pattern, measure.lower())
            if m:
                val = float(m.group(1))
                sums[metric] = sums.get(metric, 0) + val
                matched = True
                break
        if not matched:
            leftovers.append(measure)
    result = []
    for metric in sums:
        # Format to remove .0 for integers
        val = int(sums[metric]) if sums[metric].is_integer() else round(sums[metric], 2)
        result.append(f"{val}{metric}")
    if leftovers:
        result.extend(leftovers)
    return ', '.join(result)

def get_collection_ingredients(collection_id):
    collection_db = MealCollectionDatabase()
    meal_db = MealDatabase()
    collection = collection_db.getCollectionById(collection_id)
    if not collection:
        return None, None
    meal_names = []
    ingredient_totals = {}
    for meal_id in collection.get('meals', []):
        meal = meal_db.getMealById(meal_id)
        if meal:
            meal_names.append(meal.get('meal'))
            for ing in meal.get('ingredients', []):
                name = ing['ingredient'].strip().lower()
                measure = ing['measure'].strip()
                if name in ingredient_totals:
                    ingredient_totals[name].append(measure)
                else:
                    ingredient_totals[name] = [measure]
    ingredient_dtos = [IngredientDTO(name, sum_measurements(ingredient_totals[name])) for name in sorted(ingredient_totals.keys())]
    return meal_names, ingredient_dtos

@collection_ingredients_bp.route('/collection-ingredients/<collection_id>')
def collection_ingredients(collection_id):
    meal_names, ingredients = get_collection_ingredients(collection_id)
    if meal_names is None:
        return render_template('collectionIngredients.html', error='Collection not found', meal_names=[], ingredients=[])
    return render_template('collectionIngredients.html', meal_names=meal_names, ingredients=ingredients)

