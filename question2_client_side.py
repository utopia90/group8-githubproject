#  SUMMARY ================================================================
# in this file we have the HTTP requests to the Flask web application run in the file question2_api.py 
# It is interacting with the Flask web application's endpoints using HTTP methods (POST, PUT, DELETE).
# This file completes the set of common CRUD (Create, Read, Update, Delete) operations, that we started
# in the question2_api file which contains GET requests.
# We use  a separate script that acts as a client for the web application, 
# demonstrating how to interact with the web application's API. 
#  =========================================================================
# Python Packages imports 

from question2_db_operations # import
import requests
import json
from random import randint


# Check if the client wants another drink
def another_drink():
    another_drink = input("Would you like to order another drink?:\n")
    if another_drink.lower() == 'yes':
        client_menu()


def client_menu():
    select_choice = input("Select 1: Pick a drink from the menu\nSelect 2: Barman recommendation\nSelect 3: Pick your drink by liquor ingredient\nSelect 4: Make your own drink\n")

    if select_choice == '1':
        print("Here is the menu.")
        all_cocktails = get_cocktails_list()
        print(all_cocktails) 
        drink_choice= input("Type the name of the cocktail here:  ")
        print("You are having a" + drink_choice + ". Enjoy your drink.")
        
    elif select_choice == '2':
        get_barman_recommendation()
    elif select_choice == '3':
        #isAlcoholic = input("Do you want your drink to contains alcohol?:\n").lower()
        #if isAlcoholic == 'yes':
            #ingredient_list = add function call in here (cannot find it)
        #else:
            #ingredient_list = add function call
        for ingredient in ingredient_list.capitalize():
            print("{}, ".format(ingredient))
        chosen_ingredient = input("What ingredient would you like in your drink?:\n")
        cocktail = get_cocktail_by_ingredient(chosen_ingredient)
        # return full recipe for the client to see (print)
        print("Your cocktail name is: {}.".format(cocktail['CocktailName']))
        for cocktail_ingredient in cocktail[ingredients]: # checking how this list/dictionary returns
            print("{}\ ".format(cocktail_ingredient.capitalize()))

    elif select_choice == '4':
        print("Let's go on a cocktail adventure. ")
        ingredient_list = # call function
        print(ingredient_list, sep=", ")
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


def get_barman_recommendation():
    all_cocktails = get_menu()
    max = len(all_cocktails) - 1
    randomId = randint(0, max)
    recommendation = get_cocktail_by_id(randomId)
    print("This is what our bartender would recommend:\nThis cocktail is called: {}, originated in {} and contains {} calories.".format(recommendation['CocktailName'], recommendation['Country'], recommendation['Calories']))


def login():
    login_name = input("Welcome to the Code Queens Cocktail Bar. Please type if you are a bartender or a client: ")

    if login_name == 'bartender':
        bartender_menu()
    elif login_name == 'client':
        client_menu()
    else:
        print('Please type "bartender" or "client":')
        login()



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


def add_ingredients(cocktailId):
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

        amount = float(input("Insert the amount:\n"))
        amounts.append(amount)

        another_ingredient = input("Do you want to add another ingredient to the recipe? (Y/N):\n").upper()
        if another_ingredient != 'Y':
            new_ingredient = False

    add_ingredients_to_cocktail(cocktailId, ingredients, amounts, units)


# a method that receive cocktailid,ingredientid,unit,and amount and modify unit, amount of ingredientid if is link to cocktailid
def modify_cocktail(cocktailId, ingredientId, unit, amount):
    ingredient = get_ingredient_by_id(ingredientId) ## create if not there or check or remove
    if cocktailId == ingredient['cocktailId']:
        ingredient['unit'] = unit
        ingredient['amount'] = amount

    url = "http://127.0.0.1:5000/cocktails/ingredients"
    headers = {'content-type': 'application/json'}

    result = requests.patch(url, headers=headers, data=json.dumps(ingredient))

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail added successfully!", result.json())

    else:
        print("there was an error adding your cocktail: ", result.status_code)


# a method to add new ingredients to a cocktail (receives cocktailId, array of ingredients, amounts and units) and post new ingredients to a given cocktail
def add_ingredients_to_cocktail(cocktailId, ingredients, amounts, units):
    ingredients_num = len(ingredients)
    for i in range(0, ingredients_num):
        new_cocktail_ingredients = {
            "cocktailId": cocktailId,
            "ingredient": ingredients[i],
            "amounts": amounts[i],
            "units": units[i]
        }
        url = "http://127.0.0.1:5000/cocktails/ingredients"
        headers = {'content-type': 'application/json'}

        result = requests.post(url, headers=headers, data=json.dumps(new_cocktail_ingredients))

        # Verify if connection was succesful
        if result.status_code == 200:
            print("ingredients added successfully!", result.json())

        else:
                print("there was an error adding your ingredients: ", result.status_code)

    # PUT REQUEST
def add_new_ingredients(cocktailId):
    added_ingredients = add_ingredients()
    ingredients = added_ingredients['ingredients']
    amounts = added_ingredients['amounts']
    units = added_ingredients['units']

    updated_cocktail_ingredients = {
        "id": cocktailId,
        "ingredients": ingredients,
        "amounts": amounts,
        "units": units
    }

    url = "http://127.0.0.1:5000/cocktails/add-new-ingredients"
    headers = {'content-type': 'application/json'}
    result = requests.put(url, headers=headers, data=json.dumps(updated_cocktail_ingredients))

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail ingredients added successfully!", result.json())

    else:
        print("there was an error adding your cocktail ingredients: ", result.status_code)


# data for cocktail recipe we want to update
def update_cocktail():
    cocktail_list = get_cocktails_list()
    print(cocktail_list, sep =", ")
    CocktailId = input("Write the Id of the cocktail recipe would like to modify:\n")
    
    if CocktailId not in cocktail_list:
          print("That recipe is not in our database")
    else:
        add_modify = input("What would like to do: add, modify or remove a cokctail?:\n").lower()
        if add_modify == 'add':
            add_ingredients(CocktailId)
        elif add_modify == 'modify':
            modify_ingredient(CocktailId)
        elif add_modify == 'remove':
            remove_ingredient(CocktailId)


def getIngredientsList():
    url = "http://127.0.0.1:5000/cocktails/ingredients"
    result = requests.get(url)

    # Verify if connection was succesful
    if result.status_code == 200:
        print(result.json())

    else:
        print("there retrieving list of ingredients: ", result.status_code)

def modify_ingredient(cocktailId):
    ingredients_list = getIngredientsList()
    print(ingredients_list)
    ingredient = input("Ingredient Id you want to modify:\n")

    unit = input("Select the measure unit (ml, gr, tea spoons or unites):\n")
    amount = float(input("Insert in the amount in {}:'\n'".format(unit)))

    url = "http://127.0.0.1:5000/cocktails/update-cocktail-ingredient"
    headers = {'content-type': 'application/json'}

    updated_ingredient = {
        "cocktailId": cocktailId,
        "ingredientId": ingredient,
        "unit": unit,
        "amount": amount
    }
    result = requests.put(url, headers=headers, data=json.dumps(updated_ingredient))

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail ingredient modified successfully!", result.json())

    else:
        print("there was an error modifying your cocktail ingredient: ", result.status_code)


def remove_ingredient(cocktailId):
    ingredients_list = getIngredientsList()

    print(ingredients_list)

    ingredient = input("Ingredient id you want to remove:\n")

    url = 'http://127.0.0.1:5000/cocktails/{}/delete-ingredient/{}'.format(cocktailId, ingredient)
    result = requests.delete(url)

    # Verify if connection was succesful
    if result.status_code == 200:
        print("ingredient removed successfully!", result.json())

    else:
        print("there was an error removing ingredient: ", result.status_code)


# POST REQUEST
# data for cocktail we want to add
def add_new_cocktail():
    CocktailName = input("What is the name of the new cocktail?:\n")
    Calories = input("If you want to add the amount of calories add the number here:\n")
    Country = input("You can add the country in which the cocktail originated:\n")
    new_cocktail = add_ingredients()
    new_cocktail['CocktailName'] = CocktailName
    new_cocktail['Calories'] = Calories
    new_cocktail['Country'] = Country
    added_ingredients = add_ingredients()
    ingredients = added_ingredients['ingredients']
    amounts = added_ingredients['amounts']
    units = added_ingredients['units']

    new_cocktail = {
        "name": CocktailName,
        "country": Country,
        "calories": Calories
    }

    url = "http://127.0.0.1:5000/cocktails/add-new-cocktail"
    headers = {'content-type': 'application/json'}

    result = requests.post(url, headers=headers, data=json.dumps(new_cocktail))

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail added successfully!", result.json())
        cocktail = get_cocktail_by_cocktailName() # If we have the time
        add_ingredients_to_cocktail(cocktail['cocktailId'],ingredients, amounts, units)

    else:
        print("there was an error adding your cocktail: ", result.status_code)
    

def get_cocktails_list():
    result = requests.get("http://127.0.0.1:5000/cocktails")
    # Verify if connection was succesful
    if result.status_code == 200:
        print(result.json())

    else:
        print("there was an error getting cocktails list: ", result.status_code)



def update_cocktail():
    # get Cocktails List in here
    cocktails_list = get_cocktails_list()
    print(cocktails_list)

    cocktailId = input("Which cocktail id would like to modify? :\n")
    add_modify = input("What would like to do with the ingredients add, modify or remove?:\n").lower

    if add_modify == 'add':
        add_new_ingredients(cocktailId)
    elif add_modify == 'modify':
        modify_ingredient(cocktailId)
    elif add_modify == 'remove':
        remove_ingredient(cocktailId)


def delete_cocktail():
    # get Cocktails List in here
    cocktails_list = get_cocktails_list()
    print(cocktails_list)

    cocktailId = input("Which cocktail id would like to remove? :\n")

    # Send DELETE request
    url = 'http://127.0.0.1:5000/cocktails/delete-cocktail/{}'.format(cocktailId)

    result = requests.delete(url)

    # Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail with id {} removed successfully!".format(cocktailId), result.json())
    else:
        print("there was an error", result.status_code)


def run():
    login()
    print("Thank you for visiting our bar. See you soon.")


if __name__ == '__main__':
    run()
