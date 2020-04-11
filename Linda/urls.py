from django.urls import path
from Linda import views

urlpatterns = [
    path('', views.signIn),
    path('Sign-in', views.homepage),
    path('Recipe/Create', views.createNewRecipe, name="createNewRecipe"),
    path('Recipe/Add', views.addNewRecipe, name="addRecipe"),
    path('Recipe/View', views.allViews, name="viewAllRecipies"),
    path(r'^post/(?P<uuid>\d+)/$', views.viewRecipe, name="viewRecipe"),
    path('Home', views.gotohomepage, name="home")
]
