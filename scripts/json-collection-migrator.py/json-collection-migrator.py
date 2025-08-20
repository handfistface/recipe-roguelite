import json
import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'REPLACE_WITH_PWD',
    'database': 'recipe-roguelite'
}

# Function to create the meals table
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mealId VARCHAR(255) NOT NULL,
            meal VARCHAR(255) NOT NULL,
            category VARCHAR(255),
            area VARCHAR(255),
            instructions TEXT,
            mealThumb VARCHAR(255),
            tags VARCHAR(255),
            youtube VARCHAR(255),
            ingredients TEXT,
            source VARCHAR(255)
        )
    """)

# Function to insert meal data into the table
def insert_meal(cursor, meal):
    ingredients = json.dumps(meal['ingredients'])
    instructions = json.dumps(meal['instructions'])
    
    cursor.execute("""
        INSERT INTO meals (mealId, meal, category, area, instructions, mealThumb, tags, youtube, ingredients, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        meal['mealId'],
        meal['meal'],
        meal['category'],
        meal['area'],
        instructions,
        meal['mealThumb'],
        meal['tags'],
        meal['youtube'],
        ingredients,
        meal.get('source', None)
    ))

# Main function to run the script
def main():
    # Load collection.json data
    with open('data/convertedMeals.json', 'r') as file:
        collection_data = json.load(file)

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create the meals table
    create_table(cursor)

    # Insert each meal into the database
    for meal in collection_data:
        insert_meal(cursor, meal)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()