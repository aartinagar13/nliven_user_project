from django.core.mail import send_mail
from django.conf import settings
import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ForgetPassword
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

#from email.mime.text import MIMEText

def generate_otp():
    return str(random.randint(100000, 999999))

def send_forget_password_mail(user,otp):
    subject = "Password Reset OTP"
    body = f"Your OTP for password reset is: {otp}"
    email_from =settings.EMAIL_HOST_USER
    recipient_list=[user]
    send_mail(subject,body,email_from,recipient_list)
    return True
    

#def send_forget_password_mail(email,token,otp):
    # subject ='Your forget password link'
    # message =f'Hii,Click on the link to reset your password http://192.168.1.69:8000/user/resetpassword/{token}/'
    # email_from =settings.EMAIL_HOST_USER
    # recipient_list=[email]
    # send_mail(subject, message,email_from,recipient_list)
    # return True