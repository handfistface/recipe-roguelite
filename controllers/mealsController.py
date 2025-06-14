from flask import Blueprint, render_template, request, jsonify
from lib.mealDatabase import MealDatabase


class MealsController:
    def __init__(self):
        self.blueprint = Blueprint("meals", __name__)
        self.register_routes()
        self.mealDatabase = MealDatabase()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "meals", self.meals_page)
        self.blueprint.add_url_rule("/add", "add_meal", self.add_meal, methods=["POST"])
        self.blueprint.add_url_rule(
            "/update", "update_meal", self.update_meal, methods=["POST"]
        )
        self.blueprint.add_url_rule("/edit/<meal_id>", "edit_meal", self.edit_meal)
        self.blueprint.add_url_rule("/get/<meal_id>", "get_meal", self.get_meal)

    def meals_page(self):
        return render_template("meals.html")

    def add_meal(self):
        data = request.json
        self.mealDatabase.addMeal(data)
        return jsonify({"message": "Meal added successfully"})

    def update_meal(self):
        data = request.json
        self.mealDatabase.updateMeal(data)
        return jsonify({"message": "Meal updated successfully"})

    def edit_meal(self, meal_id):
        return render_template("meals.html", meal_id=meal_id)

    def get_meal(self, meal_id):
        meal = self.mealDatabase.getMealById(meal_id)
        if meal:
            return jsonify(meal)
        return jsonify({"error": "Meal not found"}), 404


mealsController = MealsController()
mealsBlueprint = mealsController.blueprint
