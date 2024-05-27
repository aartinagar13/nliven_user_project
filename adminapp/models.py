
from django.db import models
from django.utils import timezone
from django.db.models import Model
from django.contrib.auth.models import User,Group,AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
# from django.core.exceptions import ValidationError
# from django.core.validators import EmailValidator
# from validate_email import validate_email

# def validate_google_email(value):
#     """
#     Validate that the email is valid and associated with Google.
#     """
#     if not validate_email(value, verify=True, check_mx=True):
#         raise ValidationError('Invalid email address.')

#     if 'google' not in value.lower():
#         raise ValidationError('Email must be associated with Google.')

# Create your models here.
class Activity(models.Model):
    username=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    news_image=models.FileField(upload_to="", max_length=254, null=True, default=None)
    #news_image=models.FileField()
    date=models.DateField()
    
    def __str__(self):
        return self.username

class Gender(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    def get_data(self):
         return {
              'gender': self.name,
         }
    
        
class Role(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    def get_data(self):
         return {
              'role': self.name,
         }
    
class ForgetPassword(models.Model):  
    username = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    #forget_password_token=models.CharField(max_length=100)
    otp=models.CharField(max_length=6)
    def __str__(self):
        return self.username   

class Profile(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', null=True, blank=True)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=255)
      
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='profile_groups',  # Set a custom related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='profile_user_permissions',  # Set a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        try:
            this =Profile.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass 
        super().save(*args, **kwargs)  
