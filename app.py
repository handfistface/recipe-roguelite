from flask import Flask
from controllers.index import indexBlueprint
from controllers.randomMeals import randomMealsBlueprint
from controllers.mealsController import mealsBlueprint
from controllers.mealCollections import mealCollectionsBlueprint
from controllers.collectionIngredientsController import collection_ingredients_bp

# from controllers.random_meals import random_meals_blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(indexBlueprint)
app.register_blueprint(randomMealsBlueprint, url_prefix="/randommeals")
app.register_blueprint(mealsBlueprint, url_prefix="/meals")
app.register_blueprint(mealCollectionsBlueprint, url_prefix="/collections")
app.register_blueprint(collection_ingredients_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
