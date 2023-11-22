from django.contrib import admin
from .models import User

# Add User item to admin panel
admin.site.register(User)
