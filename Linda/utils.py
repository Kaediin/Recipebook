from Linda.models import Recipe
from Linda import views
from Linda.models import TagThumbnail
from Linda import DefaultTagImg
import json


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
        return True

    except KeyError:
        print('invalid session')
        return False


# if cache.get('username') == 'None' or cache.get('user_email') == 'None':
#     render(request, 'index.html', {})


def getAllRecipes(db):
    docs = db.collection('recipes').stream()
    recipes = []

    for doc in docs:
        recipe = getRecipeFromFirebaseDoc(doc)
        recipes.append(recipe)

    recipes.reverse()
    return recipes


def getAllTagThumbnails(db):
    tags = views.tags
    tagThumbnails = []
    isInRecipe = False

    recipes = getAllRecipes(db)

    for i in range(len(tags)):
        for recipe in recipes:
            if tags[i] in recipe.tags and not isInRecipe:
                isInRecipe = True
                tagThumbnails.append(TagThumbnail(tags[i], recipe.imageUrls[0]))
                recipes.remove(recipe)
        if not isInRecipe:
            tagThumbnails.append(TagThumbnail(tags[i], DefaultTagImg.DefaultTags[i]))
        isInRecipe = False

    return tagThumbnails


def getRecipeFromUUID(uuid, db):
    doc = db.collection('recipes').document(uuid).get()
    recipe = getRecipeFromFirebaseDoc(doc)
    return recipe


def restoreBackup(db, file):
    json_file = str(file, 'utf-8')
    data = json.loads(json_file)
    allRecipes = []

    for json_recipes in data:
        recipe = Recipe(
            json_recipes['recipe_id'],
            json_recipes['title'],
            json_recipes['ingredients'],
            json_recipes['method'],
            json_recipes['tags'],
            json_recipes['est_time'],
            json_recipes['img_url'],
            json_recipes['img_name'],
            json_recipes['author'],
            json_recipes['cDate'],
            json_recipes['mDate'],
        )

        allRecipes.append(recipe)

    for recipe in allRecipes:
        if type(recipe.imgNames) != list:
            recipe.imgNames = recipe.imgNames.split(',')

        if type(recipe.imageUrls) != list:
            recipe.imageUrls = recipe.imageUrls.split(',')

        print(f'Recipe: {recipe.title}\nImage names: {recipe.imgNames}\nImage urls: {recipe.imageUrls}')

        if recipe.id:
            data = createDataFromRecipe(recipe)
            db.collection('recipes').document(recipe.id).set(data)
        else:
            doc = db.collection('recipes').document()
            recipe.id = doc.id
            data = createDataFromRecipe(recipe)
            doc.set(data)


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
