from Linda.models import Recipe
from Linda import firebase_utils


def filterRecipesBasedOnTags(selected_tags):
    filtered_recipes = []
    recipes = firebase_utils.getAllRecipes()
    for recipe in recipes:
        for tag in selected_tags:
            if tag in recipe.tags:
                if recipe not in filtered_recipes:
                    filtered_recipes.append(recipe)

    return filtered_recipes


def setUsername(request, email):
    if email == 'linda.schouten.1969@gmail.com':
        request.session['username'] = 'Linda Schouten'

    elif email == 'skaedin@gmail.com':
        request.session['username'] = 'Kaedin Schouten'

    elif email == 'jarecschouten@gmail.com':
        request.session['username'] = 'Jarec Schouten'


def isValidSession(request):
    global val
    try:
        val = request.session['username']
        return True

    except KeyError:
        print('invalid session')
        return False


def createDataFromRecipe(recipe):
    data = {
        'recipe_id': recipe.id,
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'tags': recipe.tags,
        'est_time': recipe.estimatedTime,
        'author': recipe.author,
        'creation date': recipe.creationDate,
        'img_url': recipe.imageUrls,
        'img_name': recipe.imgNames,
        'modification_date': recipe.modificationDate
    }
    return data


def getRecipeFromFirebaseDoc(doc):
    dictionary_recipe = doc.to_dict()
    return Recipe(
        dictionary_recipe.get("recipe_id", ""),
        dictionary_recipe.get("title", ""),
        dictionary_recipe.get("ingredients", ""),
        dictionary_recipe.get("method", ""),
        dictionary_recipe.get("tags", ""),
        dictionary_recipe.get("est_time", ""),
        dictionary_recipe.get("img_url", ""),
        dictionary_recipe.get("img_name", ""),
        dictionary_recipe.get("author", ""),
        dictionary_recipe.get("creation date", ""),
        dictionary_recipe.get("modification_date", "")
    )
