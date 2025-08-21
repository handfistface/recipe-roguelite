import mysql.connector
import json
from lib.db_config import db_config

class MealDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor(dictionary=True)

    def getMealById(self, meal_id):
        query = "SELECT * FROM meals WHERE mealId = %s"
        self.cursor.execute(query, (meal_id,))
        meal = self.cursor.fetchone()
        if meal:
            meal['ingredients'] = json.loads(meal['ingredients']) if meal.get('ingredients') else []
            meal['instructions'] = json.loads(meal['instructions']) if meal.get('instructions') else []
        return meal

    def getMealIngredients(self, meal_id):
        meal = self.getMealById(meal_id)
        if not meal:
            return []
        ingredients = meal.get('ingredients', [])
        if ingredients and isinstance(ingredients, list) and ingredients and isinstance(ingredients[0], dict):
            return [i.get('ingredient') or i.get('name') or i.get('strIngredient') for i in ingredients if i.get('ingredient') or i.get('name') or i.get('strIngredient')]
        elif ingredients and isinstance(ingredients, list) and ingredients and isinstance(ingredients[0], str):
            return ingredients
        return []

    def getMealInstructions(self, meal_id):
        meal = self.getMealById(meal_id)
        if not meal:
            return []
        instructions = meal.get('instructions', [])
        if isinstance(instructions, str):
            return [i.strip() for i in instructions.split('.') if i.strip()]
        elif isinstance(instructions, list):
            return [i.strip() for i in instructions if i.strip()]
        return []

    def searchMeals(self, mealName):
        query = "SELECT * FROM meals WHERE LOWER(meal) LIKE %s"
        self.cursor.execute(query, (f"%{mealName.lower()}%",))
        results = self.cursor.fetchall()
        for meal in results:
            meal['ingredients'] = json.loads(meal['ingredients']) if meal.get('ingredients') else []
            meal['instructions'] = json.loads(meal['instructions']) if meal.get('instructions') else []
        return results

    def getAllMeals(self):
        query = "SELECT * FROM meals"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for meal in results:
            meal['ingredients'] = json.loads(meal['ingredients']) if meal.get('ingredients') else []
            meal['instructions'] = json.loads(meal['instructions']) if meal.get('instructions') else []
        return results

    def getMainCourses(self):
        blacklist = [
            "Dessert",
            "Side Dish",
            "Appetizer",
            "Salad",
            "Bread",
            "Breakfast",
            "Soup",
            "Beverage",
            "Sauce",
            "Marinade",
            "Fingerfood",
            "Snack",
            "Drink",
        ]
        query = "SELECT * FROM meals WHERE category NOT IN (%s)"
        format_strings = ','.join(['%s'] * len(blacklist))
        query = f"SELECT * FROM meals WHERE category NOT IN ({format_strings})"
        self.cursor.execute(query, tuple(blacklist))
        results = self.cursor.fetchall()
        for meal in results:
            meal['ingredients'] = json.loads(meal['ingredients']) if meal.get('ingredients') else []
            meal['instructions'] = json.loads(meal['instructions']) if meal.get('instructions') else []
        return results

    def updateMeal(self, meal):
        query = """
            UPDATE meals SET meal=%s, category=%s, area=%s, instructions=%s, mealThumb=%s, tags=%s, youtube=%s, ingredients=%s, source=%s WHERE mealId=%s
        """
        self.cursor.execute(query, (
            meal['meal'],
            meal['category'],
            meal['area'],
            json.dumps(meal['instructions']),
            meal['mealThumb'],
            meal['tags'],
            meal['youtube'],
            json.dumps(meal['ingredients']),
            meal.get('source', None),
            meal['mealId']
        ))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def createMeal(self, meal):
        query = """
            INSERT INTO meals (mealId, meal, category, area, instructions, mealThumb, tags, youtube, ingredients, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            meal['mealId'],
            meal['meal'],
            meal['category'],
            meal['area'],
            json.dumps(meal['instructions']),
            meal['mealThumb'],
            meal['tags'],
            meal['youtube'],
            json.dumps(meal['ingredients']),
            meal.get('source', None)
        ))
        self.connection.commit()
        return self.cursor.lastrowid

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()
