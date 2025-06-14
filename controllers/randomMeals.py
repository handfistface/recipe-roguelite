import json
import random
from flask import Blueprint, render_template_string, jsonify, request
from lib.mealDatabase import MealDatabase
from lib.utilities.fileService import FileService


class RandomMealsController:
    def __init__(self):
        self.blueprint = Blueprint("randommeals", __name__)
        self.register_routes()

        self.mealDatabase = MealDatabase()
        self.fileService = FileService()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "randommeals", self.randomMeals)
        self.blueprint.add_url_rule(
            "/reroll", "reroll_meal", self.rerollMeal, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/save", "save_meals", self.saveMeals, methods=["POST"]
        )

    def randomMeals(self):
        meals = self.mealDatabase.getMainCourses()

        # Get the number of meals to generate from the query parameter
        num_meals = int(request.args.get("num_meals", 7))

        random_meals = random.sample(meals, num_meals)

        # Parse ingredients and create a grocery list
        grocery_list = self.create_grocery_list(random_meals)

        table_html = self.fileService.read("./templates/randomMeals.html")

        return render_template_string(
            table_html,
            meals=random_meals,
            grocery_list=grocery_list,
            formatIngredients=self.formatIngredients,
        )

    def rerollMeal(self):
        meals = self.mealDatabase.getAllMeals()
        new_meal = random.choice(meals)
        return jsonify(new_meal)

    def convert_measure(self, measure):
        # Implement conversion logic here
        # For simplicity, this example assumes all measures are in the same unit
        # You can extend this function to handle unit conversions
        try:
            return float(measure.split()[0])
        except ValueError:
            return 0

    def formatIngredients(self, ingredients):
        return ", ".join(
            [
                f"{ingredient['ingredient']}: {ingredient['measure']}"
                for ingredient in ingredients
            ]
        )

    def create_grocery_list(self, meals):
        grocery_list = {}
        for meal in meals:
            for ingredient in meal["ingredients"]:
                ingredient_value = ingredient["ingredient"]
                measure = ingredient["measure"]
                if not ingredient_value:
                    continue
                if ingredient_value in grocery_list:
                    grocery_list[ingredient_value] += " & " + measure
                else:
                    grocery_list[ingredient_value] = measure
        return grocery_list

    def saveMeals(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        try:
            with open("./saved_meals.json", "w") as f:
                json.dump(data, f, indent=4)
            return jsonify({"message": "Meals saved successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Initialize the controller with the Flask app
random_meals_controller = RandomMealsController()
randomMealsBlueprint = random_meals_controller.blueprint
