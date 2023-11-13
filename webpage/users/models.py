from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.db import models
from django.utils import timezone
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin ):

    # DB Fields
    email =         models.EmailField(unique=True)
    username =      models.CharField(max_length=32, unique=False)
    created_at =    models.DateTimeField(auto_now_add=True)
    updated_at =    models.DateTimeField(auto_now=True)
    is_staff =      models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    is_active =     models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"User: {self.username}, email: {self.email}, created_at: {self.created_at}, updated_at: {self.updated_at}, hash: {self.password}"