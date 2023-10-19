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
# from cocktail_data import cocktails
# from utils import function1, function2 (we are going to rename the fuction according to the new name)
from utils import format_result


app = Flask(__name__)

# GETTING INFORMATION FROM 

#MOCKED DATA: this data should be replaced for database data when we finish the conection config.
cocktails = [
    (1, 'Margarita', 'tequila, lime juice, triple sec', 'recipe of cocktail margarita'),
    (2, 'Martini', 'gin, vermouth', 'recipe of cocktail martini'),
    (3, 'Old Fashioned', 'whiskey, sugar, bitters', 'recipe of cocktail old fashioned'),
    (4, 'Tequila Sunrise', 'tequila, orange juice, grenadine', 'recipe of tequila sunrise')
]
# defining the root in our web application
@app.route('/')
# Retrieve all cocktails
@app.route('/cocktails', methods=['GET'])
def get_cocktails():
    return format_result(cocktails)

# Retrieve all cocktails with the given ID from the database
@app.route('/cocktails/<int:id>', methods=['GET'])
def get_cocktail(id):
    # get id from params
    print("id", id)
#Here we'll call a db_operations method that filter all cocktails by given id from the database. For the moment we can call mocked data with ids from 0 to 3
    cocktails_by_id = [cocktail for cocktail in cocktails if cocktail[0] == int(id)]
    return format_result(cocktails_by_id)

# Retrieve all cocktails that contain the given ingredient from the database
@app.route('/cocktails/ingredients/<string:ingredient>', methods=['GET'])
def get_cocktails_by_ingredient(ingredient):
#Here we'll call a db_operations method that filter all cocktails by given ingredient from the database. 
    filtered_cocktaiks = [cocktail for cocktail in cocktails if  ingredient in cocktail[2]]
    
    return format_result(filtered_cocktaiks)

# Retrieve all cocktails that were added in the last week from the database
@app.route('/cocktails/new', methods=['GET'])
def get_new_cocktails():
    #Here we'll call a db_operations method that retrieve all cocktails that were added in the last week from the database. For the moment we can try with Margarita
    new_cocktails = [cocktails[0]]
    return format_result(new_cocktails)

# Retrieve all cocktails from the database and sort them by name in ascending order
@app.route('/cocktails/sort-name-asc', methods=['GET'])
def get_cocktails_sorted_by_name_asc():
    #Here we'll call a db_operations method that retrieve all cocktails sorted in asc order. For the moment we can sort the mocked data

   sorted_cocktails = sorted(cocktails, key=lambda x: x[1])
   return format_result(sorted_cocktails)


@app.route('/cocktails/add-new-cocktail', methods=['POST'])
def add_new_cocktail():
    #get cocktail json from body request
    cocktail = request.get_json()
    name=cocktail['name']
    ingredients=cocktail['ingredients']
    recipe=cocktail['recipe']
    
    #Here we'll call a db_operations method that post a cocktail in database that takes as params the cocktail fields  and return the new cocktail added details
    new_cocktail_details = {
      "name": name,
      "ingredients": ingredients,
      "recipe": recipe
    } 
      
    return {"message": "cocktail added sucessfully!", "new_cocktail_added_details: ":   new_cocktail_details}


@app.route('/cocktails/update-cocktail/<string:id>', methods=['PUT'])
def update_cocktail(id):

    #get cocktail recipe json from body request
    cocktail = request.get_json()
    recipe=cocktail['recipe']

    
    #Here we'll call a db_operations method that update a cocktail in database  that takes as params the cocktail id and recipe and returns all the updated cocktail data. For now we use mocked data 
    updated_cocktail_details = {
      "updated_cocktail_id:": id,
      "updated_cocktail_name": 'name',
      "updated_cocktail_ingredients": ' cocktail ingredients',
      "updated_cocktail_recipe": recipe
    } 
      
    return {"message": "cocktail updated sucessfully!", "updated_cocktail_details: ":  updated_cocktail_details}

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
