from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        validate_password(password, user=user)# *DO NOT CATCH EXECEPTION, LET FAIL.*. If password is invalid, raises ValidationError().
        user.set_password(password)

        user.save()
        return user