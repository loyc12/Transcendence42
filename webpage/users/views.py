from django.shortcuts import render, HttpResponse
from .models import User

# Create your views here.
#users_user
# id | login | display_name | img_link | created_at | updated_at | last_login | password | is_active | socket_id 

def import_data(user_data):
    
    login = user_data.json()['login']
    if (User.objects.filter(login=login).exists()):
        return (f"User {login} already exists in database.")

    user =  User.objects.create_user(
            login=login,
            display_name=user_data.json()['displayname'],
            img_link=user_data.json()['image']['link'],
    )
    return (login)

def user_main(request):
    print(request)
    return (HttpResponse("Reached User endpoint"))

def user_create(request):
    print(request)
    print("Try create user :")
    user = User.objects.create_user(
        login="alvachon",
        display_name="Alexandra Vachon",
        img_link="https://cdn.intra.42.fr/users/alvachon.jpg",
        password="password",
    )

    return (HttpResponse(f"User {user.login} created Successfully."))

def user_get_jimmy(request):
    print(request)
    user = User.objects.get(login="alvachon")

    print("Got this user from database : ", user)
    return (HttpResponse(f"User successfully retrieved from database. user : {user}"))

def user_delete_jimmy(request):
    print(request)
    user = User.objects.get(login="alvachon")
    user.delete()
    return (HttpResponse(f"User successfully deleted from database. Good bye {user.login}."))
