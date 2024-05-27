from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from .models import Profile 
# from .models import CustomUser


# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ("email",)


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ("email",)

		
class ProfileForm(forms.ModelForm): 
	class Meta: 
		model = Profile 
		fields = ['image']


class UserSelectionForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)