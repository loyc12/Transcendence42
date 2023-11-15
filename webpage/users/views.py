from django.shortcuts import render, HttpResponse
from .models import User

# Create your views here.
#users_user
# id | login | display_name | img_link | created_at | updated_at | last_login | password | is_active | socket_id 

def import_data(user_data):
    
    login = user_data.json()['login']
    if (User.objects.filter(login=login).exists()):
        User.objects.filter(login=login).update(
            is_active=1,
        )
    else:
        user =  User.objects.create_user(
                login=login,
                display_name=user_data.json()['displayname'],
                img_link=user_data.json()['image']['link'],    
                is_active=1,    
        )
    return (f"Welcome {login} !")

def user_delete_jimmy(request):
    print(request)
    user = User.objects.get(login="alvachon")
    user.delete()
    return (HttpResponse(f"User successfully deleted from database. Good bye {user.login}."))
