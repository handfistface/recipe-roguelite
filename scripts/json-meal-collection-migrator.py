import json
import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'carbunkle9-efficient',
    'database': 'recipe-roguelite'
}

# Function to create the meal_collections table
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_collections (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            editDate VARCHAR(255),
            meals TEXT
        )
    """)

# Function to insert a collection into the table
def insert_collection(cursor, collection):
    meals_json = json.dumps(collection['meals'])
    cursor.execute("""
        INSERT INTO meal_collections (id, name, description, editDate, meals)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        collection['id'],
        collection['name'],
        collection.get('description', ''),
        collection.get('editDate', ''),
        meals_json
    ))

# Main function to run the script
def main():
    # Load mealCollections.json data
    with open('data/mealCollections.json', 'r') as file:
        data = json.load(file)
        collections = data.get('collections', [])

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create the meal_collections table
    create_table(cursor)

    # Insert each collection into the database
    for collection in collections:
        insert_collection(cursor, collection)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()
