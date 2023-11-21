"""This file is used to create the login form."""
forms.py

from django import forms

class ProfileForm(forms.Form):
    """ This class is used to create the login form. """
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    pseudo = forms.CharField(max_length=50)
