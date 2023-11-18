from django.contrib.auth.models import BaseUserManager

#class UserManager(UserManager):#(BaseUserManager):
class UserManager(BaseUserManager):
# Class object containing the methods to: create a user,
    def create_user(self, login, display_name, **extra_fields):
        user = self.model(login=login, display_name=display_name, **extra_fields)
        user.save()
        return user
    
'''    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("username", 'admin')
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        user = self.create_user(email, password, **extra_fields)
        print(f"Creating admin superuser. user : {user}, email : {email}, password : {password}, is_staff : {user.is_staff}, is_superuser : {user.is_superuser}")
        return user'''
    
'''
    def create_staffuser(self, email, password, username="staff", **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            **extra_fields
        )
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        user.is_staff = True
        user.is_admin = False
        user.is_superuser = user.is_admin
        user.save()
        return user
'''
