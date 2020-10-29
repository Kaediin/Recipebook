from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from Linda import utils, firebase_utils


def signIn(request):
    return render(request, 'index.html', {'show_alert': False})


def homepage(request):
    email = request.POST.get('email_signin')
    password = request.POST.get('password_signin')
    utils.setUsername(request, email)

    try:
        user = firebase_utils.auth.sign_in_with_email_and_password(email, password)
        tagThumbnails = firebase_utils.getAllTagThumbnails()
        return render(request, 'homepage.html', {
            'username': request.session['username'],
            'tagThumbnails': tagThumbnails
        })

    except Exception as e:
        print('sign in declined')
        print(e)
        messages.info(request, 'Invalid credentials')
        return HttpResponseRedirect("/")


def createNewRecipe(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    return render(request, 'createRecipe.html', {'tags': firebase_utils.tags})


def allViews(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    recipes = firebase_utils.getAllRecipes()

    return render(request, 'allRecipes.html', {
        'recipes': recipes,
        'tags': firebase_utils.tags
    })


def filterAllRecipes(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    selected_tags = request.POST.getlist('filter_tags')
    filtered_recipes = utils.filterRecipesBasedOnTags(selected_tags)

    return render(request, 'allRecipes.html', {
        'recipes': filtered_recipes,
        'tags': firebase_utils.tags,
        'filteredTags': selected_tags
    })


def viewRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    print(f'UUID View: {uuid}')

    recipe = firebase_utils.getRecipeFromUUID(uuid)
    return render(request, 'viewRecipe.html', {'recipe': recipe})


def deleteRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    print(f'UUID Delete: {uuid}')

    return renderThankYou(request)


def modifyRecipe(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    recipe = firebase_utils.getRecipeFromUUID(uuid)
    print(f'Recipe to modify: {recipe.imgNames}')
    return render(request, 'modifyRecipe.html', {
        'recipe': recipe,
        'tags': firebase_utils.tags
    })


def saveModification(request, uuid):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    firebase_utils.saveModifications(request, uuid)

    return renderThankYou(request)


def addNewRecipe(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    firebase_utils.addNewRecipe(request)

    return renderThankYou(request)


def gotohomepage(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    tagThumbnails = firebase_utils.getAllTagThumbnails()
    return render(request, 'homepage.html', {
        'username': request.session['username'],
        'tagThumbnails': tagThumbnails
    })


def createBackup(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    recipes = firebase_utils.getAllRecipes()
    jsons = []

    for recipe in recipes:
        data = utils.createDataFromRecipe(recipe)

        jsons.append(data)

    currentdateTime = datetime.today().strftime("%a-%d-%b-%Y")

    response = HttpResponse(str(jsons), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="Recipebook Backup - {currentdateTime}.json"'

    return response


def restoreBackup(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    return render(request, 'restoreBackup.html', {})


def importBackup(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    file = request.FILES['json_file_import'].read()
    firebase_utils.restoreBackup(file)

    return gotohomepage(request)

def renderThankYou(request):
    if not utils.isValidSession(request):
        return render(request, 'index.html', {})

    recipes = firebase_utils.getAllRecipes()
    return render(request, 'thankyou.html', {'recipes': recipes})
