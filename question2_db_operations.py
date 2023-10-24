







# Python Packages imports 
import mysql.connector
from config import HOST, USER, PASSWORD

def _connect_to_db(db_name):
    # Establish a connection to the database using the provided parameters (host, user, password, auth_plugin, and database name)
    cnx = mysql.connector.connect(
        host=HOST,        # The hostname of the database server
        user=USER,        # The username for database access
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
    

