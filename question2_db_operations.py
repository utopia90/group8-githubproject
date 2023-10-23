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
        host=HOST,        # The hostname of the database server
        user=USER,        # The username for database access
        password=PASSWORD,  # The password for database access
        auth_plugin='mysql_native_password',  # The authentication plugin to use
        database=db_name  # The name of the specific database to connect to
    )
    return cnx  # Return the established database connection

# Define a custom exception class for handling database connection errors
class DbConnectionError(Exception):
    pass

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

def get_cocktails_with_main_ingredients():
    # Create an empty list to hold the cocktail details.
    cocktails = []

    try:
        # Specify the database name.
        db_name = 'Cocktails'

        # Connect to the database.
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        # SQL Query:
        # This query selects the cocktail name and its ingredients (both alcoholic and non-alcoholic).
        # The ingredients are concatenated into a single string, separated by a comma.
        query = """
            SELECT 
                c.CocktailName, 
                GROUP_CONCAT(i.IngredientName ORDER BY i.IsAlcoholic DESC) AS MainIngredients
            FROM 
                CocktailsInfo c
            JOIN 
                CocktailIngredients ci ON c.Id = ci.CocktailId
            JOIN 
                Ingredients i ON ci.IngredientId = i.IngredientId
            GROUP BY 
                c.CocktailName
            ORDER BY 
                c.CocktailName;
        """

        # Execute the query.
        cur.execute(query)

        # Fetch the data.
        rows = cur.fetchall()

        # Loop through the returned rows and store the details in the 'cocktails' list.
        for row in rows:
            cocktail_name, main_ingredients = row
            cocktails.append({
                "CocktailName": cocktail_name,
                "MainIngredients": main_ingredients
            })

    except Exception as e:
        # If there's any exception, print the error message.
        print("Failed to read data from DB:", str(e))
    finally:
        # Close the database connection.
        if db_connection:
            db_connection.close()

    # Return the cocktails list.
    return cocktails

def add_cocktail(cocktail_name, calories, country_origin, ingredients, amounts, units):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        # Insert into CocktailsInfo
        insert_query_cocktail_info = """
            INSERT INTO CocktailsInfo (CocktailName, Calories, CountryOrigin)
            VALUES (%s, %s, %s)
        """
        cur.execute(insert_query_cocktail_info, (cocktail_name, calories, country_origin))

        cocktail_id = cur.lastrowid  # Get the last inserted cocktail ID

        # Insert ingredients
        for idx, ingredient in enumerate(ingredients):
            ingredient_id_query = "SELECT IngredientId FROM Ingredients WHERE IngredientName = %s"
            cur.execute(ingredient_id_query, (ingredient,))
            ingredient_id = cur.fetchone()[0]

            insert_query_cocktail_ingredients = """
                INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query_cocktail_ingredients, (cocktail_id, ingredient_id, amounts[idx], units[idx], None, None))

        db_connection.commit()

    except Exception as e:
        print("Failed to add cocktail to DB:", str(e))
    finally:
        if db_connection:
            db_connection.close()
            
def modify_ingredient(cocktail_id, ingredient, amount, unit):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        ingredient_id_query = "SELECT IngredientId FROM Ingredients WHERE IngredientName = %s"
        cur.execute(ingredient_id_query, (ingredient,))
        ingredient_id = cur.fetchone()[0]

        update_query = """
            UPDATE CocktailIngredients 
            SET AmountMl = %s, AmountTeaSpoons = %s, AmountUnits = %s
            WHERE CocktailId = %s AND IngredientId = %s
        """
        cur.execute(update_query, (amount, None, unit, cocktail_id, ingredient_id))
        
        db_connection.commit()

    except Exception as e:
        print("Failed to modify ingredient:", str(e))
    finally:
        if db_connection:
            db_connection.close()

def delete_cocktail(cocktail_id):
    try:
        db_name = 'Cocktails'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        # Archive the ingredients of the cocktail
        archive_query = """
            INSERT INTO RecipesArchive (CocktailName, IngredientId, AmountMl, AmountTeaSpoons, AmountUnits, WeightGr)
            SELECT c.CocktailName, ci.IngredientId, ci.AmountMl, ci.AmountTeaSpoons, ci.AmountUnits, ci.WeightGr
            FROM CocktailsInfo c
            INNER JOIN CocktailIngredients ci ON c.Id = ci.CocktailId
            WHERE c.Id = %s
        """
        cur.execute(archive_query, (cocktail_id,))

        # Delete the cocktail from CocktailIngredients and CocktailsInfo tables
        delete_cocktail_ingredients_query = "DELETE FROM CocktailIngredients WHERE CocktailId = %s"
        cur.execute(delete_cocktail_ingredients_query, (cocktail_id,))

        delete_cocktail_info_query = "DELETE FROM CocktailsInfo WHERE Id = %s"
        cur.execute(delete_cocktail_info_query, (cocktail_id,))
        
        db_connection.commit()

    except Exception as e:
        print("Failed to delete cocktail:", str(e))
    finally:
        if db_connection:
            db_connection.close()
            

# Define the main function, the entry point of the program
def main():
    try:
        # Connect to the 'Cocktails' database
        database = _connect_to_db('Cocktails')

        if database.is_connected():
            menu = get_menu()  # Retrieve the menu
            for item in menu:
                print(
                    f"CocktailId: {item['CocktailId']}, CocktailName: {item['CocktailName']}, AlcoholicBeverage: {item['AlcoholicBeverage']}, IngredientName: {item['IngredientName']}")

            alcoholic_ingredients = get_alcoholic_ingredients(menu)  # Call the function with the menu
            if alcoholic_ingredients:
                print("Alcoholic beverages:")
                for beverage in alcoholic_ingredients:
                    print(f"Alcoholic Beverage: {beverage}")
            else:
                print("The Alcoholic beverages ingredients found in the menu are:")

            user_selection = "White Rum"  # Replace with the user's selection
            selected_cocktails = get_cocktail_by_alcoholic_beverage(menu, user_selection)

            if selected_cocktails:
                print(f"Cocktails with {user_selection}:")
                for cocktail in selected_cocktails:
                    print(
                        f"CocktailId: {cocktail['CocktailId']}, CocktailName: {cocktail['CocktailName']}, AlcoholicBeverage: {cocktail['AlcoholicBeverage']}, IngredientName: {cocktail['IngredientName']}")
            else:
                print(f"No cocktails found with {user_selection}.")
                
            cocktails = get_cocktails_with_main_ingredients()
            print("\nCocktails with Main Ingredients:")
            for cocktail in cocktails:
                print(f"CocktailName: {cocktail['CocktailName']}, MainIngredients: {cocktail['MainIngredients']}")
        else:
            print("Database connection failed")

    except Exception as e:
        print("Failed to read data from DB:", str(e))


if __name__ == '__main__':
    main()

