import json
import random
import os
from datetime import datetime
from flask import Blueprint, render_template_string, jsonify, request, render_template
from lib.meal_db_singleton import meal_db
from lib.utilities.fileService import FileService


class RandomMealsController:
    def __init__(self):
        self.blueprint = Blueprint("randommeals", __name__)
        self.register_routes()

        self.mealDatabase = meal_db
        self.fileService = FileService()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "randommeals", self.randomMeals)
        self.blueprint.add_url_rule(
            "/reroll", "reroll_meal", self.rerollMeal, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/save", "save_meals", self.saveMeals, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/list_saves", "list_saves", self.listSaves, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/load_save/<filename>", "load_save", self.loadSave, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/loadMeals", "load_meals_page", self.loadMealsPage, methods=["GET"]
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

        group_name = data.get("groupName")
        creation_date = data.get("creationDate")
        grocery_list = data.get("groceryList")
        meals = data.get("meals")
        if not group_name or not creation_date or not meals:
            return jsonify({"error": "Missing groupName, creationDate, or meals"}), 400

        # Ensure directory exists
        save_dir = os.path.join(os.path.dirname(__file__), "..", "saved_meals")
        os.makedirs(save_dir, exist_ok=True)

        # Use group name for filename only (no date)
        safe_name = group_name.replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}.json"
        filepath = os.path.join(save_dir, filename)

        # Add/Update metadata
        save_data = {
            "groupName": group_name,
            "creationDate": creation_date,
            "lastLoadDate": data.get("lastLoadDate", creation_date),
            "meals": meals,
            "groceryList": grocery_list,
        }
        try:
            with open(filepath, "w") as f:
                json.dump(save_data, f, indent=4)
            return jsonify({"message": "Meals saved successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def listSaves(self):
        save_dir = os.path.join(os.path.dirname(__file__), "..", "saved_meals")
        os.makedirs(save_dir, exist_ok=True)
        saves = []
        for fname in os.listdir(save_dir):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(save_dir, fname), "r") as f:
                        data = json.load(f)
                        saves.append(
                            {
                                "filename": fname,
                                "groupName": data.get("groupName"),
                                "creationDate": data.get("creationDate"),
                                "lastLoadDate": data.get("lastLoadDate"),
                            }
                        )
                except Exception:
                    continue
        return jsonify(saves)

    def loadSave(self, filename):
        save_dir = os.path.join(os.path.dirname(__file__), "..", "saved_meals")
        filepath = os.path.join(save_dir, filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "Save file not found"}), 404
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            # Update lastLoadDate
            data["lastLoadDate"] = datetime.now().strftime("%Y-%m-%d")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def loadMealsPage(self):
        return render_template("loadMeals.html")


# Initialize the controller with the Flask app
random_meals_controller = RandomMealsController()
randomMealsBlueprint = random_meals_controller.blueprint
