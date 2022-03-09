from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class RegistrationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('image', 'username', 'email', 'telephone')
        
class ProfileUpdateForm(UserChangeForm):
    password = forms.CharField(
        help_text="",
        required=False,
        widget=forms.HiddenInput(
            
        )
    )
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'image', 'first_name', 'last_name', 'email', 'telephone', 'address')