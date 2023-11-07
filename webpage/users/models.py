from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser):

    # DB Fields
    email =         models.EmailField(unique=True)
    username =      models.CharField(max_length=32, unique=True)
    date_joined =   models.DateTimeField(default=timezone.now)

    #is_active =     models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()
