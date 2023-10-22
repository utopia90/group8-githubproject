#  SUMMARY ================================================================
# This file deals with connecting to a database, performing data operations, 
# and handling database-related exceptions.
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
            print("DB connection is closed")  # Print a message indicating a closed connection

def get_cocktail_by_id(cocktail_id):
    try:
        # Establish a database connection
        db_connection = _connect_to_db('Cocktails')
        cursor = db_connection.cursor()

        # Execute an SQL query to fetch the cocktail by ID
        query = "SELECT * FROM CocktailsInfo WHERE id = %s"
        cursor.execute(query, (cocktail_id,))


        # Fetch the data
        cocktail_data = cursor.fetchone()

        # Close the cursor and the connection
        cursor.close()
        db_connection.close()
       
        return cocktail_data  # Return the cocktail data
    except Exception as e:
        raise DbConnectionError(f"Failed to fetch cocktail by ID: {str(e)}")


def get_cocktails_by_ingredient(ingredient):
    try:
        cocktails_with_ingredient  = []  # Initialize an empty list to store cocktail data
        # Establish a database connection
        db_connection = _connect_to_db('Cocktails')
        cursor = db_connection.cursor()

        # Execute an SQL query to fetch cocktails by ingredient
        query = "SELECT c.* FROM CocktailsInfo c JOIN CocktailIngredients ci ON c.Id = ci.CocktailId JOIN Ingredients i ON ci.IngredientId = i.IngredientId WHERE i.IngredientName LIKE %s"
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
        query = "SELECT * FROM CocktailsInfo c ORDER BY c.CocktailName ASC"
        cursor.execute(query)

        # Fetch the data
        sorted_cocktails = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        db_connection.close()

        return sorted_cocktails  # Return the sorted cocktails
    except Exception as e:
        raise DbConnectionError(f"Failed to fetch sorted cocktails: {str(e)}")


# declaring cocktail variable to be populated based on table structure
cocktail = {}


# Define the main function, the entry point of the program
def main():
    # Connect to a database, but the database name is missing in the code
    database = _connect_to_db('')  # we will need to add our database name

    # Check if the database connection was successful
    if database.is_connected():
        # Uncomment the function call below to execute it (examples of database operations)
        get_all_cocktail_recipes()
    else:
        # Print a message if the database connection failed
        print("Database connection failed")


# Check if this script is being run directly
if __name__ == '__main__':
    # Call the main function to start the program
    main()
