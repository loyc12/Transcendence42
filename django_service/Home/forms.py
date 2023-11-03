from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()  # This field is used to capture the user's email.
    password = forms.CharField(widget=forms.PasswordInput())  # This field is used for the password input.

