from django.urls import re_path
from users import consumers

user_ws_urlpatterns = [
    re_path(r'user/ws/(?P<sock_id>\w+)/$', consumers.UserConsumer.as_asgi())
]