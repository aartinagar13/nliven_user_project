from django.contrib.auth import authenticate, login,logout,get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime
from .models import Profile,ForgetPassword,Gender,Activity,Role
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django import forms
from django.core import validators
from django.contrib.auth.models import Group,Permission
from django.db.models import Q
import uuid
from .emailsendtxt import send_forget_password_mail,generate_otp
from django.http import HttpResponseRedirect,HttpResponse,Http404,JsonResponse
from django.urls import reverse
from itertools import chain
from django.views import View
from .forms import ProfileForm 
from django.contrib.auth.hashers import make_password
from django.conf import settings
import os
from django.views.static import serve
from django.core.exceptions import ValidationError
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import format_html
import logging
# def Profile_list(request):
#     return render(request, 'datatable_app/Profile_list.html') 

def handle_404(request, unknown_path):
    return render(request, 'admin/404.html', status=404)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = Profile(request, username=username, password=password)
        
        if user is not None:
            # Check if the user has registration attributes
               # login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Username or password not correct.")
            return redirect('login')
    else:
        return render(request, 'admin/login.html')

def login_view(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password= request.POST.get('password')
        date= datetime.today()
        user=Profile(username=username,password=password,date=date)
        print('user here ',user)
        user.save()
        return render(request, 'admin/home.html')
    
    return render(request, 'admin/login.html')    

#=========media=========


def serve_media(request, media_path):
    # Construct the full path to the requested media file
    full_path = os.path.join(settings.MEDIA_ROOT, media_path)
    
    # Check if the file exists, otherwise raise a 404 error
    if not os.path.exists(full_path):
        raise Http404("Media file not found")

    # Use Django's built-in serve view to serve the media file
    return serve(request, media_path, document_root=settings.MEDIA_ROOT)  

#=== Registeration ====

def register_view(request):
    Profile = get_user_model() 
    # genders =Gender.objects.all()
    # role =Role.objects.all()
    # image =Profile.objects.all()
    if request.method=="POST":      
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email=request.POST.get('email')
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        mobile= request.POST.get('mobile')
        gender= request.POST.get('gender')
        role= request.POST.get('role')
        image = request.POST.get('fileInput')
        image = request.FILES.get('fileInput')
        print('image',image)
        print("hii")
        gender_mention = Gender.objects.get(name=gender)              
        if password!=confirm_password:
            messages.error(request,"your password and confirm password are not same")
            return redirect('register')   
  

        # if Profile.objects.filter(username=username).exists():
        #     messages.error(request,"user already created through this username")
        #     return redirect('register')   
 
        else:
          print(first_name, last_name, email, password, confirm_password, mobile,role, gender)  
        #   password = make_password('password')
          print(password)
          user = Profile.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,role_id=3,gender_id=gender_mention.id,image=image)
          print(user)
          user.save()
          messages.success(request,"Your account is created successfully")
          return redirect('/')
    return render(request, 'admin/registration.html')  

#==== HOME PAGE ====

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'admin/home.html')
    else:
        return redirect('login') 
   

# ==== at SUPERUSER side crud operation ====  

def user_listnoaj(request):
    gender = Gender.objects.all()
    #if logged user is superuser then this condition
    if request.user.is_superuser: 
        #list out all the user inside the Profile mode
        register_users =Profile.objects.all().order_by('-id')

        # Retrieve all Role objects
        role_users = Role.objects.all()

        # Retrieve all Gender objects
        gender_users = Gender.objects.all()
        images_users =Profile.objects.all()

        # Combine the two QuerySets
        users = list(chain(register_users, role_users,gender_users,images_users)) 
        #users =  list(chain(Register, Role))
       # Assuming you have a Profile model with foreign keys to Register, Role, and Gender
        users = Profile.objects.all()

        #This creates a paginator object that we can use to paginate the list of users.
        paginator = Paginator(users,4)
        # The request.GET.get("page") code allows you to extract the page number from the URL parameters.
        page_number = request.GET.get("page")
        #it's used to retrieve a specific page from the paginated content.
        users = paginator.get_page(page_number)

        return render(request, 'admin/users.html',{ 'users':users})

    # # show the data of logged in user     
    if request.user.is_authenticated: 
     try:
        # user = self.request.user
        user = request.user
        if user.groups.filter(name='Manager').exists():
            # Manager can see all data
            return Profile.objects.all()
        elif user.groups.filter(name='Profile').exists():
            # Profile can see their own data
            return Profile.objects.filter(username=user)

        #show the data of the requested user
        manager_role = Role.objects.get(role='Manager')
        print(manager_role)
        user_role = Role.objects.get(role='user')
        print('user_role:', user_role)

        # Print relevant information for debugging
        print('Profile:', request.user)
        users = Profile.objects.filter(role__in=[manager_role, user_role])
        print(users)
     except Role.DoesNotExist:
        # Handle the case where the role does not exist
        raise Http404("Role does not exist.")   
        
    # else:
    #     user_role = Role.objects.get(role='user')
    #     print('user_role:', user_role)
    return render(request, 'admin/users.html',{ 'users':users })



class ProfileListView(View):
    template_name = 'admin/user_ajax.html'
    search_term = ''
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            if request.user.is_superuser: 
                search_term = request.GET.get('search')
                # Assuming you have a Profile model with foreign keys to Register, Role, and Gender
                # users = Profile.objects.select_related('role','gender','image').all()
                users = Profile.objects.all()
                print(users)
                #This creates a paginator object that we can use to paginate the list of users.
                paginator = Paginator(users,4)
                # The request.GET.get("page") code allows you to extract the page number from the URL parameters.
                page_number = request.GET.get("page")
                #it's used to retrieve a specific page from the paginated content.
                users = paginator.get_page(page_number)
                return render(request, self.template_name, {'users':users})

            if request.user.is_authenticated:
             if Profile.objects.all() == request.user:  
                user = request.user
                search_term = request.GET.get('search')
                print('user details:',user)
                if user.groups.filter(name='Manager').exists():
                    # Manager can see all data
                    print('if block')
                 
                    users = Profile.objects.all()
                    paginator = Paginator(users,4)
                    page_number = request.GET.get("page")
                    users = paginator.get_page(page_number)
                    return render(request, self.template_name, {'users':users ,'search_term': search_term })
                elif user.groups.filter(name='user').exists():
                    print('elif block')
                    # Profile can see their own data
                    users = Profile.objects.filter(username=request.user)
                    return render(request, self.template_name,{'users':users ,'search_term': search_term })

                # Show the data of the requested user
                # manager_role = Role.objects.get(role='Manager')
                # user_role = Role.objects.get(role='Profile')

                # # Print relevant information for debugging
                # print('Profile:', request.user)
                # users = Register.objects.filter(role__in=[manager_role, user_role])
                # print(users)
            #  else:
            #     return render(request, 'admin/adminauth.html')            
            else:
                return render(request, 'admin/login.html')
                # user_role = Role.objects.get(role='user')
                # print('user_role:', user_role)
                # users = Register.objects.filter(role=user_role)    
        except Role.DoesNotExist:
            # Handle the case where the role does not exist
            raise Http404("Role does not exist.")
        #return render(request, self.template_name)
        return render(request, self.template_name, )

class SearchView(View):
    template_name = 'admin/search_user.html'
    search_query =''
    def get(self, request, *args, **kwargs):
      if request.user.is_superuser: 
        if request.GET.get('search')!='':
            search_query = request.GET.get('search')
            userss = Profile.objects.filter(username__icontains=search_query)
            users = Profile.objects.all()
            paginator = Paginator(userss,4)   
            page_number = request.GET.get("page")
            users = paginator.get_page(page_number)
            return render(request, self.template_name, {'users':users ,'userss' : userss,'search_query':search_query})
        else:
            # messages.error(request,"please search for the user")
            return render(request, self.template_name)
      if request.user.is_authenticated:  
        if request.GET.get('search')!='':
            if Profile.objects.all() == request.user:  
                user = request.user
                search_query = request.GET.get('search')
                userss = Profile.objects.filter(username__icontains=search_query)
                print('user details:',user)
                if user.groups.filter(name='Manager').exists():
                    # Manager can see all data
                    print('if block')
                    users = Profile.objects.all()
                    paginator = Paginator(userss,4)
                    page_number = request.GET.get("page")
                    users = paginator.get_page(page_number)
                elif user.groups.filter(name='user').exists():
                    print('elif block')
                    # Profile can see their own data
                    users = Profile.objects.filter(username=request.user)
            return render(request, self.template_name, {'users':users ,'userss' : userss,'search_query':search_query})
        else:
            # messages.error(request,"please search for the user")
            return render(request, self.template_name)  
      return render(request, self.template_name)   



class Profile_ListView(View):
    template_name = 'admin/user_list.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser: 
                profile = Profile.objects.all()
                role = Role.objects.all().values_list('name', flat=True)
                gender = Gender.objects.all().values_list('name', flat=True)
                return render(request, self.template_name, {'role': role, 'gender': gender, 'profile': profile})

            if request.user.is_authenticated:
                user = request.user
                print('user details:', user)
                search_term = request.GET.get('searchInput')
                if user.role == Role.objects.get(name='Manager'):
                    # Manager can see all data
                    print('if block')
                    users = Profile.objects.filter(role_id=1)
                    return render(request, self.template_name, {'users': users})
                else:
                    print('elif block')
                    print(request.user)
                    # Profile can see their own data
                    users = Profile.objects.filter(username=request.user)
                    return render(request, self.template_name, {'users': users})
            else:
                return render(request, 'admin/login.html')    
        except Role.DoesNotExist:
            raise Http404("Role does not exist.")



class Search_userlistView(BaseDatatableView):
    model = Profile
    columns = ['id', 'image', 'username', 'first_name', 'last_name', 'email', 'role_id', 'gender_id','action','']
    order_columns = ['id', 'image', 'username', 'first_name', 'last_name', 'email', 'role_id', 'gender_id','action','']
    def render_column(self, row, column):
        if column == 'email':
            return '<a href="mailto:{}">{}</a>'.format(row.email, row.email)
        else:
            return super(Search_userlistView, self).render_column(row, column)    
    
    def filter_queryset(self, qs):

        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(username__startswith=search)

        return qs
        

def add_user(request):
   roles = Role.objects.all()
   genders =Gender.objects.all()
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
        print(confirm_password)
        mobile= request.POST.get('mobile')
        gender= request.POST.get('gender')
        role = request.POST.get('role')
        image = request.POST.get('fileInput')
        image = request.FILES.get('fileInput')
        
        print(image)
        user =Profile.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,role_id=role ,gender_id=gender,mobile=mobile,image=image)
        user.save()
        print('add_view')
   return render(request, 'admin/add_user.html',{"roles":roles,"genders":genders})

    
# def edit_user(request,user_id=False):
#     Profile = get_user_model() 

#     if request.user.is_superuser:
#         user= Profile.objects.get(id=user_id) 
#         if user is not None:
#             return render(request, 'admin/edit_user.html',{'user_data': user})
#         else :
#            return render(request, 'admin/edit_user.html') 
#     else:
#       if Profile.objects.all() == request.user:  
#         user =  Profile.objects.get(username=request.user) 
#         print(user)
#         if user is not None:
#             return render(request, 'admin/edit_user.html',{'user_data': user})
#         else :    
#             return render(request, 'admin/edit_user.html') 
#       else:
#          return render(request, 'admin/adminauth.html')    
      
def edit_user(request, pk):

    if request.user.is_superuser:  
        user = Profile.objects.get(pk=pk)
        if user  is not None:
            return render(request, 'admin/edit_user.html',{'user_data': user})
    else:
      if Profile.objects.all() == request.user:  
        user =  Profile.objects.get(username=request.user) 
        print(user)
        if user is not None:
            return render(request, 'admin/edit_user.html',{'user_data': user})
        else :    
            return render(request, 'admin/edit_user.html') 
      else:
         return render(request, 'admin/adminauth.html')    
       
    
def delete_user(request, pk):
        if Profile.objects.filter(id=pk).exists():
            user =Profile.objects.get(id=pk)
            user.delete()
            messages.success(request,"User deleted")
            return render(request, 'admin/user_list.html')
        
        else:
            messages.error(request, f'user doesnot exsits')
            return render(request, 'admin/user_list.html')
    
def delete_selected_users(request):
        user_ids = request.POST.getlist('id')
        print(user_ids)  # Get the selected user IDs from the form
        if user_ids:
            Profile.objects.filter(id__in=user_ids).delete()
            messages.success(request, f'Selected users deleted successfully.')
            return redirect('users_list')  # Replace 'user_list' with your actual user list view name
        else:
            messages.error(request, f'user does not exsits')
            return render(request, 'admin/user_list.html')

def store(request):
  try: 
     if request.method=="POST":
        context ={}
        username=request.POST.get('username')
        firstname=request.POST.get('first_name')
        lastname= request.POST.get('last_name')
        email=request.POST.get('email')
        image = request.POST.get('fileInput')
        image = request.FILES.get('fileInput')
        gender= request.POST.get('gender')
        role = request.POST.get('role')
        # print(request.FILES.get('fileInput'))
        print('file1')

        # Now, file is saved at file_path
        print('Image saved:', image)
        if request.POST.get('user_id'):
            print("hii2") 
            user =Profile.objects.get(id=request.POST.get('user_id'))
            print(user)
            print('user')
            user.first_name=firstname
            print(firstname)
            user.last_name=lastname
            user.email=email
            user.image=image 
            user.save()
            # Additional validation, e.g., unique email
            if Profile.objects.filter(email=email).exclude(id=request.POST.get('user_id', 0)).exists():
                messages.error(request, "Email is already in use.")
                return redirect(reverse('edit_user', kwargs={'user_id': request.POST.get('user_id')}))
            
            messages.success(request, 'User updated successfully.')
            return HttpResponseRedirect(reverse('users_list'))       
        else :
            print('#user =  get_user_model()')
            print(firstname, lastname, email, image)  
            # Additional validation, e.g., unique email
            if Profile.objects.filter(email=email).exclude(id=request.POST.get('user_id', 0)).exists():
                messages.error(request, "Email is already in use.")
                return redirect('add')
            user = Profile.objects.create(username=username,first_name=firstname,last_name=lastname,email=email,image=image,gender_id=gender,role_id=role)
            user.save()
            messages.success(request, 'User created successfully.')
            return HttpResponseRedirect(reverse('users_list'))
    
  except  Exception as e:
            return redirect('users_list')
  return render(request, 'datatable_app/edit_user.html')   
    
 



#=========sending tken for password reset=====
   
# def forgetpassword(request):
#     try:
#       if request.method == "POST":
#         print(request.method)
#         username=request.POST.get('username')

#         # if not Profile.objects.filter(username="").first():
#         #     messages.success(request,"Enter username")
#         #     return render(request, 'admin/forget_password.html'
#         if not Profile.objects.filter(username=username).first():
#             messages.success(request,"empty user or Not user found with this username")
#             return render(request, 'admin/forget_password.html')
#         user=Profile.objects.get(username=username)
#         print(user)
#         otp = generate_otp()
#         # token= str(uuid.uuid4())
#         print(otp)
#         reset_password= Profile.objects.get(username = user)
#         print('hii')
#         reset_password.otp= otp
#         print(reset_password)
#         reset_password.save()
#         send_forget_password_mail(user,otp)
#         #send_forget_password_mail(user,token)
#         if Profile.objects.filter(username=username).exists():
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
            user = Profile.objects.get(username=username)
            print('hii')
            print(user)
            otp = generate_otp()
            print(otp)
            send_forget_password_mail(user,otp)
            messages.success(request," We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder also.")
            return redirect('resetpassword', username=user)
        except Profile.DoesNotExist:
            if not Profile.objects.filter(username=username).exists():
              messages.success(request,"Not user found with this username")
              return render(request, 'admin/forget_password.html')
    return render(request, 'admin/forget_password.html')


#=== Reset password view ===
def resetpassword(request, username):
    user = Profile.objects.get(username=username)
    print(user)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        entered_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print("Profilename:", user)
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
    return redirect('login')  