#  SUMMARY ================================================================
# in this file we have the HTTP requests to the Flask web application run in the file question2_api.py 
# It is interacting with the Flask web application's endpoints using HTTP methods (POST, PUT, DELETE).
# This file completes the set of common CRUD (Create, Read, Update, Delete) operations, that we started
# in the question2_api file which contains GET requests.
# We use  a separate script that acts as a client for the web application, 
# demonstrating how to interact with the web application's API. 
#  =========================================================================
# Python Packages imports 

import requests
import json


# Check if the client wants another drink
def another_drink():
    another_drink = input("Would you like to order another drink? ")

    if another_drink.lower() == 'yes':
        client_menu()

def login():
    login_name = input("Welcome to the Code Queens Cocktail Bar. Please type if you are a bartender or a client: ")

    if login_name == 'bartender':
        # Add bartender logic here
        pass
    elif login_name == 'client':
        client_menu()

    else:
        print('Please type "bartender" or "client".')
        login()

def client_menu():
    select_choice = input("Select 1: Pick a drink from the menu  Select 2: Barman recommendation  
            Select 3:  Pick your drink by liquor ingredient 
            Select 4: Make your own drink ")

    if select_choice == '1':
        print("Here is the menu.")
        # Call get_cocktails() 
        drink_choice= input("Type the name of the cocktail here.  ")
        print("You are having a" + drink_choice + ". Enjoy your drink.")
        
    elif select_choice == '2':
        print("This is what our bartender would recommend.")
        # Call get_barman_recommendation()
    elif select_choice == '3':
        ingredient=input("What ingredient you like in your drink?")
        # function(ingredient)

    elif select_choice == '4':
        print("Let`s go on a cocktail adventure. ")
        ingredient=input("What ingredient you like in your drink?")
        #function ()
    else:
        print("Choose a number from 1 to 4")
        client_menu()
    another_drink()

login()


print("Thank you for visiting our bar. See you soon.")
    
        
     












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
