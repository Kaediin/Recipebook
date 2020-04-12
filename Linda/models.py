from django.db import models

# Create your models here.

class Recipe:

    def __init__(self, title, ingredients, cookingMethod, estTime, img, imgname, author, cDate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.ingredients = ingredients
        self.cookingMethod = cookingMethod
        self.estTime = estTime
        self.img = img
        self.imgname = imgname
        self.author = author
        self.cDate = cDate



