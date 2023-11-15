from django.shortcuts import render, HttpResponse
from .models import User
from django.contrib.sessions.models import Session


# Create your views here.
#users_user
# id | login | display_name | img_link | created_at | updated_at | last_login | password | is_active | socket_id 

def import_data(user_data, request):
    
    login = user_data.json()['login']
    if (User.objects.filter(login=login).exists()):
        User.objects.filter(login=login).update(
            is_active=1,
        )
        u = User.objects.get(login=login)
    else:
        u = User.objects.create_user(
        login=login,
        display_name=user_data.json()['displayname'],
        img_link=user_data.json()['image']['link'],    
        is_active=1,    
    )
    request.session['user_id'] = u.id
    request.session['user_login'] = u.login
    request.session.save()
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    return

def user_delete_jimmy(request):
    print(request)
    user = User.objects.get(login="alvachon")
    user.delete()
    return (HttpResponse(f"User successfully deleted from database. Good bye {user.login}."))
