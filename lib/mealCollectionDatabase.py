    


import datetime
import json
import mysql.connector
import importlib.util
import os

class MealCollectionDatabase:
    def __init__(self):
        # Dynamically load db_config.py
        config_path = os.path.join(os.path.dirname(__file__), 'db_config.py')
        spec = importlib.util.spec_from_file_location("db_config", config_path)
        db_config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(db_config_module)
        self.db_config = db_config_module.db_config

    def _get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def getCollectionById(self, collection_id):
        """
        Returns the collection with the given ID, or None if not found.
        """
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meal_collections WHERE id = %s", (str(collection_id),))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            result['meals'] = json.loads(result['meals']) if result['meals'] else []
        return result

    def getAllCollections(self):
        """
        Returns a list of all meal collections.
        """
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meal_collections")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in results:
            r['meals'] = json.loads(r['meals']) if r['meals'] else []
        return results

    def addCollection(self, collection):
        conn = self._get_connection()
        cursor = conn.cursor()
        # Find max id and increment
        cursor.execute("SELECT MAX(CAST(id AS UNSIGNED)) FROM meal_collections")
        max_id = cursor.fetchone()[0]
        collection_id = str((max_id + 1) if max_id is not None else 1)
        name = collection.get("name", f"Collection {collection_id}")
        description = collection.get("description", "")
        meals = json.dumps(collection.get("meals", []))
        editDate = datetime.datetime.utcnow().isoformat() + "Z"
        cursor.execute(
            """
            INSERT INTO meal_collections (id, name, description, editDate, meals)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (collection_id, name, description, editDate, meals)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return collection_id

    def updateCollection(self, collection_id, collection_data):
        """
        Update a collection by its ID. Returns True if updated, False if not found.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        # Only update provided fields
        fields = []
        values = []
        allowed = {"name", "description", "meals", "editDate"}
        for k, v in collection_data.items():
            if k in allowed:
                if k == "meals":
                    v = json.dumps(v)
                fields.append(f"{k} = %s")
                values.append(v)
        if not fields:
            cursor.close()
            conn.close()
            return False
        values.append(str(collection_id))
        sql = f"UPDATE meal_collections SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(sql, tuple(values))
        updated = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return updated

    def deleteCollection(self, collection_id):
        """
        Delete a collection by its ID. Returns True if deleted, False if not found.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meal_collections WHERE id = %s", (str(collection_id),))
        deleted = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return deleted