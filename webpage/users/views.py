from .models import User
from django.contrib.sessions.models import Session

# Collect data from API and save it in the database, start session
def import_data(api_data, request):
    
    target_id = api_data.json()['login']
    # Check if user exists and get it
    if (User.objects.filter(login=target_id).exists()):
        User.objects.filter(login=target_id).update(
            is_active = 1,
        )
        u = User.objects.get(login=target_id)

    # If not, create it
    else:
        u = User.objects.create_user(
            login           = target_id,
            display_name    = api_data.json()['displayname'],
            img_link        = api_data.json()['image']['link'],    
            is_active       = 1,    
        )
    # Update session
    u.save()
    request.session['user_id'] = u.login
    request.session['user_login'] = u.login
    request.session.save()
    #session_key = request.session.session_key
    #session = Session.objects.get(session_key=session_key)
    return

# def remove_data(request):
#     user_id = request.session['user_id']
#     User.objects.filter(id=user_id).update(
#         is_active=0,
#     )
#     request.session.flush()
#     return
