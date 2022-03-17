from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileUpdateForm, RegistrationForm
from .models import CustomUser

# Register your models here.


class MyUserAdmin(UserAdmin):
	add_form = RegistrationForm
	form = ProfileUpdateForm
	model = CustomUser
	list_display = ['username', 'is_staff', 'is_active', 'image']

admin.site.register(CustomUser, MyUserAdmin)
