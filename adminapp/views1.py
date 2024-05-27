from django.contrib.auth import authenticate, login,logout,get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime
from .models import Register,ForgetPassword,Gender,Activity
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django import forms
from django.core import validators
from django.contrib.auth.models import User,Group
from rest_framework.response import Response
import uuid
from .emailsendtxt import send_forget_password_mail,generate_otp
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse


def custom_login(request):
   try: 
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            print('user')
            print(user)
            print(request)
            print('request')
            user.save()
            print('user saved')
            login(request,user)
            print('logged in')
            return redirect('home')  
        else:
            messages.success(request,"username or passsword not correct")
            return redirect('login')         
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
        user=User(username=username,password=password,last_login=date)
        print(user.username)
        print(user.password)
        print(user.last_login)
        #user.save()
        return render(request, 'admin/home.html')
    return render(request, 'admin/login.html')

#=== Registeration ====

def register_view(request):
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
            render(request, 'admin/registration.html') 
  
        if User.objects.filter(username=username).exists():
            messages.success(request,"user already created through this username")
            render(request, 'admin/registration.html') 
        else:
          print(first_name, last_name, email, password, confirm_password, mobile, gender)  
          user = User.objects.create_user(username,email,password)
          user.first_name=first_name
          user.last_name=last_name
          user.mobile=mobile
          user.gender=gender
          user.save()
          messages.success(request,"Your account is created successfully")
          return redirect('/user/')
    return render(request, 'admin/registration.html')    

#==== HOME PAGE ====

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'admin/home.html')
    else:
        return redirect('login')  
# ==== at SUPERUSER side crud operation ====  

def users(request):
    context ={}
    # returns currently active model in the project
    User = get_user_model()
    #if logged user is superuser then this condition
    if request.user.is_superuser: 
        #list out all the user inside the User model
        users = User.objects.all()
        role = Group.objects.all()
        #This creates a paginator object that we can use to paginate the list of users.
        paginator = Paginator(users,4)
        # The request.GET.get("page") code allows you to extract the page number from the URL parameters.
        page_number = request.GET.get("page")
        #it's used to retrieve a specific page from the paginated content.
        usersFinal = paginator.get_page(page_number)
        #dictionary 
        context={
         'users': usersFinal,
         'role':role
        }
    # show the data of logged in user     
    else:
        print('hii123')
        #show the data of the requested user
        users = User.objects.filter(user=request.user)   
  
    return render(request, 'admin/user_ajax.html' , context)


def add_user(request):
   #if logged user is superuser then this condition
   if request.user.is_superuser:
    # if requested method is post then this condition
    if request.method=="POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email=request.POST.get('email')
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        mobile= request.POST.get('mobile')
        gender= request.POST.get('gender')
        role = request.POST.get('role')
        user_role=Group(name=role)
        user =User(username=username,first_name=first_name,last_name=last_name,email=email,password=password,gender_id=gender,mobile=mobile)
   return render(request, 'admin/add_user.html')

    
def edit_user(request,user_id=False):
    User = get_user_model() 

    if request.user.is_superuser:
        user=  User.objects.get(id=user_id) 
        if user is not None:
           return render(request, 'admin/edit_user.html',{'user_data': user})
        else :
           return render(request, 'admin/edit_user.html') 
    else:
      user=  User.objects.get(id=user_id) 
      print(user)
      if user is not None:
        return render(request, 'admin/edit_user.html',{'user_data': user})
      else :    
        return render(request, 'admin/edit_user.html') 


def delete_user(request,myid):
    if request.user.is_superuser:
      user = User.objects.get(id=myid)
      user.delete()
      return HttpResponseRedirect(reverse('home')) 
    else:
      user = User.objects.filter(username=request.user.username)
      user.delete()
      return HttpResponseRedirect(reverse('home'))   

def store(request):
    if request.user.is_superuser:
        User = get_user_model()
        Group = get_user_model()
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname= request.POST.get('lastname')
        email=request.POST.get('email')
        password= request.POST.get('password')
        repassword= request.POST.get('repassword')
        role= request.POST.get('role')
        print('hii1')
        if request.POST.get('user_id'):
            print("hii2")
            user =  User.objects.get(id=request.POST.get('user_id'))
            print(user)
            user.username=email
            user.first_name=firstname
            user.last_name=lastname
            user.password=password
            user.email=email
            user.role=role
            user.save()
            return render(request, 'admin/home.html')
        else :
            User =  get_user_model()
            newUser = User(email,email,password)
            print(newUser)
            newUser.save()
            return redirect('users') 
    else:
        return redirect('login')     

# def forgetpassword(request):
#     try:
#       if request.method == "POST":
#         print(request.method)
#         username=request.POST.get('username')

#         # if not User.objects.filter(username="").first():
#         #     messages.success(request,"Enter username")
#         #     return render(request, 'admin/forget_password.html'
#         if not User.objects.filter(username=username).first():
#             messages.success(request,"empty user or Not user found with this username")
#             return render(request, 'admin/forget_password.html')
#         user=User.objects.get(username=username)
#         print(user)
#         otp = generate_otp()
#         # token= str(uuid.uuid4())
#         print(otp)
#         reset_password= User.objects.get(username = user)
#         print('hii')
#         reset_password.otp= otp
#         print(reset_password)
#         reset_password.save()
#         send_forget_password_mail(user,otp)
#         #send_forget_password_mail(user,token)
#         if User.objects.filter(username=username).exists():
#           messages.success(request,"Email is sended!!")
#           return redirect('resetpassword')
#     except  Exception as e:
#         print(e)  
#     return render(request, 'admin/forget_password.html')    
   
#=== ForgetPassword view ===
def forgetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            print('hii')
            print(user)
            otp = generate_otp()
            print(otp)
            send_forget_password_mail(user,otp)
            messages.success(request," We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder also.")
            return redirect('resetpassword', username=user)
        except User.DoesNotExist:
            if not User.objects.filter(username=username).exists():
              messages.success(request,"Not user found with this username")
              return render(request, 'admin/forget_password.html')
    return render(request, 'admin/forget_password.html')


#=== Reset password view ===
def resetpassword(request, username):
    user = User.objects.get(username=username)
    print(user)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        entered_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print("Username:", user)
        print("Entered OTP:", entered_otp)
        fp=ForgetPassword(username=user,otp=entered_otp)
        fp.save()

        otp_obj = ForgetPassword.objects.filter(username=user, otp=entered_otp).first()
       
        print('hii')
        if entered_password != confirm_password:
            messages.error(request, "Your password and confirm password are not the same")
            return redirect(reverse('user:resetpassword'))
        if otp_obj:
            user.set_password(entered_password)
            user.save()
            # authenticated_user = authenticate(request, username=username, password=entered_password)
            # if authenticated_user:
            #     login(request, authenticated_user)
            otp_obj.delete()
            print('hii')
            print('hii')
            messages.success(request, 'Password reset successfully.')
            return redirect('forgetpassword') 
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'admin/reset_password.html', {'username': username})
   
#=== Logout pageview ===
def logout_view(request):
    logout(request)
    return redirect('/user/')  

