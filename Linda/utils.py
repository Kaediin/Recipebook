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
        print('Val = ' + val)
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
        dict = doc.to_dict()
        recipe = Recipe(
            dict.get("recipe_id", ""),
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


def getAllTagThumbnails(db):
    default_img = 'https://firebasestorage.googleapis.com/v0/b/cookbook-d364e.appspot.com/o/BM140zDM2okqxq5?alt=media&token=545f93e8-6f63-4a39-b19e-bfddc9f701b4'
    tags = views.tags
    tagThumbnails = []
    isInRecipe = False

    recipes = getAllRecipes(db)

    for i in range(len(tags)):
        for recipe in recipes:
            if tags[i] in recipe.tags and isInRecipe == False:
                isInRecipe = True
                tagThumbnails.append(TagThumbnail(tags[i], recipe.img))
                recipes.remove(recipe)
        if isInRecipe == False:
            tagThumbnails.append(TagThumbnail(tags[i], DefaultTagImg.DefaultTags[i]))
        isInRecipe = False

    return tagThumbnails


def getRecipeFromUUID(uuid, db):
    recipes = getAllRecipes(db)

    for recipe in recipes:
        if recipe.title == uuid:
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
        if recipe.recipe_id:
            data = createDataFromRecipe(recipe)
            db.collection('recipes').document(recipe.recipe_id).set(data)
        else:
            doc = db.collection('recipes').document()
            recipe.recipe_id = doc.id
            data = createDataFromRecipe(recipe)
            doc.set(data)


def createDataFromRecipe(recipe):
    data = {
        'recipe_id': recipe.recipe_id,
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'tags': recipe.tags,
        'est_time': recipe.estTime,
        'author': recipe.author,
        'creation date': recipe.cDate,
        'img_url': recipe.img,
        'img_name': recipe.imgname,
        'modification_date': recipe.mDate
    }
    return data
