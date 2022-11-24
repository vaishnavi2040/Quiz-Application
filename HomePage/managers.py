from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from . import models
# from .models import (Student)



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        if user.user_role == 'Student':
            student = models.Student(user=user)
            student.save()
            

        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)




# class CustomUserManager(BaseUserManager):

#     def create_user(self,username,Reg_Id,College_Name,password,**extra_fields):
#         if not username:
#             raise ValueError(_('The username should be set'))
#         user=self.model(username=username,Reg_Id=Reg_Id,College_Name=College_Name,**extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
    
#     def create_superuser(self ,username,Reg_Id,College_Name,password,**extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_superuser',True)
#         extra_fields.setdefault('is_active',True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=true'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=true'))
#         return self.create_user(username,Reg_Id,College_Name ,password,**extra_fields)
