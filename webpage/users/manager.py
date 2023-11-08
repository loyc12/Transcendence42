from django.contrib.auth.models import BaseUserManager
#from django.contrib.auth.password_validation import validate_password

class UserManager(BaseUserManager):

    def create_user(self, login, display_name, **extra_fields):
        if not login:
            raise ValueError('The login field must be set')
        if not display_name:
            raise ValueError('The Email field must be set')
        user = self.model(login=login, display_name=display_name, **extra_fields)
        user.save()
        return user