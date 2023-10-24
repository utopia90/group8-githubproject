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

def delete_ingredient_for_cocktail(cocktail_id, ingredient_id):
    
    try:
        db_name = 'Cocktails'  # Replace with your database name
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
    # Check if the ingredient is linked to the specified cocktail
        cursor.execute("SELECT CocktailId FROM cocktailingredients WHERE CocktailId = %s AND ingredientId = %s", (cocktail_id, ingredient_id))
        result = cursor.fetchone()

        if result:
        # Delete the link between the cocktail and ingredient
         cursor.execute("DELETE FROM cocktailingredients WHERE cocktailid = %s AND ingredientid = %s", (cocktail_id, ingredient_id))
        
        #  to check if the ingredient is not linked to any other cocktails  and delete it entirely from the ingredients table
        cursor.execute("SELECT ingredient_id FROM cocktailingredients WHERE ingredientid = %s", (ingredient_id,))
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("DELETE FROM ingredients WHERE ingredientid = %s", (ingredient_id,))
        
        else:
          print("Ingredient not linked to the specified cocktail.")

    # Close the cursor and database connection when you're done
    except Exception as e:
        print("Failed to read data from DB:", str(e))
        
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
        else:
            print("Database connection failed")

    except Exception as e:
        print("Failed to read data from DB:", str(e))


if __name__ == '__main__':
    main()

