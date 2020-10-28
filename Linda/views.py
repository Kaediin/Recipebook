import firebase_admin
import pyrebase
import datetime

from datetime import datetime

from django.shortcuts import render

from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from Recipebook import settings

from django.http import HttpResponse
from django.conf import settings

from Linda import utils
from Linda.models import Recipe



if not len(firebase_admin._apps):
    cred = credentials.Certificate(cert)
    default_app = firebase_admin.initialize_app(cred)



tags = ['Curry', 'Fish', 'Meat', 'Vegetarian', 'Chicken', 'Starter', 'Salad', 'Cake', 'Biscuits', 'Drinks']

db = firestore.client()
bucket = storage.bucket("cookbook-d364e.appspot.com")
firebase_pyrebase = pyrebase.initialize_app(config)
auth = firebase_pyrebase.auth()


def signIn(request):
    return render(request, 'index.html', {'show_alert': False})


def homepage(request):
    email = request.POST.get('email_signin')
    password = request.POST.get('password_signin')
    utils.setUsername(request, email)

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        tagThumbnails = utils.getAllTagThumbnails(db)
        return render(request, 'homepage.html', {
            'username': request.session['username'],
            'tagThumbnails': tagThumbnails
        })

    except Exception as e:
        print('sign in declined')
        print(e)
        return render(request, 'index.html', {'show_alert': True})


def createNewRecipe(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global tags
    return render(request, 'createRecipe.html', {'tags': tags})


def allViews(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    recipes = utils.getAllRecipes(db)

    return render(request, 'allRecipes.html', {
        'recipes': recipes,
        'tags': tags
    })


def filterAllRecipes(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    recipes = utils.getAllRecipes(db)
    selected_tags = request.POST.getlist('filter_tags')
    filtered_recipes = []
    for recipe in recipes:
        for tag in selected_tags:
            if tag in recipe.tags:
                if recipe not in filtered_recipes:
                    filtered_recipes.append(recipe)

    return render(request, 'allRecipes.html', {
        'recipes': filtered_recipes,
        'tags': tags,
        'filteredTags': selected_tags
    })


def viewRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    recipe = utils.getRecipeFromUUID(uuid, db)
    return render(request, 'viewRecipe.html', {'recipe': recipe})


def deleteRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    recipes = utils.getAllRecipes(db)
    recipe = utils.getRecipeFromUUID(uuid, db)
    try:
        db.collection('recipes').document(recipe.title).delete()
    except:
        print('exception')

    return render(request, 'thankyou.html', {'recipes': recipes})


def modifyRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    recipe = utils.getRecipeFromUUID(uuid, db)
    return render(request, 'modifyRecipe.html', {
        'recipe': recipe,
        'tags': tags
    })


def saveModification(request, uuid):
    global db
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    modTags = request.POST.getlist('select_tags_modified')
    hiddenIMGurl = request.POST.get('url_modify')
    hiddenName = request.POST.get('urlname_modify')

    recipe = Recipe(
        uuid,
        request.POST.get('ingredients_modified_recipe'),
        request.POST.get('method_modified_recipe'),
        modTags,
        request.POST.get('est_time_modified_recipe'),
        hiddenIMGurl,
        hiddenName,
        request.session['username'],
        "",
        date
    )

    updates = {
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'est_time': recipe.estTime,
        'tags': recipe.tags,
        'img_url': recipe.img,
        'img_name': recipe.imgname,
        'modification_date': recipe.mDate
    }

    recipes = utils.getAllRecipes(db)

    db.collection('recipes').document(recipe.title).update(updates)
    return render(request, 'thankyou.html', {'recipes': recipes})


def addNewRecipe(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    global bucket
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    tags = request.POST.getlist('select_tags')

    # while len(tags) < 2:
    #     tags.append('')

    recipe = Recipe(
        request.POST.get('title_new_recipe'),
        request.POST.get('ingredients_new_recipe'),
        request.POST.get('method_new_recipe'),
        tags,
        request.POST.get('est_time_new_recipe'),
        request.POST.get('url'),
        request.POST.get('urlname'),
        request.session['username'],
        date,
        ""
    )

    data = {
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

    recipes = utils.getAllRecipes(db)

    db.collection('recipes').document(recipe.title).set(data)
    return render(request, 'thankyou.html', {'recipes': recipes})


def gotohomepage(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    tagThumbnails = utils.getAllTagThumbnails(db)
    return render(request, 'homepage.html', {
        'username': request.session['username'],
        'tagThumbnails': tagThumbnails
    })


def createBackup(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    global db
    # os.mkdir("Backups")
    recipes = utils.getAllRecipes(db)
    jsons = []
    filename = 'backup'

    for recipe in recipes:
        data = {
            "author": recipe.author,
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "method": recipe.cookingMethod,
            "cDate": recipe.cDate,
            "mDate": recipe.mDate,
            "est_time": recipe.estTime,
            "img_name": recipe.imgname,
            "img_url": recipe.img,
            "tags": recipe.tags,
        }

        # print(recipe.author)
        # print(recipe.cDate)
        # print(recipe.estTime)
        # print(recipe.imgname)
        # print(recipe.img)
        # print(recipe.ingredients)
        # print(recipe.cookingMethod)
        # print(recipe.mDate)
        # print(recipe.tags)
        # print(recipe.title)
        jsons.append(data)

    print(jsons)

    response = HttpResponse(str(jsons), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="backup.json"'

    return response
