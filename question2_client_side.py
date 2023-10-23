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
        bartender_menu()
    elif login_name == 'client':
        client_menu()

    else:
        print('Please type "bartender" or "client".')
        login()

def client_menu():
    select_choice = input("Select 1: Pick a drink from the menu'\n'Select 2: Barman recommendation'\n'Select 3: Pick your drink by liquor ingredient'\n'Select 4: Make your own drink ")

    if select_choice == '1':
        print("Here is the menu.")
        # Call get_cocktails() 
        drink_choice= input("Type the name of the cocktail here:  ")
        print("You are having a" + drink_choice + ". Enjoy your drink.")
        
    elif select_choice == '2':
        print("This is what our bartender would recommend.")
        # Call get_barman_recommendation()
    elif select_choice == '3':
        ingredient=input("What ingredient you like in your drink?:'\n'")
        # function(ingredient)

    elif select_choice == '4':
        print("Let`s go on a cocktail adventure. ")
        
        ingredients = []

        while True:  # The loop will continue until the customer decides not to add more ingredients
           ingredient = input("What ingredient would you like in your drink? ")
           ingredients.append(ingredient)  

          another_ingredient = input("Would you like any other ingredients? (yes/no) ")

          if another_ingredient.lower() != "yes":
              break  # Exit the loop 


        print("Your drink will include the following ingredients: " + ", ".join(ingredients))
        #funtion to save it in db?
    else:
        print("Choose a number from 1 to 4")
        client_menu()
    another_drink()

login()


print("Thank you for visiting our bar. See you soon.")
    
        
def bartender_menu():
    # PASSPHRASE = ""
    valid_password = PASSPHRASE
    name = input("What is your name?:'\n'")
    for i in range(4):
        password = input("Enter a valid password:'\n'")
        if password == valid_password:
            break
    if password != valid_password:
        return
    chosen_update = input("What would you like to do?: add, remove or modify a cocktail?:'\n'")
    if chosen_update == 'add':
        add_new_cocktail()
    elif chosen_update == 'remove':
        delete_cocktail()
    elif chosen_update == 'modify':
        update_cocktail()
    else:
        print("I could not understand your request")
        bartender_menu()


def add_ingredients():
    ingredients = []
    amounts = []
    units = []
    new_ingredient = True
    i = 0
    while new_ingredient:
        ingredients[i] = input("Add a new ingredient:'\n'")
        units[i] = input("Select the measure unit (ml, gr, tea spoons or unites):'\n'")
        while units[i] != 'ml' and units[i] != 'gr' and units[i].lower != 'tea spoons' and units[i].lowercase() != 'unites': #check lowercase or lower in here
            print("You did not select a valid measure unit. Please, try again")
            units[i] = input("Select between: ml, gr, tea spoons or unites:'\n'")
        amounts[i] = float(input("Insert in the amount of {} in {}:'\n'".format(ingredients[i], units[i])))
        another_ingredient = input("Do you want to add another ingredient to the recipe? (Y/N):'\n'").upper
        if another_ingredient != 'Y':
            new_ingredient = False
    return {ingredients, amounts, units,} # check return


def modify_ingredient():
    ingredient = input("Ingredient you want to modify:'\n'")
    # get data from database check ingredients if exists:
    # if exists
    unit = input("Select the measure unit (ml, gr, tea spoons or unites):'\n'")
    amount = float(input("Insert in the amount of {} in {}:'\n'".format(ingredient, unit)))
    # insert into DB
    


def remove_ingredient():
    ingredient = input("Ingredient you want to modify:'\n'")
    # get data from database check ingredients if exists:
    # if exists
    # remove from DB


#POST REQUEST
# data for cocktail we want to add
def add_new_cocktail():
    name = input("What is the name of the new cocktail?:'\n'")
    add_ingredients()
    new_cocktail = {
      "CocktailName": name,
      "ingredients": ingredients,
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
def update_cocktail():
    CocktailName = input("Which cocktail recipe would like to modify?:'\n'")
    # get Cocktails List in here
    # if CocktailName not in Cocktails:
    #       print("That recipe is not in our database")
    #       update_cocktail()
    add_modify = input("What would like to do with the ingredients add, modify or remove?:'\n'").lower
    if add_modify == 'add':
        add_ingredients()
    elif add_modify == 'modify':
        modify_ingredient()
    elif add_modify == 'remove':
        remove_ingredient()


# NOT HERE
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
    login()



if __name__ == '__main__':
   run()
