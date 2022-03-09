from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm, ProfileUpdateForm

# Register your models here.


class MyUserAdmin(UserAdmin):
	add_form = RegistrationForm
	form = ProfileUpdateForm
	model = CustomUser
	list_display = ['username', 'is_staff', 'is_active', 'image']
	# fieldsets = (
	# 	(None, {'fields': ('username', 'is_staff', 'is_active', 'telephone')}),
	# )

admin.site.register(CustomUser, MyUserAdmin)