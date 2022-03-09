from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('image', 'username', 'first_name', 'last_name', 'email', 'telephone', 'address')


class ProfileUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password = forms.CharField(
        help_text="",
        required=False,
        widget=forms.HiddenInput(

        )
    )
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('image', 'username', 'first_name', 'last_name', 'email', 'telephone', 'address')


class AdminProfileUpdateForm(UserChangeForm):
    

    password = forms.CharField(
        help_text="",
        required=False,
        widget=forms.HiddenInput(

        )
    )

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('image', 'username', 'first_name', 'last_name', 'email', 'telephone', 'address','is_active', 'is_staff')
