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


app = Flask(__name__)

# GETTING INFORMATION FROM 

# defining the root in our web application
@app.route('/')


# endpoint 1 example
@app.route('/cocktails')
def get_cocktails():
    pass

# endpoint 2

# endpoint 3

# endpoint 4


if __name__ == '__main__':
    # This condition checks whether the Python script is being run directly (not imported as a module).
    # If it is the main script, it proceeds to the following line.
    
    app.run(debug=True)
    # This line starts the Flask web application in debug mode.
    # Debug mode provides helpful error messages and automatic reloading of the application
    # when code changes are detected during development.
