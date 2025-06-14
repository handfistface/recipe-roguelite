import requests


class MealDbApi:
    def listMealsByFirstLetter(self, letter):
        # Define the API endpoint for recipe search
        base_url = f"https://www.themealdb.com/api/json/v1/1/search.php"

        # Prepare the query parameters: number of recipes per day
        params = {
            "f": letter,
        }

        # Make a GET request to the API
        response = requests.get(base_url, params)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return data

        # If the response is unsuccessful, print the error code
        print(f"Error: {response.status_code} occurred when fetching recipes.")
        return None
