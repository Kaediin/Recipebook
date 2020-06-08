from Linda.models import Recipe
# from django.core.cache import cache

# user_name = ''
# user_email = ''
# cache.set('username', 'Hello, World!', 30)
# cache1 = caches['default']

def setUsername(request, email):
    if email == 'linda.schouten.1969@gmail.com':
        request.session['username'] = 'Linda Schouten'
        # cache.set('username', 'Linda Schouten')
        # cache.set('user_email', 'linda.schouten.1969@gmail.com')

    elif email == 'skaedin@gmail.com':
        request.session['username'] = 'Kaedin Schouten'
        # cache.set('username', 'Kaedin Schouten')
        # cache.set('user_email', 'skaedin@gmail.com')

    elif email == 'jarecschouten@gmail.com':
        request.session['username'] = 'Jarec Schouten'
        # cache.set('username', 'Jarec Schouten')
        # cache.set('user_email', 'jarecschouten@gmail.com')


def isValidSession(request):
    global val
    try:
        val = request.session['username']
        print('Val = '+val)
        return True

    except KeyError:
        return False


# if cache.get('username') == 'None' or cache.get('user_email') == 'None':
    #     render(request, 'index.html', {})


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
