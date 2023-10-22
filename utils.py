#  SUMMARY ================================================================
# utils.py module's function is to provide utility functions to assist 
# in the operation of the web application.
# These utility functions are imported and used in flask_app.py 
# =========================================================================
from flask import jsonify


def format_result(cocktails):
    # Convert the result into a list of dictionaries. this method must be modified depending how fields are organized in the db
    cocktail_list = []

    for cocktail in cocktails:
        cocktail_dict = {
            'id': cocktail[0],
            'name': cocktail[1],
            'calories': cocktail[2],
            'country origin': cocktail[3],
            'is Alcoholic':  'True' if cocktail[4] == 1 else 'False'
        }
        cocktail_list.append(cocktail_dict)
    
    return jsonify(cocktail_list)