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

        # check if is linked to cocktail
        if cursor.execute("SELECT CocktailId FROM CocktailsInfo WHERE CocktailId = %s", (cocktailId)):
            ingredientsId = []
            for ingredient in ingredients:
                ingredientId = cursor.execute("SELECT IngredientId FROM Ingredients WHERE IngredientName = %s", (ingredient))
                if ingredientId:
                    ingredientsId.append(ingredientId)
                else:
                    add_new_ingredient_to_ingredients(ingredient)
                    # the previous fuction finally part is closing the db, check and connect again
                    if not db_connection:
                        db_name = 'Cocktails'  
                        db_connection = _connect_to_db(db_name)
                        cursor = db_connection.cursor()
                    ingredientId = cursor.execute("SELECT IngredientId FROM Ingredients WHERE IngredientName = %s", (ingredient))
                    ingredientsId.append(ingredientId)
            for i in range(0, len(ingredients)):
            # modify unit and amount based on unit
                if units[i] == "ml":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountMl) VALUES (%s, %s, %s)", (cocktailId, ingredientId[i], amounts[i]))
                elif units[i] == "gr":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, WeightGr) VALUES (%s, %s, %s)", (cocktailId, ingredientId[i], amounts[i]))
                elif units[i]=="tea spoons":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountTeaSpoons) VALUES (%s, %s, %s)", (cocktailId, ingredientId[i], amounts[i]))
                elif units[i]=="units":
                    cursor.execute("INSERT INTO CocktailIngredients(CocktailId, IngredientId, AmountUnits) VALUES (%s, %s, %s)", (cocktailId, ingredientId[i], amounts[i]))

            db_connection.commit()

            print(f"New ingredients have been added to cocktail with ID: {cocktailId}")

    except Exception as e:
        print("Failed to add new ingredient:", str(e))
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

        # check if is linked to cocktail
        if cursor.execute("SELECT CocktailId FROM CocktailIngredients WHERE CocktailId = %s AND IngredientId = %s", (cocktailId, ingredientId)):
        # modify unit and amount based on unit
            if unit == "ml":
                cursor.execute("UPDATE CocktailIngredients SET AmountMl = %s WHERE ingredientId = %s", (ingredientId))
            elif unit == "gr":
                cursor.execute("UPDATE CocktailIngredients SET WeightGr = %s WHERE ingredientId = %s", (ingredientId))
            elif unit=="tea spoons":
                cursor.execute("UPDATE CocktailIngredients SET AmountTeaSpoons = %s WHERE ingredientId = %s", (ingredientId))
            elif unit=="units":
                cursor.execute("UPDATE CocktailIngredients SET AmountUnits = %s WHERE ingredientId = %s", (ingredientId))

            db_connection.commit()
            print(f"Amount of ingredient with ID: {ingredientId} has been modified for cocktail with ID: {cocktailId}")
        else:
            print(f"Ingredient with ID: {ingredientId} is not in recipe for cocktail with ID: {cocktailId}")

     except Exception as e:
        print("Failed to modify ingredient:", str(e))
     finally:
        if db_connection:
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


def get_all_ingredients(menu):
    all_ingredients = set()  # Use a set to store unique values

    for item in menu:
        if item["AlcoholicBeverage"] is not None and item["IngredientName"]:
            all_ingredients.add(item["IngredientName"])
    return list(all_ingredients)  # Convert the set back to a list


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

            delete_cocktail_by_id(1)

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
