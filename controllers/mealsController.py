from flask import Blueprint, render_template, request, jsonify
from lib.mealDatabase import MealDatabase


class MealsController:
    def __init__(self):
        self.blueprint = Blueprint("meals", __name__)
        self.register_routes()
        self.mealDatabase = MealDatabase()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "meals", self.meals_page)
        self.blueprint.add_url_rule("/create", "create_meal", self.create_meal, methods=["GET"])
        self.blueprint.add_url_rule("/add", "add_meal", self.add_meal, methods=["POST"])
        self.blueprint.add_url_rule(
            "/update", "update_meal", self.update_meal, methods=["POST"]
        )
        self.blueprint.add_url_rule("/edit/<meal_id>", "edit_meal", self.edit_meal)
        self.blueprint.add_url_rule("/get/<meal_id>", "get_meal", self.get_meal)

    def meals_page(self):
        # Optionally, redirect to create page or show a list
        return render_template("meals.html", meal=None, meal_id=None)

    def create_meal(self):
        # Render the meal form with empty/default values
        empty_meal = {
            "meal": "",
            "category": "",
            "area": "",
            "instructions": [],
            "mealThumb": "",
            "tags": "",
            "youtube": "",
            "ingredients": [],
            "dateModified": None
        }
        return render_template("meals.html", meal=empty_meal, meal_id=None)

    def add_meal(self):
        data = request.json
        from datetime import datetime
        data["dateModified"] = datetime.utcnow().isoformat()
        self.mealDatabase.addMeal(data)
        return jsonify({"message": "Meal added successfully"})

    def update_meal(self):
        data = request.json
        from datetime import datetime
        data["dateModified"] = datetime.utcnow().isoformat()
        self.mealDatabase.updateMeal(data)
        return jsonify({"message": "Meal updated successfully"})

    def edit_meal(self, meal_id):
        meal = self.mealDatabase.getMealById(meal_id)
        return render_template("meals.html", meal=meal, meal_id=meal_id)

    def get_meal(self, meal_id):
        meal = self.mealDatabase.getMealById(meal_id)
        if meal:
            return jsonify(meal)
        return jsonify({"error": "Meal not found"}), 404


mealsController = MealsController()
mealsBlueprint = mealsController.blueprint
