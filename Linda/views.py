from datetime import datetime

import firebase_admin
import pyrebase
from django.http import HttpResponse
from django.shortcuts import render
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from Linda.models import Recipe
from Recipebook import urls

if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('Linda/Cookbook-6b61f3e4b995.json')
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

tags = [
    
]

db = firestore.client()
bucket = storage.bucket("cookbook-d364e.appspot.com")
firebase_pyrebase = pyrebase.initialize_app(config)
auth = firebase_pyrebase.auth()


def signIn(request):
    return render(request, 'index.html', {'show_alert': False})


def homepage(request):
    email = request.POST.get('email_signin')
    password = request.POST.get('password_signin')
    urls.email = email

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return render(request, 'homepage.html', {'email': email})

    except:
        print('sign in declined')
        return render(request, 'index.html', {'show_alert': True})


def createNewRecipe(request):
    return render(request, 'createRecipe.html')


def allViews(request):
    recipes = getAllRecipes()

    return render(request, 'allRecipes.html', {'recipes': recipes})


def viewRecipe(request, uuid):
    recipe = getRecipeFromUUID(uuid)
    return render(request, 'viewRecipe.html', {'recipe': recipe})

def deleteRecipe(request, uuid):
    recipes = getAllRecipes()
    recipe = getRecipeFromUUID(uuid)
    db.collection('recipes').document(recipe.title).delete()
    return render(request, 'thankyou.html', {'recipes': recipes})

def modifyRecipe(request, uuid):
    recipe = getRecipeFromUUID(uuid)
    return render(request, 'modifyRecipe.html', {'recipe': recipe})

def saveModification(request, uuid):
    global db
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    recipe = Recipe(
        uuid,
        request.POST.get('ingredients_modified_recipe'),
        request.POST.get('method_modified_recipe'),
        "",
        "",
        "",
        urls.email,
        date
    )

    updates = {
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'author': recipe.author,
    }

    recipes = getAllRecipes()

    db.collection('recipes').document(recipe.title).update(updates)
    return render(request, 'thankyou.html', {'recipes': recipes})

def addNewRecipe(request):
    global db
    global bucket
    date = datetime.now().strftime("%d %B %Y - %H:%M")
    recipe = Recipe(
        request.POST.get('title_new_recipe'),
        request.POST.get('ingredients_new_recipe'),
        request.POST.get('method_new_recipe'),
        request.POST.get('est_time_new_recipe'),
        request.POST.get('url'),
        request.POST.get('urlname'),
        urls.email,
        date
    )

    data = {
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'method': recipe.cookingMethod,
        'est time': recipe.estTime,
        'author': recipe.author,
        'creation date': recipe.cDate,
        'img url': recipe.img,
        'img name': recipe.imgname
    }

    recipes = getAllRecipes()

    db.collection('recipes').document(recipe.title).set(data)
    return render(request, 'thankyou.html', {'recipes': recipes})


def gotohomepage(request):
    return render(request, 'homepage.html', {'email': urls.email})


def getRecipeFromUUID(uuid):
    recipes = getAllRecipes()

    for recipe in recipes:
        if recipe.title == uuid:
            return recipe


def getAllRecipes():
    global db
    docs = db.collection('recipes').stream()
    recipes = []

    for doc in docs:
        dict = doc.to_dict()
        recipe = Recipe(
            dict.get("title", "No value found"),
            dict.get("ingredients", "No value found"),
            dict.get("method", "No value found"),
            dict.get("est time", "No value found"),
            dict.get("img url", "No value found"),
            dict.get("img name", "No value found"),
            dict.get("author", "No value found"),
            dict.get("creation date", "No value found")
        )
        recipes.append(recipe)

    recipes.reverse()
    return recipes
