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

cert = {
  "type": "service_account",
  "project_id": "cookbook-d364e",
  "private_key_id": "6b61f3e4b99591de73d32ad07a09f7919d25d7f2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDFhwRGQUXwZ50a\nqwfsLXAhCNYHITr6/VQInwU4r0gmhcoWDxB3+9NqVeKkQWvUwCf46Pu55W9IotMv\nUGBZTjzesfOzmzU7OElVE0wLlxQW/Z48Q+R4TXdwg8EXL0HhEG2fWLCGy/4Op+dt\nJuadtQv3WGuAmu9fYk7OL/40J8vuh+A0KzonhJHxjS2MuEiFUSwSJjLuUzjM5Kjj\nQhf4q8LHyXMkphj0BlYIdTuesqhkg1nCWBxUcJ9Sww5O5vp2ALXib1zVAoUXdCrD\ngHrkts5xvU2Fy6p+wsak1F1Dd/NJhxyVGPeHxpNsEs4rO3ZvfWMWTp8FXfyoajSk\nRyOSHkMbAgMBAAECggEACvSQQUtD00UT5WjrUWc7Fayf85jyuf1Mk1vVK3iBR8ME\n2yYDvlEvv8aQAZcv9rFKUO0Eb8zbWAvRKwnKBjn8zfHQYpDu/2ABpTUi8xjygCHv\nNvLMXFBuREXHyFQ9KFFDxeI34YoKhwqQnzEDT7znsyoVcEu85K1Bp1WUbj/EzkUP\nBKl18TlXqollvN+UNU+lzCaAuV8fTtTk2YiNNKPnkBsQA0gpUorOuwpU6S9aSPTS\n0FZhrjC5+LtFhM2+p97NV+3ghZ+RAJQZHWU1BWxrUaC/ye5SRVT7R+CsxwhlusBq\nG0SkmsHZRilMouQKlIutw+q+AnxKX39z0wNQfILUUQKBgQDnMhuLyaIJ8pwSQiZW\nHcr4ypzh71FPzcvVTuwgmQX1+rEk2ib4UQxM57HUbpE5oIq+Js9qwY3+J0h5TjxF\nSx9RIGLgcifcc20O63UQaFOhPRG+sMuFBR0cnsjNZ46nlCnuTY4waZuN7iFV15Uk\n0jkjDDzyWYL7g8IXUtFvCp3DMQKBgQDauDGb77Z/OWHYWjHmCj0TMIIbL1tCzyrI\n9h9g1Bhl8Bz1I1ZRYhEPBQJ26ocNkwbQy0iB7E1gtMmrK8BPGFlC8n0kO1A7cOyL\nDYNjEeDmX6mjg5B9TUg7NmXyjTGhyVUXY4IxwV5ZyKb1PmoUfKy164mKBwFpCrQ0\nqwZYIEzgCwKBgDpFUNgMvACR23Bmp87wt2W5e40einn4vrVGrRESQIRc6SUGrufL\nVbRUeWe3bnb91bpTgdfAbQ9vyz53z40PgBcseH9lhlJz7TrjcZ/vC5UKFVzgposi\nXNIH20iaH0RxfZgIiBv/oitFp7VBHuAm9Cu3O+1BTlgiP1stjofUPyshAoGBANZn\ngZoPHqMQqS3hHNEYcE6DWsczYQ7Y7mQZgSD2SQSEoJ5diZw1ueszSfswZDuWSTQc\nUnOqJSALmTXGqbnfcIEEHFCMJFZgmECneoh/Wiv60tyLd/Sc8ZW5+a4PYvvp1RQc\nY+BKYic5XxFBodN7dALRZf58Z5GFAKowjQOOhk2JAoGAa/BSRYIGeVBk0GKOLulx\ngGaa/wmRQWwL1vA/bqcG7fWpK7oiuiltzupcQSqglOH4d1te3syYnO4hwurZhGBP\nvSvzabw5ApjYIJr0RRRwU98VtaqGKsB0UCq0KhtdY2DWjPhd+ZD7CqKpzEape8yz\n9sN/DEDODP8MM0ymn8hh62A=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ibd6z@cookbook-d364e.iam.gserviceaccount.com",
  "client_id": "104881551889276032259",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ibd6z%40cookbook-d364e.iam.gserviceaccount.com"
}


if not len(firebase_admin._apps):
    cred = credentials.Certificate(cert)
    default_app = firebase_admin.initialize_app(cred)

config = {
    'apiKey': "AIzaSyBvdVFeFAfNvk3syObxsVSu4qYQPR3eAE0",
    'authDomain': "cookbook-d364e.firebaseapp.com",
    'databaseURL': "https://cookbook-d364e.firebaseio.com",
    'projectId': "cookbook-d364e",
    'storageBucket': "cookbook-d364e.appspot.com",
    'messagingSenderId': "24604178353",
    'appId': "1:24604178353:web:483fdcc8ed8550c774ef90",
    'measurementId': "G-X0S4HHWN15"
}

tags = ['Curry', 'Fish', 'Meat', 'Vegetarian', 'Chicken', 'Starter', 'Salad', 'Cake', 'Biscuits']

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
        return render(request, 'homepage.html', {'username': request.session['username']})

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
    global db
    recipe = utils.getRecipeFromUUID(uuid, db)
    return render(request, 'viewRecipe.html', {'recipe': recipe})


def deleteRecipe(request, uuid):
    global db
    recipes = utils.getAllRecipes(db)
    recipe = utils.getRecipeFromUUID(uuid, db)
    try:
        db.collection('recipes').document(recipe.title).delete()
    except:
        print('exception')

    return render(request, 'thankyou.html', {'recipes': recipes})


def modifyRecipe(request, uuid):
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

    return render(request, 'homepage.html', {'username': request.session['username']})



def createBackup(request):
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
