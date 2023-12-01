from django.contrib.auth.models import BaseUserManager

#class UserManager(UserManager):#(BaseUserManager):
class UserManager(BaseUserManager):
# Class object containing the methods to: create a user,
    def create_user(self, login, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.save()
        return user
