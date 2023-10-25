#  SUMMARY ================================================================
# This file deals with connecting to a database, performing data operations, 
# and handling database-related exceptions.
#  retrieve the menu (alcohol and not alcohol) with ingredients and allergies (Lydia)
#  retrieve cocktail alcohol and non-alcohol main ingredients (Lydia)
#  retrieve cocktail with a specific selected main ingredient (Lydia)
# =========================================================================

# Python Packages imports 
import mysql.connector
from config import HOST, USER, PASSWORD


# Define a function to connect to the database with the given name
def _connect_to_db(db_name):
    # Establish a connection to the database using the provided parameters (host, user, password, auth_plugin, and database name)
    cnx = mysql.connector.connect(
        host=HOST,  # The hostname of the database server
        user=USER,  # The username for database access
        password=PASSWORD,  # The password for database access
        auth_plugin='mysql_native_password',  # The authentication plugin to use
        database=db_name  # The name of the specific database to connect to
    )
    return cnx  # Return the established database connection



# Define a custom exception class for handling database connection errors
class DbConnectionError(Exception):
    pass

# Define a function to get all cocktail recipes from the database
def get_all_cocktail_recipes():
    cocktail_menu = []  # Initialize an empty list to store cocktail data
    try:
        db_name = 'Cocktails'  # Name of the database to connect to
        db_connection = _connect_to_db(db_name)  # Establish a database connection
        cur = db_connection.cursor()  # Create a cursor object for executing SQL queries
        print("Connected to DB: %s" % db_name)  # Print a message indicating a successful connection

        query = """
        SELECT *
        FROM CocktailsInfo
        """

        cur.execute(query)  # Execute the SQL query to retrieve cocktail data

        # Fetch all the data from the cursor and store it in cocktail_menu
        cocktail_menu = cur.fetchall()

        cur.close()  # Close the cursor

        # You can now work with the fetched data if needed
        return cocktail_menu

    except Exception:
        raise DbConnectionError("Failed to read data from DB")  # Raise a custom exception for database connection errors

    finally:
        if db_connection:
            db_connection.close()  # Close the database connection


def get_cocktail_by_id(cocktail_id):
    try:
        # Establish a database connection
        db_connection = _connect_to_db('Cocktails')
        cursor = db_connection.cursor()

        # Execute an SQL query to fetch the cocktail by ID
        query = "SELECT * FROM CocktailsInfo WHERE Id = %s"
        cursor.execute(query, (cocktail_id,))


        # Fetch the data
        cocktail_data = cursor.fetchone()

        # Close the cursor and the connection
        cursor.close()
        db_connection.close()
        return cocktail_data
       
    except Exception:
        raise DbConnectionError("Failed to read data from DB")  # Raise a custom exception for database connection errors

    finally:
        if db_connection:
            db_connection.close()  # Close the database connection

def get_cocktails_by_ingredient(ingredient):
    try:
        cocktails_with_ingredient  = []  # Initialize an empty list to store cocktail data
        # Establish a database connection
        db_connection = _connect_to_db('Cocktails')
        cursor = db_connection.cursor()

        # Execute an SQL query to fetch cocktails by ingredient
        query = "SELECT c.* FROM CocktailsInfo c JOIN CocktailIngredients ci ON c.Id = ci.CocktailId JOIN Ingredients i ON ci.IngredientId = i.IngredientId WHERE i.IngredientId LIKE %s"
        cursor.execute(query, ('%'+ingredient+'%',))


        # Fetch the data
        cocktails_with_ingredient = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        db_connection.close()
        return cocktails_with_ingredient

    except Exception as e:
        raise DbConnectionError(f"Failed to fetch cocktails by ingredient: {str(e)}")

def get_cocktails_sorted_by_name_asc():
    try:
        # Establish a database connection
        db_connection = _connect_to_db('Cocktails')
        cursor = db_connection.cursor()

        # Execute an SQL query to fetch all cocktails and sort them by name in ascending order
        query = "SELECT * FROM CocktailsInfo ORDER BY CocktailName ASC"
        cursor.execute(query)

        # Fetch the data
        sorted_cocktails = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        db_connection.close()

        return sorted_cocktails  # Return the sorted cocktails
    except Exception as e:
        raise DbConnectionError(f"Failed to fetch sorted cocktails: {str(e)}")


            
def add_new_ingredient_to_ingredients(ingredientName):
    try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()

        if cursor.execute("SELECT IngredientName FROM Ingredients WHERE IngredientName = %s ", (ingredientName)):
            print(f"{ingredientName.capitalize()} is an existing ingredient, we can not duplicate it")
        else:
            cursor.execute("INSERT INTO Ingredients(IngredientName) VALUES(%s)", (ingredientName))

            db_connection.commit()
            print(f"New ingredient: {ingredientName} has been added to ingredients")

    except Exception as e:
        print("Failed to modify ingredient:", str(e))
    finally:
        if db_connection:
            cursor.close()
            db_connection.close()


# a method to add new ingredients to a cocktail (receives cocktailId, array of ingredients, amounts and units) and post new ingredients to a given cocktail
def add_new_ingredient_to_cocktail(cocktailId, ingredients, amounts, units):
    try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()

        for i in range(0, len(ingredients)):
            # modify unit and amount based on unit
                if units[i] == "ml":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountMl) VALUES (%s, %s, %s)", (cocktailId, ingredients[i], amounts[i]))
                elif units[i] == "gr":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, WeightGr) VALUES (%s, %s, %s)", (cocktailId, ingredients[i], amounts[i]))
                elif units[i]=="tea spoons":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountTeaSpoons) VALUES (%s, %s, %s)", (cocktailId, ingredients[i], amounts[i]))
                elif units[i]=="units":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountUnits) VALUES (%s, %s, %s)", (cocktailId, ingredients[i], amounts[i]))

        db_connection.commit()

        return "New ingredients have been added to cocktail with ID: {}".format(cocktailId)

    except Exception as e:
        return "Failed to add new ingredient:", str(e)
    finally:
        if db_connection:
            cursor.close()
            db_connection.close()

# a method that receive cocktailid,ingredientid,unit,and amount and modify unit, amount of ingredientid if is link to cocktailid
def modify_ingredients(cocktailId, ingredientId, unit, amount):
     try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()

        # modify unit and amount based on unit
        if unit == "ml":
                cursor.execute("UPDATE CocktailIngredients SET AmountMl = %s WHERE ingredientId = %s", (amount,ingredientId))
        elif unit == "gr":
                cursor.execute("UPDATE CocktailIngredients SET WeightGr = %s WHERE ingredientId = %s", (amount,ingredientId))
        elif unit=="tea spoons":
                cursor.execute("UPDATE CocktailIngredients SET AmountTeaSpoons = %s WHERE ingredientId = %s", (amount,ingredientId))
        elif unit=="units":
                cursor.execute("UPDATE CocktailIngredients SET AmountUnits = %s WHERE ingredientId = %s", (amount,ingredientId))

        db_connection.commit()
        return "Amount of ingredient has been modified"


     except Exception as e:
        return "Failed to modify ingredient:", str(e)
     finally:
        if db_connection:
            print("Cocktail with ID: {} updated successfully!".format(cocktailId))
            cursor.close()
            db_connection.close()
    
# Define a function to get the menu with ingredients and allergies

# Example of using the get_menu function
def get_menu():
    menu = []
    try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        query = """
            SELECT
                c.Id AS CocktailId,
                c.CocktailName,
                GROUP_CONCAT(
                    CASE
                        WHEN i.IsAlcoholic = TRUE THEN i.IngredientName
                        ELSE NULL
                    END
                    SEPARATOR ', ') AS AlcoholicBeverage,
                GROUP_CONCAT(
                    CASE
                        WHEN i.IsAlcoholic = FALSE THEN i.IngredientName
                        ELSE NULL
                    END
                    SEPARATOR ', ') AS IngredientName
            FROM CocktailsInfo c
            LEFT JOIN CocktailIngredients ci ON c.Id = ci.CocktailId
            LEFT JOIN Ingredients i ON ci.IngredientId = i.IngredientId
            GROUP BY c.Id, c.CocktailName;
        """

        # Execute the query
        cur.execute(query)

        # Fetch the data
        rows = cur.fetchall()

        for row in rows:
            cocktail_id, cocktail_name, alcoholic_beverage, ingredient_name = row
            menu.append({
                "CocktailId": cocktail_id,
                "CocktailName": cocktail_name,
                "AlcoholicBeverage": alcoholic_beverage,
                "IngredientName": ingredient_name
            })

    except Exception as e:
        print("Failed to read data from DB:", str(e))
    finally:
        if db_connection:
            db_connection.close()

    return menu


def get_alcoholic_ingredients(menu):
    alcoholic_ingredients = set()  # Use a set to store unique values

    for item in menu:
        if item["AlcoholicBeverage"] is not None:
            alcoholic_ingredients.add(item["AlcoholicBeverage"])

    return list(alcoholic_ingredients)  # Convert the set back to a list


def get_not_alcoholic_ingredients(menu):
    not_alcoholic_ingredients = set()  # Use a set to store unique values

    for item in menu:
        if item["AlcoholicBeverage"] is None and item["IngredientName"]:
            not_alcoholic_ingredients.add(item["IngredientName"])

    return list(not_alcoholic_ingredients)  # Convert the set back to a list


def get_alcoholic_ingredients(menu):
    all_ingredients = set()  # Use a set to store unique values

    for item in menu:
        if item["AlcoholicBeverage"] is not None and item["IngredientName"]:
            all_ingredients.add(item["IngredientName"])
    return list(all_ingredients)  # Convert the set back to a list


def get_all_ingredients(only_non_alcoholic=False):
    ingredients = []

    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        if only_non_alcoholic:
            query = "SELECT IngredientName, IngredientId FROM Ingredients WHERE IsAlcoholic = FALSE"
        else:
            query = "SELECT IngredientName, IngredientId FROM Ingredients"

        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            cocktail_dict = {
            'Ingredient_Name': row[0],
            'Ingredient_Id': row[1],
              }
            ingredients.append( cocktail_dict )  

    except Exception as e:
        return "Failed to fetch ingredients from DB:", str(e)
    finally:
        if db_connection:
            db_connection.close()

    return ingredients
def get_cocktail_by_alcoholic_beverage(menu, user_selection):
    cocktails = []
    for item in menu:
        if item["AlcoholicBeverage"] is not None and user_selection in item["AlcoholicBeverage"]:
            cocktails.append({
                "CocktailId": item["CocktailId"],
                "CocktailName": item["CocktailName"],
                "AlcoholicBeverage": item["AlcoholicBeverage"],
                "IngredientName": item["IngredientName"]
            })
    return cocktails

def delete_ingredient_for_cocktail(cocktail_id, ingredient_id):
    
    try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
   
       
        cursor.execute("DELETE FROM CocktailIngredients WHERE IngredientId =%s AND CocktailId =%s", (ingredient_id, cocktail_id))


        
        return "Ingredient with id {} removed successfully!".format(ingredient_id)
      

    # Close the cursor and database connection when you're done
    except Exception as e:
        return "Failed to read data from DB:", str(e)
        
    finally:
        if db_connection:
            db_connection.close()



def post_new_cocktail(cocktail_name,country,calories, ingredients, amounts, units):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        
        # Insert into CocktailsInfo
        insert_query_cocktail_info = """
            INSERT INTO CocktailsInfo (CocktailName,Calories,CountryOrigin,Alcoholic)
            VALUES (%s,%s,%s,%s)
        """
        cur.execute(insert_query_cocktail_info, (cocktail_name, calories, country, True))

        cocktail_id = cur.lastrowid  # Get the last inserted cocktail ID

        # Insert ingredients
        for idx, ingredientId in enumerate(ingredients):
            ingredient_id_query = "SELECT IngredientId FROM Ingredients WHERE IngredientId = %s"
            cur.execute(ingredient_id_query, (ingredientId,))
            ingredient_id = cur.fetchone()[0]
       
            
            if units[idx] == "ml":
                insert_query_cocktail_ingredients = """
                INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
                cur.execute(insert_query_cocktail_ingredients,  (cocktail_id, ingredient_id, amounts[idx], None, None, None))
            elif units[idx] == "gr":
                 insert_query_cocktail_ingredients = """
                INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
                 cur.execute(insert_query_cocktail_ingredients,  (cocktail_id, ingredient_id, None, None, None,  amounts[idx]))
            elif units[idx]=="tea spoons":
                 insert_query_cocktail_ingredients = """
                INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
                 cur.execute(insert_query_cocktail_ingredients,  (cocktail_id, ingredient_id, None, amounts[idx], None,  None))
            elif units[idx]=="units":
                insert_query_cocktail_ingredients = """
                INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
                cur.execute(insert_query_cocktail_ingredients,  (cocktail_id, ingredient_id, None, None, amounts[idx],  None))
          


        db_connection.commit()
        return 'Cocktail with name {} was added successfully!'.format(cocktail_name)

    except Exception as e:
        return "Failed to add cocktail to DB:", str(e)
    finally:
        if db_connection:
            db_connection.close()
# Define the main function, the entry point of the program

def delete_cocktail(cocktail_id):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()


        # Delete the cocktail from CocktailIngredients and CocktailsInfo tables
        delete_cocktail_ingredients_query = "DELETE FROM CocktailIngredients WHERE CocktailId = %s"
        cur.execute(delete_cocktail_ingredients_query, (cocktail_id,))

        delete_cocktail_info_query = "DELETE FROM CocktailsInfo WHERE Id = %s"
        cur.execute(delete_cocktail_info_query, (cocktail_id,))
        
        db_connection.commit()
        return "Cocktail with id {} removed successfully!".format(cocktail_id)

    except Exception as e:
        return "Failed to delete cocktail:", str(e)
    finally:
        if db_connection:
            db_connection.close()
            
def get_ingredients_by_cocktailId(cocktailId):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        # Archive the ingredients of the cocktail
        archive_query = """
           SELECT Ingredients.*
FROM Ingredients
JOIN CocktailIngredients ON Ingredients.IngredientId = CocktailIngredients.IngredientId
WHERE CocktailIngredients.CocktailId = %s;
        """
        cur.execute(archive_query, (cocktailId,))
        
        return cur.fetchall()
        
    except Exception as e:
        print("Failed to delete cocktail:", str(e))
    finally:
        if db_connection:
            db_connection.close()
def main():
    try:
        # Connect to the 'Cocktails' database
        database = _connect_to_db('Cocktails')

        if database.is_connected():
            menu = get_menu()  # Retrieve the menu
            for item in menu:
                print(
                    f"CocktailId: {item['CocktailId']}, CocktailName: {item['CocktailName']}, AlcoholicBeverage: {item['AlcoholicBeverage']}, IngredientName: {item['IngredientName']}")

            alcoholic_ingredients = get_alcoholic_ingredients(menu)
            if alcoholic_ingredients:
                print("Alcoholic beverages:")
                for beverage in alcoholic_ingredients:
                    print(f"Alcoholic Beverage: {beverage}")
            else:
                print("No alcoholic beverages found in the menu.")

            not_alcoholic_ingredients = get_not_alcoholic_ingredients(menu)
            if not_alcoholic_ingredients:
                print("Non-alcoholic ingredients:")
                for ingredient in not_alcoholic_ingredients:
                    print(f"Ingredient: {ingredient}")
            else:
                print("No non-alcoholic ingredients found in the menu.")

            all_ingredients = get_all_ingredients(menu)
            if all_ingredients:
                print("All ingredients")
                for ingredient in all_ingredients:
                    print(f"Ingredient: {ingredient}")
                else:
                    print("No Ingredient")

            user_selection = "White Rum"  # Replace with the user's selection
            selected_cocktails = get_cocktail_by_alcoholic_beverage(menu, user_selection)

            if selected_cocktails:
                print(f"Cocktails with {user_selection}:")
                for cocktail in selected_cocktails:
                    print(
                        f"CocktailId: {cocktail['CocktailId']}, CocktailName: {cocktail['CocktailName']}, AlcoholicBeverage: {cocktail['AlcoholicBeverage']}, IngredientName: {cocktail['IngredientName']}")
            else:
                print(f"No cocktails found with {user_selection}.")
        else:
            print("Database connection failed")

    except Exception as e:
        print("Failed to read data from DB:", str(e))


if __name__ == '__main__':
    main()
