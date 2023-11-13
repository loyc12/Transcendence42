"""This file is used to create the login form."""
from django import forms

class LoginForm(forms.Form):
    """This class is used to create the login form."""
    email = forms.EmailField()  # This field is used to capture the user's email.
    password = forms.CharField(widget=forms.PasswordInput())
