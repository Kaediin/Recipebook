from django.db import models

# Create your models here.

class Recipe:

    def __init__(self, title, description, ingredients, cookingMethod, estTime, img, author, cDate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.cookingMethod = cookingMethod
        self.estTime = estTime
        self.img = img
        self.author = author
        self.cDate = cDate



