#  SUMMARY ================================================================
# This file deals with connecting to a database, performing data operations, 
# and handling database-related exceptions.
# =========================================================================

# Python Packages imports 
import mysql.connector
from config import HOST, USER, PASSWORD 


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx

# defining a dummy DBConnectionError class
class DbConnectionError(Exception):
    pass

# get access to all data in db
def get_all_cocktail_recipes():
    pass

# to be added others data operations

# declaring cocktail variable to be populated based on table structure
cocktail = {}

# Define the main function, the entry point of the program
def main():
    # Connect to a database, but the database name is missing in the code
    database = _connect_to_db('') # we will need to add our database name

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
