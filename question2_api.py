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
from db_utils import get_all_cocktail_recipes, get_cocktail_by_id,get_cocktails_by_ingredient,get_cocktails_sorted_by_name_asc,post_new_cocktail,modify_ingredients,add_new_ingredient_to_cocktail, delete_ingredient_for_cocktail, delete_cocktail, get_all_ingredients
# from utils import function1, function2 (we are going to rename the function according to the new name)
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
@app.route('/cocktails/ingredients', methods=['GET'])
def get_all_cocktail_ingredients():
    all_ingredients = get_all_ingredients(), 
    return jsonify(all_ingredients)

# Retrieve all cocktails with the given ID from the database
@app.route('/cocktails/<int:id>', methods=['GET'])
def get_cocktail(id):

    cocktail_by_id = get_cocktail_by_id(id)
    print(cocktail_by_id)
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
    country = cocktail['country']
    calories = cocktail['calories']
    ingredients=cocktail['ingredients']
    amounts=cocktail['amounts']
    units=cocktail['units']
    
    print(name, country, calories, ingredients, amounts, units)
    add_new_cocktail = post_new_cocktail(name,country, calories, ingredients, amounts, units)
    return add_new_cocktail

@app.route('/cocktails/update-cocktail-ingredient-amount', methods=['PUT'])
def update_cocktail_ingredient_amounts():

    #get cocktail ingredient details from body request json
    ingredient = request.get_json()
    cocktailId=ingredient['cocktailId']
    ingredientId = ingredient['ingredientId']
    unit=ingredient['unit']
    amount = ingredient['amount']

    
    #Here we'll call a db_operations method that update a cocktail in database  that updates cocktail
    updated_cocktail = modify_ingredients(cocktailId, ingredientId,unit,amount)
      
    return updated_cocktail

@app.route('/cocktails/add-new-ingredients', methods=['PUT'])
def add_cocktail_ingredients():

    #get cocktail ingredient details from body request json
    ingredient = request.get_json()
    cocktailId = ingredient['cocktailId']
    ingredients = ingredient['ingredients']
    amounts = ingredient['amounts']
    units = ingredient['units']

    #call db method to add new ingredients
    
    add_new_ingredients =  add_new_ingredient_to_cocktail(cocktailId,ingredients,amounts,units)
      
    return add_new_ingredients 

@app.route('/cocktails/<string:cocktailid>/delete-ingredient/<string:ingredientid>', methods=['DELETE'])
def delete_cocktail_ingredient(cocktailid, ingredientid):

    #Here we'll call a db_operations method that removes the cocktail ingredient in database 
    remove_cocktail = delete_ingredient_for_cocktail(cocktailid, ingredientid)
    
    return remove_cocktail
                                                     
                                        
@app.route('/cocktails/delete-cocktail/<string:id>', methods=['DELETE'])
def delete_cocktail_by_id(id):
    #Here we'll call a db_operations method that removes the cocktail in database 
    remove_cocktail = delete_cocktail(id)
    
    return remove_cocktail

if __name__ == '__main__':
    # This condition checks whether the Python script is being run directly (not imported as a module).
    # If it is the main script, it proceeds to the following line.
    
    app.run(debug=True, port=5000)
    # This line starts the Flask web application in debug mode.
    # Debug mode provides helpful error messages and automatic reloading of the application
    # when code changes are detected during development.
