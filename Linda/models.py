from django.db import models

# Create your models here.

class Recipe:

    def __init__(self, title, ingredients, cookingMethod, tags, estTime, img, imgname, author, cDate, mDate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.ingredients = ingredients
        self.cookingMethod = cookingMethod
        self.tags = tags
        self.estTime = estTime
        self.img = img
        self.imgname = imgname
        self.author = author
        self.cDate = cDate
        self.mDate = mDate



class TagThumbnail:

    def __init__(self, name, imgUrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.imgUrl = imgUrl



