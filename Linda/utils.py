from Linda.models import Recipe
from Recipebook import settings


def setUsername(email):
    if email == 'linda.schouten.1969@gmail.com':
        settings.user_email = email
        settings.user_name = 'Linda Schouten'

    elif email == 'skaedin@gmail.com':
        settings.user_email = email
        settings.user_name = 'Kaedin Schouten'



def isValidSession(request, render):
    if settings.user_name == '' or settings.user_email == '':
        render(request, 'index.html', {})


def getAllRecipes(db):
    docs = db.collection('recipes').stream()
    recipes = []

    for doc in docs:
        dict = doc.to_dict()
        recipe = Recipe(
            dict.get("title", "No value found"),
            dict.get("ingredients", "No value found"),
            dict.get("method", "No value found"),
            dict.get("tags", "No value found"),
            dict.get("est_time", "No value found"),
            dict.get("img_url", "No value found"),
            dict.get("img_name", "No value found"),
            dict.get("author", "No value found"),
            dict.get("creation_date", "No value found"),
            dict.get("modification_date", "No value found")
        )
        recipes.append(recipe)

    recipes.reverse()
    return recipes



def getRecipeFromUUID(uuid, db):
    recipes = getAllRecipes(db)

    for recipe in recipes:
        if recipe.title == uuid:
            return recipe
