from django.urls import path
from Linda import views

urlpatterns = [
    path('', views.signIn),
    path('Sign-in', views.homepage),
    path('Recipe/Create', views.createNewRecipe),
    path('Recipe/Add', views.addNewRecipe),
    path('Recipe/View', views.allViews),
    path(r'^post/(?P<uuid>\d+)/$', views.viewRecipe, name="viewRecipe"),
    path('Home', views.gotohomepage)
]
