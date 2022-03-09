from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL


def register(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data

            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)

            # # Set the chosen password
            new_user.set_password(cd['password1'])

            name = cd['username']

            user_form.save()
            messages.success(
                request, f"Profile created for {name} successfully")

            return redirect('login')

    else:
        user_form = RegistrationForm()

    context = {
        'user_form': user_form
    }

    return render(request, 'registration/register.html', context)


@login_required
def profile(request):

    return render(request, 'registration/profile.html')


@login_required
def profile_update(request):
    if request.method == "POST":
        user_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = ProfileUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
    }

    return render(request, 'registration/profile_update.html', context)
