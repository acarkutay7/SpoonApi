from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import requests


app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return render_template('search.html')

api = Api(app) # create an API instance

saved_recipes = {} # store saved recipes

# define a class to handle Get request to the /recipes/search endpoint
class RecipeSearch(Resource):
    def get(self, query):
        # set up to the api endpoint and api key
        api_key = 'write your api here'
        endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
        params = {
            'query': query,
            'apiKey': api_key
        }
        response = requests.get(endpoint, params=params) # make a request to the API with the query parameters
        data = response.json()['results']
        results = []
        for recipe in data:
            ingredients = []
            if 'missedIngredients' in recipe:
                ingredients += recipe['missedIngredients']
            if 'usedIngredients' in recipe:
                ingredients += recipe['usedIngredients']
            result = {
                'id': recipe['id'],
                'name': recipe['title'],
                'image': recipe['image'],
                'ingredients': ingredients
            }
            results.append(result)
        return jsonify(results) # return JSON response
    
# define a class to handle POST requests to the /recipes/save endpoint
class RecipeSave(Resource):
    def post(self):
        #extract the recipe info from the JSON payload of the request
        data = request.get_json()
        recipe_id = data['id']
        recipe_name = data['name']
        recipe_image = data['image']

        #check if the recipe has already been saved
        if recipe_id not in saved_recipes:
            saved_recipes[recipe_id] = {
                'name':recipe_name,
                'image':recipe_image
            }
            return {'status': 'success'}
        else:
            return{'status':'already_saved'}
        

# define a class to handle GET requests to the /recipe/saved endpoint
class SavedRecipes(Resource):
    def get(self):
        # loop through the saved_recipes dictionary and construct a list of saved recipes 
        results = []
        for recipe_id, recipe_data in saved_recipes.items():
            result = {
                'id': recipe_id,
                'name': recipe_data['name'],
                'image': recipe_data['image']
            }
            results.append(result)
        
        return jsonify(results) # return the list of saved recipes as JSON response

"""
    In Flask-RESTful, you define a resource as a Python class that inherits 
from the Resource class. You then use api.add_resource to add this resource 
to your app's REST API, specifying the endpoint URL and the HTTP methods that the resource supports.
"""

# add the RecipeSearch, RecipeSave, and SavedRecipes resources to the API
api.add_resource(RecipeSearch, '/recipes/search/<string:query>')
api.add_resource(RecipeSave, '/recipes/save')
api.add_resource(SavedRecipes, '/recipes/saved')

"""
1- http://localhost:5000/recipes/search/chicken
2- http://localhost:5000/recipes/save with a JSON payload like {"id": 123, "name": "Chicken ...
3- GET request to http://localhost:5000/recipes/saved.
"""


# run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)