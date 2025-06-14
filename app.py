from flask import Flask
from controllers.index import indexBlueprint
from controllers.randomMeals import randomMealsBlueprint
from controllers.mealsController import mealsBlueprint

# from controllers.random_meals import random_meals_blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(indexBlueprint)
app.register_blueprint(randomMealsBlueprint, url_prefix="/randommeals")
app.register_blueprint(mealsBlueprint, url_prefix="/meals")

if __name__ == "__main__":
    app.run(debug=True)
