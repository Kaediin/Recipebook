from Linda.models import Recipe
from Recipebook.settings import user_name
from Recipebook.settings import user_email


def setUsername(email):
    global user_name
    global user_email
    if email == 'linda.schouten.1969@gmail.com':
        user_email = email
        user_name = 'Linda Schouten'

    elif email == 'skaedin@gmail.com':
        user_email = email
        user_name = 'Kaedin Schouten'



def isValidSession(request, render):
    if user_name == '' or user_email == '':
        render(request, 'index.html', {})


def getAllRecipes(db):
    docs = db.collection('recipes').stream()
    recipes = []

    for doc in docs:
        dict = doc.to_dict()
        recipe = Recipe(
            dict.get("title", ""),
            dict.get("ingredients", ""),
            dict.get("method", ""),
            dict.get("tags", ""),
            dict.get("est_time", ""),
            dict.get("img_url", ""),
            dict.get("img_name", ""),
            dict.get("author", ""),
            dict.get("creation date", ""),
            dict.get("modification_date", "")
        )
        recipes.append(recipe)

    recipes.reverse()
    return recipes



def getRecipeFromUUID(uuid, db):
    recipes = getAllRecipes(db)

    for recipe in recipes:
        if recipe.title == uuid:
            return recipe
