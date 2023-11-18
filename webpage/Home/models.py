""" This file contains the models for the Home app. """
from django.db import models

class MyModel(models.Model):
    """ This class is used to create a model."""
    my_field = models.CharField(max_length=50)
