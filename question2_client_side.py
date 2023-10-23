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
        all_cocktails = get_cocktails_list()
        print(all_cocktails)
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





    
        
def bartender_menu():
    PASSPHRASE = "password"
    valid_password = PASSPHRASE
    password = input("What is your password?:\n")
    #for i in range(4):

    if password != valid_password:
        password = input("Enter a valid password:\n")
        return
    if password == valid_password:

        chosen_update = input("What would you like to do?: add, remove or modify a cocktail?:\n")
        if chosen_update == 'add':
            add_new_cocktail()
        elif chosen_update == 'remove':
            print("remove")
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

    return {'ingredients': ingredients, 'amounts': amounts, 'units': units}

def getIngredientsList():
    url = "http://127.0.0.1:5000/cocktails/ingredients"
    result = requests.get(url)

 #Verify if connection was succesful
    if result.status_code == 200:
        print(result.json())
       
    else:
        print("there retrieving list of ingredients: ", result.status_code)
    
def modify_ingredient(cocktailId):
    
    ingredients_list = getIngredientsList()
    print(ingredients_list)
    ingredient = input("Ingredient Id you want to modify:'\n'")
 

    unit = input("Select the measure unit (ml, gr, tea spoons or unites):'\n'")
    amount = float(input("Insert in the amount in {}:'\n'".format(unit)))
        
    url = "http://127.0.0.1:5000/cocktails/update-cocktail-ingredient"
    headers = {'content-type': 'application/json'}
        
    updated_ingredient = {
            "cocktailId":cocktailId,
            "ingredientId": ingredient,
            "unit": unit,
            "amount": amount
        }
    result = requests.put(url,headers=headers, data=json.dumps(updated_ingredient))

 #Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail ingredient modified successfully!", result.json())
       
    else:
        print("there was an error modifying your cocktail ingredient: ", result.status_code)

  


def remove_ingredient(cocktailId):
    
    ingredients_list = getIngredientsList()
    
    print(ingredients_list)
    
    ingredient = input("Ingredient id you want to remove:'\n'")
    
       
    url='http://127.0.0.1:5000/cocktails/{}/delete-ingredient/{}'.format(cocktailId,ingredient)
    result = requests.delete(url)

 #Verify if connection was succesful
    if result.status_code == 200:
        print("ingredient removed successfully!", result.json())
       
    else:
        print("there was an error removing ingredient: ", result.status_code)


#POST REQUEST
# data for cocktail we want to add
def add_new_cocktail():
    name = input("What is the name of the new cocktail?:\n")
    added_ingredients =  add_ingredients()
    ingredients = added_ingredients['ingredients']
    amounts = added_ingredients['amounts']
    units = added_ingredients ['units']
    
    new_cocktail = {
      "name": name,
     "ingredients": ingredients,
     "amounts": amounts,
     "units": units
       }
    
    url = "http://127.0.0.1:5000/cocktails/add-new-cocktail"
    headers = {'content-type': 'application/json'}

    result = requests.post(url,headers=headers, data=json.dumps(new_cocktail))

 #Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail added successfully!", result.json())
       
    else:
        print("there was an error adding your cocktail: ", result.status_code)

def get_cocktails_list():
    result = requests.get("http://127.0.0.1:5000/cocktails")
     #Verify if connection was succesful
    if result.status_code == 200:
        print(result.json())
       
    else:
        print("there was an error getting cocktails list: ", result.status_code)
        
#PUT REQUEST
def add_new_ingredients(cocktailId):
    added_ingredients =  add_ingredients()
    ingredients = added_ingredients['ingredients']
    amounts = added_ingredients['amounts']
    units = added_ingredients ['units']
 
    updated_cocktail_ingredients = {
          "id": cocktailId,
          "ingredients": ingredients,
          "amounts": amounts,
          "units": units
    }
          
    url = "http://127.0.0.1:5000/cocktails/add-new-ingredients"
    headers = {'content-type': 'application/json'}
    result = requests.put(url,headers=headers, data=json.dumps(updated_cocktail_ingredients))

 #Verify if connection was succesful
    if result.status_code == 200:
        print("cocktail ingredients added successfully!", result.json())
       
    else:
        print("there was an error adding your cocktail ingredients: ", result.status_code)

def update_cocktail():
    
    # get Cocktails List in here
    cocktails_list = get_cocktails_list()
    print(cocktails_list)
   
    cocktailId = input("Which cocktail  id would like to modify? :'\n'")
    add_modify = input("What would like to do with the ingredients add, modify or remove?:'\n'").lower
    
    if add_modify == 'add':     
        add_new_ingredients(cocktailId)
    elif add_modify == 'modify':
          modify_ingredient(cocktailId)
    elif add_modify == 'remove':
        remove_ingredient(cocktailId)

def  delete_cocktail():
      cocktailId = input("Which cocktail id would like to remove? :'\n'")
     # get Cocktails List in here
      cocktails_list = get_cocktails_list()
      print(cocktails_list)
      
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
