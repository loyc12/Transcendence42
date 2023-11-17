from django.shortcuts import render, HttpResponse
from .models import User

# Create your views here.

def user_main(request):
    print(request)
    return (HttpResponse("Reached User endpoint"))

def user_create(request):
    print(request)
    print("Try create user :")
    user = User.objects.create_user(
        #username="Jimmy_Johnson",
        username="Jimmy",
        email="asdf@jambon.com",
        password="myplainpassword"
    )

    return (HttpResponse(f"User {user.username} created Successfully."))

def user_get_jimmy(request):
    print(request)
    user = User.objects.get(username="Jimmy") 

    print("Got this user from database : ", user)
    return (HttpResponse(f"User successfully retrieved from database. user : {user}"))

def user_delete_jimmy(request):
    print(request)
    user = User.objects.get(username="Jimmy")
    user.delete()
    return (HttpResponse(f"User successfully deleted from database. Good bye {user.username}."))
