""" This file contains the models for the Home app. """
from django.db import models
# models.py
# AV

class UserProfile(models.Model):
    """ This class is used to create the user profile model. """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pseudo = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.pseudo})'
