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
    another_drink = input("Would you like to order another drink?\n")

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
    select_choice = input("Select 1: Pick a drink from the menu\nSelect 2: Barman recommendation\nSelect 3: Pick your drink by liquor ingredient\nSelect 4: Make your own drink\n")

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

    
        
# following th UI logic, if bartender is selected
# password and a name will be asked to modify the database
# it will be possible to -add a new cocktail
#                        -delete an existing one
#                        -modify one        
def bartender_menu():
    PASSPHRASE = "password"
    valid_password = PASSPHRASE
    # asking the barman their name
    name = input("What is your name?:\n")
    print("Welcome, {}!".format(name))
    # we are giving the users a few attempts to enter the right password 
    for i in range(3):
        password = input("Please, enter your password:\n")
        if password == valid_password:
        # if the password entered is the right one, loop stops
            break
    if password != valid_password:
        print("You didn't enter a valid password")
    # if after the loop a valid password was not submitted the function ends
        return
    chosen_update = ""
    # a different function will be called upon selection
    while chosen_update not in ['add', 'remove', 'modify']:
        chosen_update = input("What would you like to do: add, remove or modify a cocktail?:\n").lower()
    if chosen_update == 'add':
        add_new_cocktail()
    elif chosen_update == 'remove':
        delete_cocktail()
    elif chosen_update == 'modify':
        update_cocktail()


def add_ingredients():
    ingredients = []
    amounts = []
    units = []
    new_ingredient = True
    
    while new_ingredient:
        ingredient = input("Add a new ingredient:\n")
        ingredients.append(ingredient)

        unit = input("Select the measurement unit (ml, gr, tea spoons, or units):\n")
        while unit not in ['ml', 'gr', 'tea spoons', 'units']:
            print("You did not select a valid measurement unit. Please, try again")
            unit = input("Select between: ml, gr, tea spoons, or units:\n")
        units.append(unit)

        amount = float(input("Insert the amount \n"))
        amounts.append(amount)

        another_ingredient = input("Do you want to add another ingredient to the recipe? (Y/N):\n").upper()
        if another_ingredient != 'Y':
            new_ingredient = False

    return {'ingredients': ingredients, 'amounts': amounts, 'units': units} # check if this is the return we will be wanting


def modify_ingredient():
    ingredient = input("Ingredient you want to modify:\n")
    # get data from database check ingredients if exists:
    # if exists
    unit = input("Select the measure unit (ml, gr, tea spoons or unites):\n")
    amount = float(input("Insert in the amount of {} in {}:\n".format(ingredient, unit)))
    # insert into DB



def remove_ingredient():
    ingredient = input("Ingredient you want to modify:\n")
    # get data from database check ingredients if exists:
    # if exists
    # remove from DB



# GET request to get all the cocktails in a json file
def get_cocktails_list():
    result = requests.get('http://127.0.0.1:5000/cocktails',
        headers={'content-type': 'application/json'}
    )
    return result.json()


#POST REQUEST
# data for cocktail we want to add
def add_new_cocktail():
    CocktailName = input("What is the name of the new cocktail?:\n")
    new_cocktail = []
    new_cocktail.append(CocktailName)
    new_ingredients = add_ingredients()
    for ingredient in new_ingredients:
        new_cocktail.append(ingredient)


# Send POST request
def post_new_cocktail(new_cocktail):
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
def update_cocktail(name):
    CocktailName = input("Which cocktail recipe would like to modify?:'\n'")
    # get Cocktails List in here
    cocktail_list = get_cocktails_list()
    if CocktailName not in cocktail_list:
          print("That recipe is not in our database")
    else:
        add_modify = input("What would like to do: add, modify or remove a cokctail?:'\n'").lower()
        if add_modify == 'add':
            add_ingredients()
        elif add_modify == 'modify':
            modify_ingredient()
        elif add_modify == 'remove':
            remove_ingredient()



# Send PUT request
def put_modified_cocktail(updated_cocktail):
    url = 'http://127.0.0.1:5000/cocktails/update-cocktail/{}'.format(id)
    headers = {'content-type': 'application/json'}


    result = requests.put(url,headers=headers, data=json.dumps(updated_cocktail))

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail updated successfully!", result.json())
    else:
        print("there was an error", result.status_code)


#DELETE REQUEST
def delete_cocktail(name):
    pass
# code

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
    print("Thank you for visiting our bar. See you soon.")


if __name__ == '__main__':
    run()
