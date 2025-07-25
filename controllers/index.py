from flask import Blueprint, render_template_string, request
from lib.mealDatabase import MealDatabase
from lib.utilities.fileService import FileService


class IndexController:
    def __init__(self):
        self.blueprint = Blueprint("index", __name__)
        self.mealDatabase = MealDatabase()
        self.fileService = FileService()
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule("/", "index", self.index)

    def index(self):
        # Get pagination parameters from query string
        try:
            page = int(request.args.get("page", 1))
        except (TypeError, ValueError):
            page = 1
        try:
            per_page = int(request.args.get("per_page", 10))
        except (TypeError, ValueError):
            per_page = 10
        start = (page - 1) * per_page
        end = start + per_page

        # Get filter parameters from query string
        filter_name = request.args.get("name", "").lower()

        # Apply filters
        meals = []
        if filter_name:
            meals = self.mealDatabase.searchMeals(filter_name)
        else:
            meals = self.mealDatabase.getAllMeals()

        paginated_meals = meals[start:end]

        table_html = self.fileService.read("./templates/index.html")

        return render_template_string(
            table_html,
            meals=paginated_meals,
            prev_page=page - 1 if page > 1 else 1,
            next_page=page + 1,
            per_page=per_page,
            filter_name=filter_name,
        )


# Instantiate the controller and get the blueprint
index_controller = IndexController()
indexBlueprint = index_controller.blueprint
