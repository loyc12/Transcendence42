""" This file is used to render the home page and login page. """
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm


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
            else:
                error_message = 'Invalid email or password. Please try again.'

    else:
        form = LoginForm()

    return render(request, 'Login/login.html',
            {'form': form, 'error_message': error_message
                 if 'error_message' in locals() else ''})

def logo_view(request):
    """ This function is used to render the home page."""
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True

    return render(request, 'Home/home.html', context)

def home_view(request):
    """ This function is used to render the home page."""
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True

    return render(request, 'Home/home.html', context)


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Process form data and perform login here
#             return redirect('home')  # Redirect to the home page after login
#     else:
#         form = LoginForm()

#     return render(request, 'Home/login.html', {'form': form})
