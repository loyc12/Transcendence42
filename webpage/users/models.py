from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from .manager import UserManager

#public data
#   "login": "string",
#   "display_name": "string"
#   "image": {
#     "link": "string",
#     "versions":{
#       "large": "string",
#       "medium": "string",
#       "small": "string",
#       "micro": "string"
#     }
#  },

# GET FROM 42 API TO DB FIELD
class User(AbstractBaseUser):

    # DB Fields
    login =             models.CharField(max_length=32, unique=True)
    display_name =      models.CharField(max_length=60, unique=False)
    
    img_link =          models.CharField(max_length=120, unique=False)
    img_vlarg=          models.CharField(max_length=120, unique=False)
    img_vmed=           models.CharField(max_length=120, unique=False)
    img_vsmall=         models.CharField(max_length=120, unique=False)
    img_vmicro=         models.CharField(max_length=120, unique=False)
    
    created_at =        models.DateTimeField(auto_now_add=True)
    updated_at =        models.DateTimeField(auto_now=True)
    
    password =          models.CharField(max_length=120, unique=False)
    #is_active =     models.BooleanField(default=False)

    USERNAME_FIELD = "login"

    objects = UserManager()

    def __str__(self):
        return f"User: {self.login}, display_name: {self.display_name}, created_at: {self.created_at}, updated_at: {self.updated_at}"