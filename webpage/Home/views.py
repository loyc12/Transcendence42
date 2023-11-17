""" This file is used to render the home page and login page. """
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def home_view(request):
    """ This function is used to render the home page."""
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True
    return render(request, 'Home/home.html', context)


def login_view(request):
    """ This function is used to render the login page."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            # Authenticate user and redirect to home page if successful
            if user is not None:
                login(request, user)
                return redirect('home')
            error_message = 'Invalid email or password. Please try again.'
    else:
        form = LoginForm()

    return render(request, 'Login/login.html',
            {'form': form, 'error_message': error_message
                 if 'error_message' in locals() else ''})


def logo_view(request):
    """ This function is used to render the home page."""
    return render(request, 'logo.html')


def hero_view(request):
    """ This function is used to render the home page."""
    return render(request, 'shell.html')