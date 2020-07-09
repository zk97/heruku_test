from flask import Flask, jsonify, request
from http import HTTPStatus

# Create an instance of Flask class
app = Flask(__name__)

# Define recipes list
recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]


# Use route decorator to tell Flask that the /recipes route to the get_recipes
# function, and the methods = ['GET'] argument to specify that the route decorator
# will only respond to GET requests:
@app.route('/recipes', methods=['GET'])
def get_recipes():
    # use jsonify to convert the list of recipes to JSON format and respond
    # to the client
    return jsonify({'data': recipes})


# to retrieve only one specific recipe
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # iterate over all recipes and find matching id
    # adding to iterator and yielding the recipe
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id),
                  None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'message': 'recipe not found'}, HTTPStatus.NOT_FOUND)


# post methods to create a recipe in memory
@app.route('/recipes', methods=['POST'])
def create_recipe():
    # get the name and description from the client POST request
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }
    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED


# update a recipe by #id
@app.route('/recipes/<int:recipe_id>',
           methods=['PUT'])
def update_recipe(recipe_id):
    # same as previous, retrieve recipe with the desired id
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id),
                  None)

    # if not found, return message and HTTP status 404
    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    # receive data in json format
    data = request.get_json()
    # update recipe with the json attributes from input
    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )
    # return recipe and HTTP status 200
    return jsonify(recipe), HTTPStatus.OK


# With students: How to create a method to delete a recipe
@app.route('/recipes/<int:recipe_id>',
           methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id),
                  None)
    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    recipes.remove(recipe)
    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run(debug=True)
