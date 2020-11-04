from django.db import models

# Create your models here.

class Recipe:

    def __init__(self, recipe_id, title, ingredients, cookingMethod, tags, estTime, imageUrl, imgname, author_id, cDate, mDate, is_archived, authorUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = recipe_id
        self.title = title
        self.ingredients = ingredients
        self.cookingMethod = cookingMethod
        self.tags = tags
        self.estimatedTime = estTime
        self.imageUrls = imageUrl
        self.imgNames = imgname
        self.author_id = author_id
        self.creationDate = cDate
        self.modificationDate = mDate
        self.is_archived = is_archived
        self.authorUser = authorUser



class TagThumbnail:

    def __init__(self, name, imgUrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.imgUrl = imgUrl



class AuthorUser:

    def __init__(self, displayName, email, phoneNumber, photoURL, uid):
        self.displayName = displayName
        self.email = email
        self.phoneNumber = phoneNumber
        self.photoURL = photoURL
        self.uid = uid
