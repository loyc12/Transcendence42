from django.contrib import admin
from .models import User
#from .forms import UserCreationForm, UserChangeForm

# Add User item to admin panel
admin.site.register(User)
