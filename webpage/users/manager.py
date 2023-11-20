from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
# Class object containing the methods to: create a user,
    def create_user(self, login, display_name, **extra_fields):
        user = self.model(login=login, display_name=display_name, **extra_fields)
        user.save()
        return user