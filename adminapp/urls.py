import django
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import ProfileListView,SearchView,Search_userlistView,Profile_ListView
# from .views import delete_selected_users,delete_user


#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.custom_login, name='login'),
    path('login', views.custom_login, name='login'),
    #path('user/', views.custom_login, name='login'),
    path('register', views.register_view, name='register'),
    path('home', views.home_view, name='home'),

    #forget & reset password urls 
    path('forgetpassword/',views.forgetpassword, name="forgetpassword"),
    path('resetpassword/<str:username>',views.resetpassword, name="resetpassword"),

    #userlist without ajax
    path('home/user_listnoaj',views.user_listnoaj, name="user_listnoaj"),
  
    path('home/users', ProfileListView.as_view(), name='users'),
    path('home/users/search_user/',SearchView.as_view(), name='search_user'),

    #user_list loader form search

    path('home/users_list', Profile_ListView.as_view(), name='users_list'),
    # path('home/users_list',views.user_list, name='users_list'),
    path('home/users_list/search_userlist/',Search_userlistView.as_view(), name='search_userlist'),

    #at superuser side crud operation url
    #path('home/users', views.users, name='users'),
    path('home/users_list/add/user', views.add_user, name='add'),
    path('home/users_list/edit/user/<int:pk>/', views.edit_user, name='edit_user'),
    path('home/users_list/delete/<int:pk>/',views.delete_user, name='delete_user'),
    #delete multiple users
    path('home/users_list/delete_selected_users/', views.delete_selected_users, name='delete_selected_users'),
    path('home/users_list/store', views.store, name='store'),
   
    #logout url   
    path('logout', views.logout_view, name='logout'),
    # Media URL pattern
    path('media/<path:media_path>', views.serve_media),
    #unknown path
    path('<path:unknown_path>', views.handle_404)

    # path('home', auth_views.home_view, name='home'),
    # path('login', auth_views.custom_login, name='login'),
    # path('logout/', auth_views.register_view, name='logout'),
    # # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Add other authentication-related URLs as needed (e.g., logout, password reset)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)