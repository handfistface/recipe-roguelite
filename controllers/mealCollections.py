import json
from flask import Blueprint, render_template, request, jsonify
from lib.mealCollectionDatabase import MealCollectionDatabase
from lib.meal_db_singleton import meal_db

class MealCollectionsController:
    def __init__(self):
        self.blueprint = Blueprint("mealCollections", __name__)
        self.register_routes()
        self.mealDatabase = meal_db
        self.collections = {}  # In-memory store for collections (replace with persistent storage as needed)
        self.mealCollectionsDatabase = MealCollectionDatabase()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "collections_page", self.collections_page)
        self.blueprint.add_url_rule("/create", "create_collection", self.create_collection, methods=["POST"])
        self.blueprint.add_url_rule("/search_meals", "search_meals", self.search_meals, methods=["GET"])
        self.blueprint.add_url_rule("/add_meal", "add_meal_to_collection", self.add_meal_to_collection, methods=["POST"])
        self.blueprint.add_url_rule("/get/<collection_id>", "get_collection", self.get_collection)
        self.blueprint.add_url_rule("/create_collection", "create_collection_page", self.create_collection_page, methods=["GET"])
        self.blueprint.add_url_rule("/delete/<collection_id>", "delete_collection", self.delete_collection, methods=["DELETE"])

    def delete_collection(self, collection_id):
        deleted = self.mealCollectionsDatabase.deleteCollection(collection_id)
        if deleted:
            return jsonify({"message": "Collection deleted", "collection_id": collection_id})
        else:
            return jsonify({"error": "Collection not found"}), 404

    def create_collection_page(self):
        return render_template("createCollection.html")

    def collections_page(self):
        # Pagination parameters
        try:
            current_page = int(request.args.get("page", 1))
        except ValueError:
            current_page = 1
        per_page = 5  # Number of collections per page

        # Get all collections from DB
        all_collections = self.mealCollectionsDatabase.getAllCollections()
        total_collections = len(all_collections)
        page_count = (total_collections + per_page - 1) // per_page

        # Slice collections for current page
        start_idx = (current_page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_collections = all_collections[start_idx:end_idx]

        return render_template(
            "mealCollections.html",
            collections=paginated_collections,
            page_count=page_count,
            current_page=current_page
        )

    def create_collection(self):
        data = request.json
        # Parse meals from comma-separated string if provided
        meals_raw = data.get("meals", "")
        if isinstance(meals_raw, str):
            meals = [m.strip() for m in meals_raw.split(",") if m.strip()]
        elif isinstance(meals_raw, list):
            meals = meals_raw
        else:
            meals = []
        # Prepare collection dict for DB
        collection_data = {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "meals": meals
        }
        collection_id = data.get("collection_id")
        if collection_id:
            # Editing: update existing collection
            updated = self.mealCollectionsDatabase.updateCollection(collection_id, collection_data)
            if updated:
                return jsonify({"message": "Collection updated", "collection_id": collection_id})
            else:
                return jsonify({"error": "Collection not found or update failed"}), 404
        else:
            # Creating: add new collection
            new_id = self.mealCollectionsDatabase.addCollection(collection_data)
            return jsonify({"message": "Collection created", "collection_id": new_id})

    def search_meals(self):
        query = request.args.get("query", "")
        results = self.mealDatabase.searchMeals(query)
        # Ensure each result has mealId, meal, mealThumb
        formatted = []
        for m in results:
            formatted.append({
                "mealId": m.get("mealId") or m.get("idMeal") or m.get("id"),
                "meal": m.get("meal") or m.get("strMeal"),
                "mealThumb": m.get("mealThumb") or m.get("strMealThumb")
            })
        return jsonify(formatted)

    def add_meal_to_collection(self):
        data = request.json
        collection_id = data.get("collection_id")
        meal_id = data.get("meal_id")
        if collection_id in self.collections:
            meal = self.mealDatabase.getMealById(meal_id)
            if meal:
                self.collections[collection_id]["meals"].append(meal)
                return jsonify({"message": "Meal added to collection"})
            return jsonify({"error": "Meal not found"}), 404
        return jsonify({"error": "Collection not found"}), 404

    def get_collection(self, collection_id):
        # Fetch from persistent DB, not in-memory
        collection = self.mealCollectionsDatabase.getCollectionById(collection_id)
        if collection:
            # Replace meals (IDs) with full meal objects
            meal_ids = collection.get("meals", [])
            meals = []
            for meal_id in meal_ids:
                meal = self.mealDatabase.getMealById(meal_id)
                if meal:
                    meals.append(meal)
            collection = dict(collection)  # Copy to avoid mutating DB
            collection["meals"] = meals
            collectionJson = json.dumps(collection, indent=4)  # Format for readability
            return jsonify(collection)
        return jsonify({"error": "Collection not found"}), 404

mealCollectionsController = MealCollectionsController()
mealCollectionsBlueprint = mealCollectionsController.blueprint
