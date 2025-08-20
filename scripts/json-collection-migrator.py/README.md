# Recipe Roguelite

This project is designed to migrate meal data from a JSON format into a MySQL database. It includes scripts for handling the migration process and JSON files containing the meal data.

## Project Structure

- `scripts/json-collection-migrator.py`: A Python script that ingests the `collection.json` file, creates a MySQL database table reflecting the structure of the data, and inserts all of the data into that table. It handles the conversion of JSON arrays for ingredients and instructions into text fields.
  
- `temp/collection.json`: Contains the JSON data representing a collection of meals, which will be migrated to the database.

- `temp/meal.json`: Contains the JSON data for individual meals, which is referenced in the `collection.json`.

- `requirements.txt`: Lists the Python dependencies required for the project, such as `mysql-connector-python` for MySQL database interaction.

## Setup Instructions

1. **Install MySQL**: Ensure that you have MySQL installed and running on your local machine.

2. **Create Database**: Create a database named `recipe-roguelite` in your MySQL server.

3. **Install Dependencies**: Navigate to the project directory and install the required Python packages using the following command:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Migration Script**: Execute the migration script to transfer the data from `collection.json` to the MySQL database:
   ```
   python scripts/json-collection-migrator.py
   ```

## Usage

After running the migration script, the meal data will be available in the `recipe-roguelite` database. You can query the database to access the meal information as needed.