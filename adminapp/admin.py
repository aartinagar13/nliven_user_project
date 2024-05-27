from django.contrib import admin
from .models import Profile,ForgetPassword,Gender,Activity,Role
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group
from django.conf import settings 

admin.site.register(Profile)
admin.site.register(ForgetPassword)
admin.site.register(Gender)
admin.site.register(Activity)
admin.site.register(Role)


    
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

