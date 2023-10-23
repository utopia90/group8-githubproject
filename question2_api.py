#  SUMMARY ================================================================
# This file defines a Flask web application,  and its primary purpose is to 
# provide a web-based interface for managing and interacting with our app data.
# which is a Python web framework for building web applications and APIs.
# Of all the CRUD operations(Create, Read, Update, Delete) operations,
# in this file we will handle all the GET request. 
# POST, PUT, DELETE request are in the file question2_client_side.py
#  =========================================================================

# Python Packages imports 
from flask import Flask, jsonify, request
# below additional import we will have to specify and uncomment in order to import the data and utils functions
from question2_db_operations import get_all_cocktail_recipes, get_cocktail_by_id,get_cocktails_by_ingredient,get_cocktails_sorted_by_name_asc
# from utils import function1, function2 (we are going to rename the fuction according to the new name)
from utils import format_result


app = Flask(__name__)

# defining the root in our web applications
@app.route('/')
# Retrieve all cocktails
@app.route('/cocktails', methods=['GET'])
def get_cocktails():
    all_cocktails = get_all_cocktail_recipes()
    return format_result(all_cocktails)

# Retrieve all ingredients
@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    all_ingredients = "all ingredients", #call db method
    return format_result(all_ingredients)

# Retrieve all cocktails with the given ID from the database
@app.route('/cocktails/<int:id>', methods=['GET'])
def get_cocktail(id):

    cocktail_by_id = get_cocktail_by_id(id)
    return format_result([cocktail_by_id])

@app.route('/cocktails/ingredients/<string:ingredient>', methods=['GET'])
def get_cocktails_filtered_by_ingredient(ingredient):
    filtered_cocktaiks = get_cocktails_by_ingredient(ingredient)
    
    return format_result(filtered_cocktaiks)


# Retrieve all cocktails from the database and sort them by name in ascending order
@app.route('/cocktails/sort-name-asc', methods=['GET'])
def get_all_cocktails_sorted_by_name_asc():
   sorted_cocktails = get_cocktails_sorted_by_name_asc()
   return format_result(sorted_cocktails)

@app.route('/cocktails/add-new-cocktail', methods=['POST'])
def add_new_cocktail():
    #get cocktail json from body request
    cocktail = request.get_json()
    name=cocktail['name']
    ingredients=cocktail['ingredients']
    amounts=cocktail['amounts']
    units=cocktail['units']
    
    #Here we'll call a db_operations method that post a cocktail in database that takes as params the cocktail fields  and return the new cocktail added details
    new_cocktail_details = {
      "name": name,
      "ingredients": ingredients,
      "amounts": amounts,
      "units":units
    } 
      
    return {"message": "cocktail added sucessfully!", "new_cocktail_added_details: ":   new_cocktail_details}

@app.route('/cocktails/update-cocktail-ingredient', methods=['PUT'])
def update_cocktail():

    #get cocktail ingredient details from body request json
    ingredient = request.get_json()
    id=ingredient['id']
    unit=ingredient['unit']
    amount = ingredient['amount']

    
    #Here we'll call a db_operations method that update a cocktail in database  that takes as params the cocktail id and recipe and returns all the updated cocktail data. For now we use mocked data 
  
      
    return {"message": "cocktail updated sucessfully!", "updated_cocktail_details: ":  ingredient}

@app.route('/cocktails/delete-ingredient/<string:id>', methods=['DELETE'])
def delete_cocktail_ingredient(id):

    #Here we'll call a db_operations method that removes the cocktail ingredient in database 
    cocktail_was_removed = True
    
    if cocktail_was_removed:
        return {"message": "cocktail with id {} was removed sucessfully!".format(id)}
    else:
        return {"message": "There was an error removing cocktail with id {}".format(id)}
@app.route('/cocktails/delete-cocktail/<string:id>', methods=['DELETE'])
def delete_cocktail(id):

    
    #Here we'll call a db_operations method that removes the cocktail in database and takes as params the cocktail id and if cocktail was succcesfully deleted returns a  boolean true and if not, false
    cocktail_was_removed = True
    
    if cocktail_was_removed:
        return {"message": "cocktail with id {} was removed sucessfully!".format(id)}
    else:
        return {"message": "There was an error removing cocktail with id {}".format(id)}

if __name__ == '__main__':
    # This condition checks whether the Python script is being run directly (not imported as a module).
    # If it is the main script, it proceeds to the following line.
    
    app.run(debug=True, port=5000)
    # This line starts the Flask web application in debug mode.
    # Debug mode provides helpful error messages and automatic reloading of the application
    # when code changes are detected during development.
