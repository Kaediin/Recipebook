import json
from datetime import datetime

import pyrebase
import firebase_admin

from Linda import DefaultTagImg, utils
from Linda.firebase_auth import *
from Linda.models import *
from firebase_admin import credentials, storage, firestore, auth

if not len(firebase_admin._apps):
    cred = credentials.Certificate(cert)
    default_app = firebase_admin.initialize_app(cred)

tags = ['Curry', 'Fish', 'Meat', 'Vegetarian', 'Chicken', 'Starter', 'Salad', 'Cake', 'Biscuits', 'Drinks']

db = firestore.client()
bucket = storage.bucket(storage_bucket)
firebase_pyrebase = pyrebase.initialize_app(config)
pyrebase_auth = firebase_pyrebase.auth()


def addNewRecipe(request):
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    tags = request.POST.getlist('select_tags')
    urlArray = str(request.POST['url']).split(',')
    urlNameArray = str(request.POST['urlname']).split(',')

    doc = db.collection('recipes').document()

    recipe = Recipe(
        doc.id,
        request.POST.get('title_new_recipe'),
        request.POST.get('ingredients_new_recipe'),
        request.POST.get('method_new_recipe'),
        tags,
        request.POST.get('est_time_new_recipe'),
        urlArray,
        urlNameArray,
        request.session['uid'],
        date,
        "",
        False
    )

    data = utils.createDataFromRecipe(recipe)

    doc.set(data)


def getAllTagThumbnails():
    tagThumbnails = []
    isInRecipe = False

    recipes = getAllRecipes()

    for i in range(len(tags)):
        for recipe in recipes:
            if tags[i] in recipe.tags and not isInRecipe:
                isInRecipe = True
                try:
                    tagThumbnails.append(TagThumbnail(tags[i], recipe.imageUrls[0]))
                except IndexError:
                    tagThumbnails.append(TagThumbnail(tags[i], None))

                recipes.remove(recipe)
        if not isInRecipe:
            tagThumbnails.append(TagThumbnail(tags[i], DefaultTagImg.DefaultTags[i]))
        isInRecipe = False

    return tagThumbnails


def getAllRecipes():
    docs = db.collection('recipes').stream()
    recipes = []

    for doc in docs:
        recipe = utils.getRecipeFromFirebaseDoc(doc)
        recipes.append(recipe)

    recipes.reverse()
    return recipes


def getRecipeFromUUID(uuid):
    doc = db.collection('recipes').document(uuid).get()
    recipe = utils.getRecipeFromFirebaseDoc(doc)
    return recipe


def restoreBackup(file):
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
            json_recipes['author_id'],
            json_recipes['creation_date'],
            json_recipes['modification_date'],
            json_recipes['is_archived']
        )

        allRecipes.append(recipe)

    for recipe in allRecipes:
        if type(recipe.imgNames) != list:
            recipe.imgNames = recipe.imgNames.split(',')

        if type(recipe.imageUrls) != list:
            recipe.imageUrls = recipe.imageUrls.split(',')

        if recipe.id:
            data = utils.createDataFromRecipe(recipe)
            db.collection('recipes').document(recipe.id).set(data)
        else:
            doc = db.collection('recipes').document()
            recipe.id = doc.id
            data = utils.createDataFromRecipe(recipe)
            doc.set(data)


def saveModifications(request, uuid):
    oldRecipe = getRecipeFromUUID(uuid)
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    modTags = request.POST.getlist('select_tags_modified')

    if request.POST.get('est_time_modified_recipe'):
        estTime = request.POST.get('est_time_modified_recipe')
    else:
        estTime = oldRecipe.estimatedTime

    recipe = Recipe(
        uuid,
        request.POST.get('title_modified_recipe'),
        request.POST.get('ingredients_modified_recipe'),
        request.POST.get('method_modified_recipe'),
        modTags,
        estTime,
        None,
        None,
        # urlArray,
        # urlNameArray,
        request.session['uid'],
        "",
        date,
        False
        # add logic in this function
    )

    oldNameArray = oldRecipe.imgNames
    nameArray = str(request.POST['urlname_modify'])
    oldUrlArray = oldRecipe.imageUrls
    urlArray = str(request.POST['url_modify'])

    if str(oldNameArray) != str(nameArray) and str(oldUrlArray) != str(urlArray):
        recipe.imageUrls = urlArray.split(',')
        recipe.imgNames = nameArray.split(',')
        print('Image changed')
    elif str(oldNameArray) == str(nameArray) and str(oldUrlArray) == str(urlArray):
        recipe.imageUrls = oldRecipe.imageUrls
        recipe.imgNames = oldRecipe.imgNames
        print('Image not changed!')

    updates = {
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'est_time': recipe.estimatedTime,
        'tags': recipe.tags,
        'img_url': recipe.imageUrls,
        'img_name': recipe.imgNames,
        'modification_date': recipe.modificationDate,
        'is_archived': recipe.is_archived
    }

    db.collection('recipes').document(recipe.id).update(updates)


def archiveRecipe(uuid):
    recipe = getRecipeFromUUID(uuid)
    update = {
        'is_archived': not recipe.is_archived
    }
    db.collection('recipes').document(uuid).update(update)

def getAllArchivedRecipes():
    docs = db.collection('recipes').where('is_archived', '==', True).stream()
    recipes = []
    for doc in docs:
        print(doc.id)
        recipe = utils.getRecipeFromFirebaseDoc(doc)
        recipes.append(recipe)

    return recipes


def getCurrentByUID(request):
    return auth.get_user(request.session['uid'])