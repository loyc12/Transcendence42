from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField(max_length=32, unique=True, blank=False)


    hash = models.CharField(max_length=64, blank=False, )
