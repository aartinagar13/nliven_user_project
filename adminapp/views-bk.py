from django.contrib.auth import authenticate, login,logout,get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Register,ForgetPassword,Gender,Activity
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from rest_framework.response import Response
import uuid
from .emailsendtxt import send_forget_password_mail,generate_otp
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import pyotp
from django.db.models.query_utils import Q



# Create your views here.
def custom_login(request):
   try: 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')  
        else:
            messages.success(request,"username or passsword not correct")
            return render(request, 'admin/login.html')          
    else : 
        return render(request, 'admin/login.html')
   except  Exception as e:
        print(e)      
   return render(request, 'admin/login.html')      

def login_view(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password= request.POST.get('password')
        date= datetime.today()
        user=User(username=username,password=password,date=date)
        user.save()
        return render(request, 'admin/home.html')
    
    return render(request, 'admin/login.html')


def register_view(request):
  try:  
    if request.method=="POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email=request.POST.get('email')
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        mobile= request.POST.get('mobile')
        gender= request.POST.get('gender')
        print("hii")
        if password!=confirm_password:
            messages.success(request,"your password and confirm password are not same")
            return render('register')

        if User.objects.filter(username=username).exists():
            messages.success(request,"user already created through this username")
            return render('register')   
    
        else:
        # print(first_name, last_name, email, password, confirm_password, mobile, gender)
          user = User.objects.create_user(username,email, password)
          user.username=username
          user.first_name=first_name
          user.last_name=last_name
          user.email=email
          user.password=password
          user.confirm_password=confirm_password
          user.mobile=mobile
          user.gender=gender
          user.save()
          messages.success(request,"Your account is created successfully")
          return render('login') 
    else:
        return render(request, "admin/registration.html" )
  except  Exception as e:
        messages.success(request,"Please fill the form")    
        print(e)      
  return render(request, 'admin/registration.html')      
    
def add_user(request):
    return render(request, 'admin/add_user.html')

    
def edit_user(request,user_id=False):
    User = get_user_model()
    print(User)
    user=  User.objects.get(id=user_id) 
    print(user)
    if user is not None:
        return render(request, 'admin/edit_user.html',{'user_data': user})
    else :
        return render(request, 'admin/edit_user.html') 

def delete_user(request,myid):
    user = User.objects.get(id=myid)
    print(user)
    user.delete()
    return HttpResponseRedirect(reverse('home'))


def store(request):
    if request.user.is_authenticated:
        first_name = forms.CharField(initial = 'First Name', required=True)
        email = forms.EmailField(initial = 'Enter your email', required=True, validators=[validators.EmailValidator(message="Invalid Email")])
        User = get_user_model()
        firstname=request.POST.get('firstname')
        lastname= request.POST.get('lastname')
        email=request.POST.get('email')
        password= request.POST.get('password')
        password= request.POST.get('confirm_password')
        if request.POST.get('user_id'):
            user =  User.objects.get(id=request.POST.get('user_id')) 
            user.username=email
            user.first_name=firstname
            user.last_name=lastname
            user.password=password
            user.email=email
            user.save()
            return redirect('users') 
        else :
            User=  get_user_model()
            newUser=User.objects.create_user(email,email,password)
            newUser.first_name=firstname
            newUser.last_name=lastname
            newUser.save()
            return redirect('users') 
    else:
        return redirect('login')  


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'admin/home.html')
    else:
        return redirect('login')  
    
def users(request):
    if request.user.is_authenticated:
        User = get_user_model()
        users = User.objects.all()
        paginator = Paginator(users,5)
        page_number = request.GET.get("page")
        usersFinal = paginator.get_page(page_number)
        print(users)
        return render(request, 'admin/users.html' , {'users': usersFinal})
    else:
        return redirect('login')  

def forgetpassword(request):
    try:
      if request.method == "POST":
        print(request.method)
        username=request.POST.get('username')

        # if not User.objects.filter(username = "").first():
        #     messages.success(request,"Enter username")
        #     return render(request, 'admin/forget_password.html')
        
        if not User.objects.filter(username=username).first():
            messages.success(request,"empty user or Not user found with this username")
            return render(request, 'admin/forget_password.html')
        
        if User.objects.filter(username=username).exists():
           user=User.objects.get(username=username) 
           print(user)
           otp = generate_otp()
           # token= str(uuid.uuid4())
           print(otp)
           user= User.objects.get(username = user)
           print('hii')
           user.otp= otp
           print(user)
           user.save()
           send_forget_password_mail(user,otp)
           #send_forget_password_mail(user,token)
           messages.success(request,"Email is sended!!")
           return redirect('resetpassword')
    except  Exception as e:
        print(e)  
    return render(request, 'admin/forget_password.html')    

def resetpassword(request):
    
    context ={} 
    try:
         print('hii3')
         if request.method == "POST":
            entered_otp = request.POST.get('otp')
            print('Entered OTP:', entered_otp)
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id') 
            print(user_id)
             
            stored_otp = get_object_or_404(ForgetPassword, username_id=user_id)
            print("Stored OTP:", stored_otp)
            print('hii4')
            if entered_otp != stored_otp:
                return HttpResponse('Invalid OTP. Please try again.')


            if new_password != confirm_password:
                messages.error(request, "Your password and confirm password are not the same")
                return render('resetpassword')

            #validate_password(new_password)  

            if User.objects.filter(password=new_password).exists():
                messages.error(request, "This is an old password. Enter a new password")
                return render('resetpassword')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            print('hii5')
            messages.success(request, "Password reset successfully")
            return redirect('login')

    except Exception as e:
        messages.error(request, "An error occurred during password reset. Please try again.")
        print('Error:', e)

    return render(request, 'admin/reset_password.html',context)


def logout_view(request):
    logout(request)
    return redirect('login')  