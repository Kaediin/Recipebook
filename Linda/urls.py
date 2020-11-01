from django.urls import path
from Linda import views

urlpatterns = [
    path('', views.signIn),
    path('Sign-in/', views.homepage, name="signin"),
    path('Recipe/Create/', views.createNewRecipe, name="createNewRecipe"),
    path('Recipe/Add/', views.addNewRecipe, name="addRecipe"),
    path('Recipe/View/All/', views.allViews, name="viewAllRecipes"),
    path('Recipe/Archived', views.allArchivedRecipes, name="viewAllArchivedRecipes"),
    path('Recipe/View/Filtered/<tags>', views.filterAllRecipes, name="filterAllRecipes"),
    path('Recipe/Delete/<uuid>/', views.deleteRecipe, name="deleteRecipe"),
    path('Recipe/Modify/<uuid>/', views.modifyRecipe, name="modifyRecipe"),
    path('Recipe/Modifying/<uuid>/', views.saveModification, name="saveModification"),
    path('Recipe/View/<uuid>/', views.viewRecipe, name="viewRecipe"),
    path('Home', views.gotohomepage, name="home"),
    path('Backup', views.createBackup, name="createBackup"),
    path('Restore', views.restoreBackup, name="restoreBackup"),
    path('Restore-Backup', views.importBackup, name="importBackup"),
    path('Recipe/Archive/<uuid>', views.archiveRecipe, name="archiveRecipe")
]
