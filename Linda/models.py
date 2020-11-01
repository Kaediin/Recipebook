from django.db import models

# Create your models here.

class Recipe:

    def __init__(self, recipe_id, title, ingredients, cookingMethod, tags, estTime, imageUrl, imgname, author, cDate, mDate, is_archived, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = recipe_id
        self.title = title
        self.ingredients = ingredients
        self.cookingMethod = cookingMethod
        self.tags = tags
        self.estimatedTime = estTime
        self.imageUrls = imageUrl
        self.imgNames = imgname
        self.author = author
        self.creationDate = cDate
        self.modificationDate = mDate
        self.is_archived = is_archived



class TagThumbnail:

    def __init__(self, name, imgUrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.imgUrl = imgUrl



