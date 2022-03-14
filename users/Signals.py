from django.conf import settings
from django.contrib import messages
from django.contrib.auth.signals import (user_logged_in, user_logged_out, user_login_failed)
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL
from django.db.models.signals import post_save, pre_delete


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if user:
        msg = f'You have been signed out {request.user.username}!.'
    else:
        msg = 'You have been logged out!'

    messages.add_message(request, messages.SUCCESS, msg)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if user:
        msg = f'Successfully signed in as {request.user.username}'
    else:
        msg = f'Successfully signed in'
        
    messages.add_message(request, messages.SUCCESS, msg)

@receiver(user_login_failed)
def on_user_logged_in_failed(sender, request, user, **kwargs):
    if user:
        msg = 'Sign in attempt failed'
    else:
        msg = 'Sign in attempt failed'
        
    messages.add_message(request, messages.ERROR, msg)
    

@receiver(post_save, sender=User)
def create_profile(sender,instance):
    pass
