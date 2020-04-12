from django.urls import path
from Linda import views

urlpatterns = [
    path('', views.signIn),
    path('Sign-in/', views.homepage, name="signin"),
    path('Recipe/Create/', views.createNewRecipe, name="createNewRecipe"),
    path('Recipe/Add/', views.addNewRecipe, name="addRecipe"),
    path('Recipe/View/All/', views.allViews, name="viewAllRecipies"),
    path('Recipe/View/Filtered/', views.filterAllRecipes, name="filterAllRecipes"),
    path('Recipe/Delete/<uuid>/', views.deleteRecipe, name="deleteRecipe"),
    path('Recipe/Modify/<uuid>/', views.modifyRecipe, name="modifyRecipe"),
    path('Recipe/Modifying/<uuid>/', views.saveModification, name="saveModification"),
    path('Recipe/View/<uuid>/', views.viewRecipe, name="viewRecipe"),
    path('Home', views.gotohomepage, name="home")
]
