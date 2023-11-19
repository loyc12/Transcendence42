from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from .manager import UserManager

class User(AbstractBaseUser):
    # Fields of table users_user
    login           = models.CharField    (max_length=32, unique=True)
    display_name    = models.CharField    (max_length=60, unique=False)
    img_link        = models.CharField    (max_length=120, unique=False) 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField (default=False)
    socket_id       = models.CharField    (max_length=120, unique=False)
    
    # Variable that contain the name of the field used to identify the user
    USERNAME_FIELD = "login"
    
    # Method that return a string with the information of the user
    objects = UserManager()

    def __str__(self):
        return f"User: {self.login},\
                display_name: {self.display_name},\
                created_at: {self.created_at},\
                updated_at: {self.updated_at}"