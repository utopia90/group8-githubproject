#  SUMMARY ================================================================
# in this file we have the HTTP requests to the Flask web application run in the file question2_api.py 
# It is interacting with the FLsk web application's endpoints using HTTP methods (POST, PUT, DELETE).
# This file completes the set of common CRUD (Create, Read, Update, Delete) operations, that we started
# in the question2_api file which contains GET requests.
# We use  a separate script that acts as a client for the web application, 
# demonstrating how to interact with the web application's API. 
#  =========================================================================

# Python Packages imports 
import requests
import json

#Welcome message are you a bartender or a client?
login_name=input ('Welcome to the Code Queens Cocktail Bar. Please, type in if you are a bartender or a client')
if login_name =='bartender':

else if login_name=='client':

else :
    print('Please, type bartender or client.')


#POST REQUEST
# data for cocktail we want to add
def add_new_cocktail(name, ingredients, recipe):
    new_cocktail = {
      "name": name,
      "ingredients": ingredients,
      "recipe": recipe
    }
    
# Send POST request
    url = "http://127.0.0.1:5000/cocktails/add-new-cocktail"
    headers = {'content-type': 'application/json'}

    result = requests.post(url,headers=headers, data=json.dumps(new_cocktail))

# Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail added successfully!", result.json())
       
    else:
        print("there was an error adding your cocktail: ", result.status_code)


#PUT REQUEST

# data for cocktail recipe we want to update 
def update_cocktail(id, updated_recipe):

    updated_recipe = {
      "id": id,
      "recipe": updated_recipe
    }
    # Send PUT request
    url = 'http://127.0.0.1:5000/cocktails/update-cocktail/{}'.format(id)
    headers = {'content-type': 'application/json'}


    result = requests.put(url,headers=headers, data=json.dumps(updated_recipe))
    
    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail updated successfully!", result.json())
    else:
        print("there was an error", result.status_code)


#DELETE REQUEST
def delete_cocktail(id):

# Send DELETE request
    url = 'http://127.0.0.1:5000/cocktails/delete-cocktail/{}'.format(id)

    result = requests.delete(url)
    
    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail with id {} removed successfully!".format(id), result.json())
    else:
        print("there was an error", result.status_code)


def run():
    print('############################')
    print('Hello, welcome to our fancy Code Queens Cocktails Bar')
    print('############################')
    print('Lets create a new fantastic cocktail!')
    name = input('Please pick a name for your cocktail ')
    ingredients = input('Choose the ingredients for your cocktail. Please write them separated by commas ')
    recipe = input('Choose the recipe for your cocktail ')
    add_new_cocktail(name, ingredients, recipe)
    print('Oh! It seems that now you want to modify one of our cocktails recipes!')
    id = input('Please, introduce the id of the cocktail you want to modify: ')
    updated_recipe = input('Now enter the new recipe so that we can update it: ')
    update_cocktail(id, updated_recipe)
    print('I see you dont like one of our cocktails. its a pity! Lets delete it right now!')
    id=input('Please, introduce the id of the cocktail you want to delete: ')
    delete_cocktail(id)



if __name__ == '__main__':
   run()
